from enum import Enum

class LegacyDirection(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class LegacySide(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"

class CanonicalDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class IntegrationMode(str, Enum):
    AUDIT_ONLY = "AUDIT_ONLY"
    PILOT_SHADOW = "PILOT_SHADOW"

class StageStatus(str, Enum):
    NOT_RUN = "NOT_RUN"
    PASSED = "PASSED"
    GATED = "GATED"
    FAILED = "FAILED"

class LifecycleState(str, Enum):
    FIRST_SEEN = "FIRST_SEEN"
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"

class DifferentialStatus(str, Enum):
    MATCH = "MATCH"
    MISSING_CANONICAL = "MISSING_CANONICAL"
    EXTRA_CANONICAL = "EXTRA_CANONICAL"
    FIELD_MISMATCH = "FIELD_MISMATCH"
