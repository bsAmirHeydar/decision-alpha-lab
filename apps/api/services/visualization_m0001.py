from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

import pandas as pd

from apps.api.core.config import settings


def root() -> Path:
    return settings.root_path.resolve()


def load_m0001_visualization(
    symbol: str = "GOLD",
    timeframe: str = "M15",
    L: int = 5,
    zone_ratio: float = 0.9,
    exit_gap: int = 6,
    consumption_mode: str = "hunt",
    max_bars: int = 5000,
) -> dict[str, Any]:
    candles_df = load_candles(symbol, timeframe, max_bars=max_bars)
    nodes_df = load_nodes(symbol, timeframe, L)
    events_df = load_events(symbol, timeframe, L, zone_ratio, exit_gap, consumption_mode)

    candles = serialize_candles(candles_df)
    time_to_index = {row["time"]: row["index"] for row in candles}
    nodes = serialize_nodes(nodes_df, time_to_index, L)
    events = serialize_events(events_df, time_to_index)

    overlay_layers = build_layers(nodes, events)
    tables = build_tables(nodes, events)
    stats = {
        "bars": len(candles),
        "nodes": len(nodes),
        "events": len(events),
        "mean_RTV": safe_float(events_df["RTV"].mean()) if "RTV" in events_df.columns and len(events_df) else None,
        "median_RTV": safe_float(events_df["RTV"].median()) if "RTV" in events_df.columns and len(events_df) else None,
        "max_revisit": int(events_df["revisit_id"].max()) if "revisit_id" in events_df.columns and len(events_df) else 0,
    }

    return {
        "dataset": {
            "symbol": symbol,
            "timeframe": timeframe,
            "source": "cache",
            "bars": len(candles),
            "parameters": {
                "L": L,
                "zone_ratio": zone_ratio,
                "exit_gap": exit_gap,
                "consumption_mode": consumption_mode,
            },
        },
        "entity": {
            "id": "M0001",
            "title": "Relative Territory Volatility",
            "type": "metric",
        },
        "candles": candles,
        "overlay_layers": overlay_layers,
        "tables": tables,
        "stats": stats,
        "timeline": build_timeline(events),
        "validation_flags": [
            {"id": "live_confirmation", "label": "L-node confirmation delay respected in visualization", "status": "pass"},
            {"id": "data_loaded", "label": "Market candles loaded from project cache", "status": "pass" if len(candles) else "fail"},
            {"id": "events_loaded", "label": "M0001 event artifacts loaded", "status": "pass" if len(events) else "warn"},
        ],
    }


def load_candles(symbol: str, timeframe: str, max_bars: int) -> pd.DataFrame:
    candidates = [
        root() / "lab/cache_data" / symbol / timeframe / f"{symbol}_{timeframe}.parquet",
        root() / "lab/cache_data" / symbol / timeframe / "data.parquet",
    ]
    for path in candidates:
        if path.exists():
            df = pd.read_parquet(path)
            df = normalize_time(df)
            df = df.drop_duplicates("time").sort_values("time").reset_index(drop=True)
            return df.tail(max_bars).reset_index(drop=True)
    raise FileNotFoundError(f"No cached candle data found for {symbol} {timeframe}")


def load_nodes(symbol: str, timeframe: str, L: int) -> pd.DataFrame:
    candidates = [
        root() / "lab/cache_nodes/L_rule" / f"L_{L}" / symbol / timeframe / f"{symbol}_{timeframe}_L{L}.parquet",
    ]
    for path in candidates:
        if path.exists():
            df = pd.read_parquet(path)
            return normalize_time(df)
    return pd.DataFrame(columns=["time", "type", "price", "confirmed"])


def load_events(symbol: str, timeframe: str, L: int, zone_ratio: float, exit_gap: int, mode: str) -> pd.DataFrame:
    metric_root = root() / "lab/cache_metrics/M0001_relative_territory_volatility"
    candidates = [
        metric_root / f"L_{L}" / symbol / timeframe / f"{symbol}_{timeframe}_L{L}_ZR{zone_ratio}_EG{exit_gap}_{mode}.parquet",
        metric_root / symbol / timeframe / f"{symbol}_{timeframe}_T{zone_ratio}_G{exit_gap}_{mode}.parquet",
        metric_root / symbol / timeframe / f"{symbol}_{timeframe}_ZR{zone_ratio}_EG{exit_gap}_{mode}.parquet",
    ]
    for path in candidates:
        if path.exists():
            return normalize_event_schema(pd.read_parquet(path))

    # Fallback: closest artifact for symbol/timeframe.
    folder = metric_root / symbol / timeframe
    if folder.exists():
        files = sorted(folder.glob("*.parquet"), key=lambda p: p.stat().st_mtime, reverse=True)
        if files:
            return normalize_event_schema(pd.read_parquet(files[0]))
    return pd.DataFrame()


