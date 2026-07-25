from __future__ import annotations
from enum import IntEnum

class DataQuality(IntEnum):
    UNKNOWN = 0
    VALID = 1
    MISSING = 2
    STALE = 3
    INVALID = 4
    ESTIMATED = 5

class ClockMode(IntEnum):
    GMT_NATIVE = 0
    BROKER_FIXED_OFFSET = 1
    SERVER_INFERRED_OFFSET = 2
    FIXTURE = 3

class TimezoneKind(IntEnum):
    UTC = 0
    BROKER = 1
    NEW_YORK = 2
    FIXED_OFFSET = 3

class MissingBarPolicy(IntEnum):
    FAIL_CLOSED = 0
    ALLOW_WITH_WARNING = 1
    ESTIMATE_DISABLED = 2

class SyncStatus(IntEnum):
    UNKNOWN = 0
    READY = 1
    MISSING_SERIES = 2
    STALE_SERIES = 3
    SKEW_EXCEEDED = 4
    GAP_DETECTED = 5
