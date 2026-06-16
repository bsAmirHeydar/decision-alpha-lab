from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd

from .math_utils import log_move
from .schemas import RTVConfig, RTVEvent, ReferencePoint
from .time_utils import format_mql_time

VISUAL_HEADER = [
    "kind",
    "baseline",
    "id",
    "start_time",
    "end_time",
    "anchor_time",
    "price",
    "lower",
    "upper",
    "label",
    "node_type",
    "rtv",
    "hunted",
    "node_id",
    "revisit_id",
    "entry_index",
    "exit_index",
    "candle_index",
    "value1",
    "value2",
    "note",
]


def build_visual_rows(
    reference_points: list[ReferencePoint],
    events: list[RTVEvent],
    candles_df: pd.DataFrame | None = None,
    config: RTVConfig | None = None,
) -> list[dict[str, Any]]:
    """Build the MT5 visual contract from the Python research engine output.

    MQL does not compute the metric. Every visual object here is derived from
    the same Python M0001 engine used for tests, exports, validation and live
    visual inspection.
    """
    rows: list[dict[str, Any]] = []
    candles = _normalize_candles(candles_df)

    for ref in reference_points:
        node_label = f"{ref.baseline_kind[:3].upper()} {ref.normalized_type()} #{ref.ref_id}"
        rows.append(
            _row(
                kind="NODE",
                baseline=ref.baseline_kind,
                id=f"{ref.baseline_kind.upper()}_NODE_{ref.ref_id}",
                anchor_time=ref.time,
                price=ref.price,
                label=node_label,
                node_type=ref.normalized_type(),
                node_id=ref.ref_id,
                note="reference point from Python single-source engine",
            )
        )
        rows.append(
            _row(
                kind="NODE_PRICE",
                baseline=ref.baseline_kind,
                id=f"{ref.baseline_kind.upper()}_NODE_{ref.ref_id}_PRICE",
                anchor_time=ref.time,
                price=ref.price,
                label=f"NODE PRICE {ref.price:.5g}",
                node_type=ref.normalized_type(),
                node_id=ref.ref_id,
            )
        )
        if candles is not None and ref.active_from_index is not None and 0 <= int(ref.active_from_index) < len(candles):
            rows.append(
                _row(
                    kind="ACTIVE_FROM",
                    baseline=ref.baseline_kind,
                    id=f"{ref.baseline_kind.upper()}_NODE_{ref.ref_id}_ACTIVE_FROM",
                    anchor_time=candles.iloc[int(ref.active_from_index)]["time"],
                    price=ref.price,
                    label=f"ACTIVE FROM +L={config.L if config else ''}",
                    node_type=ref.normalized_type(),
                    node_id=ref.ref_id,
                    candle_index=ref.active_from_index,
                    note="node logic starts here; not before confirmation",
                )
            )
            if ref.index is not None and 0 <= int(ref.index) < len(candles):
                rows.append(
                    _row(
                        kind="CONFIRMATION_WINDOW",
                        baseline=ref.baseline_kind,
                        id=f"{ref.baseline_kind.upper()}_NODE_{ref.ref_id}_CONFIRM_WINDOW",
                        start_time=candles.iloc[int(ref.index)]["time"],
                        end_time=candles.iloc[int(ref.active_from_index)]["time"],
                        lower=ref.price,
                        upper=ref.price,
                        label="confirmation delay",
                        node_type=ref.normalized_type(),
                        node_id=ref.ref_id,
                    )
                )

    for event in events:
        base = event.baseline_kind
        event_id = f"{base.upper()}_EVENT_{event.node_id}_{event.revisit_id}_{event.entry_index}"
        label = f"RTV {event.RTV:.2f}"
        node_label = f"{event.node_type} node #{event.node_id} r{event.revisit_id}"

        rows.extend(
            [
                _row(
                    kind="TERRITORY",
                    baseline=base,
                    id=f"{event_id}_TERRITORY",
                    start_time=event.entry_time,
                    end_time=event.exit_time,
                    lower=event.territory_lower,
                    upper=event.territory_upper,
                    label=label,
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    entry_index=event.entry_index,
                    exit_index=event.exit_index,
                ),
                _row(
                    kind="EVENT",
                    baseline=base,
                    id=f"{event_id}_WINDOW",
                    start_time=event.entry_time,
                    end_time=event.exit_time,
                    lower=event.territory_lower,
                    upper=event.territory_upper,
                    label=node_label,
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    entry_index=event.entry_index,
                    exit_index=event.exit_index,
                ),
                _row(
                    kind="RTV_LABEL",
                    baseline=base,
                    id=f"{event_id}_RTV",
                    anchor_time=_mid_time(event.entry_time, event.exit_time),
                    price=event.territory_upper,
                    label=label,
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    entry_index=event.entry_index,
                    exit_index=event.exit_index,
                    value1=event.mean_inside,
                    value2=event.mean_before,
                    note=f"RTV={event.RTV:.6g} = mean_inside {event.mean_inside:.6g} / mean_before {event.mean_before:.6g}",
                ),
                _row(
                    kind="RTV_FORMULA",
                    baseline=base,
                    id=f"{event_id}_FORMULA",
                    anchor_time=_mid_time(event.entry_time, event.exit_time),
                    price=event.territory_upper,
                    label=f"inside={event.mean_inside:.3f} before={event.mean_before:.3f} RTV={event.RTV:.2f}",
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    entry_index=event.entry_index,
                    exit_index=event.exit_index,
                    value1=event.mean_inside,
                    value2=event.mean_before,
                ),
                _row(
                    kind="ENTRY",
                    baseline=base,
                    id=f"{event_id}_ENTRY",
                    anchor_time=event.entry_time,
                    price=event.territory_upper,
                    label="ENTRY",
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    candle_index=event.entry_index,
                    note="first wick intersection with territory",
                ),
                _row(
                    kind="EXIT",
                    baseline=base,
                    id=f"{event_id}_EXIT",
                    anchor_time=event.exit_time,
                    price=event.territory_lower,
                    label=f"EXIT gap={config.exit_gap if config else ''}",
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    candle_index=event.exit_index,
                    note="event closed by outside_count >= exit_gap",
                ),
                _row(
                    kind="EXPANSION_EXTREME",
                    baseline=base,
                    id=f"{event_id}_EXTREME",
                    anchor_time=event.entry_time,
                    price=event.expansion_extreme,
                    label=f"EXTREME {event.expansion_extreme:.5g}",
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                ),
                _row(
                    kind="EVENT_INFO",
                    baseline=base,
                    id=f"{event_id}_INFO",
                    anchor_time=event.exit_time,
                    price=event.territory_upper,
                    label=(
                        f"node={event.node_id} r={event.revisit_id} "
                        f"inside_n={event.event_length} before_n={event.event_length} "
                        f"RTV={event.RTV:.3f} hunted={int(event.hunted)}"
                    ),
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=event.hunted,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    entry_index=event.entry_index,
                    exit_index=event.exit_index,
                ),
            ]
        )

        if event.hunted and event.hunt_time is not None and event.hunt_price is not None:
            rows.append(
                _row(
                    kind="HUNT",
                    baseline=base,
                    id=f"{event_id}_HUNT",
                    anchor_time=event.hunt_time,
                    price=event.hunt_price,
                    label="HUNT" if base == "actual" else "RND HUNT",
                    node_type=event.node_type,
                    rtv=event.RTV,
                    hunted=True,
                    node_id=event.node_id,
                    revisit_id=event.revisit_id,
                    candle_index=event.hunt_index,
                    note="first candle that breached node_price",
                )
            )

        if candles is not None:
            _append_sample_rows(rows, candles, event, event_id, config)

    return rows


