from __future__ import annotations
from .enums import HealthState,LifecycleAction,Severity
from .hashing import stable_id
from .models import HealthSnapshot,LifecycleRecommendation

def build_health(known_time_ms:int,active:tuple[tuple[str,Severity],...],dropped:int,duplicates:int,schema_rejections:int,extra_reasons:tuple[str,...]=())->HealthSnapshot:
    critical=sum(1 for _,s in active if s in {Severity.CRITICAL,Severity.EMERGENCY});reasons=list(extra_reasons)
    if critical: reasons.append("CRITICAL_ALERT_ACTIVE")
    if dropped: reasons.append("TELEMETRY_DROPPED")
    if schema_rejections: reasons.append("SCHEMA_REJECTION")
    state=HealthState.HEALTHY
    if active or dropped or schema_rejections or reasons: state=HealthState.DEGRADED
    if critical or schema_rejections>0 or any(r in {"DISTRIBUTION_DRIFT_CRITICAL","EXECUTION_DRIFT_CRITICAL"} for r in reasons): state=HealthState.CRITICAL
    if any(r in {"RECONCILIATION_MISMATCH","MISSING_LIVE_TRANSACTION","MODEL_INTEGRITY_FAILURE"} for r in reasons): state=HealthState.SUSPEND_RECOMMENDED
    sid=stable_id("sf19-health",known_time_ms,state.value,len(active),critical,dropped,duplicates,schema_rejections,*sorted(reasons))
    return HealthSnapshot(sid,known_time_ms,state,len(active),critical,dropped,duplicates,schema_rejections,tuple(dict.fromkeys(reasons)))

def recommend(health:HealthSnapshot,scope_id:str,model_id:str,generation_id:str,evidence_ids:tuple[str,...])->LifecycleRecommendation:
    action=LifecycleAction.CONTINUE
    if health.state==HealthState.DEGRADED:action=LifecycleAction.OBSERVE
    elif health.state==HealthState.CRITICAL:action=LifecycleAction.INVESTIGATE
    elif health.state==HealthState.SUSPEND_RECOMMENDED:action=LifecycleAction.SUSPEND
    if "MODEL_INTEGRITY_FAILURE" in health.reasons:action=LifecycleAction.ROLLBACK
    rid=stable_id("sf19-recommendation",health.snapshot_id,action.value,scope_id,model_id,generation_id,*evidence_ids)
    return LifecycleRecommendation(rid,action,scope_id,model_id,generation_id,health.known_time_ms,health.reasons,evidence_ids,True,False)
