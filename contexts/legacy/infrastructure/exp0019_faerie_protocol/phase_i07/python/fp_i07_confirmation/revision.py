from .canonical import canonical_sha256,stable_id
from .contracts import RevisionImpact
from .enums import RevisionDisposition,ConfirmationState

def assess_revision(candidate_or_result,revision_id,start_utc_ms,end_utc_ms):
    candidate=getattr(candidate_or_result,"candidate",None)
    if candidate is None:
        # ConfirmationResult: confirmed evidence is immutable; nonconfirmed records are also audit evidence.
        cid=candidate_or_result.candidate_id
        disp=RevisionDisposition.CONFIRMED_PRESERVED if candidate_or_result.final_state is ConfirmationState.CONFIRMED else RevisionDisposition.UNAFFECTED
        reason="FP_CRC_CONFIRMED_EVIDENCE_PRESERVED" if disp is RevisionDisposition.CONFIRMED_PRESERVED else "FP_CRC_TERMINAL_RESULT_UNAFFECTED"
    else:
        cid=candidate.candidate_id
        overlaps=start_utc_ms < candidate_or_result.projection.target_close_utc_ms and end_utc_ms > candidate.first_hunt_minute_utc_ms
        disp=RevisionDisposition.PENDING_INVALIDATED if overlaps else RevisionDisposition.UNAFFECTED
        reason="FP_CRC_PENDING_INVALIDATED_BY_REVISION" if overlaps else "FP_CRC_REVISION_OUTSIDE_CANDIDATE_RANGE"
    material={"revision":revision_id,"start":start_utc_ms,"end":end_utc_ms,"candidate":cid,"disposition":disp,"reason":reason}
    return RevisionImpact(stable_id("FPREVIMP",material,32),revision_id,start_utc_ms,end_utc_ms,cid,disp,reason,canonical_sha256(material))
