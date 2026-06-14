"""
Real-market integration tests for M0001 — Relative Territory Volatility.

This test intentionally uses the project data path and real market candles.
It has two data modes:

1) cache mode, default:
   Uses existing parquet candles under lab/cache_data/{SYMBOL}/{TIMEFRAME}/.
   This is still a real-market test, not synthetic data.

2) mt5 mode:
   Set M0001_MARKET_SOURCE=mt5 to fetch/sync from MetaTrader 5 via MT5Connector.

Useful environment variables:
    M0001_MARKET_SOURCE=cache|mt5       default: cache
    M0001_CASES=GOLD:M15,#US30:M15     default: GOLD:M15,#US30:M15
    M0001_BARS=5000                    default: 5000
    M0001_L=5                          default: 5
    M0001_ZONE_RATIO=0.9               default: 0.9
    M0001_EXIT_GAP=6                   default: 6
    M0001_CONSUMPTION_MODE=hunt        default: hunt
    M0001_RESET_MARKET_CACHE=0|1       default: 0
    M0001_MIN_EVENTS=1                 default: 1

Run examples:
    pytest -q lab/core/CP0001_structural_nodes/metrics/test_M0001_real_market_integration.py -s

    M0001_MARKET_SOURCE=mt5 M0001_CASES=GOLD:M15 M0001_BARS=10000 pytest -q \
        lab/core/CP0001_structural_nodes/metrics/test_M0001_real_market_integration.py -s
"""

from __future__ import annotations

import os
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import pytest


# Ensure project root is importable when pytest is launched from any folder.
PROJECT_ROOT = Path(__file__).resolve()
for parent in PROJECT_ROOT.parents:
    if (parent / "lab").is_dir():
        sys.path.insert(0, str(parent))
        break


# ---------------------------------------------------------------------------
# Test configuration: real variables, not synthetic fixtures.
# ---------------------------------------------------------------------------

MARKET_SOURCE = os.getenv("M0001_MARKET_SOURCE", "cache").strip().lower()
BARS = int(os.getenv("M0001_BARS", "5000"))
L = int(os.getenv("M0001_L", "5"))
ZONE_RATIO = float(os.getenv("M0001_ZONE_RATIO", "0.9"))
EXIT_GAP = int(os.getenv("M0001_EXIT_GAP", "6"))
CONSUMPTION_MODE = os.getenv("M0001_CONSUMPTION_MODE", "hunt").strip().lower()
RESET_MARKET_CACHE = os.getenv("M0001_RESET_MARKET_CACHE", "0") == "1"
MIN_EVENTS = int(os.getenv("M0001_MIN_EVENTS", "1"))

DEFAULT_CASES = "GOLD:M1,#US30:M1"


@dataclass(frozen=True)
class RealMarketCase:
    symbol: str
    timeframe_name: str

    @property
    def id(self) -> str:
        return f"{self.symbol}-{self.timeframe_name}"


def _parse_cases(raw: str | None = None) -> list[RealMarketCase]:
    raw = (raw or os.getenv("M0001_CASES", DEFAULT_CASES)).strip()
    cases: list[RealMarketCase] = []

    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue

        if ":" not in item:
            raise ValueError(
                "M0001_CASES must use SYMBOL:TIMEFRAME items, "
                f"got {item!r}. Example: GOLD:M15,#US30:M15"
            )

        symbol, timeframe_name = item.split(":", 1)
        cases.append(
            RealMarketCase(
                symbol=symbol.strip(),
                timeframe_name=timeframe_name.strip().upper(),
            )
        )

    if not cases:
        raise ValueError("No real-market cases configured.")

    return cases


# ---------------------------------------------------------------------------
# MetaTrader5 import handling.
# ---------------------------------------------------------------------------
# The project Timeframe enum imports MetaTrader5 at module import time.
# In CI/cache-only environments MetaTrader5 may not be installed, even though
# real parquet market data is available. A small constant-only stub lets cache
# tests import Timeframe without pretending that MT5 live access exists.
# ---------------------------------------------------------------------------


