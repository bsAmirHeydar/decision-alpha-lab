from .contracts import ModuleHealth,IndicatorHealthReport
from .enums import *
from .canonical import canonical_sha256,stable_id,sorted_unique

def build_module_health(descriptor,last_processed_m1,source_revision_id,work_units=0,extra_reasons=()):
    status=descriptor.status
    payload={'phase_id':descriptor.phase_id,'version':descriptor.version,'status':status.value,'last_processed_m1':last_processed_m1,'source_revision_id':source_revision_id,'work_units':work_units,'reason_codes':sorted_unique(descriptor.reason_codes+tuple(extra_reasons))}
    return ModuleHealth(descriptor.phase_id,descriptor.version,status,last_processed_m1,source_revision_id,work_units,payload['reason_codes'],canonical_sha256(payload))

def aggregate_health(*,lifecycle,data_readiness,history_ready,checkpoint_disposition,module_health,incremental_lag_minutes,last_processing_duration_us,generated_utc_ms,config_hash,extra_reasons=()):
    reasons=list(extra_reasons)
    if any(m.status is ModuleStatus.BLOCKED for m in module_health): reasons.append('FP_IND_UPSTREAM_BLOCKED')
    if data_readiness is DataReadiness.BLOCKED: reasons.append('FP_IND_DATA_BLOCKED')
    if not history_ready: reasons.append('FP_IND_HISTORY_NOT_READY')
    if checkpoint_disposition in (CheckpointDisposition.REBUILD_REQUIRED,CheckpointDisposition.REJECT_CONFIG,CheckpointDisposition.REJECT_HASH,CheckpointDisposition.REJECT_INSTANCE,CheckpointDisposition.REJECT_VERSION): reasons.append('FP_IND_CHECKPOINT_REBUILD')
    if incremental_lag_minutes>0: reasons.append('FP_IND_INCREMENTAL_LAG')
    if lifecycle in (LifecycleState.BLOCKED,LifecycleState.STOPPED): overall=HealthState.BLOCKED
    elif any(m.status is ModuleStatus.BLOCKED for m in module_health) or data_readiness is DataReadiness.BLOCKED: overall=HealthState.BLOCKED
    elif lifecycle is LifecycleState.INITIALIZING or any(m.status is ModuleStatus.DEGRADED for m in module_health) or not history_ready or incremental_lag_minutes>0: overall=HealthState.DEGRADED
    else: overall=HealthState.READY
    reasons=sorted_unique(reasons)
    payload={'overall':overall.value,'lifecycle':lifecycle.value,'data_readiness':data_readiness.value,'history_ready':history_ready,'checkpoint_disposition':checkpoint_disposition.value,'module_health':[m.state_hash for m in module_health],'incremental_lag_minutes':incremental_lag_minutes,'last_processing_duration_us':last_processing_duration_us,'reason_codes':reasons,'generated_utc_ms':generated_utc_ms,'config_hash':config_hash}
    return IndicatorHealthReport(stable_id('FPHEALTH',payload),overall,lifecycle,data_readiness,history_ready,checkpoint_disposition,tuple(module_health),incremental_lag_minutes,last_processing_duration_us,reasons,generated_utc_ms,config_hash,canonical_sha256(payload))
