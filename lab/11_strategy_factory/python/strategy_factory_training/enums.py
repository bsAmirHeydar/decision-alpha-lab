from enum import IntEnum

class DatasetRole(IntEnum):
    TRAIN = 1
    VALIDATION = 2
    TEST = 3
    PURGED = 4
    EMBARGO = 5

class LabelKind(IntEnum):
    BINARY_NET_R = 1
    REGRESSION_NET_R = 2
    RANKING_NET_R = 3

class AmbiguousLabelPolicy(IntEnum):
    EXCLUDE = 1
    NEGATIVE = 2
    ZERO_UTILITY = 3

class MissingValuePolicy(IntEnum):
    REJECT_ROW = 1
    TRAIN_MEDIAN = 2
    TRAIN_CONSTANT = 3

class ScalePolicy(IntEnum):
    NONE = 1
    STANDARDIZE = 2

class ModelFamily(IntEnum):
    NEVER_TRADE = 1
    ALWAYS_TRADE = 2
    TRAIN_PREVALENCE = 3
    SINGLE_FEATURE_THRESHOLD = 4
    LOGISTIC_RIDGE = 5
    RIDGE_REGRESSION = 6
    DECISION_STUMP = 7

class CalibrationMethod(IntEnum):
    NONE = 1
    PLATT = 2

class PredictionRole(IntEnum):
    TRAIN_DIAGNOSTIC = 1
    VALIDATION_SELECTION = 2
    TEST_OOS = 3

class TrainingStatus(IntEnum):
    COMPLETE = 1
    REJECTED = 2
    FAILED = 3

class TaskKind(IntEnum):
    BINARY_CLASSIFICATION = 1
    REGRESSION = 2
    RANKING = 3
