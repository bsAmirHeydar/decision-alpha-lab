from __future__ import annotations

import json
import math
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .canonical import sha256_file

MINUTE_MS = 60_000


@dataclass(frozen=True, slots=True)
class M1Bar:
    symbol: str
    open_time_ms: int
    close_time_ms: int
    known_time_ms: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: int
    spread: int
    real_volume: int
    tick_size: float
    source_sequence: int
    source_terminal_id: str
    source_revision: str


@dataclass(frozen=True, slots=True)
class M1Touch:
    symbol: str
    interval_start_ms: int
    interval_end_ms: int
    known_time_ms: int
    observable_time_ms: int
    touch_price: float
    close_price: float
    side: str


class M1BarSeries:
    def __init__(self, symbol: str, bars: Iterable[M1Bar], source_path: Path):
        self.symbol = symbol
        self.bars = tuple(sorted(bars, key=lambda x: (x.open_time_ms, x.known_time_ms, x.source_sequence)))
        if not self.bars:
            raise ValueError(f"no closed M1 bars for {symbol}")
        self.open_times = tuple(x.open_time_ms for x in self.bars)
        self.close_times = tuple(x.close_time_ms for x in self.bars)
        self.by_open = {x.open_time_ms: x for x in self.bars}
        self.source_path = source_path
        self.source_hash = sha256_file(source_path)
        sizes = {round(x.tick_size, 12) for x in self.bars}
        if len(sizes) != 1:
            raise ValueError(f"tick size changes require a versioned symbol adapter: {symbol}")
        self.tick_size = self.bars[0].tick_size

    def between(self, start_ms: int, end_ms: int, *, include_end: bool = False) -> tuple[M1Bar, ...]:
        if end_ms <= start_ms:
            return ()
        left = bisect_left(self.open_times, start_ms)
        bars: list[M1Bar] = []
        for bar in self.bars[left:]:
            if bar.close_time_ms > end_ms:
                break
            if bar.open_time_ms >= start_ms and (bar.close_time_ms <= end_ms if include_end else bar.close_time_ms < end_ms):
                bars.append(bar)
        return tuple(bars)

    def latest_closed_at_or_before(self, time_ms: int, *, known_by_ms: int | None = None) -> M1Bar | None:
        index = bisect_right(self.close_times, time_ms) - 1
        while index >= 0:
            bar = self.bars[index]
            if known_by_ms is None or bar.known_time_ms <= known_by_ms:
                return bar
            index -= 1
        return None

    def has_exact_interval(self, start_ms: int, end_ms: int) -> bool:
        if end_ms <= start_ms or (end_ms - start_ms) % MINUTE_MS:
            return False
        return all(t in self.by_open for t in range(start_ms, end_ms, MINUTE_MS))

    def first_touch(self, start_ms: int, side: str, level: float) -> M1Touch | None:
        index = bisect_left(self.open_times, start_ms)
        for bar in self.bars[index:]:
            touched = bar.high >= level if side == "HIGH" else bar.low <= level if side == "LOW" else None
            if touched is None:
                raise ValueError(side)
            if touched:
                return M1Touch(bar.symbol, bar.open_time_ms, bar.close_time_ms, bar.known_time_ms, bar.close_time_ms,
                               bar.high if side == "HIGH" else bar.low, bar.close, side)
        return None


def _validate_bar(raw: dict, path: Path, line_number: int, expected_symbol: str) -> M1Bar:
    symbol = str(raw["symbol"])
    if symbol != expected_symbol:
        raise ValueError(f"{path}:{line_number}: expected symbol {expected_symbol}, got {symbol}")
    timeframe_seconds = int(raw.get("timeframe_seconds", 60))
    if timeframe_seconds != 60:
        raise ValueError(f"{path}:{line_number}: canonical source must be M1")
    open_time = int(raw["bar_open_time_utc_ms"])
    close_time = int(raw["bar_close_time_utc_ms"])
    known_time = int(raw["known_time_utc_ms"])
    if close_time - open_time != MINUTE_MS or open_time % MINUTE_MS:
        raise ValueError(f"{path}:{line_number}: invalid M1 interval")
    if known_time < close_time:
        raise ValueError(f"{path}:{line_number}: known time precedes bar close")
    o, h, l, c = (float(raw[k]) for k in ("open", "high", "low", "close"))
    if not all(math.isfinite(x) and x > 0 for x in (o, h, l, c)):
        raise ValueError(f"{path}:{line_number}: OHLC must be positive finite numbers")
    if l > h or not l <= o <= h or not l <= c <= h:
        raise ValueError(f"{path}:{line_number}: invalid OHLC ordering")
    tick_size = float(raw["tick_size"])
    if not math.isfinite(tick_size) or tick_size <= 0:
        raise ValueError(f"{path}:{line_number}: tick_size must be positive")
    return M1Bar(symbol, open_time, close_time, known_time, o, h, l, c, int(raw.get("tick_volume", 0)),
                 int(raw.get("spread", 0)), int(raw.get("real_volume", 0)), tick_size,
                 int(raw.get("source_sequence", line_number)), str(raw.get("source_terminal_id", "UNKNOWN_TERMINAL")),
                 str(raw.get("source_revision", "R1")))


def load_m1_bar_jsonl(path: Path, expected_symbol: str, start_ms: int | None, end_ms: int | None) -> M1BarSeries:
    bars: list[M1Bar] = []
    seen: dict[int, M1Bar] = {}
    previous_open: int | None = None
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            bar = _validate_bar(json.loads(line), path, line_number, expected_symbol)
            if start_ms is not None and bar.open_time_ms < start_ms:
                continue
            if end_ms is not None and bar.close_time_ms > end_ms:
                continue
            if previous_open is not None and bar.open_time_ms < previous_open:
                raise ValueError(f"{path}:{line_number}: bars must be causally ordered")
            previous_open = bar.open_time_ms
            existing = seen.get(bar.open_time_ms)
            if existing is not None:
                if existing != bar:
                    raise ValueError(f"{path}:{line_number}: conflicting duplicate M1 bar")
                continue
            seen[bar.open_time_ms] = bar
            bars.append(bar)
    return M1BarSeries(expected_symbol, bars, path)
