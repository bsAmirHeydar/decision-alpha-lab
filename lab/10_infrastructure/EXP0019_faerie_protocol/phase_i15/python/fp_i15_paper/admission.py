from .contracts import *
from .canonical import stable_id

def admit_winner(proof:DiagnosticAcceptanceProof,winner:WinnerSignalInput,readiness:CausalReadiness)->AdmissionDecision:
    reasons=[]
    if proof.status!="PASS": reasons.append("FP_PAPER_DIAGNOSTIC_ACCEPTANCE_NOT_PASS")
    if proof.pair_id not in winner.quota_key_id: reasons.append("FP_PAPER_PAIR_QUOTA_MISMATCH")
    if proof.config_hash!=winner.config_hash: reasons.append("FP_PAPER_CONFIG_MISMATCH")
    if proof.source_revision_id!=winner.source_revision_id: reasons.append("FP_PAPER_SOURCE_REVISION_MISMATCH")
    if not readiness.reservation_is_active_winner: reasons.append("FP_PAPER_NOT_ACTIVE_I09_WINNER")
    if readiness.watermark_utc_ms<winner.confirmation_close_utc_ms: reasons.append("FP_PAPER_CAUSAL_WATERMARK_BEHIND")
    if not readiness.complete: reasons.append("FP_PAPER_CAUSAL_DATA_INCOMPLETE")
    status=AdmissionStatus.ADMITTED if not reasons else AdmissionStatus.BLOCKED
    return AdmissionDecision(status,winner.signal_id,tuple(sorted(reasons)),stable_id("FPADM",{"proof":proof.acceptance_id,"signal":winner.signal_id,"readiness":readiness,"reasons":reasons}))
