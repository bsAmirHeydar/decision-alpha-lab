from __future__ import annotations
from .canonical import digest_object

RISK_DIMENSIONS = [
    {"dimension_id":"STATEFULNESS","weight":12,"critical":False,"evidence":"global state, mutable lifecycle stores and restart state"},
    {"dimension_id":"MULTI_TIMEFRAME_ALIGNMENT","weight":12,"critical":False,"evidence":"timeframe API or explicit period projection"},
    {"dimension_id":"SESSION_DST_DEPENDENCE","weight":12,"critical":False,"evidence":"session API, wall-clock or timezone rules"},
    {"dimension_id":"PERSISTENCE_FILE_IO","weight":10,"critical":False,"evidence":"file read/write or persistent ledger"},
    {"dimension_id":"DRAWING_OBJECT_LIFECYCLE","weight":8,"critical":False,"evidence":"chart-object mutation and lifecycle"},
    {"dimension_id":"MULTI_CHART_BEHAVIOR","weight":10,"critical":False,"evidence":"chart enumeration or cross-chart state"},
    {"dimension_id":"EXECUTION_COUPLING","weight":100,"critical":True,"evidence":"order/trade API surface"},
    {"dimension_id":"BROKER_OR_NETWORK_COUPLING","weight":100,"critical":True,"evidence":"network, broker or external service API"},
    {"dimension_id":"CURRENT_BAR_OR_FUTURE_AWARENESS","weight":80,"critical":True,"evidence":"current-bar, future-derived or dynamic execution surface"},
    {"dimension_id":"NONDETERMINISM","weight":80,"critical":True,"evidence":"unstable randomness or wall-clock identity"},
    {"dimension_id":"SECURITY_SENSITIVITY","weight":100,"critical":True,"evidence":"security-sensitive classification"},
    {"dimension_id":"IDENTITY_AMBIGUITY","weight":100,"critical":True,"evidence":"unresolved collision or ambiguous identity"},
    {"dimension_id":"OWNER_APPROVAL","weight":20,"critical":False,"evidence":"role binding and architect-approved pilot scope"},
    {"dimension_id":"CHARACTERIZATION_GAP","weight":15,"critical":False,"evidence":"missing observed traces and golden cases"},
    {"dimension_id":"PACKAGE_SURFACE_COMPLEXITY","weight":10,"critical":False,"evidence":"source size, dependency count and package file count"},
]

PILOT_GATES = [
    "SOURCE_EXISTS",
    "PACKAGE_CONTEXT_GRANULARITY",
    "NOT_PROTECTED_PLATFORM",
    "NOT_SECURITY_SENSITIVE",
    "NO_DIRECT_ORDER_AUTHORITY",
    "NO_NETWORK_OR_DYNAMIC_EXECUTION",
    "NO_UNSTABLE_RANDOMNESS",
    "NO_CURRENT_BAR_OR_FUTURE_AWARENESS",
    "NO_IDENTITY_COLLISION",
    "OWNER_ROLE_BOUND",
    "ARCHITECT_APPROVED_SELECTION_POLICY",
    "DOCUMENTATION_EVIDENCE_PRESENT",
    "BOUNDED_PACKAGE_SURFACE",
    "REFERENCE_RUNTIME_AVAILABLE",
    "ROLLBACK_SAFE_SOURCE_BOUNDARY",
]

REASON_CODES = [
    "PASS",
    "SOURCE_MISSING",
    "PROTECTED_PLATFORM",
    "SECURITY_REVIEW_REQUIRED",
    "DIRECT_ORDER_AUTHORITY",
    "NETWORK_OR_DYNAMIC_EXECUTION",
    "UNSTABLE_RANDOMNESS",
    "CURRENT_BAR_OR_FUTURE_AWARENESS",
    "IDENTITY_COLLISION",
    "HUMAN_OWNER_ROLE_PENDING",
    "NOT_A_PACKAGE_CONTEXT",
    "DOCUMENTATION_EVIDENCE_INSUFFICIENT",
    "PACKAGE_SURFACE_UNBOUNDED",
    "MQL5_RUNTIME_UNAVAILABLE",
    "CHARACTERIZATION_REQUIRED",
    "DEPENDENCY_BLOCKED",
    "SELECTED_BY_DETERMINISTIC_POLICY",
    "REJECTED_HIGHER_RISK",
    "REJECTED_TIE_BREAK",
    "BLOCKED_UNKNOWN",
]


def closed_registry(registry_id: str, values, purpose: str) -> dict:
    obj = {"schema_version":"1.0.0","registry_id":registry_id,"purpose":purpose,"closed_values":values,"registry_digest":None}
    obj["registry_digest"] = digest_object(obj, "registry_digest")
    return obj
