"""Reproducible latency benchmark helpers."""
from __future__ import annotations

from statistics import mean
from time import perf_counter_ns
from typing import Callable, Sequence


def benchmark(call: Callable[[], object], *, warmup: int = 100, iterations: int = 1000) -> dict[str, float]:
    for _ in range(max(0, warmup)):
        call()
    values: list[int] = []
    for _ in range(max(1, iterations)):
        start = perf_counter_ns()
        call()
        values.append(perf_counter_ns() - start)
    ordered = sorted(values)

    def percentile(p: float) -> float:
        idx = int(round((len(ordered) - 1) * p))
        return float(ordered[idx])

    return {
        "iterations": float(len(values)),
        "mean_ns": float(mean(values)),
        "p50_ns": percentile(0.50),
        "p95_ns": percentile(0.95),
        "p99_ns": percentile(0.99),
        "max_ns": float(max(values)),
    }
