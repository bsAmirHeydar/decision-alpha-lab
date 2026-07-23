from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Iterable
from zoneinfo import ZoneInfo

from .symbols import ResolvedSymbol

MINUTE_MS = 60_000
NY = ZoneInfo("America/New_York")

PROFILE_AUTO = "AUTO"
PROFILE_WEEKLY_ONLY = "WEEKLY_ONLY_V1"
PROFILE_US_INDEX_CFD_NY = "US_INDEX_CFD_NY_V1"
SUPPORTED_PROFILES = frozenset({PROFILE_AUTO, PROFILE_WEEKLY_ONLY, PROFILE_US_INDEX_CFD_NY})
HOLIDAY_RULE_VERSION = "US_MARKET_HOLIDAYS_V1"


@dataclass(frozen=True, slots=True)
class GapInterval:
    start_ms: int
    end_ms: int
    duration_minutes: int


@dataclass(frozen=True, slots=True)
class CalendarResolution:
    requested_profile: str
    resolved_profile: str
    resolution_reason: str
    primary_match: bool
    secondary_match: bool

    def to_dict(self) -> dict:
        return {
            "requested_profile": self.requested_profile,
            "resolved_profile": self.resolved_profile,
            "resolution_reason": self.resolution_reason,
            "primary_match": self.primary_match,
            "secondary_match": self.secondary_match,
        }


@dataclass(frozen=True, slots=True)
class ScheduledClosure:
    closure_id: str
    holiday_id: str
    holiday_date_ny: str
    profile: str
    start_utc_ms: int
    end_utc_ms: int
    duration_minutes: int
    boundary_bars_confirmed: bool
    classification_basis: str

    def to_dict(self) -> dict:
        return {
            "closure_id": self.closure_id,
            "holiday_id": self.holiday_id,
            "holiday_date_ny": self.holiday_date_ny,
            "profile": self.profile,
            "start_utc_ms": self.start_utc_ms,
            "end_utc_ms": self.end_utc_ms,
            "duration_minutes": self.duration_minutes,
            "boundary_bars_confirmed": self.boundary_bars_confirmed,
            "classification_basis": self.classification_basis,
        }


