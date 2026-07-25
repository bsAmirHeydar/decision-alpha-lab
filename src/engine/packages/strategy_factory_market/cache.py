from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
from .enums import DataQuality
from strategy_factory_contracts.records import BarRecord
from strategy_factory_contracts.validation import validate_terminal_symbol

@dataclass(frozen=True, slots=True)
class TickSnapshot:
    symbol: str
    source_time_milliseconds: int
    received_at_utc_milliseconds: int
    bid: float
    ask: float
    last: float
    source_generation: int
    quality: DataQuality = DataQuality.VALID

    def __post_init__(self) -> None:
        validate_terminal_symbol(self.symbol, "symbol")
        if self.source_time_milliseconds < 0 or self.received_at_utc_milliseconds < 0:
            raise ValueError("negative tick time")
        if self.ask > 0 and self.bid > 0 and self.ask < self.bid:
            raise ValueError("ask below bid")
        if self.source_generation < 0:
            raise ValueError("negative source generation")

class TickCache:
    def __init__(self) -> None:
        self._items: dict[str, TickSnapshot] = {}

    def put(self, snapshot: TickSnapshot) -> None:
        previous = self._items.get(snapshot.symbol)
        if previous and snapshot.source_time_milliseconds < previous.source_time_milliseconds:
            raise ValueError("out-of-order tick")
        self._items[snapshot.symbol] = snapshot

    def get(self, symbol: str, now_utc_milliseconds: int, max_age_milliseconds: int) -> TickSnapshot:
        snapshot = self._items.get(symbol)
        if snapshot is None:
            raise KeyError("tick not cached")
        age = now_utc_milliseconds - snapshot.received_at_utc_milliseconds
        if age < 0:
            raise ValueError("tick from future")
        if max_age_milliseconds >= 0 and age > max_age_milliseconds:
            raise RuntimeError("tick stale")
        return snapshot

class BarSeries:
    def __init__(self, symbol: str, timeframe_seconds: int, capacity: int = 2048) -> None:
        validate_terminal_symbol(symbol, "symbol")
        if timeframe_seconds <= 0 or capacity < 2:
            raise ValueError("invalid series configuration")
        self.symbol = symbol
        self.timeframe_seconds = timeframe_seconds
        self.capacity = capacity
        self._bars: list[BarRecord] = []
        self.has_gap = False
        self.generation = 0

    @property
    def bars(self) -> tuple[BarRecord, ...]:
        return tuple(self._bars)

    @property
    def latest(self) -> BarRecord:
        if not self._bars:
            raise KeyError("series empty")
        return self._bars[-1]

    def upsert(self, bar: BarRecord) -> str:
        if bar.symbol != self.symbol or bar.timeframe_seconds != self.timeframe_seconds:
            raise ValueError("bar key mismatch")
        if self._bars:
            last = self._bars[-1]
            if bar.open_time.utc_epoch_milliseconds < last.open_time.utc_epoch_milliseconds:
                raise ValueError("out-of-order bar")
            if bar.open_time.utc_epoch_milliseconds == last.open_time.utc_epoch_milliseconds:
                if bar == last:
                    return "duplicate"
                self._bars[-1] = bar
                self.generation += 1
                return "replaced"
            expected = last.open_time.utc_epoch_milliseconds + self.timeframe_seconds * 1000
            if bar.open_time.utc_epoch_milliseconds > expected:
                self.has_gap = True
        self._bars.append(bar)
        if len(self._bars) > self.capacity:
            self._bars = self._bars[-self.capacity :]
        self.generation += 1
        return "gap_inserted" if self.has_gap else "inserted"

    def recent(self, requested: int) -> tuple[BarRecord, ...]:
        if requested < 0:
            raise ValueError("requested must be non-negative")
        return tuple(self._bars[-requested:]) if requested else ()

class BarCache:
    def __init__(self) -> None:
        self._series: dict[tuple[str, int], BarSeries] = {}

    def ensure(self, symbol: str, timeframe_seconds: int, capacity: int = 2048) -> BarSeries:
        key = (symbol, timeframe_seconds)
        if key not in self._series:
            self._series[key] = BarSeries(symbol, timeframe_seconds, capacity)
        return self._series[key]

    def upsert(self, bar: BarRecord) -> str:
        return self.ensure(bar.symbol, bar.timeframe_seconds).upsert(bar)

    def get(self, symbol: str, timeframe_seconds: int) -> BarSeries:
        try:
            return self._series[(symbol, timeframe_seconds)]
        except KeyError as exc:
            raise KeyError("series not registered") from exc