def _ensure_mt5_importable_for_cache_mode() -> None:
    try:
        import MetaTrader5  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    if MARKET_SOURCE == "mt5":
        pytest.skip("MetaTrader5 package is required when M0001_MARKET_SOURCE=mt5")

    mt5_stub = types.ModuleType("MetaTrader5")

    # Timeframe constants used by lab.core.CP0000_market_data.utils.timeframes.
    for name, value in {
        "TIMEFRAME_M1": 1,
        "TIMEFRAME_M2": 2,
        "TIMEFRAME_M3": 3,
        "TIMEFRAME_M4": 4,
        "TIMEFRAME_M5": 5,
        "TIMEFRAME_M6": 6,
        "TIMEFRAME_M10": 10,
        "TIMEFRAME_M12": 12,
        "TIMEFRAME_M15": 15,
        "TIMEFRAME_M20": 20,
        "TIMEFRAME_M30": 30,
        "TIMEFRAME_H1": 60,
        "TIMEFRAME_H2": 120,
        "TIMEFRAME_H3": 180,
        "TIMEFRAME_H4": 240,
        "TIMEFRAME_H6": 360,
        "TIMEFRAME_H8": 480,
        "TIMEFRAME_H12": 720,
        "TIMEFRAME_D1": 1440,
        "TIMEFRAME_W1": 10080,
        "TIMEFRAME_MN1": 43200,
    }.items():
        setattr(mt5_stub, name, value)

    mt5_stub.initialize = lambda: False
    mt5_stub.shutdown = lambda: None
    mt5_stub.last_error = lambda: (0, "MetaTrader5 stub active in cache mode")
    mt5_stub.symbol_info = lambda symbol: None
    mt5_stub.symbols_get = lambda: []
    mt5_stub.copy_rates_range = lambda *args, **kwargs: None
    mt5_stub.copy_rates_from_pos = lambda *args, **kwargs: None

    sys.modules["MetaTrader5"] = mt5_stub


_ensure_mt5_importable_for_cache_mode()


from lab.core.CP0000_market_data.services.MarketDataEngine import MarketDataEngine
from lab.core.CP0000_market_data.utils.timeframes import Timeframe
from lab.core.CP0001_structural_nodes.detectors.L_Rule import LRuleNodeDetector
from lab.core.CP0001_structural_nodes.metrics.M0001_relative_territory_volatility import (
    M0001RTV,
)


class CacheOnlyConnector:
    """Connector used when testing against existing real parquet candles.

    MarketDataEngine.fetch() tries to sync existing cache by calling connector.fetch().
    In cache mode we deliberately return an empty DataFrame so the test uses only the
    already-cached real market candles and never synthetic/generated candles.
    """

    connected = True

    def connect(self) -> None:
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False

    def fetch(self, *args, **kwargs) -> pd.DataFrame:
        return pd.DataFrame()


@pytest.fixture(scope="module")
def engine() -> Iterable[MarketDataEngine]:
    if MARKET_SOURCE == "mt5":
        try:
            from lab.core.CP0000_market_data.connectors.MT5Connector import MT5Connector
        except Exception as exc:  # pragma: no cover - machine dependent
            pytest.skip(f"MT5Connector is unavailable: {exc}")

        connector = MT5Connector()
        try:
            connector.connect()
        except Exception as exc:  # pragma: no cover - machine dependent
            pytest.skip(f"MetaTrader5 connection failed: {exc}")

        try:
            yield MarketDataEngine(connector)
        finally:
            connector.disconnect()
        return

    if MARKET_SOURCE != "cache":
        raise ValueError("M0001_MARKET_SOURCE must be either 'cache' or 'mt5'.")

    yield MarketDataEngine(CacheOnlyConnector())


def _timeframe_from_name(name: str) -> Timeframe:
    try:
        return getattr(Timeframe, name)
    except AttributeError as exc:
        valid = ", ".join(member.name for member in Timeframe)
        raise ValueError(f"Unknown timeframe {name!r}. Valid values: {valid}") from exc


