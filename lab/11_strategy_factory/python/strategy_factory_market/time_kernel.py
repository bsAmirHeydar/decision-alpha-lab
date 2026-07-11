from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from calendar import monthcalendar
from .enums import ClockMode, TimezoneKind

UTC = timezone.utc

@dataclass(frozen=True, slots=True)
class ClockConfig:
    mode: ClockMode = ClockMode.GMT_NATIVE
    broker_utc_offset_minutes: int = 0
    broker_timezone_id: str = "broker"
    source_clock_id: str = "sf03_time_kernel"
    strict_offset_validation: bool = True

    def __post_init__(self) -> None:
        if not -840 <= self.broker_utc_offset_minutes <= 840:
            raise ValueError("broker UTC offset out of range")
        if not self.broker_timezone_id:
            raise ValueError("broker timezone id required")
        if not self.source_clock_id:
            raise ValueError("source clock id required")

def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("naive datetime is not allowed")
    return value.astimezone(UTC)

def _nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> int:
    matches = [week[weekday] for week in monthcalendar(year, month) if week[weekday]]
    if occurrence <= 0 or occurrence > len(matches):
        raise ValueError("invalid occurrence")
    return matches[occurrence - 1]

class TimeKernel:
    """Strict research mirror of the MQL5 time kernel."""

    def __init__(self, config: ClockConfig, fixture_utc: datetime | None = None) -> None:
        self.config = config
        self._fixture_utc = _ensure_utc(fixture_utc) if fixture_utc else None

    @staticmethod
    def to_epoch_milliseconds(value: datetime) -> int:
        return int(_ensure_utc(value).timestamp() * 1000)

    @staticmethod
    def from_epoch_milliseconds(value: int) -> datetime:
        if value < 0:
            raise ValueError("negative epoch milliseconds")
        return datetime.fromtimestamp(value / 1000, tz=UTC)

    @staticmethod
    def new_york_dst_start_utc(year: int) -> datetime:
        day = _nth_weekday(year, 3, 6, 2)  # Sunday, second occurrence
        return datetime(year, 3, day, 7, 0, tzinfo=UTC)

    @staticmethod
    def new_york_dst_end_utc(year: int) -> datetime:
        day = _nth_weekday(year, 11, 6, 1)  # Sunday, first occurrence
        return datetime(year, 11, day, 6, 0, tzinfo=UTC)

    @classmethod
    def is_new_york_dst(cls, value: datetime) -> bool:
        utc = _ensure_utc(value)
        return cls.new_york_dst_start_utc(utc.year) <= utc < cls.new_york_dst_end_utc(utc.year)

    @classmethod
    def new_york_utc_offset_minutes(cls, value: datetime) -> int:
        return -240 if cls.is_new_york_dst(value) else -300

    def resolve_offset_minutes(
        self,
        kind: TimezoneKind,
        value: datetime,
        fixed_offset_minutes: int = 0,
    ) -> int:
        utc = _ensure_utc(value)
        if kind is TimezoneKind.UTC:
            return 0
        if kind is TimezoneKind.BROKER:
            return self.config.broker_utc_offset_minutes
        if kind is TimezoneKind.NEW_YORK:
            return self.new_york_utc_offset_minutes(utc)
        if not -840 <= fixed_offset_minutes <= 840:
            raise ValueError("fixed offset out of range")
        return fixed_offset_minutes

    def broker_to_utc(self, broker_time: datetime) -> datetime:
        if broker_time.tzinfo is not None and broker_time.utcoffset() is not None:
            raise ValueError("broker wall-clock input must be naive")
        return (broker_time - timedelta(minutes=self.config.broker_utc_offset_minutes)).replace(tzinfo=UTC)

    def local_datetime(
        self,
        value: datetime,
        kind: TimezoneKind,
        fixed_offset_minutes: int = 0,
    ) -> datetime:
        utc = _ensure_utc(value)
        offset = self.resolve_offset_minutes(kind, utc, fixed_offset_minutes)
        return utc + timedelta(minutes=offset)

    def trading_day_id(
        self,
        value: datetime,
        kind: TimezoneKind,
        rollover_minute: int,
        fixed_offset_minutes: int = 0,
    ) -> int:
        if not 0 <= rollover_minute < 1440:
            raise ValueError("rollover minute out of range")
        local = self.local_datetime(value, kind, fixed_offset_minutes)
        shifted = local - timedelta(minutes=rollover_minute)
        return shifted.year * 10000 + shifted.month * 100 + shifted.day
