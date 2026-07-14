from .contracts import *
from .canonical import sha256,stable_id,sorted_unique

def build_health(product_states,mismatch_count,trace_lag_events=0,export_backlog=0):
    reasons=[]
    vals=dict(product_states)
    if any(v=='BLOCKED' for v in vals.values()) or mismatch_count>0: state=HealthState.BLOCKED;reasons.append('FP_DIAG_HEALTH_BLOCKED')
    elif any(v=='DEGRADED' for v in vals.values()) or trace_lag_events>0 or export_backlog>0: state=HealthState.DEGRADED;reasons.append('FP_DIAG_HEALTH_DEGRADED')
    else: state=HealthState.READY;reasons.append('FP_DIAG_HEALTH_READY')
    pairs=tuple(sorted(product_states));rs=sorted_unique(reasons)
    sid=stable_id('FPDHEALTH',{'states':pairs,'mismatches':mismatch_count,'lag':trace_lag_events,'backlog':export_backlog})
    body={'snapshot_id':sid,'state':state.value,'states':pairs,'mismatches':mismatch_count,'lag':trace_lag_events,'backlog':export_backlog,'reasons':rs}
    return HealthSnapshot(sid,state,pairs,mismatch_count,trace_lag_events,export_backlog,rs,sha256(body))
