from enum import Enum


class EvidenceStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    PENDING = "pending"
    NOT_APPLICABLE = "not_applicable"


class QualificationDecision(str, Enum):
    QUALIFIED = "qualified"
    BLOCKED = "blocked"
    HOLD = "hold"


class ReleaseStage(str, Enum):
    FROZEN = "frozen"
    TESTER = "tester"
    PAPER = "paper"
    SHADOW = "shadow"
    MICRO_LIVE = "micro_live"
    LIMITED_LIVE = "limited_live"
    PRODUCTION = "production"
    ROLLED_BACK = "rolled_back"
    BLOCKED = "blocked"


class GateName(str, Enum):
    SOURCE_INTEGRITY = "source_integrity"
    METAEDITOR_COMPILE = "metaeditor_compile"
    CROSS_LANGUAGE_PARITY = "cross_language_parity"
    TESTER_DIFFERENTIAL = "tester_differential"
    SOAK = "soak"
    CHAOS = "chaos"
    RECOVERY = "recovery"
    BROKER_RECONCILIATION = "broker_reconciliation"
    SECURITY = "security"
    PAPER = "paper"
    SHADOW = "shadow"
    MICRO_LIVE = "micro_live"
    LIMITED_LIVE = "limited_live"
    PRODUCTION = "production"
    ROLLBACK = "rollback"
    HUMAN_APPROVAL = "human_approval"


class IncidentSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"
