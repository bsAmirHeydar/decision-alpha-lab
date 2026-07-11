from enum import IntEnum

class SplitMethod(IntEnum):
    ANCHORED_WALK_FORWARD = 1
    ROLLING_WALK_FORWARD = 2
    COMBINATORIALLY_SYMMETRIC = 3

class FoldRole(IntEnum):
    TRAIN = 1
    VALIDATION = 2
    TEST = 3
    PURGED = 4
    EMBARGO = 5

class CorrectionMethod(IntEnum):
    BONFERRONI = 1
    HOLM = 2
    BENJAMINI_HOCHBERG = 3

class GateStatus(IntEnum):
    PASS = 1
    WARN = 2
    FAIL = 3
    NOT_EVALUATED = 4

class PromotionStatus(IntEnum):
    REJECTED = 1
    EVIDENCE_ONLY = 2
    ELIGIBLE_FOR_DATASET_REVIEW = 3

class StressKind(IntEnum):
    ADDITIVE_COST_R = 1
    ENTRY_DELAY_PENALTY_R = 2
    EXIT_DELAY_PENALTY_R = 3
    DETERMINISTIC_TRADE_DROP = 4
    BEST_TRADE_REMOVAL = 5
    CLUSTER_EXCLUSION = 6

class LeakageSeverity(IntEnum):
    INFO = 1
    WARNING = 2
    FATAL = 3