def _assert_real_ohlc_integrity(df: pd.DataFrame, symbol: str, timeframe: Timeframe) -> None:
    required = {"time", "open", "high", "low", "close"}
    missing = required.difference(df.columns)
    assert not missing, f"{symbol} {timeframe.name} missing OHLC columns: {sorted(missing)}"

    assert len(df) > L + EXIT_GAP + 20, (
        f"Not enough real candles for {symbol} {timeframe.name}: "
        f"len(df)={len(df)}, L={L}, exit_gap={EXIT_GAP}"
    )

    assert df["time"].is_monotonic_increasing, f"{symbol} {timeframe.name} time is not sorted"
    assert not df["time"].duplicated().any(), f"{symbol} {timeframe.name} has duplicate candles"

    numeric = df[["open", "high", "low", "close"]].astype(float)
    assert np.isfinite(numeric.to_numpy()).all(), f"{symbol} {timeframe.name} has non-finite OHLC"
    assert (numeric["high"] >= numeric["low"]).all(), f"{symbol} {timeframe.name} high < low found"
    assert (numeric["high"] >= numeric["open"]).all(), f"{symbol} {timeframe.name} high < open found"
    assert (numeric["high"] >= numeric["close"]).all(), f"{symbol} {timeframe.name} high < close found"
    assert (numeric["low"] <= numeric["open"]).all(), f"{symbol} {timeframe.name} low > open found"
    assert (numeric["low"] <= numeric["close"]).all(), f"{symbol} {timeframe.name} low > close found"


