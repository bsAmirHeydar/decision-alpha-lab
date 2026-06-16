from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd

from .schemas import RTVEvent, ReferencePoint
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
]


def build_visual_rows(reference_points: list[ReferencePoint], events: list[RTVEvent]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for ref in reference_points:
        rows.append(
            _row(
                kind="NODE",
                baseline=ref.baseline_kind,
                id=f"{ref.baseline_kind.upper()}_NODE_{ref.ref_id}",
                anchor_time=ref.time,
                price=ref.price,
                label=f"{ref.baseline_kind[:3].upper()} {ref.normalized_type()} #{ref.ref_id}",
                node_type=ref.normalized_type(),
            )
        )

    for event in events:
        base = event.baseline_kind
        event_id = f"{base.upper()}_EVENT_{event.node_id}_{event.revisit_id}_{event.entry_index}"
        label = f"RTV {event.RTV:.2f}"
        rows.append(
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
            )
        )
        rows.append(
            _row(
                kind="EVENT",
                baseline=base,
                id=f"{event_id}_WINDOW",
                start_time=event.entry_time,
                end_time=event.exit_time,
                lower=event.territory_lower,
                upper=event.territory_upper,
                label=label,
                node_type=event.node_type,
                rtv=event.RTV,
                hunted=event.hunted,
            )
        )
        rows.append(
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
            )
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
                )
            )

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
    }


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
    text = str(value)
    return text.replace(",", " ").replace("\n", " ").replace("\r", " ").strip()
