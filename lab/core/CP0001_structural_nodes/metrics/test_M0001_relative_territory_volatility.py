from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from lab.core.CP0001_structural_nodes.metrics.M0001_relative_territory_volatility import M0001RTV
from lab.core.CP0001_structural_nodes.metrics.M0001_rtv import (
    RTVConfig,
    build_visual_rows,
    compute_rtv_events,
    reference_points_from_lrule_nodes,
    write_visual_csv,
)


class _Timeframe:
    name = "M15"


class _DataFrameEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_df(self, symbol, timeframe):
        return self.df.copy()


class _Detector:
    L = 5

    def __init__(self, nodes: pd.DataFrame):
        self.nodes = nodes

    def detect(self, symbol, timeframe):
        return self.nodes.copy()


def _synthetic_revisit_case() -> tuple[pd.DataFrame, pd.DataFrame]:
    times = pd.date_range("2026-01-01", periods=60, freq="15min")
    rows = []
    for i, t in enumerate(times):
        if i < 10:
            open_, high, low, close = 109, 111, 107, 110
        elif i == 10:
            open_, high, low, close = 105, 106, 100, 104
        elif 11 <= i <= 25:
            base = 108 + (i - 11) * 1.5
            open_, high, low, close = base, base + 4, base - 1, base + 2
        elif 26 <= i <= 28:
            open_, high, low, close = 101.0, 102.4, 99.2, 101.8
        elif 29 <= i <= 33:
            open_, high, low, close = 112, 116, 110, 115
        else:
            open_, high, low, close = 118, 121, 116, 120
        rows.append({"time": t, "open": open_, "high": high, "low": low, "close": close})

    candles = pd.DataFrame(rows)
    nodes = pd.DataFrame([
        {"time": times[10], "type": "LOW", "price": 100.0, "confirmed": True},
    ])
    return candles, nodes


def test_m0001_modular_engine_on_synthetic_live_revisit(tmp_path: Path) -> None:
    candles, nodes = _synthetic_revisit_case()
    engine = _DataFrameEngine(candles)
    detector = _Detector(nodes)

    metric = M0001RTV(
        engine=engine,
        detector=detector,
        zone_ratio=0.9,
        exit_gap=2,
        consumption_mode="hunt",
        base_path=str(tmp_path / "metrics"),
    )
    result = metric.compute("GOLD", _Timeframe(), reset_cache=True)

    assert not result.empty
    assert list(result.columns) == metric.OUTPUT_COLUMNS
    assert set(result["node_type"].unique()) == {"LOW"}
    assert result["RTV"].astype(float).map(np.isfinite).all()
    assert (result["event_length"].astype(int) > 0).all()

    time_to_index = {pd.Timestamp(t): i for i, t in enumerate(candles["time"])}
    first = result.iloc[0]
    assert time_to_index[pd.Timestamp(first["entry_time"])] > 10 + detector.L
    assert float(first["territory_lower"]) <= 100.0 <= float(first["territory_upper"])


def test_m0001_mql_visual_contract_export(tmp_path: Path) -> None:
    candles, nodes = _synthetic_revisit_case()
    refs = reference_points_from_lrule_nodes(nodes, candles, L=5)
    events = compute_rtv_events(candles, refs, RTVConfig(L=5, zone_ratio=0.9, exit_gap=2, consumption_mode="hunt"))
    rows = build_visual_rows(refs, events)

    assert refs
    assert events
    assert any(row["kind"] == "RTV_LABEL" for row in rows)
    assert any(row["kind"] == "TERRITORY" for row in rows)

    out = write_visual_csv(tmp_path / "GOLD_M15_visual.csv", rows)
    text = out.read_text(encoding="utf-8")
    assert "RTV_LABEL" in text
    assert "TERRITORY" in text
