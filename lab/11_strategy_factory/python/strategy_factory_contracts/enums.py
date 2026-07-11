from __future__ import annotations
from enum import Enum, IntEnum

class Direction(IntEnum):
    SHORT = -1
    NONE = 0
    LONG = 1

class TimestampPrecision(IntEnum):
    SECONDS = 0
    MILLISECONDS = 1
    MICROSECONDS = 2

class FeatureType(str, Enum):
    NULL = "NULL"
    DOUBLE = "DOUBLE"
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    TIMESTAMP = "TIMESTAMP"

class FeatureQuality(str, Enum):
    UNKNOWN = "UNKNOWN"
    VALID = "VALID"
    MISSING = "MISSING"
    STALE = "STALE"
    INVALID = "INVALID"
    ESTIMATED = "ESTIMATED"

class Compatibility(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    COMPATIBLE_WITH_MIGRATION = "COMPATIBLE_WITH_MIGRATION"
    INCOMPATIBLE = "INCOMPATIBLE"
