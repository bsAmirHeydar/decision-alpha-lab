from .canonical import canonical_sha256,stable_id
from .contracts import ConfirmationTransitionRecord
from .enums import ConfirmationState,ConfirmationTransition
from .errors import FPI07Error
_ALLOWED={
ConfirmationState.PENDING:{ConfirmationState.CONFIRMED,ConfirmationState.CANCELLED_SECOND_TOUCH,ConfirmationState.CANCELLED_ROLE_CHANGED,ConfirmationState.NO_SIGNAL_AT_CLOSE,ConfirmationState.INVALID_DATA,ConfirmationState.EXPIRED_DEADLINE,ConfirmationState.MISSED_CLOSE_REPLAY_REQUIRED,ConfirmationState.SUPERSEDED}}
_TRANS={
ConfirmationState.CONFIRMED:ConfirmationTransition.CONFIRMED,ConfirmationState.CANCELLED_SECOND_TOUCH:ConfirmationTransition.SECOND_TOUCH_CANCELLED,ConfirmationState.CANCELLED_ROLE_CHANGED:ConfirmationTransition.ROLE_CHANGED_CANCELLED,ConfirmationState.NO_SIGNAL_AT_CLOSE:ConfirmationTransition.NO_SIGNAL_FINALIZED,ConfirmationState.INVALID_DATA:ConfirmationTransition.DATA_INVALIDATED,ConfirmationState.EXPIRED_DEADLINE:ConfirmationTransition.DEADLINE_EXPIRED,ConfirmationState.MISSED_CLOSE_REPLAY_REQUIRED:ConfirmationTransition.MISSED_CLOSE_BLOCKED,ConfirmationState.SUPERSEDED:ConfirmationTransition.SUPERSEDED}
def transition(candidate_id,sequence,prior,next_state,event_utc_ms,evidence_id,reason_code):
    if prior not in _ALLOWED or next_state not in _ALLOWED[prior]: raise FPI07Error("FP_CRC_ILLEGAL_TRANSITION",f"illegal {prior}->{next_state}")
    material={"candidate":candidate_id,"sequence":sequence,"prior":prior,"next":next_state,"at":event_utc_ms,"evidence":evidence_id,"reason":reason_code}
    return ConfirmationTransitionRecord(stable_id("FPCONFEVT",material,32),candidate_id,sequence,_TRANS[next_state],prior,next_state,event_utc_ms,evidence_id,reason_code,canonical_sha256(material))
def admission_event(pending):
    material={"candidate":pending.candidate.candidate_id,"pending":pending.pending_id,"at":pending.admitted_utc_ms,"reason":"FP_CRC_CANDIDATE_ADMITTED"}
    return ConfirmationTransitionRecord(stable_id("FPCONFEVT",material,32),pending.candidate.candidate_id,0,ConfirmationTransition.ADMITTED,None,ConfirmationState.PENDING,pending.admitted_utc_ms,pending.pending_id,"FP_CRC_CANDIDATE_ADMITTED",canonical_sha256(material))
