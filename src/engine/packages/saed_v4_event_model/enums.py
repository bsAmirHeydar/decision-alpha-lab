from enum import Enum
class EventKind(str,Enum):
    TICK='tick'; QUOTE='quote'; TRADE='trade'; BAR='bar'; CONTEXT_TRANSITION='context_transition'; REFERENCE_TOUCH='reference_touch'; SESSION_BOUNDARY='session_boundary'; RELATED_SYMBOL='related_symbol'; BROKER_STATE='broker_state'; HEARTBEAT='heartbeat'; DATA_GAP='data_gap'; CORRECTION='correction'; CUSTOM='custom'
class ClockDomain(str,Enum):
    EXCHANGE='exchange'; BROKER='broker'; TERMINAL='terminal'; RESEARCH='research'; CANONICAL_UTC='canonical_utc'
class LatePolicy(str,Enum):
    ACCEPT_FLAG='accept_flag'; QUARANTINE='quarantine'; REJECT='reject'
class AppendDisposition(str,Enum):
    COMMITTED='committed'; IDEMPOTENT='idempotent'; REJECTED='rejected'; QUARANTINED='quarantined'
class ProjectionReducer(str,Enum):
    LAST='last'; COUNT='count'; SUM='sum'; MIN='min'; MAX='max'; MEAN='mean'; BOOLEAN_ANY='boolean_any'; BOOLEAN_ALL='boolean_all'; TIME_SINCE='time_since'; EVENT_RATE='event_rate'; DELTA='delta'
class ProjectionStatus(str,Enum):
    COMPLETE='complete'; DEGRADED='degraded'; UNKNOWN='unknown'; CONFLICTED='conflicted'
class AlignmentStatus(str,Enum):
    COMPLETE='complete'; DEGRADED='degraded'; UNKNOWN='unknown'
class GapSeverity(str,Enum):
    INFO='info'; WARNING='warning'; MATERIAL='material'; CRITICAL='critical'