def collapse_minute_runs(values: Iterable[int]) -> tuple[GapInterval, ...]:
    ordered = sorted(set(values))
    if not ordered:
        return ()
    intervals: list[GapInterval] = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + MINUTE_MS:
            previous = value
            continue
        intervals.append(GapInterval(start, previous + MINUTE_MS, ((previous - start) // MINUTE_MS) + 1))
        start = previous = value
    intervals.append(GapInterval(start, previous + MINUTE_MS, ((previous - start) // MINUTE_MS) + 1))
    return tuple(intervals)


def _nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> date:
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + 7 * (occurrence - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    if month == 12:
        cursor = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        cursor = date(year, month + 1, 1) - timedelta(days=1)
    return cursor - timedelta(days=(cursor.weekday() - weekday) % 7)


def _easter_sunday(year: int) -> date:
    # Anonymous Gregorian algorithm; deterministic and dependency-free.
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def _observed_fixed_holiday(day: date, *, saturday_observed: bool = True) -> date:
    if day.weekday() == 5:
        return day - timedelta(days=1) if saturday_observed else day
    if day.weekday() == 6:
        return day + timedelta(days=1)
    return day


def us_market_holidays(year: int) -> dict[date, str]:
    holidays: dict[date, str] = {
        _observed_fixed_holiday(date(year, 1, 1), saturday_observed=False): "US_NEW_YEARS_DAY",
        _nth_weekday(year, 1, 0, 3): "US_MLK_DAY",
        _nth_weekday(year, 2, 0, 3): "US_PRESIDENTS_DAY",
        _easter_sunday(year) - timedelta(days=2): "US_GOOD_FRIDAY",
        _last_weekday(year, 5, 0): "US_MEMORIAL_DAY",
        _observed_fixed_holiday(date(year, 7, 4)): "US_INDEPENDENCE_DAY",
        _nth_weekday(year, 9, 0, 1): "US_LABOR_DAY",
        _nth_weekday(year, 11, 3, 4): "US_THANKSGIVING_DAY",
        _observed_fixed_holiday(date(year, 12, 25)): "US_CHRISTMAS_DAY",
    }
    if year >= 2022:
        holidays[_observed_fixed_holiday(date(year, 6, 19))] = "US_JUNETEENTH"
    return holidays


def _looks_like_us_index(symbol: ResolvedSymbol) -> bool:
    metadata = symbol.metadata
    text = " ".join(
        str(metadata.get(key) or "")
        for key in ("name", "description", "path", "canonical_instrument_id")
    ).casefold()
    index_marker = any(token in text for token in ("index", "indices", "spx", "s&p", "nasdaq", "ndaq", "dow", "us30", "us100", "us500"))
    us_marker = any(token in text for token in ("#us", " us ", "united states", "spx", "s&p", "nasdaq", "ndaq", "us30", "us100", "us500"))
    usd_settlement = str(metadata.get("currency_profit") or "").upper() == "USD"
    return index_marker and us_marker and usd_settlement


def resolve_calendar_profile(primary: ResolvedSymbol, secondary: ResolvedSymbol, requested_profile: str) -> CalendarResolution:
    requested = requested_profile.strip().upper()
    if requested not in SUPPORTED_PROFILES:
        raise ValueError(f"unsupported session calendar profile: {requested_profile}")
    primary_match = _looks_like_us_index(primary)
    secondary_match = _looks_like_us_index(secondary)
    if requested != PROFILE_AUTO:
        return CalendarResolution(requested, requested, "EXPLICIT_CONFIGURATION", primary_match, secondary_match)
    if primary_match and secondary_match:
        return CalendarResolution(requested, PROFILE_US_INDEX_CFD_NY, "BOTH_SYMBOLS_MATCH_US_INDEX_CFD_METADATA", True, True)
    return CalendarResolution(requested, PROFILE_WEEKLY_ONLY, "AUTO_PROFILE_REMAINS_CONSERVATIVE", primary_match, secondary_match)


def _local_dates(start_ms: int, end_ms: int) -> tuple[date, ...]:
    if end_ms <= start_ms:
        return ()
    start = datetime.fromtimestamp(start_ms / 1000, timezone.utc).astimezone(NY).date()
    end = datetime.fromtimestamp((end_ms - 1) / 1000, timezone.utc).astimezone(NY).date()
    days: list[date] = []
    cursor = start
    while cursor <= end:
        days.append(cursor)
        cursor += timedelta(days=1)
    return tuple(days)


def classify_scheduled_closure(
    interval: GapInterval,
    primary: ResolvedSymbol,
    secondary: ResolvedSymbol,
    requested_profile: str,
    max_scheduled_closure_minutes: int,
    require_boundary_bars: bool,
    primary_open_times: set[int],
    secondary_open_times: set[int],
) -> tuple[ScheduledClosure | None, CalendarResolution]:
    resolution = resolve_calendar_profile(primary, secondary, requested_profile)
    if resolution.resolved_profile != PROFILE_US_INDEX_CFD_NY:
        return None, resolution
    if interval.duration_minutes > max_scheduled_closure_minutes:
        return None, resolution

    before = interval.start_ms - MINUTE_MS
    after = interval.end_ms
    boundary_confirmed = (
        before in primary_open_times
        and before in secondary_open_times
        and after in primary_open_times
        and after in secondary_open_times
    )
    if require_boundary_bars and not boundary_confirmed:
        return None, resolution

    holiday: tuple[date, str] | None = None
    for local_day in _local_dates(interval.start_ms, interval.end_ms):
        holiday_id = us_market_holidays(local_day.year).get(local_day)
        if holiday_id:
            holiday = (local_day, holiday_id)
            break
    if holiday is None:
        return None, resolution

    holiday_day, holiday_id = holiday
    closure_id = f"{resolution.resolved_profile}:{holiday_id}:{holiday_day.isoformat()}:{interval.start_ms}:{interval.end_ms}"
    return ScheduledClosure(
        closure_id=closure_id,
        holiday_id=holiday_id,
        holiday_date_ny=holiday_day.isoformat(),
        profile=resolution.resolved_profile,
        start_utc_ms=interval.start_ms,
        end_utc_ms=interval.end_ms,
        duration_minutes=interval.duration_minutes,
        boundary_bars_confirmed=boundary_confirmed,
        classification_basis="DECLARED_HOLIDAY_RULE_AND_PAIRED_BOUNDARY_BARS",
    ), resolution
