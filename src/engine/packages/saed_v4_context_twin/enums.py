from enum import Enum
class TwinState(str,Enum):
    SEEDED='seeded'; INITIALIZED='initialized'; OBSERVING='observing'; DEGRADED='degraded'; CONFLICTED='conflicted'; QUARANTINED='quarantined'; RETIRED='retired'
class SupportStatus(str,Enum):
    SUPPORTED='supported'; DEGRADED='degraded'; UNSUPPORTED='unsupported'; UNKNOWN='unknown'
class HypothesisStatus(str,Enum):
    DECLARED='declared'; SUPPORTED='supported'; CHALLENGED='challenged'; REJECTED='rejected'; UNRESOLVED='unresolved'
class ContradictionSeverity(str,Enum):
    INFO='info'; WARNING='warning'; MATERIAL='material'; CRITICAL='critical'
class DebtSeverity(str,Enum):
    LOW='low'; MEDIUM='medium'; HIGH='high'; BLOCKING='blocking'
class ObservationKind(str,Enum):
    CANONICAL_FACT='canonical_fact'; DERIVED_FACT='derived_fact'; QUALITY_SIGNAL='quality_signal'; SUPPORT_SIGNAL='support_signal'; EXTERNAL_ASSESSMENT='external_assessment'
class RelationKind(str,Enum):
    IS_A='is_a'; PART_OF='part_of'; PRECEDES='precedes'; REQUIRES='requires'; CONTRADICTS='contradicts'; DERIVED_FROM='derived_from'; RELATED_TO='related_to'
class TransitionDisposition(str,Enum):
    APPLIED='applied'; REJECTED='rejected'; REVIEW='review'; NOOP='noop'
class Authority(str,Enum):
    READ_UEE_TRUTH='read_ucee_truth'; COMPILE_TWIN='compile_twin'; APPEND_OBSERVATION='append_observation'; APPEND_HYPOTHESIS_ASSESSMENT='append_hypothesis_assessment'; TRANSITION_TWIN='transition_twin'; MUTATE_UEE_TRUTH='mutate_ucee_truth'; SELECT_TREATMENT='select_treatment'; ALLOCATE_RISK='allocate_risk'; ACTIVATE_RUNTIME='activate_runtime'; SEND_ORDER='send_order'; NETWORK_ACCESS='network_access'
