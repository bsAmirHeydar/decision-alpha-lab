from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from .canonical import stable_id
from .ticks import Tick, TickSeries

NY = ZoneInfo("America/New_York")
UTC = timezone.utc
CYCLE_DEFINITION_VERSION = "1.0.0"


def to_ms(value: datetime) -> int:
    return int(value.timestamp() * 1000)


def from_ms(value: int) -> datetime:
    return datetime.fromtimestamp(value / 1000, UTC)


def local_dt(day: date, hh: int, mm: int = 0) -> datetime:
    return datetime.combine(day, time(hh, mm), NY)


@dataclass(frozen=True, slots=True)
class CycleKey:
    cycle_type: str
    start_ms: int
    end_ms: int
    trading_day_ny: str
    completeness: str

    @property
    def cycle_instance_id(self) -> str:
        return stable_id("RTHPCYCLE_", (self.cycle_type, self.start_ms, self.end_ms), 24, True)


@dataclass(slots=True)
class SymbolExtrema:
    high: float = float("-inf")
    low: float = float("inf")
    first_price: float | None = None
    last_price: float | None = None
    first_time_ms: int | None = None
    last_time_ms: int | None = None
    max_known_time_ms: int = 0
    tick_count: int = 0

    def update(self, tick: Tick) -> None:
        self.high = max(self.high, tick.price)
        self.low = min(self.low, tick.price)
        if self.first_price is None:
            self.first_price = tick.price
            self.first_time_ms = tick.event_time_ms
        self.last_price = tick.price
        self.last_time_ms = tick.event_time_ms
        self.max_known_time_ms = max(self.max_known_time_ms, tick.known_time_ms)
        self.tick_count += 1


@dataclass(slots=True)
class CycleAggregate:
    key: CycleKey
    symbols: dict[str, SymbolExtrema] = field(default_factory=dict)

    def update(self, tick: Tick) -> None:
        self.symbols.setdefault(tick.symbol, SymbolExtrema()).update(tick)

    def complete_for(self, primary_symbol: str, secondary_symbol: str) -> bool:
        return primary_symbol in self.symbols and secondary_symbol in self.symbols

    @property
    def known_time_ms(self) -> int:
        return max([self.key.end_ms, *(x.max_known_time_ms for x in self.symbols.values())])


def _daily_key(local: datetime) -> CycleKey | None:
    d = local.date()
    wd = local.weekday()  # Monday=0, Sunday=6
    minute = local.hour * 60 + local.minute
    if wd == 6:  # Sunday
        if 18 * 60 <= minute < 20 * 60:
            return CycleKey("DAILY", to_ms(local_dt(d, 18)), to_ms(local_dt(d, 20)), d.isoformat(), "PARTIAL")
        if minute >= 20 * 60:
            td = d + timedelta(days=1)
            return CycleKey("DAILY", to_ms(local_dt(d, 20)), to_ms(local_dt(td, 20)), td.isoformat(), "COMPLETE")
        return None
    if wd in (0, 1, 2):
        if minute >= 20 * 60:
            td = d + timedelta(days=1)
            return CycleKey("DAILY", to_ms(local_dt(d, 20)), to_ms(local_dt(td, 20)), td.isoformat(), "COMPLETE")
        return CycleKey("DAILY", to_ms(local_dt(d - timedelta(days=1), 20)), to_ms(local_dt(d, 20)), d.isoformat(), "COMPLETE")
    if wd == 3:  # Thursday
        if minute >= 20 * 60:
            td = d + timedelta(days=1)
            return CycleKey("DAILY", to_ms(local_dt(d, 20)), to_ms(local_dt(td, 17)), td.isoformat(), "PARTIAL_MARKET_WEEK_END")
        return CycleKey("DAILY", to_ms(local_dt(d - timedelta(days=1), 20)), to_ms(local_dt(d, 20)), d.isoformat(), "COMPLETE")
    if wd == 4 and minute < 17 * 60:
        return CycleKey("DAILY", to_ms(local_dt(d - timedelta(days=1), 20)), to_ms(local_dt(d, 17)), d.isoformat(), "PARTIAL_MARKET_WEEK_END")
    return None


