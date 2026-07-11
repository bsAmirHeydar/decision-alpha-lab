"""Latency measurement, budgets, and breach reporting."""
from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter_ns
from typing import Mapping


@dataclass(frozen=True, slots=True)
class LatencyBudget:
    stage_limits_ns: Mapping[str, int]
    total_limit_ns: int | None = None
    action_on_breach: str = "record"  # record | abstain | raise


@dataclass(frozen=True, slots=True)
class LatencyReport:
    stages_ns: Mapping[str, int]
    total_ns: int
    breaches: tuple[str, ...]


class LatencyTracker:
    __slots__ = ("_starts", "_durations", "_overall_start")

    def __init__(self) -> None:
        self._starts: dict[str, int] = {}
        self._durations: dict[str, int] = {}
        self._overall_start = perf_counter_ns()

    def start(self, stage: str) -> None:
        self._starts[stage] = perf_counter_ns()

    def stop(self, stage: str) -> int:
        start = self._starts.pop(stage, None)
        if start is None:
            raise KeyError(f"latency stage was not started: {stage}")
        duration = perf_counter_ns() - start
        self._durations[stage] = self._durations.get(stage, 0) + duration
        return duration

    def report(self, budget: LatencyBudget | None = None) -> LatencyReport:
        total = perf_counter_ns() - self._overall_start
        breaches: list[str] = []
        if budget is not None:
            for stage, limit in budget.stage_limits_ns.items():
                if self._durations.get(stage, 0) > limit:
                    breaches.append(stage)
            if budget.total_limit_ns is not None and total > budget.total_limit_ns:
                breaches.append("total")
        return LatencyReport(dict(self._durations), total, tuple(breaches))
