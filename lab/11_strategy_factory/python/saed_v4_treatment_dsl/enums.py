from enum import Enum


class EvidenceRole(str, Enum):
    DEVELOPMENT = "development"
    CALIBRATION = "calibration"
    SELECTION_VALIDATION = "selection_validation"
    LOCKED_FINAL = "locked_final"
    PROSPECTIVE = "prospective"
    SHADOW = "shadow"
    MICRO_LIVE = "micro_live"
    LIVE = "live"
    SYNTHETIC_STRESS = "synthetic_stress"
    EXTERNAL_STATIC = "external_static"
    EXTERNAL_ACTUAL = "external_actual"


class PrimitiveKind(str, Enum):
    ACTION = "action"
    PAYOFF = "payoff"
    DIRECTION = "direction"
    ENTRY = "entry"
    TRIGGER = "trigger"
    STOP = "stop"
    TARGET = "target"
    EXIT = "exit"
    TRAIL = "trail"
    MANAGEMENT = "management"
    TIME = "time"
    COST = "cost"
    CAPABILITY = "capability"


class ParameterType(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    DECIMAL = "decimal"
    STRING = "string"
    ENUM = "enum"
    DURATION_MS = "duration_ms"


class MonotonicDirection(str, Enum):
    NONE = "none"
    INCREASING = "increasing"
    DECREASING = "decreasing"


class ProgramStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"


class PackageStatus(str, Enum):
    COMPLETE = "complete"
    DEGRADED = "degraded"
    UNSUPPORTED = "unsupported"
    QUARANTINED = "quarantined"


class BindingStatus(str, Enum):
    BOUND = "bound"
    UNBOUND = "unbound"
    REJECTED = "rejected"


class ConstraintKind(str, Enum):
    REQUIRES_COMPONENT = "requires_component"
    EXCLUDES_COMPONENT = "excludes_component"
    PARAMETER_RELATION = "parameter_relation"
    FEATURE_PREDICATE = "feature_predicate"
    CAPABILITY_REQUIRED = "capability_required"
    STATE_TRANSITION_GUARD = "state_transition_guard"


class Operator(str, Enum):
    EQ = "eq"
    NE = "ne"
    LT = "lt"
    LE = "le"
    GT = "gt"
    GE = "ge"
    IN = "in"
    EXISTS = "exists"


class StateKind(str, Enum):
    INITIAL = "initial"
    ACTIVE = "active"
    TERMINAL = "terminal"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class DiffClass(str, Enum):
    IDENTICAL = "identical"
    METADATA_ONLY = "metadata_only"
    SEMANTIC = "semantic"