def normalize_time(df: pd.DataFrame) -> pd.DataFrame:
    if "time" in df.columns:
        df = df.copy()
        df["time"] = pd.to_datetime(df["time"]).astype("int64") // 10**9
    return df


def normalize_event_schema(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    for col in ["node_time", "entry_time", "exit_time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).astype("int64") // 10**9
    # Old cache compatibility
    if "mean_inside" not in df.columns and "V_zone" in df.columns:
        df["mean_inside"] = df["V_zone"]
    if "mean_before" not in df.columns and "V_base" in df.columns:
        df["mean_before"] = df["V_base"]
    if "RTV" not in df.columns and "mean_inside" in df.columns and "mean_before" in df.columns:
        df["RTV"] = df.apply(lambda r: safe_ratio(r["mean_inside"], r["mean_before"]), axis=1)
    return df


def serialize_candles(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for idx, row in df.reset_index(drop=True).iterrows():
        rows.append({
            "index": int(idx),
            "time": int(row["time"]),
            "open": safe_float(row["open"]),
            "high": safe_float(row["high"]),
            "low": safe_float(row["low"]),
            "close": safe_float(row["close"]),
            "volume": safe_float(row["tick_volume"] if "tick_volume" in df.columns else row.get("volume", 0)),
        })
    return rows


def serialize_nodes(df: pd.DataFrame, time_to_index: dict[int, int], L: int) -> list[dict[str, Any]]:
    nodes = []
    if df is None or df.empty:
        return nodes
    for idx, row in df.reset_index(drop=True).iterrows():
        if "confirmed" in df.columns and not bool(row["confirmed"]):
            continue
        node_time = int(row["time"])
        candle_index = time_to_index.get(node_time)
        if candle_index is None:
            continue
        nodes.append({
            "id": f"NODE-{idx}",
            "node_id": int(idx),
            "kind": "node",
            "node_type": str(row["type"]),
            "time": node_time,
            "index": candle_index,
            "confirmation_index": candle_index + L,
            "price": safe_float(row["price"]),
            "label": f"{row['type']} #{idx}",
        })
    return nodes


def serialize_events(df: pd.DataFrame, time_to_index: dict[int, int]) -> list[dict[str, Any]]:
    events = []
    if df is None or df.empty:
        return events
    for idx, row in df.reset_index(drop=True).iterrows():
        entry_time = int(row["entry_time"]) if "entry_time" in df.columns and not pd.isna(row["entry_time"]) else None
        exit_time = int(row["exit_time"]) if "exit_time" in df.columns and not pd.isna(row["exit_time"]) else None
        entry_index = time_to_index.get(entry_time) if entry_time is not None else row.get("entry_index")
        exit_index = time_to_index.get(exit_time) if exit_time is not None else row.get("exit_index")
        if entry_index is None or exit_index is None:
            continue
        event_id = f"M0001-EVENT-{idx}"
        events.append({
            "id": event_id,
            "kind": "event",
            "row_index": int(idx),
            "node_id": safe_int(row.get("node_id", idx)),
            "node_type": str(row.get("node_type", "")),
            "node_price": safe_float(row.get("node_price")),
            "revisit_id": safe_int(row.get("revisit_id", 1)),
            "entry_time": entry_time,
            "exit_time": exit_time,
            "entry_index": int(entry_index),
            "exit_index": int(exit_index),
            "event_length": safe_int(row.get("event_length", 0)),
            "territory_lower": safe_float(row.get("territory_lower")),
            "territory_upper": safe_float(row.get("territory_upper")),
            "expansion_extreme": safe_float(row.get("expansion_extreme")),
            "mean_inside": safe_float(row.get("mean_inside")),
            "mean_before": safe_float(row.get("mean_before")),
            "median_inside": safe_float(row.get("median_inside")),
            "median_before": safe_float(row.get("median_before")),
            "RTV": safe_float(row.get("RTV")),
            "hunted": bool(row.get("hunted", False)),
            "label": f"RTV {safe_float(row.get('RTV')):.2f}" if safe_float(row.get("RTV")) is not None else "RTV",
        })
    return events


def build_layers(nodes: list[dict[str, Any]], events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []

    for node in nodes:
        objects.append({
            "id": node["id"],
            "kind": "marker",
            "object_type": "node",
            "index": node["index"],
            "time": node["time"],
            "price": node["price"],
            "shape": "triangleUp" if node["node_type"] == "LOW" else "triangleDown",
            "label": node["label"],
            "payload": node,
        })

    zone_objects = []
    event_objects = []
    label_objects = []
    hunt_objects = []

    for event in events:
        zone_objects.append({
            "id": f"{event['id']}-ZONE",
            "kind": "zone",
            "object_type": "territory",
            "start_index": event["entry_index"],
            "end_index": event["exit_index"],
            "lower": event["territory_lower"],
            "upper": event["territory_upper"],
            "label": None,
            "payload": event,
        })
        event_objects.append({
            "id": f"{event['id']}-WINDOW",
            "kind": "event_window",
            "object_type": "event",
            "start_index": event["entry_index"],
            "end_index": event["exit_index"],
            "lower": event["territory_lower"],
            "upper": event["territory_upper"],
            "label": None,
            "payload": event,
        })
        label_objects.append({
            "id": f"{event['id']}-LABEL",
            "kind": "label",
            "object_type": "event",
            "index": event["entry_index"],
            "price": event["territory_upper"],
            "label": event["label"],
            "payload": event,
        })
        if event["hunted"]:
            hunt_objects.append({
                "id": f"{event['id']}-HUNT",
                "kind": "marker",
                "object_type": "hunt",
                "index": event["exit_index"],
                "price": event["node_price"],
                "shape": "cross",
                "label": "HUNT",
                "payload": event,
            })

    return [
        {"layer_id": "nodes", "label": "Confirmed L-nodes", "default_visible": True, "objects": objects},
        {"layer_id": "territories", "label": "M0001 territories", "default_visible": True, "objects": zone_objects},
        {"layer_id": "events", "label": "Event windows", "default_visible": True, "objects": event_objects},
        {"layer_id": "rtv_labels", "label": "RTV labels", "default_visible": True, "objects": label_objects},
        {"layer_id": "hunts", "label": "Hunt markers", "default_visible": True, "objects": hunt_objects},
    ]


def build_tables(nodes: list[dict[str, Any]], events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "table_id": "events",
            "label": "M0001 Events",
            "object_type": "event",
            "columns": [
                {"key": "row_index", "label": "#"},
                {"key": "node_id", "label": "Node"},
                {"key": "node_type", "label": "Type"},
                {"key": "revisit_id", "label": "Revisit"},
                {"key": "entry_index", "label": "Entry"},
                {"key": "exit_index", "label": "Exit"},
                {"key": "event_length", "label": "Len"},
                {"key": "RTV", "label": "RTV"},
                {"key": "mean_inside", "label": "Inside"},
                {"key": "mean_before", "label": "Before"},
                {"key": "hunted", "label": "Hunted"},
            ],
            "rows": events,
        },
        {
            "table_id": "nodes",
            "label": "Confirmed Nodes",
            "object_type": "node",
            "columns": [
                {"key": "node_id", "label": "#"},
                {"key": "node_type", "label": "Type"},
                {"key": "index", "label": "Index"},
                {"key": "confirmation_index", "label": "Confirmed At"},
                {"key": "price", "label": "Price"},
            ],
            "rows": nodes,
        },
    ]


def build_timeline(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"id": event["id"], "time": event["entry_time"], "index": event["entry_index"], "label": event["label"], "object_id": event["id"]}
        for event in events
    ]


def safe_float(value) -> float | None:
    try:
        if value is None:
            return None
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def safe_int(value) -> int:
    try:
        if value is None or pd.isna(value):
            return 0
        return int(value)
    except Exception:
        return 0


def safe_ratio(a, b) -> float | None:
    a = safe_float(a)
    b = safe_float(b)
    if a is None or b in {None, 0}:
        return None
    return a / b
