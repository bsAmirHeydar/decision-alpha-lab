"""Closed enumerations for UCE-I11 contracts."""

from enum import Enum


class AdmissionDecision(str, Enum):
    ACCEPT = "accept"
    WARN = "warn"
    REJECT = "reject"


class SearchKind(str, Enum):
    BASELINE = "baseline"
    GRID = "grid"
    RANDOM = "random"
    QUASI_RANDOM = "quasi_random"
    TPE = "tpe"
    SUCCESSIVE_HALVING = "successive_halving"
    HYPERBAND = "hyperband"
    EVOLUTIONARY = "evolutionary"
    MULTI_OBJECTIVE = "multi_objective"


class ParameterKind(str, Enum):
    INTEGER = "integer"
    FLOAT = "float"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"


class NodeKind(str, Enum):
    DATASET = "dataset"
    SPLIT = "split"
    TRANSFORM = "transform"
    TRAINER = "trainer"
    TRIAL = "trial"
    FOLD = "fold"
    SEED = "seed"
    CALIBRATION = "calibration"
    THRESHOLD = "threshold"
    ENSEMBLE = "ensemble"
    VALIDATION = "validation"
    REPORT = "report"
    EXPORT = "export"


class NodeStatus(str, Enum):
    PLANNED = "planned"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PRUNED = "pruned"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"
    QUARANTINED = "quarantined"
    TIMED_OUT = "timed_out"
    CACHED = "cached"
    INVALID = "invalid"


class LedgerAction(str, Enum):
    ATTEMPTED = "attempted"
    SKIPPED = "skipped"
    INVALID = "invalid"
    PRUNED = "pruned"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    SELECTED = "selected"
    REJECTED = "rejected"
    THRESHOLDED = "thresholded"
    CALIBRATED = "calibrated"
    ENSEMBLED = "ensembled"
    MANUAL_OVERRIDE = "manual_override"
    CACHED = "cached"
    RESUMED = "resumed"
    CANCELLED = "cancelled"
    SUCCEEDED = "succeeded"


class BudgetDecision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    DENY = "deny"


class CacheStatus(str, Enum):
    VALID = "valid"
    MISS = "miss"
    STALE = "stale"
    INCOMPATIBLE = "incompatible"
    CORRUPT = "corrupt"


class ObjectiveDirection(str, Enum):
    MINIMIZE = "minimize"
    MAXIMIZE = "maximize"


class SchedulerEventKind(str, Enum):
    PLAN = "plan"
    READY = "ready"
    CLAIM = "claim"
    START = "start"
    HEARTBEAT = "heartbeat"
    COMPLETE = "complete"
    FAIL = "fail"
    RETRY = "retry"
    TIMEOUT = "timeout"
    CANCEL = "cancel"
    QUARANTINE = "quarantine"
    CACHE_HIT = "cache_hit"
    RESUME = "resume"
    SKIP = "skip"


class FailureDisposition(str, Enum):
    RETRYABLE = "retryable"
    TERMINAL = "terminal"
    QUARANTINE = "quarantine"


class ResourceDevice(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    ANY = "any"
