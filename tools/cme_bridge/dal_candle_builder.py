"""Decision Alpha Lab candle builder utilities.

This module is vendor-neutral. It can build bars from any tick/trade stream that
provides timestamp, price, and optional size. It does not bypass or replace CME
market-data entitlements; it only normalizes legally obtained data into DAL's
internal candle schema.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Iterable, Iterator, Optional


@dataclass(frozen=True)
class Tick:
    symbol: str
    time_utc: datetime
    price: float
    size: float = 0.0


@dataclass
class Bar:
    symbol: str
    time_utc: datetime
    timeframe_seconds: int
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    source: str = "EXTERNAL"
    contract: str = ""

    def to_csv_row(self) -> str:
        ts = self.time_utc.strftime("%Y-%m-%d %H:%M:%S")
        return f"{ts},{self.open},{self.high},{self.low},{self.close},{self.volume:.0f}\n"


def floor_time(dt: datetime, seconds: int) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    epoch = int(dt.timestamp())
    floored = epoch - (epoch % seconds)
    return datetime.fromtimestamp(floored, tz=timezone.utc)


class CandleBuilder:
    def __init__(self, timeframe_seconds: int = 60, source: str = "EXTERNAL") -> None:
        if timeframe_seconds <= 0:
            raise ValueError("timeframe_seconds must be positive")
        self.timeframe_seconds = timeframe_seconds
        self.source = source
        self._bar: Optional[Bar] = None

    def update(self, tick: Tick) -> list[Bar]:
        bucket = floor_time(tick.time_utc, self.timeframe_seconds)
        emitted: list[Bar] = []
        if self._bar is None:
            self._bar = Bar(
                symbol=tick.symbol,
                time_utc=bucket,
                timeframe_seconds=self.timeframe_seconds,
                open=tick.price,
                high=tick.price,
                low=tick.price,
                close=tick.price,
                volume=tick.size,
                source=self.source,
            )
            return emitted

        if bucket != self._bar.time_utc or tick.symbol != self._bar.symbol:
            emitted.append(self._bar)
            self._bar = Bar(
                symbol=tick.symbol,
                time_utc=bucket,
                timeframe_seconds=self.timeframe_seconds,
                open=tick.price,
                high=tick.price,
                low=tick.price,
                close=tick.price,
                volume=tick.size,
                source=self.source,
            )
            return emitted

        self._bar.high = max(self._bar.high, tick.price)
        self._bar.low = min(self._bar.low, tick.price)
        self._bar.close = tick.price
        self._bar.volume += tick.size
        return emitted

    def flush(self) -> list[Bar]:
        if self._bar is None:
            return []
        b = self._bar
        self._bar = None
        return [b]


def build_bars_from_ticks(ticks: Iterable[Tick], timeframe_seconds: int = 60, source: str = "EXTERNAL") -> Iterator[Bar]:
    builders: dict[str, CandleBuilder] = {}
    for tick in ticks:
        builder = builders.setdefault(tick.symbol, CandleBuilder(timeframe_seconds, source))
        yield from builder.update(tick)
    for builder in builders.values():
        yield from builder.flush()
