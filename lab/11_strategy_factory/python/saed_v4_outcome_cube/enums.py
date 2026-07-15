from enum import Enum
class EvidenceRole(str,Enum):
    DEVELOPMENT='development'; VALIDATION='validation'; TEST='test'; PROSPECTIVE='prospective'; LIVE='live'
class DataFidelity(str,Enum):
    TICK='tick'; BID_ASK='bid_ask'; BAR='bar'; SYNTHETIC='synthetic'; UNKNOWN='unknown'
class AmbiguityPolicy(str,Enum):
    STOP_FIRST='stop_first'; TARGET_FIRST='target_first'; EXCLUDE='exclude'; REQUIRE_HIGHER_FIDELITY='require_higher_fidelity'
class GapPolicy(str,Enum):
    CONSERVATIVE_OPEN='conservative_open'; REQUESTED_PRICE='requested_price'; EXCLUDE='exclude'
class ActionClass(str,Enum):
    ORDINARY='ordinary'; SKIP='skip'; ABSTAIN='abstain'
class RowStatus(str,Enum):
    CLOSED='closed'; ENTRY_EXPIRED='entry_expired'; TRIGGER_REJECTED='trigger_rejected'; SKIPPED='skipped'; ABSTAINED='abstained'; AMBIGUOUS='ambiguous'; INVALID='invalid'
class ExitReason(str,Enum):
    TARGET='target'; STOP='stop'; TIME='time'; PARTIAL_THEN_STOP='partial_then_stop'; PARTIAL_THEN_TIME='partial_then_time'; ENTRY_EXPIRED='entry_expired'; TRIGGER_FALSE='trigger_false'; SKIP_ACTION='skip_action'; ABSTAIN_ACTION='abstain_action'; AMBIGUOUS_BAR='ambiguous_bar'; INVALID_PATH='invalid_path'
class PathEventKind(str,Enum):
    REGISTERED='registered'; TRIGGER_ACCEPTED='trigger_accepted'; FILLED='filled'; FAVORABLE_EXTREME='favorable_extreme'; ADVERSE_EXTREME='adverse_extreme'; PARTIAL_EXIT='partial_exit'; TRAIL_ACTIVATED='trail_activated'; STOP_MOVED='stop_moved'; CLOSED='closed'
