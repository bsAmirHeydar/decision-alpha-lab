"""Closed enumerations for the UCE-I12 promotion-governance surface."""
from __future__ import annotations
from enum import Enum

class GateOutcome(str, Enum):
    REJECT = "reject"
    CHALLENGE = "challenge"
    PROMOTE = "promote"

class EvidenceStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class TrialDisposition(str, Enum):
    ATTEMPTED = "attempted"
    SKIPPED = "skipped"
    INVALID = "invalid"
    PRUNED = "pruned"
    FAILED = "failed"
    TIMED_OUT = "timed_out"
    CANCELLED = "cancelled"
    SELECTED = "selected"
    ENSEMBLED = "ensembled"
    MANUAL_OVERRIDE = "manual_override"

class CorrectionMethod(str, Enum):
    BONFERRONI = "bonferroni"
    HOLM = "holm"
    BENJAMINI_HOCHBERG = "benjamini_hochberg"
    BENJAMINI_YEKUTIELY = "benjamini_yekutiely"

class NullKind(str, Enum):
    MATCHED_TIME = "matched_time"
    MATCHED_CONTEXT = "matched_context"
    RANDOM_DIRECTION = "random_direction"
    LABEL_PERMUTATION = "label_permutation"
    PLACEBO_TRIGGER = "placebo_trigger"
    DELAYED_TRIGGER = "delayed_trigger"
    RANDOM_TREATMENT = "random_treatment"
    MANUAL_BASELINE = "manual_baseline"

class StressKind(str, Enum):
    PARAMETER_NEIGHBORHOOD = "parameter_neighborhood"
    SEED = "seed"
    FOLD = "fold"
    REGIME = "regime"
    SESSION = "session"
    SYMBOL = "symbol"
    COST = "cost"
    SPREAD = "spread"
    SLIPPAGE = "slippage"
    LATENCY = "latency"
    FILL = "fill"
    TRADE_DROP = "trade_drop"
    BEST_TRADE_REMOVAL = "best_trade_removal"
    TAIL = "tail"
    CAPACITY = "capacity"
    SOURCE_REVISION = "source_revision"

class DecisionRole(str, Enum):
    DISCOVERY = "discovery"
    INNER_SELECTION = "inner_selection"
    CONFIRMATION = "confirmation"
    PROSPECTIVE_CHALLENGE = "prospective_challenge"
    FINAL_TEST = "final_test"
