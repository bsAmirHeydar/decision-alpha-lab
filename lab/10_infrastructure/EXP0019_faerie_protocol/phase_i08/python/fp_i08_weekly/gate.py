from __future__ import annotations
from fp_i02_kernel.enums import RelationCode
from .canonical import canonical_sha256,stable_id
from .contracts import DirectionGateDecision
from .enums import GateEligibility,WWDataState

def evaluate_direction_gate(subject_signal_id,relation,direction,stack,evaluated_utc_ms):
    if relation is RelationCode.WW:
        eligibility=GateEligibility.NOT_APPLICABLE;reason="FP_WRC_WW_DIRECT_SETUP_NOT_SELF_GATED"
    elif stack.data_state is not WWDataState.COMPLETE:
        eligibility=GateEligibility.BLOCKED;reason="FP_RC_WW_DATA_INCOMPLETE"
    elif not stack.active_ww_context_id:
        eligibility=GateEligibility.ALLOWED;reason="FP_RC_WW_NONE_ALLOW_BOTH"
    elif direction is stack.active_direction:
        eligibility=GateEligibility.ALLOWED;reason="FP_WRC_DIRECTION_ALIGNED_WITH_ACTIVE_WW"
    else:
        eligibility=GateEligibility.SUPPRESSED;reason="FP_RC_SUPPRESSED_BY_WW"
    mat={"subject":subject_signal_id,"relation":relation,"direction":direction,"eligibility":eligibility,"active":stack.active_ww_context_id,"active_direction":stack.active_direction,"at":evaluated_utc_ms,"stack":stack.stack_hash}
    return DirectionGateDecision(stable_id("FPWWGATE",mat,32),subject_signal_id,relation,direction,eligibility,stack.active_ww_context_id,stack.active_direction,evaluated_utc_ms,reason,stack.stack_hash,canonical_sha256(mat))