def _assert_metric_schema_and_values(result: pd.DataFrame) -> None:
    expected_columns = [
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

    missing = set(expected_columns).difference(result.columns)
    assert not missing, f"M0001 output missing columns: {sorted(missing)}"

    assert len(result) >= MIN_EVENTS, f"Expected at least {MIN_EVENTS} real market events"
    assert (result["event_length"].astype(int) > 0).all(), "event_length must be positive"
    assert result["revisit_id"].astype(int).ge(1).all(), "revisit_id must start from 1"

    numeric_columns = [
        "node_price",
        "territory_lower",
        "territory_upper",
        "expansion_extreme",
        "mean_inside",
        "mean_before",
        "median_inside",
        "median_before",
        "RTV",
    ]
    numeric = result[numeric_columns].astype(float)
    assert np.isfinite(numeric.to_numpy()).all(), "M0001 output contains non-finite metric values"

    assert (result["territory_lower"].astype(float) <= result["node_price"].astype(float)).all()
    assert (result["territory_upper"].astype(float) >= result["node_price"].astype(float)).all()
    assert set(result["node_type"].unique()).issubset({"HIGH", "LOW"})


def _assert_events_use_confirmed_l_nodes_only(
    result: pd.DataFrame,
    nodes: pd.DataFrame,
    df: pd.DataFrame,
    symbol: str,
    timeframe: Timeframe,
) -> None:
    confirmed = nodes[nodes["confirmed"] == True].copy()
    assert not confirmed.empty, f"No confirmed L-nodes found for {symbol} {timeframe.name}"

    confirmed_keys = {
        (pd.Timestamp(row.time), str(row.type), round(float(row.price), 8))
        for row in confirmed.itertuples(index=False)
    }

    time_to_index = {pd.Timestamp(t): i for i, t in enumerate(df["time"])}

    for row in result.itertuples(index=False):
        node_key = (
            pd.Timestamp(row.node_time),
            str(row.node_type),
            round(float(row.node_price), 8),
        )
        assert node_key in confirmed_keys, (
            "M0001 event references a node that is not a confirmed L-node: "
            f"{node_key}"
        )

        node_time = pd.Timestamp(row.node_time)
        entry_time = pd.Timestamp(row.entry_time)
        exit_time = pd.Timestamp(row.exit_time)

        assert node_time in time_to_index, f"node_time not found in candles: {node_time}"
        assert entry_time in time_to_index, f"entry_time not found in candles: {entry_time}"
        assert exit_time in time_to_index, f"exit_time not found in candles: {exit_time}"

        node_index = time_to_index[node_time]
        entry_index = time_to_index[entry_time]
        exit_index = time_to_index[exit_time]
        confirmation_index = node_index + L

        assert confirmation_index < len(df), (
            f"Confirmed node has no full right-side L candles: node_index={node_index}, L={L}"
        )

        # Live rule: the confirmation candle itself is only known after it closes.
        # M0001 may begin evaluating the node only from the next candle.
        assert entry_index > confirmation_index, (
            "Future leakage detected: event entered before the L-node was live-confirmed. "
            f"node_time={node_time}, entry_time={entry_time}, "
            f"node_index={node_index}, confirmation_index={confirmation_index}, "
            f"entry_index={entry_index}, L={L}"
        )

        assert exit_index >= entry_index, (
            f"exit_time must be >= entry_time, got {exit_time} < {entry_time}"
        )


@pytest.mark.parametrize(
    "case",
    _parse_cases(),
    ids=lambda case: case.id,
)
def test_m0001_on_real_market_inputs(engine: MarketDataEngine, case: RealMarketCase, tmp_path: Path) -> None:
    """Run M0001 on real market candles through the real project stack.

    Stack under test:
        MarketDataEngine.fetch/get_df
            -> LRuleNodeDetector.detect
                -> M0001RTV.compute

    This test must fail if M0001 opens events before L-rule confirmation,
    uses non-confirmed nodes, returns the old cache schema, or returns None.
    """

    timeframe = _timeframe_from_name(case.timeframe_name)

    df = engine.fetch(
        symbol=case.symbol,
        timeframe=timeframe,
        bars=BARS,
        reset_cache=RESET_MARKET_CACHE,
    )

    if df is None or df.empty:
        pytest.skip(
            f"No real market data available for {case.symbol} {timeframe.name} "
            f"from source={MARKET_SOURCE!r}."
        )

    _assert_real_ohlc_integrity(df, case.symbol, timeframe)

    detector = LRuleNodeDetector(engine=engine, L=L)
    nodes = detector.detect(case.symbol, timeframe)
    confirmed_nodes = nodes[nodes["confirmed"] == True]

    assert not confirmed_nodes.empty, (
        f"No confirmed L={L} nodes found for {case.symbol} {timeframe.name}. "
        "Increase M0001_BARS or choose another case."
    )

    metric = M0001RTV(
        engine=engine,
        detector=detector,
        zone_ratio=ZONE_RATIO,
        exit_gap=EXIT_GAP,
        consumption_mode=CONSUMPTION_MODE,
        base_path=str(tmp_path / "cache_metrics"),
    )

    result = metric.compute(
        symbol=case.symbol,
        timeframe=timeframe,
        reset_cache=True,
    )

    assert isinstance(result, pd.DataFrame), "M0001.compute() must return a DataFrame"
    assert not result.empty, (
        f"M0001 produced no events for real market case {case.id}. "
        "This may be valid for very small samples, but default cached inputs should produce events."
    )

    _assert_metric_schema_and_values(result)
    _assert_events_use_confirmed_l_nodes_only(result, nodes, df, case.symbol, timeframe)

    print(
        "\nREAL M0001 SUMMARY | "
        f"source={MARKET_SOURCE} symbol={case.symbol} timeframe={timeframe.name} "
        f"bars={len(df)} L={L} zone_ratio={ZONE_RATIO} exit_gap={EXIT_GAP} "
        f"mode={CONSUMPTION_MODE} confirmed_nodes={len(confirmed_nodes)} "
        f"events={len(result)} mean_RTV={result['RTV'].astype(float).mean():.6f} "
        f"median_RTV={result['RTV'].astype(float).median():.6f} "
        f"max_revisit={int(result['revisit_id'].astype(int).max())}"
    )
