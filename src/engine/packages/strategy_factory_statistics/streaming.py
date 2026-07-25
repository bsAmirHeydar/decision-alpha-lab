from __future__ import annotations
from dataclasses import dataclass
import bisect, math

class OnlineMoments:
    __slots__ = ("count", "mean", "m2", "minimum", "maximum")
    def __init__(self) -> None:
        self.count = 0; self.mean = 0.0; self.m2 = 0.0
        self.minimum = math.inf; self.maximum = -math.inf
    def add(self, value: float) -> None:
        if not math.isfinite(value): raise ValueError("non-finite observation")
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        self.m2 += delta * (value - self.mean)
        self.minimum = min(self.minimum, value); self.maximum = max(self.maximum, value)
    @property
    def variance(self) -> float:
        return self.m2 / (self.count - 1) if self.count > 1 else 0.0
    @property
    def standard_deviation(self) -> float: return math.sqrt(max(0.0, self.variance))
    @property
    def standard_error(self) -> float:
        return self.standard_deviation / math.sqrt(self.count) if self.count else 0.0

class DrawdownTracker:
    __slots__ = ("equity", "peak", "maximum_drawdown", "trough", "maximum_runup")
    def __init__(self) -> None:
        self.equity = 0.0; self.peak = 0.0; self.maximum_drawdown = 0.0
        self.trough = 0.0; self.maximum_runup = 0.0
    def add(self, value: float) -> None:
        self.equity += value
        self.peak = max(self.peak, self.equity)
        self.maximum_drawdown = max(self.maximum_drawdown, self.peak - self.equity)
        self.trough = min(self.trough, self.equity)
        self.maximum_runup = max(self.maximum_runup, self.equity - self.trough)

class BoundedQuantileSketch:
    __slots__ = ("capacity", "values", "seen")
    def __init__(self, capacity: int = 4096) -> None:
        if capacity < 16: raise ValueError("quantile capacity too small")
        self.capacity = capacity; self.values: list[float] = []; self.seen = 0
    def add(self, value: float) -> None:
        if not math.isfinite(value): raise ValueError("non-finite quantile observation")
        self.seen += 1
        if len(self.values) < self.capacity:
            bisect.insort(self.values, value); return
        # deterministic bounded compression: replace one evenly spaced slot.
        slot = (self.seen * 2654435761) % self.capacity
        del self.values[slot]
        bisect.insort(self.values, value)
    def quantile(self, q: float) -> float:
        if not self.values: return 0.0
        if not 0 <= q <= 1: raise ValueError("invalid quantile")
        pos = q * (len(self.values) - 1)
        lo = int(math.floor(pos)); hi = int(math.ceil(pos))
        if lo == hi: return self.values[lo]
        return self.values[lo] + (self.values[hi] - self.values[lo]) * (pos - lo)

class DistributionAccumulator:
    def __init__(self, quantile_capacity: int = 4096) -> None:
        self.moments = OnlineMoments(); self.quantiles = BoundedQuantileSketch(quantile_capacity)
        self.drawdown = DrawdownTracker(); self.sum_positive = 0.0; self.sum_negative_abs = 0.0
        self.best = -math.inf; self.worst = math.inf
    def add(self, value: float) -> None:
        self.moments.add(value); self.quantiles.add(value); self.drawdown.add(value)
        if value > 0: self.sum_positive += value
        elif value < 0: self.sum_negative_abs += abs(value)
        self.best = max(self.best, value); self.worst = min(self.worst, value)
    @property
    def profit_factor(self) -> float:
        if self.sum_negative_abs > 0: return self.sum_positive / self.sum_negative_abs
        return 1e9 if self.sum_positive > 0 else 0.0
