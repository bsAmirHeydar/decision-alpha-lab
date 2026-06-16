from __future__ import annotations

import os
from typing import Optional

import pandas as pd

from lab.core.CP0001_structural_nodes.metrics.M0001_rtv import (
    OUTPUT_COLUMNS,
    RTVConfig,
    compute_rtv_dataframe,
    reference_points_from_lrule_nodes,
)


class M0001RTV:
    """M0001 — Relative Territory Volatility (RTV).

    Compatibility facade around the modular M0001_rtv package.

    The old public API is preserved:
        metric = M0001RTV(engine, detector, ...)
        result = metric.compute(symbol, timeframe)

    The actual metric logic now lives in small modules:
        M0001_rtv.schemas
        M0001_rtv.math_utils
        M0001_rtv.reference_points
        M0001_rtv.engine
        M0001_rtv.mql_visual_contract
    """

    OUTPUT_COLUMNS = OUTPUT_COLUMNS
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
        if detector is None:
            if L is None:
                raise ValueError("Either detector or L must be provided.")
            from lab.core.CP0001_structural_nodes.detectors.L_Rule import LRuleNodeDetector

            detector = LRuleNodeDetector(engine=engine, L=L)

        self.engine = engine
        self.detector = detector
        self.config = RTVConfig(
            L=int(getattr(detector, "L", L if L is not None else 5)),
            zone_ratio=float(zone_ratio),
            exit_gap=int(exit_gap),
            consumption_mode=str(consumption_mode),
            max_before_logs=int(max_before_logs),
        )
        self.config.validate()
        self.zone_ratio = self.config.zone_ratio
        self.exit_gap = self.config.exit_gap
        self.consumption_mode = self.config.consumption_mode
        self.base_path = base_path
        self.max_before_logs = self.config.max_before_logs
        self._cache = {}

    def _timeframe_name(self, timeframe) -> str:
        return getattr(timeframe, "name", str(timeframe))

    def _detector_L(self) -> int:
        return int(self.config.L)

    def _metric_file(self, symbol, timeframe) -> str:
        timeframe_name = self._timeframe_name(timeframe)
        path = os.path.join(
            self.base_path,
            "M0001_relative_territory_volatility",
            f"L_{self.config.L}",
            symbol,
            timeframe_name,
        )
        os.makedirs(path, exist_ok=True)
        filename = (
            f"{symbol}_{timeframe_name}_"
            f"L{self.config.L}_ZR{self.config.zone_ratio}_EG{self.config.exit_gap}_"
            f"{self.config.consumption_mode}.parquet"
        )
        return os.path.join(path, filename)

    def _load_cache(self, symbol, timeframe) -> Optional[pd.DataFrame]:
        file = self._metric_file(symbol, timeframe)
        if not os.path.exists(file):
            return None
        cached = pd.read_parquet(file)
        if set(self.OUTPUT_COLUMNS).issubset(cached.columns):
            return cached[self.OUTPUT_COLUMNS]
        return None

    def _save_cache(self, result: pd.DataFrame, symbol, timeframe) -> None:
        file = self._metric_file(symbol, timeframe)
        try:
            result.to_parquet(file, index=False)
        except Exception:
            # Parquet is the canonical project cache format, but lightweight
            # test/MT5-only environments may not have pyarrow installed.
            # In that case computation still returns a valid DataFrame and a
            # CSV sidecar is written for inspection instead of failing.
            result.to_csv(file + ".csv", index=False)

    def compute(self, symbol, timeframe, reset_cache: bool = False) -> pd.DataFrame:
        if not reset_cache:
            cached = self._load_cache(symbol, timeframe)
            if cached is not None:
                return cached

        df = self.engine.get_df(symbol, timeframe)
        if df is None or df.empty:
            return pd.DataFrame(columns=self.OUTPUT_COLUMNS)

        df = df.drop_duplicates(subset=["time"], keep="last").sort_values("time").reset_index(drop=True)
        nodes_df = self.detector.detect(symbol, timeframe)
        refs = reference_points_from_lrule_nodes(nodes_df, df, self.config.L)
        result = compute_rtv_dataframe(df, refs, self.config, include_visual_fields=False)
        result = result[self.OUTPUT_COLUMNS]
        self._save_cache(result, symbol, timeframe)
        return result
