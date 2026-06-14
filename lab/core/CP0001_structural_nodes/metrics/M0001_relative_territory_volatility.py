import os
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


class M0001RTV:
    """M0001 — Relative Territory Volatility (RTV).

    Live-compatible implementation:
    - market data comes from MarketDataEngine.get_df(symbol, timeframe)
    - structural nodes come from LRuleNodeDetector.detect(symbol, timeframe)
    - a node is not usable until its L-rule confirmation candle is complete
    - the first tradable/evaluable candle is the candle after confirmation
    - no baseline, extreme update, territory check, or event can occur before that
    """

    OUTPUT_COLUMNS = [
        "node_id",
        "node_time",
        "node_type",
        "node_price",
        "revisit_id",
        "entry_time",
        "exit_time",
        "event_length",
        "territory_lower",
        "territory_upper",
        "expansion_extreme",
        "mean_inside",
        "mean_before",
        "median_inside",
        "median_before",
        "RTV",
        "hunted",
    ]

    VALID_CONSUMPTION_MODES = {"touch", "hunt"}

    def __init__(
        self,
        engine,
        detector=None,
        L: Optional[int] = None,
        zone_ratio: float = 0.9,
        exit_gap: int = 6,
        consumption_mode: str = "hunt",
        base_path: str = "lab/cache_metrics",
        max_before_logs: int = 500,
    ):
        """
        Parameters
        ----------
        engine:
            MarketDataEngine-like object. Must expose get_df(symbol, timeframe).

        detector:
            LRuleNodeDetector-like object. Must expose detect(symbol, timeframe)
            and ideally an L attribute.

        L:
            Backward-compatible shortcut. If detector is omitted, M0001RTV will
            instantiate LRuleNodeDetector(engine=engine, L=L).

        zone_ratio:
            Territory construction ratio from the frozen M0001 spec.

        exit_gap:
            Consecutive completed candles fully outside territory required to
            terminate an active event.

        consumption_mode:
            "touch" consumes after the first completed event.
            "hunt" consumes only after the node is hunted.

        base_path:
            Root path for metric cache.

        max_before_logs:
            Rolling cap for baseline observations per node/revisit.
        """
        if detector is None:
            if L is None:
                raise ValueError("Either detector or L must be provided.")
            try:
                from lab.core.CP0001_structural_nodes.detectors.L_Rule import (
                    LRuleNodeDetector,
                )
            except Exception as exc:  # pragma: no cover - environment dependent
                raise ValueError(
                    "detector was not provided and LRuleNodeDetector could not "
                    "be imported. Pass detector=LRuleNodeDetector(...)."
                ) from exc
            detector = LRuleNodeDetector(engine=engine, L=L)

        zone_ratio = float(zone_ratio)
        exit_gap = int(exit_gap)
        max_before_logs = int(max_before_logs)

        if not 0.0 <= zone_ratio <= 1.0:
            raise ValueError("zone_ratio must be between 0 and 1.")
        if exit_gap <= 0:
            raise ValueError("exit_gap must be a positive integer.")
        if consumption_mode not in self.VALID_CONSUMPTION_MODES:
            raise ValueError(
                "consumption_mode must be either 'touch' or 'hunt'."
            )
        if max_before_logs <= 0:
            raise ValueError("max_before_logs must be a positive integer.")

        self.engine = engine
        self.detector = detector
        self.zone_ratio = zone_ratio
        self.exit_gap = exit_gap
        self.consumption_mode = consumption_mode
        self.base_path = base_path
        self.max_before_logs = max_before_logs
        self._cache = {}

    # ==================================================
    # CACHE PATHS
    # ==================================================

    def _timeframe_name(self, timeframe) -> str:
        return getattr(timeframe, "name", str(timeframe))

    def _detector_L(self) -> int:
        L = getattr(self.detector, "L", None)
        if L is None:
            raise ValueError(
                "The detector must expose an L attribute so M0001 can apply "
                "live L-rule confirmation delay."
            )
        return int(L)

    def _metric_file(self, symbol, timeframe) -> str:
        timeframe_name = self._timeframe_name(timeframe)
        L = self._detector_L()

        path = os.path.join(
            self.base_path,
            "M0001_relative_territory_volatility",
            f"L_{L}",
            symbol,
            timeframe_name,
        )
        os.makedirs(path, exist_ok=True)

        filename = (
            f"{symbol}_{timeframe_name}_"
            f"L{L}_ZR{self.zone_ratio}_EG{self.exit_gap}_"
            f"{self.consumption_mode}.parquet"
        )
        return os.path.join(path, filename)

    def _load_cache(self, symbol, timeframe) -> Optional[pd.DataFrame]:
        file = self._metric_file(symbol, timeframe)
        if not os.path.exists(file):
            return None
        return pd.read_parquet(file)

    def _save_cache(self, result: pd.DataFrame, symbol, timeframe) -> None:
        file = self._metric_file(symbol, timeframe)
        result.to_parquet(file, index=False)

    # ==================================================
    # SPEC HELPERS
    # ==================================================

    def _log_move(self, high, low) -> float:
        move = abs(float(high) - float(low))
        if move <= 0:
            return 0.0
        return float(np.log(move))

    def _in_zone(self, high, low, lower, upper) -> bool:
        if lower is None or upper is None:
            return False
        return not (float(high) < float(lower) or float(low) > float(upper))

    def _build_zone(self, node_price, extreme) -> Tuple[float, float]:
        distance = abs(float(extreme) - float(node_price))
        half_width = distance * (1.0 - self.zone_ratio)
        return float(node_price) - half_width, float(node_price) + half_width

    def _find_candle_index_by_time(self, df: pd.DataFrame, candle_time) -> Optional[int]:
        matches = df.index[df["time"] == candle_time].tolist()
        if not matches:
            return None
        return int(matches[0])

    # ==================================================
    # NODE STATE INITIALIZATION
    # ==================================================

    def _initialize_node_states(self, nodes_df, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Create states only for L-rule confirmed nodes.

        Important live rule:
        A node at node_index is only known after L candles to its right have
        completed. Therefore active_from_index = node_index + L. The metric
        does not process the confirmation candle itself; it starts from the
        next completed candle to avoid same-candle confirmation/entry leakage.
        """
        states: List[Dict[str, Any]] = []
        if nodes_df is None or nodes_df.empty:
            return states

        required = {"time", "type", "price", "confirmed"}
        missing = required.difference(nodes_df.columns)
        if missing:
            raise ValueError(f"nodes_df is missing required columns: {sorted(missing)}")

        L = self._detector_L()
        confirmed_nodes = nodes_df[nodes_df["confirmed"] == True].copy()
        if confirmed_nodes.empty:
            return states

        # LRuleNodeDetector.iNode exposes newest-first, but a live simulator must
        # process state identity deterministically in chronological order.
        confirmed_nodes = confirmed_nodes.sort_values("time").reset_index(drop=True)

        for node_id, node in confirmed_nodes.iterrows():
            node_index = self._find_candle_index_by_time(df, node["time"])
            if node_index is None:
                continue

            confirmation_index = node_index + L
            if confirmation_index >= len(df):
                # Not enough received candles to know this node in live mode.
                continue

            node_type = str(node["type"]).upper()
            if node_type not in {"LOW", "HIGH"}:
                continue

            node_price = float(node["price"])

            states.append(
                {
                    # Identity
                    "node_id": int(node_id),
                    "node_time": node["time"],
                    "node_index": int(node_index),
                    "confirmation_index": int(confirmation_index),
                    "confirmation_time": df.iloc[confirmation_index]["time"],
                    "active_from_index": int(confirmation_index),
                    "node_price": node_price,
                    "node_type": node_type,
                    # Tracking
                    "extreme": node_price,
                    "consumed": False,
                    "hunted": False,
                    # Event
                    "in_event": False,
                    "revisit_id": 0,
                    "outside_count": 0,
                    "entry_index": None,
                    "entry_time": None,
                    "exit_index": None,
                    "exit_time": None,
                    # Zone
                    "territory_lower": None,
                    "territory_upper": None,
                    # Metric storage
                    "before_logs": [],
                    "inside_logs": [],
                    "event_before_logs": [],
                    # Frozen event data
                    "frozen_extreme": None,
                }
            )

        return states

    # ==================================================
    # STATE TRANSITIONS
    # ==================================================

    def _append_before_log(self, state: Dict[str, Any], log_move: float) -> None:
        state["before_logs"].append(float(log_move))
        if len(state["before_logs"]) > self.max_before_logs:
            state["before_logs"].pop(0)

    def _update_extreme(self, state: Dict[str, Any], high, low) -> None:
        if state["in_event"] or state["extreme"] is None:
            return

        if state["node_type"] == "LOW":
            if float(high) > float(state["extreme"]):
                state["extreme"] = float(high)
        else:
            if float(low) < float(state["extreme"]):
                state["extreme"] = float(low)

    def _update_territory(self, state: Dict[str, Any]) -> None:
        if state["extreme"] is None:
            return
        lower, upper = self._build_zone(state["node_price"], state["extreme"])
        state["territory_lower"] = lower
        state["territory_upper"] = upper

    def _check_hunt(self, state: Dict[str, Any], high, low) -> None:
        if state["hunted"]:
            return

        if state["node_type"] == "LOW":
            if float(low) < float(state["node_price"]):
                state["hunted"] = True
        else:
            if float(high) > float(state["node_price"]):
                state["hunted"] = True

    def _consume_if_needed(self, state: Dict[str, Any]) -> None:
        if self.consumption_mode == "touch":
            state["consumed"] = True
        elif self.consumption_mode == "hunt" and state["hunted"]:
            state["consumed"] = True

    def _consume_hunted_without_event_if_needed(self, state: Dict[str, Any]) -> None:
        """Handle gap-through hunts that never intersect preserved/current territory."""
        if self.consumption_mode == "hunt" and state["hunted"] and not state["in_event"]:
            state["consumed"] = True

    def _seed_revisit_extreme(self, state: Dict[str, Any], high, low) -> None:
        if state["node_type"] == "LOW":
            state["extreme"] = float(high)
        else:
            state["extreme"] = float(low)

    def _start_event(self, state: Dict[str, Any], i: int, time, log_move: float) -> None:
        state["in_event"] = True
        state["revisit_id"] += 1
        state["outside_count"] = 0
        state["entry_index"] = int(i)
        state["entry_time"] = time
        state["exit_index"] = None
        state["exit_time"] = None
        state["inside_logs"] = [float(log_move)]
        state["event_before_logs"] = list(state["before_logs"])
        state["frozen_extreme"] = state["extreme"]

    def _reset_after_event(self, state: Dict[str, Any]) -> None:
        state["in_event"] = False
        state["outside_count"] = 0
        state["inside_logs"] = []
        state["event_before_logs"] = []
        state["entry_index"] = None
        state["entry_time"] = None
        state["exit_index"] = None
        state["exit_time"] = None

        if not state["consumed"]:
            # Revisit rule: preserve territory, reset extreme, build a fresh
            # baseline until the preserved territory is revisited again.
            state["extreme"] = None
            state["hunted"] = False
            state["before_logs"] = []

    def _event_record(self, state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        inside_logs = list(state["inside_logs"])
        N = len(inside_logs)
        if N == 0:
            return None

        before = list(state["event_before_logs"])[-N:]
        if len(before) < N:
            return None

        mean_inside = float(np.mean(inside_logs))
        mean_before = float(np.mean(before))
        median_inside = float(np.median(inside_logs))
        median_before = float(np.median(before))
        rtv = None if mean_before == 0 else float(mean_inside / mean_before)

        return {
            "node_id": state["node_id"],
            "node_time": state["node_time"],
            "node_type": state["node_type"],
            "node_price": state["node_price"],
            "revisit_id": state["revisit_id"],
            "entry_time": state["entry_time"],
            "exit_time": state["exit_time"],
            "event_length": N,
            "territory_lower": state["territory_lower"],
            "territory_upper": state["territory_upper"],
            "expansion_extreme": state["frozen_extreme"],
            "mean_inside": mean_inside,
            "mean_before": mean_before,
            "median_inside": median_inside,
            "median_before": median_before,
            "RTV": rtv,
            "hunted": bool(state["hunted"]),
        }

    # ==================================================
    # CANDLE PROCESSING
    # ==================================================

    def _process_active_event(
        self,
        state: Dict[str, Any],
        i: int,
        time,
        high,
        low,
        log_move: float,
        events: List[Dict[str, Any]],
    ) -> None:
        inside = self._in_zone(
            high,
            low,
            state["territory_lower"],
            state["territory_upper"],
        )

        self._check_hunt(state, high, low)

        if inside:
            state["inside_logs"].append(float(log_move))
            state["outside_count"] = 0
        else:
            state["outside_count"] += 1

        if state["outside_count"] < self.exit_gap:
            return

        state["exit_index"] = int(i)
        state["exit_time"] = time

        record = self._event_record(state)
        if record is not None:
            events.append(record)

        # Completion happened even if the metric row was discarded due to
        # insufficient baseline, so consumption rules still apply.
        self._consume_if_needed(state)
        self._reset_after_event(state)

    def _process_waiting_for_revisit(
        self,
        state: Dict[str, Any],
        i: int,
        time,
        high,
        low,
        log_move: float,
    ) -> None:
        # territory is preserved, extreme is None
        inside_preserved = self._in_zone(
            high,
            low,
            state["territory_lower"],
            state["territory_upper"],
        )

        self._check_hunt(state, high, low)

        if inside_preserved:
            self._seed_revisit_extreme(state, high, low)
            self._start_event(state, i, time, log_move)
            return

        self._consume_hunted_without_event_if_needed(state)
        if not state["consumed"]:
            self._append_before_log(state, log_move)

    def _process_tracking(
        self,
        state: Dict[str, Any],
        i: int,
        time,
        high,
        low,
        log_move: float,
    ) -> None:
        # First event mode: dynamic territory evolves from post-confirmation
        # completed candles only.
        self._update_extreme(state, high, low)
        self._update_territory(state)
        self._check_hunt(state, high, low)

        inside = self._in_zone(
            high,
            low,
            state["territory_lower"],
            state["territory_upper"],
        )

        if inside:
            self._start_event(state, i, time, log_move)
            return

        self._consume_hunted_without_event_if_needed(state)
        if not state["consumed"]:
            self._append_before_log(state, log_move)

    # ==================================================
    # COMPUTE
    # ==================================================

    def compute(self, symbol, timeframe, reset_cache: bool = False) -> pd.DataFrame:
        """Run the full candle-by-candle simulation over currently cached bars.

        This method does not fetch new data by itself. The caller controls what
        "currently received" means by calling MarketDataEngine.fetch(...) first.
        M0001 then reads the canonical cache through engine.get_df(...), exactly
        like other project components.
        """
        if not reset_cache:
            cached = self._load_cache(symbol, timeframe)
            if cached is not None:
                return cached

        df = self.engine.get_df(symbol, timeframe)
        if df is None or df.empty:
            return pd.DataFrame(columns=self.OUTPUT_COLUMNS)

        required = {"time", "high", "low"}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"df is missing required columns: {sorted(missing)}")

        df = df.drop_duplicates(subset=["time"], keep="last")
        df = df.sort_values("time").reset_index(drop=True)

        nodes_df = self.detector.detect(symbol, timeframe)
        states = self._initialize_node_states(nodes_df, df)
        events: List[Dict[str, Any]] = []

        for i in range(len(df)):
            candle = df.iloc[i]
            high = candle["high"]
            low = candle["low"]
            time = candle["time"]
            log_move = self._log_move(high, low)

            for state in states:
                # Strict live rule: the node is usable only after the L-rule
                # confirmation candle has completed. Therefore candle
                # confirmation_index itself is not processed for that node.
                if i <= state["active_from_index"] or state["consumed"]:
                    continue

                if state["in_event"]:
                    self._process_active_event(
                        state,
                        i,
                        time,
                        high,
                        low,
                        log_move,
                        events,
                    )
                    continue

                if state["extreme"] is None:
                    self._process_waiting_for_revisit(
                        state,
                        i,
                        time,
                        high,
                        low,
                        log_move,
                    )
                    continue

                self._process_tracking(
                    state,
                    i,
                    time,
                    high,
                    low,
                    log_move,
                )

        result = pd.DataFrame(events, columns=self.OUTPUT_COLUMNS)
        self._save_cache(result, symbol, timeframe)
        return result
