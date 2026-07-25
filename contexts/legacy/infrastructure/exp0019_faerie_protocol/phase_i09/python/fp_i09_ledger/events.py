from .canonical import canonical_sha256,stable_id
from .contracts import LedgerEvent
from .enums import LedgerEventType

def make_event(sequence,event_type,aggregate_id,occurred_utc_ms,payload,*,signal_id="",quota_key_id="",source_phase="FP-I09",reason_code="FP_LDG_EVENT_RECORDED",prior_event_hash=""):
    ph=canonical_sha256(payload)
    core={"sequence":sequence,"event_type":event_type.value,"aggregate_id":aggregate_id,"signal_id":signal_id,"quota_key_id":quota_key_id,"occurred_utc_ms":occurred_utc_ms,"source_phase":source_phase,"reason_code":reason_code,"payload_hash":ph,"prior_event_hash":prior_event_hash}
    eh=canonical_sha256(core); return LedgerEvent(stable_id("FPEV",core),sequence,event_type,aggregate_id,signal_id,quota_key_id,occurred_utc_ms,source_phase,reason_code,ph,prior_event_hash,eh)

def verify_chain(events):
    prior=""
    for i,e in enumerate(events):
        if e.sequence!=i or e.prior_event_hash!=prior: return False
        core={"sequence":e.sequence,"event_type":e.event_type.value,"aggregate_id":e.aggregate_id,"signal_id":e.signal_id,"quota_key_id":e.quota_key_id,"occurred_utc_ms":e.occurred_utc_ms,"source_phase":e.source_phase,"reason_code":e.reason_code,"payload_hash":e.payload_hash,"prior_event_hash":e.prior_event_hash}
        if canonical_sha256(core)!=e.event_hash: return False
        prior=e.event_hash
    return True
