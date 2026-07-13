from .canonical import canonical_sha256
CONTRACTS=("WWConfig","WWRelationInstance","WWSidePlan","WWCompilationReport","WWScanRecord","WWContext","WWTransitionRecord","WWNeutralizationObservation","WWNeutralizationResult","WWStackEntry","WWActiveStack","DirectionGateDecision","WWEngineSnapshot","WWCheckpoint","WWRevisionImpact")
REASONS=(
"FP_WRC_WW_RELATION_COMPILED","FP_WRC_WW_SIDE_PLAN_ELIGIBLE","FP_WRC_WW_CONFIRMED_ACTIVE","FP_RC_WW_NEUTRALIZED","FP_RC_WW_DATA_INCOMPLETE","FP_RC_WW_NONE_ALLOW_BOTH","FP_RC_SUPPRESSED_BY_WW","FP_WRC_NEWEST_ACTIVE_WW_WINS","FP_WRC_OLDER_ACTIVE_WW_SHADOWED","FP_WRC_DIRECTION_ALIGNED_WITH_ACTIVE_WW","FP_WRC_WW_DIRECT_SETUP_NOT_SELF_GATED","FP_WRC_WW_CHECK_WEEK_EXPIRED","FP_WRC_CONFIRMED_WW_EVIDENCE_PRESERVED")
def contract_registry_hash(): return canonical_sha256(CONTRACTS)
def reason_registry_hash(): return canonical_sha256(REASONS)
