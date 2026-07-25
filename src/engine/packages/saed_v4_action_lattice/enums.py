from enum import Enum

class EvaluationStatus(str, Enum):
    SATISFIED='satisfied'
    VIOLATED='violated'
    DEFERRED='deferred_known_time'

class CandidateStatus(str, Enum):
    FEASIBLE='feasible'
    PRUNED='pruned'

class EdgeKind(str, Enum):
    ATOMIC_PARAMETER_STEP='atomic_parameter_step'
    FALLBACK_ABSTAIN='fallback_abstain'
    FALLBACK_SKIP='fallback_skip'

class ActionClass(str, Enum):
    ORDINARY='ordinary'
    ABSTAIN='abstain'
    SKIP='skip'

class DiffClass(str, Enum):
    IDENTICAL='identical'
    SEMANTIC='semantic'
    INTEGRITY='integrity'