def write_visual_csv(path: str | Path, rows: list[dict[str, Any]]) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=VISUAL_HEADER, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _clean_value(row.get(key, "")) for key in VISUAL_HEADER})
    return path


def _append_sample_rows(rows: list[dict[str, Any]], candles: pd.DataFrame, event: RTVEvent, event_id: str, config: RTVConfig | None) -> None:
    before_start = event.before_start_index
    before_end = event.before_end_index
    if before_start is not None and before_end is not None:
        for i in range(max(0, int(before_start)), min(len(candles) - 1, int(before_end)) + 1):
            candle = candles.iloc[i]
            rows.append(
                _candle_row(
                    kind="BEFORE_SAMPLE",
                    event=event,
                    event_id=event_id,
                    candle=candle,
                    candle_index=i,
                    label="BEFORE",
                    note="baseline candle used in mean_before",
                )
            )

    inside_set = set(int(i) for i in (event.inside_indices or []))
    for i in sorted(inside_set):
        if 0 <= i < len(candles):
            rows.append(
                _candle_row(
                    kind="INSIDE_SAMPLE",
                    event=event,
                    event_id=event_id,
                    candle=candles.iloc[i],
                    candle_index=i,
                    label="INSIDE",
                    note="inside-territory candle used in mean_inside",
                )
            )

    if event.entry_index is not None and event.exit_index is not None:
        for i in range(max(0, int(event.entry_index)), min(len(candles) - 1, int(event.exit_index)) + 1):
            if i in inside_set:
                continue
            candle = candles.iloc[i]
            rows.append(
                _candle_row(
                    kind="OUTSIDE_ACTIVE",
                    event=event,
                    event_id=event_id,
                    candle=candle,
                    candle_index=i,
                    label="OUT",
                    note="outside territory while event was still active",
                )
            )


