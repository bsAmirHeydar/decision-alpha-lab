"""Bounded in-memory telemetry for the decision path."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from threading import RLock
from typing import Mapping


@dataclass(frozen=True, slots=True)
class DecisionTelemetry:
    event_id: str
    strategy_id: str
    status: str
    total_latency_ns: int
    stage_latency_ns: Mapping[str, int]
    cache_hits: int
    cache_misses: int
    candidate_count: int
    reason_codes: tuple[str, ...]
    plan_hash: str


class TelemetryBuffer:
    def __init__(self, maxlen: int = 10000) -> None:
        self._items: deque[DecisionTelemetry] = deque(maxlen=maxlen)
        self._lock = RLock()

    def append(self, item: DecisionTelemetry) -> None:
        with self._lock:
            self._items.append(item)

    def snapshot(self) -> tuple[DecisionTelemetry, ...]:
        with self._lock:
            return tuple(self._items)

    def latency_percentile_ns(self, percentile: float) -> float:
        values = sorted(item.total_latency_ns for item in self.snapshot())
        if not values:
            return 0.0
        p = min(100.0, max(0.0, float(percentile))) / 100.0
        index = int(round((len(values) - 1) * p))
        return float(values[index])
