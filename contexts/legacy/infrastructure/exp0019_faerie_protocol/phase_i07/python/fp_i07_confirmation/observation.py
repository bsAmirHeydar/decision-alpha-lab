from .canonical import canonical_sha256,stable_id
from .contracts import CloseObservation
from .enums import ClosePairState

def observe_close(candidate,bar,pair_state,source_available_through_utc_ms,source_revision_id):
    hunter=pair_state in (ClosePairState.HUNTER_ONLY,ClosePairState.BOTH)
    protected=pair_state in (ClosePairState.PROTECTED_ONLY,ClosePairState.BOTH)
    reason={ClosePairState.HUNTER_ONLY:"FP_CRC_HUNTER_ONLY_AT_CLOSE",ClosePairState.BOTH:"FP_CRC_BOTH_TOUCHED_AT_CLOSE",ClosePairState.PROTECTED_ONLY:"FP_CRC_ROLE_CHANGED_AT_CLOSE",ClosePairState.NONE:"FP_CRC_NONE_AT_CLOSE",ClosePairState.DATA_INCOMPLETE:"FP_CRC_DATA_INCOMPLETE_AT_CLOSE"}[pair_state]
    material={"candidate":candidate.candidate_id,"bar":bar.host_bar_id,"state":pair_state,"available":source_available_through_utc_ms,"revision":source_revision_id,"m1":bar.constituent_m1_hash}
    return CloseObservation(stable_id("FPCLOSEOBS",material,32),candidate.candidate_id,bar.host_bar_id,pair_state,bar.close_utc_ms,source_available_through_utc_ms,hunter,protected,source_revision_id,canonical_sha256(material),reason)
