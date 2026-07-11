from enum import IntEnum

class RegistryState(IntEnum):
    DRAFT = 1
    REGISTERED = 2
    EVIDENCE_VALIDATED = 3
    CANDIDATE = 4
    CHALLENGER = 5
    CHAMPION = 6
    SUSPENDED = 7
    RETIRED = 8
    REJECTED = 9

class GovernanceDecisionType(IntEnum):
    REGISTER = 1
    VALIDATE_EVIDENCE = 2
    NOMINATE_CANDIDATE = 3
    ASSIGN_CHALLENGER = 4
    PROMOTE_CHAMPION = 5
    SUSPEND = 6
    RESTORE_CHALLENGER = 7
    RETIRE = 8
    REJECT = 9
    ROLLBACK = 10
    SUPERSEDE = 11

class GateStatus(IntEnum):
    PASS = 1
    FAIL = 2
    NOT_APPLICABLE = 3

class PromotionVerdict(IntEnum):
    ELIGIBLE = 1
    INELIGIBLE = 2
    MANUAL_REVIEW = 3

class ReleaseChannel(IntEnum):
    RESEARCH_ONLY = 1
    INFERENCE_CANDIDATE = 2
    SHADOW_ELIGIBLE = 3

class AttestationKind(IntEnum):
    NONE = 1
    EXTERNAL_DETACHED_SIGNATURE = 2
    CI_PROVENANCE = 3

class ArtifactRole(IntEnum):
    MODEL = 1
    TRANSFORM = 2
    CALIBRATION = 3
    FEATURE_SCHEMA = 4
    LABEL_CONTRACT = 5
    MODEL_CARD = 6
    TRAINING_REPORT = 7
    OOS_PREDICTIONS = 8
    VALIDATION_REPORT = 9
    PROMOTION_EVIDENCE = 10
    SOURCE_CODE = 11
    OTHER = 12
