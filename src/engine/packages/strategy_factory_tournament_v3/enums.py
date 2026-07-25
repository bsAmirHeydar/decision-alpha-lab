from enum import Enum
class DataMode(str,Enum): FIXTURE='fixture'; HISTORICAL_REAL='historical_real'; PROSPECTIVE_PAPER='prospective_paper'
class ContextKind(str,Enum): EXP0017='exp0017'; HOOK_ZONE='hook_zone'
class TreatmentFamily(str,Enum):
 TIGHT_CONVEX='tight_convex';WIDE_SURVIVAL='wide_survival';LIMIT='limit';CONFIRMATION='confirmation';FIXED_TARGET='fixed_target';RUNNER='runner';FIXED_PLUS_TRAIL='fixed_plus_trail';PARTIAL_PLUS_RUNNER='partial_plus_runner';CAPITAL_POLICY='capital_policy'
class AlgorithmFamily(str,Enum): MANUAL='manual';NAIVE='naive';CLASSICAL='classical';RANKING='ranking';TREATMENT_CHOICE='treatment_choice';SURVIVAL='survival';DISTRIBUTIONAL='distributional';DEEP='deep'
class TrialStatus(str,Enum): DECLARED='declared';RUNNING='running';SUCCEEDED='succeeded';FAILED='failed';PRUNED='pruned';SKIPPED='skipped';REJECTED='rejected'
class Stage(str,Enum): INVENTORY='inventory';CONTEXT='context';FREEZE='freeze';TOURNAMENT='tournament';CONFIRMATORY='confirmatory';PROSPECTIVE='prospective';DECISION='decision'
class DecisionStatus(str,Enum): PROMOTE='promote';REJECT='reject';PENDING='pending';CHALLENGE='challenge'
class ReconciliationStatus(str,Enum): MATCH='match';MISMATCH='mismatch';MISSING='missing';DUPLICATE='duplicate'
