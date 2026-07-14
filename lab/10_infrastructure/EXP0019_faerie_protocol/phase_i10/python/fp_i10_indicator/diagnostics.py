from .contracts import DiagnosticReport
from .constants import PHASE_ID,PHASE_VERSION,NO_RUNTIME_AUTHORITY
from .canonical import canonical_sha256,stable_id

def build_diagnostic(engine,generated_utc_ms):
    counters=tuple(sorted((k,int(v)) for k,v in engine.counters.items()))
    payload={'instance_id':engine.instance.instance_id,'phase_id':PHASE_ID,'phase_version':PHASE_VERSION,'runtime_authority':NO_RUNTIME_AUTHORITY,'lifecycle_event_count':len(engine.event_chain.events),'chain_head_hash':engine.event_chain.head,'snapshot_hash':engine.snapshot.snapshot_hash,'health':int(engine.snapshot.health.overall),'counters':counters,'reason_codes':engine.snapshot.health.reason_codes,'generated_utc_ms':generated_utc_ms}
    return DiagnosticReport(stable_id('FPDIAG',payload),engine.instance.instance_id,PHASE_ID,PHASE_VERSION,NO_RUNTIME_AUTHORITY,len(engine.event_chain.events),engine.event_chain.head,engine.snapshot.snapshot_hash,engine.snapshot.health.overall,counters,engine.snapshot.health.reason_codes,generated_utc_ms,canonical_sha256(payload))