def _candle_row(kind: str, event: RTVEvent, event_id: str, candle: pd.Series, candle_index: int, label: str, note: str) -> dict[str, Any]:
    move = log_move(candle["high"], candle["low"])
    return _row(
        kind=kind,
        baseline=event.baseline_kind,
        id=f"{event_id}_{kind}_{candle_index}",
        start_time=candle["time"],
        end_time=candle["time"],
        anchor_time=candle["time"],
        price=candle["high"],
        lower=candle["low"],
        upper=candle["high"],
        label=label,
        node_type=event.node_type,
        rtv=event.RTV,
        hunted=event.hunted,
        node_id=event.node_id,
        revisit_id=event.revisit_id,
        entry_index=event.entry_index,
        exit_index=event.exit_index,
        candle_index=candle_index,
        value1=move,
        note=note,
    )


def _row(
    kind: str,
    baseline: str,
    id: str,
    start_time: Any = "",
    end_time: Any = "",
    anchor_time: Any = "",
    price: Any = "",
    lower: Any = "",
    upper: Any = "",
    label: str = "",
    node_type: str = "",
    rtv: Any = "",
    hunted: Any = "",
    node_id: Any = "",
    revisit_id: Any = "",
    entry_index: Any = "",
    exit_index: Any = "",
    candle_index: Any = "",
    value1: Any = "",
    value2: Any = "",
    note: str = "",
) -> dict[str, Any]:
    return {
        "kind": kind,
        "baseline": baseline,
        "id": id,
        "start_time": format_mql_time(start_time) if start_time != "" else "",
        "end_time": format_mql_time(end_time) if end_time != "" else "",
        "anchor_time": format_mql_time(anchor_time) if anchor_time != "" else "",
        "price": price,
        "lower": lower,
        "upper": upper,
        "label": label,
        "node_type": node_type,
        "rtv": rtv,
        "hunted": hunted,
        "node_id": node_id,
        "revisit_id": revisit_id,
        "entry_index": entry_index,
        "exit_index": exit_index,
        "candle_index": candle_index,
        "value1": value1,
        "value2": value2,
        "note": note,
    }


def _normalize_candles(candles_df: pd.DataFrame | None) -> pd.DataFrame | None:
    if candles_df is None or candles_df.empty or "time" not in candles_df.columns:
        return None
    out = candles_df.copy()
    out["time"] = pd.to_datetime(out["time"])
    out = out.drop_duplicates("time", keep="last").sort_values("time").reset_index(drop=True)
    return out


def _mid_time(entry: Any, exit: Any) -> Any:
    if entry is None or exit is None:
        return entry or exit
    entry_ts = pd.Timestamp(entry)
    exit_ts = pd.Timestamp(exit)
    return entry_ts + (exit_ts - entry_ts) / 2


def _clean_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, float):
        return f"{value:.10g}"
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    text = str(value)
    return text.replace(",", " ").replace("\n", " ").replace("\r", " ").strip()
