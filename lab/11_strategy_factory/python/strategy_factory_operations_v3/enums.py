from enum import Enum


class DeploymentStage(str, Enum):
    FROZEN = "frozen"
    PAPER = "paper"
    SHADOW = "shadow"
    MICRO_LIVE = "micro_live"
    LIMITED_LIVE = "limited_live"
    PRODUCTION = "production"
    SAFE_HALT = "safe_halt"
    ROLLED_BACK = "rolled_back"
    RETIRED = "retired"


class EvidenceState(str, Enum):
    PASS = "pass"
    DEGRADED = "degraded"
    FAIL = "fail"
    PENDING = "pending"
    NOT_APPLICABLE = "not_applicable"


class ControlDecision(str, Enum):
    BLOCK = "block"
    HOLD = "hold"
    ALLOW_NO_SEND = "allow_no_send"
    ALLOW_BOUNDED = "allow_bounded"
    DERISK = "derisk"
    SAFE_HALT = "safe_halt"
    ROLLBACK = "rollback"
    RETIRE = "retire"


class RampVerdict(str, Enum):
    BLOCKED = "blocked"
    HOLD = "hold"
    ELIGIBLE_FOR_HUMAN_APPROVAL = "eligible_for_human_approval"


class IncidentSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentState(str, Enum):
    OPEN = "open"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ChangeClass(str, Enum):
    DOCUMENTATION_ONLY = "documentation_only"
    NON_AUTHORITY_OPERATIONS = "non_authority_operations"
    RISK_REDUCTION = "risk_reduction"
    QUALIFICATION_INVALIDATING = "qualification_invalidating"
    FORBIDDEN_HOT_CHANGE = "forbidden_hot_change"


class GateName(str, Enum):
    RELEASE_BINDING = "release_binding"
    LEASE = "lease"
    HEALTH = "health"
    RECONCILIATION = "reconciliation"
    INCIDENT = "incident"
    CAPITAL_ENVELOPE = "capital_envelope"
    EOD_CONTROL = "eod_control"
    CHANGE_CONTROL = "change_control"
    RAMP = "ramp"
    ROLLBACK = "rollback"
    RETIREMENT = "retirement"
