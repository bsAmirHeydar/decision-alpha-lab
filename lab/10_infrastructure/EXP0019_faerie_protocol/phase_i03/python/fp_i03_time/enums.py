"""Closed enums for FP-I03 exact New York time and calendar semantics."""
from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class DstRegime(StrEnum):
    STANDARD = "STANDARD"
    DAYLIGHT = "DAYLIGHT"


class LocalTimeStatus(StrEnum):
    UNIQUE = "UNIQUE"
    AMBIGUOUS = "AMBIGUOUS"
    NONEXISTENT = "NONEXISTENT"


class LocalResolutionPolicy(StrEnum):
    REJECT = "REJECT"
    EARLIEST = "EARLIEST"
    LATEST = "LATEST"


class CalendarSegment(StrEnum):
    A = "A"
    L = "L"
    N = "N"
    DAILY_GAP = "DAILY_GAP"
    WEEKEND_CLOSED = "WEEKEND_CLOSED"


class WeekState(StrEnum):
    ACTIVE = "ACTIVE"
    CLOSED_AFTER_FRIDAY = "CLOSED_AFTER_FRIDAY"
    CLOSED_BEFORE_SUNDAY_OPEN = "CLOSED_BEFORE_SUNDAY_OPEN"


class BoundaryKind(StrEnum):
    SESSION_START = "SESSION_START"
    SESSION_END = "SESSION_END"
    TRADING_DAY_START = "TRADING_DAY_START"
    TRADING_DAY_END = "TRADING_DAY_END"
    DAILY_GAP_START = "DAILY_GAP_START"
    DAILY_GAP_END = "DAILY_GAP_END"
    WEEK_START = "WEEK_START"
    WEEK_END = "WEEK_END"
    DST_START = "DST_START"
    DST_END = "DST_END"


class TimeSource(StrEnum):
    UTC = "UTC"
    BROKER_EXPLICIT_OFFSET = "BROKER_EXPLICIT_OFFSET"


class CalendarHealth(StrEnum):
    READY = "READY"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"
