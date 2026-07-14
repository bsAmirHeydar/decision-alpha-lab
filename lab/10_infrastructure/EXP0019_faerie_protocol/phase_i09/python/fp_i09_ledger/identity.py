from fp_i02_kernel.enums import RelationCode,Direction
from .canonical import canonical_sha256,stable_id
from .constants import RELATION_ORDER,DIRECTION_ORDER
from .contracts import PairSessionQuotaKey,EligibilityEvidence,ArbitrationContender
from .enums import PrecheckState

def build_quota_key(context_epoch,trading_day_id,pair_id,owner_session_id,session_kind):
    payload={"context_epoch":context_epoch,"trading_day_id":trading_day_id,"pair_id":pair_id,"owner_session_id":owner_session_id,"session_kind":session_kind}
    h=canonical_sha256(payload); return PairSessionQuotaKey(stable_id("FPQK",payload),context_epoch,trading_day_id,pair_id,owner_session_id,session_kind,h)

def build_eligibility(signal,gate,*,relation_enabled=True,data_ready=True,precheck_state=PrecheckState.PASSED,evaluated_utc_ms=None,extra_reasons=()):
    reasons=[]
    if not relation_enabled: reasons.append("FP_LDG_RELATION_DISABLED")
    if not data_ready: reasons.append("FP_LDG_DATA_NOT_READY")
    if gate.eligibility.value=="SUPPRESSED": reasons.append("FP_LDG_SUPPRESSED_BY_WW")
    elif gate.eligibility.value=="BLOCKED": reasons.append("FP_LDG_BLOCKED_BY_WW_DATA")
    if precheck_state is PrecheckState.BLOCKED: reasons.append("FP_LDG_PRECHECK_BLOCKED")
    reasons=tuple(sorted(set(reasons+list(extra_reasons))))
    t=signal.confirmation_close_utc_ms if evaluated_utc_ms is None else evaluated_utc_ms
    p={"signal_id":signal.signal_id,"relation_enabled":relation_enabled,"data_ready":data_ready,"precheck_state":precheck_state.value,"gate_decision_id":gate.decision_id,"gate_eligibility":gate.eligibility.value,"evaluated_utc_ms":t,"reason_codes":reasons}
    h=canonical_sha256(p); return EligibilityEvidence(stable_id("FPEL",p),signal.signal_id,relation_enabled,data_ready,precheck_state,gate.decision_id,gate.eligibility,t,reasons,h)

def rank_key(signal):
    return (signal.first_hunt_minute_utc_ms,signal.confirmation_close_utc_ms,RELATION_ORDER.index(signal.relation.value),DIRECTION_ORDER.index(signal.direction.value),signal.hunter_symbol,signal.signal_id)

def build_contender(signal,quota_key,eligibility):
    rk=rank_key(signal); p={"signal_id":signal.signal_id,"quota_key_id":quota_key.quota_key_id,"eligibility_id":eligibility.evidence_id,"rank_key":rk}
    h=canonical_sha256(p); return ArbitrationContender(stable_id("FPCT",p),signal,quota_key,eligibility,rk,h)
