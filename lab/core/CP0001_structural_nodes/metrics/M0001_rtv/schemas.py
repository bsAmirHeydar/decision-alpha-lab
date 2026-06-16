from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class RTVConfig:
    """Runtime configuration for M0001 Relative Territory Volatility."""

    L: int = 5
    zone_ratio: float = 0.9
    exit_gap: int = 6
    consumption_mode: str = "hunt"  # "hunt" or "touch"
    max_before_logs: int = 500

    def validate(self) -> None:
        if self.L < 1:
            raise ValueError("L must be >= 1")
        if not 0.0 <= float(self.zone_ratio) <= 1.0:
            raise ValueError("zone_ratio must be between 0 and 1")
        if int(self.exit_gap) < 1:
            raise ValueError("exit_gap must be >= 1")
        if self.consumption_mode not in {"hunt", "touch"}:
            raise ValueError("consumption_mode must be either 'hunt' or 'touch'")
        if int(self.max_before_logs) < 1:
            raise ValueError("max_before_logs must be >= 1")


@dataclass(frozen=True)
class ReferencePoint:
    """A point that can be tested by the M0001 engine.

    The engine does not care whether this point came from a structural L-rule
    node or from a random baseline. That separation is intentional: actual and
    random tests must share the exact same metric logic.
    """

    ref_id: int
    time: Any
    index: int
    ref_type: str  # LOW or HIGH
    price: float
    confirmed: bool = True
    active_from_index: int | None = None
    baseline_kind: str = "actual"  # actual or random

    def normalized_type(self) -> str:
        value = str(self.ref_type).upper()
        if value not in {"LOW", "HIGH"}:
            raise ValueError(f"Invalid reference point type: {self.ref_type!r}")
        return value


@dataclass
class RTVEvent:
    node_id: int
    node_time: Any
    node_type: str
    node_price: float
    revisit_id: int
    entry_time: Any
    exit_time: Any
    event_length: int
    territory_lower: float
    territory_upper: float
    expansion_extreme: float
    mean_inside: float
    mean_before: float
    median_inside: float
    median_before: float
    RTV: float
    hunted: bool
    entry_index: int | None = None
    exit_index: int | None = None
    hunt_index: int | None = None
    hunt_time: Any | None = None
    hunt_price: float | None = None
    baseline_kind: str = "actual"

    def to_dict(self, include_visual_fields: bool = False) -> dict[str, Any]:
        row = asdict(self)
        if not include_visual_fields:
            for key in [
                "entry_index",
                "exit_index",
                "hunt_index",
                "hunt_time",
                "hunt_price",
                "baseline_kind",
            ]:
                row.pop(key, None)
        return row


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

VISUAL_COLUMNS = OUTPUT_COLUMNS + [
    "entry_index",
    "exit_index",
    "hunt_index",
    "hunt_time",
    "hunt_price",
    "baseline_kind",
]


def events_to_dataframe(events: list[RTVEvent], include_visual_fields: bool = False) -> pd.DataFrame:
    columns = VISUAL_COLUMNS if include_visual_fields else OUTPUT_COLUMNS
    return pd.DataFrame([event.to_dict(include_visual_fields=include_visual_fields) for event in events], columns=columns)
