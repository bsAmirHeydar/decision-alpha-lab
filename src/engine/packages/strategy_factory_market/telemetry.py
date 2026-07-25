from __future__ import annotations
from dataclasses import dataclass, replace

@dataclass(frozen=True, slots=True)
class MarketTelemetrySnapshot:
    tick_updates: int = 0
    tick_hits: int = 0
    tick_misses: int = 0
    bar_refreshes: int = 0
    bar_insertions: int = 0
    bar_replacements: int = 0
    bar_duplicates: int = 0
    detected_gaps: int = 0
    sync_checks: int = 0
    sync_failures: int = 0
    specification_refreshes: int = 0
    source_errors: int = 0
    last_refresh_latency_us: int = 0
    maximum_refresh_latency_us: int = 0

class MarketTelemetry:
    def __init__(self) -> None:
        self._values = {field: 0 for field in MarketTelemetrySnapshot.__dataclass_fields__}

    def increment(self, field: str, amount: int = 1) -> None:
        if field not in self._values:
            raise KeyError(field)
        if amount < 0:
            raise ValueError("negative telemetry increment")
        self._values[field] += amount

    def refresh_latency(self, value_us: int) -> None:
        if value_us < 0:
            raise ValueError("negative latency")
        self._values["last_refresh_latency_us"] = value_us
        self._values["maximum_refresh_latency_us"] = max(
            self._values["maximum_refresh_latency_us"], value_us
        )

    def snapshot(self) -> MarketTelemetrySnapshot:
        return MarketTelemetrySnapshot(**self._values)
