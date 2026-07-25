from __future__ import annotations

import json
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .canonical import sha256_file


@dataclass(frozen=True, slots=True)
class Tick:
    symbol: str
    event_time_ms: int
    known_time_ms: int
    price: float
    tick_size: float
    source_sequence: int


class TickSeries:
    def __init__(self, symbol: str, ticks: Iterable[Tick], source_path: Path):
        self.symbol = symbol
        self.ticks = tuple(sorted(ticks, key=lambda x: (x.event_time_ms, x.known_time_ms, x.source_sequence)))
        if not self.ticks:
            raise ValueError(f"no ticks for {symbol}")
        self.times = tuple(x.event_time_ms for x in self.ticks)
        self.source_path = source_path
        self.source_hash = sha256_file(source_path)
        sizes = {round(x.tick_size, 12) for x in self.ticks}
        if len(sizes) != 1:
            raise ValueError(f"tick size changes require a versioned symbol adapter: {symbol}")
        self.tick_size = self.ticks[0].tick_size

    def between(self, start_ms: int, end_ms: int, *, include_end: bool = False) -> tuple[Tick, ...]:
        left = bisect_left(self.times, start_ms)
        right = bisect_right(self.times, end_ms) if include_end else bisect_left(self.times, end_ms)
        return self.ticks[left:right]

    def latest_at_or_before(self, time_ms: int, *, known_by_ms: int | None = None) -> Tick | None:
        index = bisect_right(self.times, time_ms) - 1
        while index >= 0:
            tick = self.ticks[index]
            if known_by_ms is None or tick.known_time_ms <= known_by_ms:
                return tick
            index -= 1
        return None

    def first_touch(self, start_ms: int, side: str, level: float) -> Tick | None:
        index = bisect_left(self.times, start_ms)
        if side == "HIGH":
            for tick in self.ticks[index:]:
                if tick.price >= level:
                    return tick
        elif side == "LOW":
            for tick in self.ticks[index:]:
                if tick.price <= level:
                    return tick
        else:
            raise ValueError(side)
        return None


def load_tick_jsonl(path: Path, expected_symbol: str, start_ms: int | None, end_ms: int | None) -> TickSeries:
    ticks: list[Tick] = []
    previous_key: tuple[int, int, int] | None = None
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            raw = json.loads(line)
            symbol = str(raw["symbol"])
            if symbol != expected_symbol:
                raise ValueError(f"{path}:{line_number}: expected symbol {expected_symbol}, got {symbol}")
            event_time_ms = int(raw["event_time_ms"])
            known_time_ms = int(raw["known_time_ms"])
            if known_time_ms < event_time_ms:
                raise ValueError(f"{path}:{line_number}: known_time precedes event_time")
            if start_ms is not None and event_time_ms < start_ms:
                continue
            if end_ms is not None and event_time_ms > end_ms:
                continue
            price = float(raw["bid"])
            tick_size = float(raw["tick_size"])
            if price <= 0 or tick_size <= 0:
                raise ValueError(f"{path}:{line_number}: price and tick_size must be positive")
            source_sequence = int(raw.get("source_sequence", line_number))
            key = (event_time_ms, known_time_ms, source_sequence)
            if previous_key is not None and key < previous_key:
                raise ValueError(f"{path}:{line_number}: source must be causally ordered")
            previous_key = key
            ticks.append(Tick(symbol, event_time_ms, known_time_ms, price, tick_size, source_sequence))
    return TickSeries(expected_symbol, ticks, path)
