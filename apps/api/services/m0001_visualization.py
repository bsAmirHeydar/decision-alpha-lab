from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pandas as pd

from apps.api.adapters.cache_market import CacheMarketDataEngine
from apps.api.core.config import settings
from apps.api.core.timeframes import parse_timeframe
from apps.api.schemas.visualization import (
    Candle,
    DataQuality,
    DatasetDescriptor,
    InspectorPayload,
    MetricSummary,
    OverlayLayer,
    ReplayPayload,
    SourceRef,
    TableColumn,
    TableSpec,
    VisualObject,
)
from lab.core.CP0001_structural_nodes.detectors.L_Rule import LRuleNodeDetector
from lab.core.CP0001_structural_nodes.metrics.M0001_relative_territory_volatility import (
    M0001RTV,
)


def _iso(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return str(value)


def _json_scalar(value: Any) -> Any:
    if pd.isna(value) if not isinstance(value, (list, tuple, dict)) else False:
        return None
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _time_index(df: pd.DataFrame) -> Dict[str, int]:
    return {_iso(row["time"]): int(i) for i, row in df.iterrows()}


def _quality(df: pd.DataFrame) -> DataQuality:
    if df.empty:
        return DataQuality(has_duplicates=False, is_sorted=True, missing_bars=None)
    return DataQuality(
        has_duplicates=bool(df["time"].duplicated().any()),
        is_sorted=bool(df["time"].is_monotonic_increasing),
        missing_bars=None,
    )


def _candles(df: pd.DataFrame) -> List[Candle]:
    output: List[Candle] = []
    for i, row in df.iterrows():
        volume = row.get("tick_volume", row.get("volume", None))
        output.append(
            Candle(
                id=f"candle:{int(i)}",
                index=int(i),
                time=_iso(row["time"]) or "",
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=None if pd.isna(volume) else float(volume),
                spread=None if pd.isna(row.get("spread", None)) else float(row.get("spread")),
            )
        )
    return output


def _node_objects(nodes_df: pd.DataFrame, df: pd.DataFrame, L: int) -> Tuple[List[VisualObject], List[Dict[str, Any]]]:
    objects: List[VisualObject] = []
    rows: List[Dict[str, Any]] = []
    if nodes_df is None or nodes_df.empty:
        return objects, rows

    time_to_index = _time_index(df)
    confirmed = nodes_df[nodes_df["confirmed"] == True].sort_values("time").reset_index(drop=True)
    for node_id, row in confirmed.iterrows():
        time = _iso(row["time"])
        node_index = time_to_index.get(time)
        if node_index is None:
            continue
        confirmation_index = node_index + L
        if confirmation_index >= len(df):
            continue
        node_type = str(row["type"]).upper()
        price = float(row["price"])
        object_id = f"node:{node_id}"
        selection_ref = {
            "kind": "node",
            "object_id": object_id,
            "table_id": "structural_nodes",
            "row_id": object_id,
        }
        objects.append(
            VisualObject(
                id=object_id,
                kind="marker",
                source_ref=SourceRef(
                    object_type="structural_node",
                    object_id=str(node_id),
                    hypothesis_id="H0001",
                ),
                time=time,
                index=node_index,
                price=price,
                shape="arrow_up" if node_type == "LOW" else "arrow_down",
                label=f"{node_type} L{L}",
                visible_from_index=confirmation_index,
                metadata={
                    "node_id": int(node_id),
                    "node_type": node_type,
                    "L": L,
                    "confirmed": True,
                    "confirmation_index": confirmation_index,
                    "confirmation_time": _iso(df.iloc[confirmation_index]["time"]),
                    "selection_ref": selection_ref,
                },
            )
        )
        rows.append(
            {
                "node_object_id": object_id,
                "node_id": int(node_id),
                "time": time,
                "type": node_type,
                "price": price,
                "node_index": node_index,
                "confirmation_index": confirmation_index,
                "confirmation_time": _iso(df.iloc[confirmation_index]["time"]),
                "selection_ref": selection_ref,
            }
        )
    return objects, rows


def _event_layers(events_df: pd.DataFrame, df: pd.DataFrame) -> Tuple[List[OverlayLayer], List[Dict[str, Any]]]:
    time_to_index = _time_index(df)
    zones: List[VisualObject] = []
    windows: List[VisualObject] = []
    labels: List[VisualObject] = []
    hunts: List[VisualObject] = []
    baselines: List[VisualObject] = []
    rows: List[Dict[str, Any]] = []

    if events_df is None or events_df.empty:
        return [
            OverlayLayer(layer_id="M0001:zones", label="M0001 Territories", type="zones", z_index=20, opacity=0.35, objects=[]),
            OverlayLayer(layer_id="M0001:events", label="M0001 Events", type="event_windows", z_index=30, opacity=0.55, objects=[]),
            OverlayLayer(layer_id="M0001:labels", label="RTV Labels", type="labels", z_index=60, objects=[]),
            OverlayLayer(layer_id="M0001:hunts", label="Hunt Markers", type="markers", z_index=70, objects=[]),
            OverlayLayer(layer_id="M0001:baseline", label="Baseline Windows", type="segments", z_index=10, opacity=0.35, objects=[]),
        ], rows

    for idx, row in events_df.reset_index(drop=True).iterrows():
        entry_time = _iso(row["entry_time"])
        exit_time = _iso(row["exit_time"])
        entry_index = time_to_index.get(entry_time)
        exit_index = time_to_index.get(exit_time)
        if entry_index is None or exit_index is None:
            continue

        node_id = int(row["node_id"])
        revisit_id = int(row["revisit_id"])
        event_id = f"m0001:event:node{node_id}:revisit{revisit_id}"
        rtv = None if pd.isna(row["RTV"]) else float(row["RTV"])
        event_length = int(row["event_length"])
        hunted = bool(row["hunted"])
        lower = float(row["territory_lower"])
        upper = float(row["territory_upper"])
        selection_ref = {
            "kind": "event",
            "object_id": event_id,
            "table_id": "M0001:events",
            "row_id": event_id,
        }

        source_ref = SourceRef(
            object_type="metric_event",
            object_id=f"node{node_id}:revisit{revisit_id}",
            metric_id="M0001",
            hypothesis_id="H0002",
            experiment_id="EXP0001",
        )
        common_metadata = {
            "node_id": node_id,
            "node_type": str(row["node_type"]),
            "node_price": float(row["node_price"]),
            "revisit_id": revisit_id,
            "RTV": rtv,
            "event_length": event_length,
            "hunted": hunted,
            "mean_inside": None if pd.isna(row["mean_inside"]) else float(row["mean_inside"]),
            "mean_before": None if pd.isna(row["mean_before"]) else float(row["mean_before"]),
            "median_inside": None if pd.isna(row["median_inside"]) else float(row["median_inside"]),
            "median_before": None if pd.isna(row["median_before"]) else float(row["median_before"]),
            "expansion_extreme": None if pd.isna(row["expansion_extreme"]) else float(row["expansion_extreme"]),
            "selection_ref": selection_ref,
        }

        zones.append(
            VisualObject(
                id=f"{event_id}:zone",
                kind="zone",
                source_ref=source_ref,
                start_index=entry_index,
                end_index=exit_index,
                lower=lower,
                upper=upper,
                visible_from_index=entry_index,
                complete_from_index=exit_index,
                metadata=common_metadata,
            )
        )
        windows.append(
            VisualObject(
                id=event_id,
                kind="event_window",
                source_ref=source_ref,
                entry_index=entry_index,
                exit_index=exit_index,
                entry_time=entry_time,
                exit_time=exit_time,
                visible_from_index=entry_index,
                complete_from_index=exit_index,
                metadata=common_metadata,
            )
        )
        labels.append(
            VisualObject(
                id=f"{event_id}:rtv",
                kind="label",
                source_ref=source_ref,
                time=exit_time,
                index=exit_index,
                price=upper,
                visible_from_index=exit_index,
                label="RTV —" if rtv is None else f"RTV {rtv:.2f}",
                metadata=common_metadata,
            )
        )
        baseline_start = max(entry_index - event_length, 0)
        baselines.append(
            VisualObject(
                id=f"{event_id}:baseline",
                kind="segment",
                source_ref=source_ref,
                start_index=baseline_start,
                end_index=max(entry_index - 1, baseline_start),
                lower=float(df["low"].iloc[baseline_start:max(entry_index, baseline_start + 1)].min()),
                upper=float(df["high"].iloc[baseline_start:max(entry_index, baseline_start + 1)].max()),
                visible_from_index=entry_index,
                metadata={**common_metadata, "role": "baseline_sample"},
            )
        )
        if hunted:
            hunts.append(
                VisualObject(
                    id=f"{event_id}:hunt",
                    kind="marker",
                    source_ref=source_ref,
                    time=exit_time,
                    index=exit_index,
                    price=float(row["node_price"]),
                    shape="circle",
                    label="HUNT",
                    visible_from_index=exit_index,
                    metadata=common_metadata,
                )
            )

        rows.append(
            {
                "event_id": event_id,
                "node_id": node_id,
                "node_type": str(row["node_type"]),
                "node_price": float(row["node_price"]),
                "revisit_id": revisit_id,
                "entry_time": entry_time,
                "exit_time": exit_time,
                "entry_index": entry_index,
                "exit_index": exit_index,
                "event_length": event_length,
                "territory_lower": lower,
                "territory_upper": upper,
                "expansion_extreme": None if pd.isna(row["expansion_extreme"]) else float(row["expansion_extreme"]),
                "mean_inside": None if pd.isna(row["mean_inside"]) else float(row["mean_inside"]),
                "mean_before": None if pd.isna(row["mean_before"]) else float(row["mean_before"]),
                "median_inside": None if pd.isna(row["median_inside"]) else float(row["median_inside"]),
                "median_before": None if pd.isna(row["median_before"]) else float(row["median_before"]),
                "RTV": rtv,
                "hunted": hunted,
                "selection_ref": selection_ref,
            }
        )

    layers = [
        OverlayLayer(layer_id="M0001:baseline", label="Baseline Windows", type="segments", z_index=10, opacity=0.25, objects=baselines),
        OverlayLayer(layer_id="M0001:zones", label="M0001 Territories", type="zones", z_index=20, opacity=0.35, objects=zones),
        OverlayLayer(layer_id="M0001:events", label="M0001 Events", type="event_windows", z_index=30, opacity=0.5, objects=windows),
        OverlayLayer(layer_id="M0001:labels", label="RTV Labels", type="labels", z_index=60, opacity=1.0, objects=labels),
        OverlayLayer(layer_id="M0001:hunts", label="Hunt Markers", type="markers", z_index=70, opacity=1.0, objects=hunts),
    ]
    return layers, rows


def build_m0001_replay(
    *,
    symbol: str,
    timeframe: str,
    L: int = 5,
    zone_ratio: float = 0.9,
    exit_gap: int = 6,
    consumption_mode: str = "hunt",
    source: str = "cache",
    reset_metric_cache: bool = False,
) -> ReplayPayload:
    if source != "cache":
        raise ValueError("The first UI implementation supports source=cache. Sync MT5 through MarketDataEngine before viewing live cache.")

    tf = parse_timeframe(timeframe)
    engine = CacheMarketDataEngine(base_path=settings.cache_data_path)
    df = engine.get_df(symbol, tf)
    if df.empty:
        raise ValueError(f"Dataset is empty: {symbol} {timeframe}")

    detector = LRuleNodeDetector(engine=engine, L=int(L), base_path=str(settings.cache_nodes_path))
    nodes_df = detector.detect(symbol, tf)
    metric = M0001RTV(
        engine=engine,
        detector=detector,
        zone_ratio=zone_ratio,
        exit_gap=exit_gap,
        consumption_mode=consumption_mode,
        base_path=str(settings.cache_metrics_path),
    )
    events_df = metric.compute(symbol, tf, reset_cache=reset_metric_cache)

    node_objects, node_rows = _node_objects(nodes_df, df, int(L))
    event_layers, event_rows = _event_layers(events_df, df)

    layers = [
        OverlayLayer(
            layer_id="structural_nodes",
            label=f"Confirmed L{int(L)} Nodes",
            type="markers",
            z_index=50,
            opacity=1.0,
            objects=node_objects,
        ),
        *event_layers,
    ]

    rtv_values = [row["RTV"] for row in event_rows if row.get("RTV") is not None]
    summary = {
        "confirmed_nodes": len(node_rows),
        "events": len(event_rows),
        "mean_RTV": None if not rtv_values else float(pd.Series(rtv_values).mean()),
        "median_RTV": None if not rtv_values else float(pd.Series(rtv_values).median()),
        "max_revisit": 0 if not event_rows else int(max(row["revisit_id"] for row in event_rows)),
    }

    tables = [
        TableSpec(
            table_id="M0001:events",
            label="M0001 RTV Events",
            primary_key="event_id",
            columns=[
                TableColumn(key="event_id", label="Event"),
                TableColumn(key="node_id", label="Node", type="integer"),
                TableColumn(key="node_type", label="Type"),
                TableColumn(key="revisit_id", label="Revisit", type="integer"),
                TableColumn(key="entry_index", label="Entry", type="integer"),
                TableColumn(key="exit_index", label="Exit", type="integer"),
                TableColumn(key="event_length", label="Length", type="integer"),
                TableColumn(key="RTV", label="RTV", type="number"),
                TableColumn(key="hunted", label="Hunted", type="boolean"),
            ],
            rows=event_rows,
        ),
        TableSpec(
            table_id="structural_nodes",
            label="Confirmed Structural Nodes",
            primary_key="node_object_id",
            columns=[
                TableColumn(key="node_object_id", label="Node Object"),
                TableColumn(key="node_id", label="Node", type="integer"),
                TableColumn(key="type", label="Type"),
                TableColumn(key="price", label="Price", type="number"),
                TableColumn(key="node_index", label="Node Index", type="integer"),
                TableColumn(key="confirmation_index", label="Confirmed At", type="integer"),
            ],
            rows=node_rows,
        ),
    ]

    selection_map: Dict[str, Dict[str, Any]] = {}
    for row in event_rows:
        selection_map[row["event_id"]] = {
            "title": f"M0001 Event {row['event_id']}",
            "subtitle": f"{row['node_type']} node {row['node_id']} · revisit {row['revisit_id']}",
            "kind": "event",
            "row": row,
        }
    for row in node_rows:
        selection_map[row["node_object_id"]] = {
            "title": f"{row['type']} L{int(L)} Node {row['node_id']}",
            "subtitle": f"Confirmed at candle {row['confirmation_index']}",
            "kind": "node",
            "row": row,
        }

    dataset = DatasetDescriptor(
        dataset_id=f"{symbol}:{tf.name}:{source}:M0001:L{int(L)}:ZR{zone_ratio}:EG{exit_gap}:{consumption_mode}",
        source=source,
        symbol=symbol,
        timeframe=tf.name,
        start_time=_iso(df.iloc[0]["time"]),
        end_time=_iso(df.iloc[-1]["time"]),
        bars=int(len(df)),
        data_quality=_quality(df),
        parameters={
            "metric_id": "M0001",
            "L": int(L),
            "zone_ratio": float(zone_ratio),
            "exit_gap": int(exit_gap),
            "consumption_mode": consumption_mode,
            **summary,
        },
        contract_version=settings.contract_version,
    )

    return ReplayPayload(
        dataset=dataset,
        candles=_candles(df),
        layers=layers,
        tables=tables,
        selection_map=selection_map,
        inspector=InspectorPayload(
            title="M0001 RTV Replay",
            subtitle=f"{symbol} {tf.name} · {len(event_rows)} events · {len(node_rows)} confirmed nodes",
            sections=[
                {"label": "Parameters", "items": dataset.parameters},
                {"label": "Source", "items": {"source": source, "bars": len(df), "contract": settings.contract_version}},
            ],
        ),
    )


def build_m0001_summary(**kwargs: Any) -> MetricSummary:
    payload = build_m0001_replay(**kwargs)
    params = payload.dataset.parameters
    return MetricSummary(
        source=payload.dataset.source,
        symbol=payload.dataset.symbol,
        timeframe=payload.dataset.timeframe,
        bars=payload.dataset.bars,
        L=int(params["L"]),
        zone_ratio=float(params["zone_ratio"]),
        exit_gap=int(params["exit_gap"]),
        consumption_mode=str(params["consumption_mode"]),
        confirmed_nodes=int(params["confirmed_nodes"]),
        events=int(params["events"]),
        mean_RTV=params["mean_RTV"],
        median_RTV=params["median_RTV"],
        max_revisit=int(params["max_revisit"]),
    )
