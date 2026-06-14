from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UiTimeframe:
    """Small timeframe object compatible with current lab components.

    Existing detectors and metrics only require `timeframe.name`. This avoids a
    hard runtime dependency on MetaTrader5 for cache-only UI inspection.
    """

    name: str


ALLOWED_TIMEFRAMES = {
    "M1", "M2", "M3", "M4", "M5", "M6", "M10", "M12", "M15", "M20", "M30",
    "H1", "H2", "H3", "H4", "H6", "H8", "H12", "D1", "W1", "MN1",
}


def parse_timeframe(value: str) -> UiTimeframe:
    normalized = str(value).upper().strip()
    if normalized not in ALLOWED_TIMEFRAMES:
        raise ValueError(f"Unsupported timeframe: {value}")
    return UiTimeframe(name=normalized)