def _weekly_key(local: datetime) -> CycleKey | None:
    d = local.date()
    days_since_sunday = (local.weekday() + 1) % 7
    sunday = d - timedelta(days=days_since_sunday)
    start = local_dt(sunday, 18)
    if local < start:
        sunday -= timedelta(days=7)
        start = local_dt(sunday, 18)
    end = local_dt(sunday + timedelta(days=5), 17)
    if not start <= local < end:
        return None
    return CycleKey("WEEKLY", to_ms(start), to_ms(end), sunday.isoformat(), "COMPLETE")


def _intraday_key(local: datetime, cycle_type: str, start_h: int, start_m: int, end_h: int, end_m: int, completeness: str = "COMPLETE") -> CycleKey | None:
    start = local_dt(local.date(), start_h, start_m)
    end = local_dt(local.date(), end_h, end_m)
    if start <= local < end:
        return CycleKey(cycle_type, to_ms(start), to_ms(end), local.date().isoformat(), completeness)
    return None


def cycle_keys_for_tick(tick: Tick) -> tuple[CycleKey, ...]:
    local = from_ms(tick.event_time_ms).astimezone(NY)
    keys: list[CycleKey] = []
    daily = _daily_key(local)
    weekly = _weekly_key(local)
    if daily:
        keys.append(daily)
    if weekly:
        keys.append(weekly)
    definitions = (
        ("L", 7, 0, 9, 30),
        ("N", 9, 30, 16, 0),
        ("A", 16, 0, 20, 0),
        ("FCR_1", 9, 30, 10, 0),
        ("FCR_2", 10, 0, 16, 0),
        ("PP_1", 9, 0, 9, 30),
        ("PP_2", 9, 30, 16, 0),
    )
    for cycle_type, sh, sm, eh, em in definitions:
        completeness = "PARTIAL_MARKET_WEEK_END" if cycle_type == "A" and local.weekday() == 4 else "COMPLETE"
        key = _intraday_key(local, cycle_type, sh, sm, eh if not (cycle_type == "A" and local.weekday() == 4) else 17, em, completeness)
        if key:
            keys.append(key)
    n_start = local_dt(local.date(), 9, 30)
    n_end = local_dt(local.date(), 16, 0)
    if n_start <= local < n_end:
        elapsed = int((local - n_start).total_seconds() // 900)
        start = n_start + timedelta(minutes=15 * elapsed)
        end = start + timedelta(minutes=15)
        keys.append(CycleKey("M15", to_ms(start), to_ms(end), local.date().isoformat(), "COMPLETE"))
    return tuple(keys)


def build_cycles(primary: TickSeries, secondary: TickSeries) -> tuple[CycleAggregate, ...]:
    cycles: dict[tuple[str, int, int], CycleAggregate] = {}
    for tick in sorted((*primary.ticks, *secondary.ticks), key=lambda x: (x.event_time_ms, x.known_time_ms, x.symbol, x.source_sequence)):
        for key in cycle_keys_for_tick(tick):
            aggregate = cycles.setdefault((key.cycle_type, key.start_ms, key.end_ms), CycleAggregate(key))
            aggregate.update(tick)
    min_time = min(primary.ticks[0].event_time_ms, secondary.ticks[0].event_time_ms)
    max_time = max(primary.ticks[-1].event_time_ms, secondary.ticks[-1].event_time_ms)
    result: list[CycleAggregate] = []
    for aggregate in cycles.values():
        if not aggregate.complete_for(primary.symbol, secondary.symbol):
            continue
        if aggregate.key.start_ms < min_time or aggregate.key.end_ms > max_time:
            if aggregate.key.completeness == "COMPLETE":
                aggregate.key = CycleKey(
                    aggregate.key.cycle_type,
                    aggregate.key.start_ms,
                    aggregate.key.end_ms,
                    aggregate.key.trading_day_ny,
                    "PARTIAL",
                )
        result.append(aggregate)
    return tuple(sorted(result, key=lambda x: (x.key.start_ms, x.key.cycle_type, x.key.end_ms)))


def confirmation_closes(cycle: CycleAggregate) -> tuple[int, ...]:
    start_local = from_ms(cycle.key.start_ms).astimezone(NY)
    end_local = from_ms(cycle.key.end_ms).astimezone(NY)
    minute = start_local.minute
    delta = (15 - (minute % 15)) % 15
    candidate = start_local.replace(second=0, microsecond=0) + timedelta(minutes=delta)
    if candidate <= start_local:
        candidate += timedelta(minutes=15)
    closes: list[int] = []
    while candidate <= end_local:
        closes.append(to_ms(candidate))
        candidate += timedelta(minutes=15)
    return tuple(closes)
