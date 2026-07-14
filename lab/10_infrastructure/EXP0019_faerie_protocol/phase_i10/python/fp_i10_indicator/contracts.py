from __future__ import annotations
from dataclasses import dataclass
from .canonical import require_identifier,require_sha256,require_semver,require_m1,canonical_sha256,sorted_unique
from .constants import *
from .enums import *
from .errors import FPI10Error

@dataclass(frozen=True,slots=True)
class UpstreamModuleDescriptor:
    phase_id:str; version:str; contract_hash:str; authority:str; status:ModuleStatus; reason_codes:tuple[str,...]=()
    def __post_init__(self):
        require_identifier(self.phase_id,'phase_id'); require_semver(self.version,'version'); require_sha256(self.contract_hash,'contract_hash')
        if self.authority!=NO_RUNTIME_AUTHORITY: raise FPI10Error('FP_IND_UPSTREAM_AUTHORITY_INVALID','upstream module authority must be NONE')
        if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI10Error('FP_IND_REASON_CODES_NONCANONICAL','reason codes must be sorted unique')
    @property
    def descriptor_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class IndicatorConfig:
    context_id:str; context_epoch:str; primary_symbol:str; secondary_symbol:str; pair_id:str
    host_timeframe_minutes:int; timer_seconds:int; history_days:int; max_incremental_minutes:int
    enable_state_buffers:bool; enable_diagnostics:bool; fail_init_on_blocked_manifest:bool
    indicator_version:str=PHASE_VERSION; composition_version:str=COMPOSITION_VERSION; output_version:str=OUTPUT_VERSION
    def __post_init__(self):
        for n in ('context_id','context_epoch','primary_symbol','secondary_symbol','pair_id'): require_identifier(getattr(self,n),n)
        for n in ('indicator_version','composition_version','output_version'): require_semver(getattr(self,n),n)
        if self.primary_symbol==self.secondary_symbol: raise FPI10Error('FP_IND_SYMBOLS_IDENTICAL','symbols must differ')
        if self.host_timeframe_minutes not in (1,2,3,4,5,6,10,12,15,20,30,60,120,180,240,360,480,720,1440,10080,43200): raise FPI10Error('FP_IND_HOST_TIMEFRAME_INVALID','host timeframe minutes unsupported')
        if not MIN_TIMER_SECONDS<=self.timer_seconds<=MAX_TIMER_SECONDS: raise FPI10Error('FP_IND_TIMER_SECONDS_INVALID','timer seconds outside policy')
        if not MIN_HISTORY_DAYS<=self.history_days<=MAX_HISTORY_DAYS: raise FPI10Error('FP_IND_HISTORY_DAYS_INVALID','history days outside policy')
        if not 1<=self.max_incremental_minutes<=MAX_INCREMENTAL_LIMIT: raise FPI10Error('FP_IND_INCREMENTAL_LIMIT_INVALID','incremental limit outside policy')
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class InstanceIdentity:
    instance_id:str; chart_id:int; terminal_instance_id:str; program_name:str; pair_id:str; context_epoch:str; config_hash:str; object_namespace:str; checkpoint_key:str; identity_hash:str
    def __post_init__(self):
        require_identifier(self.instance_id,'instance_id'); require_identifier(self.terminal_instance_id,'terminal_instance_id'); require_identifier(self.program_name,'program_name'); require_identifier(self.pair_id,'pair_id'); require_identifier(self.context_epoch,'context_epoch'); require_sha256(self.config_hash,'config_hash'); require_sha256(self.identity_hash,'identity_hash')
        if self.chart_id<=0: raise FPI10Error('FP_IND_CHART_ID_INVALID','chart id must be positive')
        if not self.object_namespace.startswith('FP19::'): raise FPI10Error('FP_IND_NAMESPACE_INVALID','namespace must be FP19 scoped')

@dataclass(frozen=True,slots=True)
class CompositionManifest:
    composition_id:str; composition_version:str; config_hash:str; modules:tuple[UpstreamModuleDescriptor,...]; manifest_hash:str
    def __post_init__(self):
        require_identifier(self.composition_id,'composition_id'); require_semver(self.composition_version,'composition_version'); require_sha256(self.config_hash,'config_hash'); require_sha256(self.manifest_hash,'manifest_hash')
        if tuple(x.phase_id for x in self.modules)!=EXPECTED_UPSTREAM_PHASES: raise FPI10Error('FP_IND_MODULE_SEQUENCE_INVALID','exact FP-I03..FP-I09 sequence required')

@dataclass(frozen=True,slots=True)
class ModuleHealth:
    phase_id:str; version:str; status:ModuleStatus; last_processed_m1:int; source_revision_id:str; incremental_work_units:int; reason_codes:tuple[str,...]; state_hash:str
    def __post_init__(self):
        require_identifier(self.phase_id,'phase_id'); require_semver(self.version,'version'); require_m1(self.last_processed_m1,'last_processed_m1'); require_identifier(self.source_revision_id,'source_revision_id'); require_sha256(self.state_hash,'state_hash')
        if self.incremental_work_units<0: raise FPI10Error('FP_IND_WORK_UNITS_INVALID','work units negative')
        if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI10Error('FP_IND_REASON_CODES_NONCANONICAL','reason codes must be sorted unique')

@dataclass(frozen=True,slots=True)
class IncrementalPlan:
    plan_id:str; mode:WorkMode; start_m1:int; end_m1:int; work_minutes:int; remaining_minutes:int; trigger:ProcessTrigger; reason_codes:tuple[str,...]; plan_hash:str
    def __post_init__(self):
        require_identifier(self.plan_id,'plan_id'); require_m1(self.start_m1,'start_m1'); require_m1(self.end_m1,'end_m1'); require_sha256(self.plan_hash,'plan_hash')
        if self.end_m1<self.start_m1: raise FPI10Error('FP_IND_PLAN_RANGE_INVALID','plan end before start')
        if self.work_minutes<0 or self.remaining_minutes<0: raise FPI10Error('FP_IND_PLAN_COUNT_INVALID','plan counts negative')

@dataclass(frozen=True,slots=True)
class IndicatorHealthReport:
    health_report_id:str; overall:HealthState; lifecycle:LifecycleState; data_readiness:DataReadiness; history_ready:bool; checkpoint_disposition:CheckpointDisposition
    module_health:tuple[ModuleHealth,...]; incremental_lag_minutes:int; last_processing_duration_us:int; reason_codes:tuple[str,...]; generated_utc_ms:int; config_hash:str; report_hash:str
    def __post_init__(self):
        require_identifier(self.health_report_id,'health_report_id'); require_m1(self.generated_utc_ms,'generated_utc_ms'); require_sha256(self.config_hash,'config_hash'); require_sha256(self.report_hash,'report_hash')
        if self.incremental_lag_minutes<0 or self.last_processing_duration_us<0: raise FPI10Error('FP_IND_HEALTH_COUNTER_INVALID','health counters negative')
        if tuple(m.phase_id for m in self.module_health)!=EXPECTED_UPSTREAM_PHASES: raise FPI10Error('FP_IND_HEALTH_MODULE_SET_INVALID','health must include I03-I09')
        if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI10Error('FP_IND_REASON_CODES_NONCANONICAL','reason codes must be sorted unique')

@dataclass(frozen=True,slots=True)
class OutputBufferFrame:
    frame_id:str; values:tuple[float,...]; available:bool; generated_utc_ms:int; output_version:str; frame_hash:str
    def __post_init__(self):
        require_identifier(self.frame_id,'frame_id'); require_m1(self.generated_utc_ms,'generated_utc_ms'); require_semver(self.output_version,'output_version'); require_sha256(self.frame_hash,'frame_hash')
        if len(self.values)!=BUFFER_COUNT: raise FPI10Error('FP_IND_BUFFER_COUNT_INVALID',f'exactly {BUFFER_COUNT} buffers required')

@dataclass(frozen=True,slots=True)
class IndicatorSnapshot:
    snapshot_id:str; sequence:int; instance:InstanceIdentity; composition:CompositionManifest; health:IndicatorHealthReport; buffers:OutputBufferFrame
    active_ww_direction:ActiveWWDirection; confirmed_signal_count:int; allowed_signal_count:int; suppressed_by_ww_count:int; suppressed_by_quota_count:int; quota_winner_signal_id:str; ledger_event_count:int; source_revision_sequence:int; source_revision_id:str; last_processed_m1:int; generated_utc_ms:int; snapshot_hash:str
    def __post_init__(self):
        require_identifier(self.snapshot_id,'snapshot_id'); require_identifier(self.source_revision_id,'source_revision_id'); require_m1(self.last_processed_m1,'last_processed_m1'); require_m1(self.generated_utc_ms,'generated_utc_ms'); require_sha256(self.snapshot_hash,'snapshot_hash')
        for n in ('sequence','confirmed_signal_count','allowed_signal_count','suppressed_by_ww_count','suppressed_by_quota_count','ledger_event_count','source_revision_sequence'):
            if getattr(self,n)<0: raise FPI10Error('FP_IND_SNAPSHOT_COUNTER_INVALID',f'{n} negative')
        if self.allowed_signal_count>self.confirmed_signal_count: raise FPI10Error('FP_IND_ALLOWED_COUNT_INVALID','allowed cannot exceed confirmed')

@dataclass(frozen=True,slots=True)
class LifecycleEvent:
    event_id:str; sequence:int; event_type:LifecycleEventType; occurred_utc_ms:int; instance_id:str; reason_code:str; payload_hash:str; prior_event_hash:str; event_hash:str
    def __post_init__(self):
        require_identifier(self.event_id,'event_id'); require_m1(self.occurred_utc_ms,'occurred_utc_ms'); require_identifier(self.instance_id,'instance_id'); require_identifier(self.reason_code,'reason_code'); require_sha256(self.payload_hash,'payload_hash'); require_sha256(self.event_hash,'event_hash')
        if self.sequence<0: raise FPI10Error('FP_IND_EVENT_SEQUENCE_INVALID','event sequence negative')
        if self.sequence==0 and self.prior_event_hash: raise FPI10Error('FP_IND_GENESIS_PRIOR_HASH_INVALID','genesis cannot have prior hash')
        if self.sequence>0: require_sha256(self.prior_event_hash,'prior_event_hash')

@dataclass(frozen=True,slots=True)
class IndicatorCheckpoint:
    checkpoint_id:str; checkpoint_version:str; instance_id:str; config_hash:str; composition_hash:str; last_processed_m1:int; lifecycle_sequence:int; snapshot_hash:str; source_revision_id:str; payload_hash:str
    def __post_init__(self):
        require_identifier(self.checkpoint_id,'checkpoint_id'); require_semver(self.checkpoint_version,'checkpoint_version'); require_identifier(self.instance_id,'instance_id'); require_sha256(self.config_hash,'config_hash'); require_sha256(self.composition_hash,'composition_hash'); require_m1(self.last_processed_m1,'last_processed_m1'); require_sha256(self.snapshot_hash,'snapshot_hash'); require_identifier(self.source_revision_id,'source_revision_id'); require_sha256(self.payload_hash,'payload_hash')
        if self.lifecycle_sequence<0: raise FPI10Error('FP_IND_CHECKPOINT_SEQUENCE_INVALID','checkpoint sequence negative')

@dataclass(frozen=True,slots=True)
class CheckpointValidation:
    disposition:CheckpointDisposition; accepted:bool; reason_codes:tuple[str,...]; validation_hash:str
    def __post_init__(self):
        require_sha256(self.validation_hash,'validation_hash')
        if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI10Error('FP_IND_REASON_CODES_NONCANONICAL','reason codes must be sorted unique')

@dataclass(frozen=True,slots=True)
class DiagnosticReport:
    diagnostic_id:str; instance_id:str; phase_id:str; phase_version:str; runtime_authority:str; lifecycle_event_count:int; chain_head_hash:str; snapshot_hash:str; health:HealthState; counters:tuple[tuple[str,int],...]; reason_codes:tuple[str,...]; generated_utc_ms:int; diagnostic_hash:str
    def __post_init__(self):
        require_identifier(self.diagnostic_id,'diagnostic_id'); require_identifier(self.instance_id,'instance_id'); require_identifier(self.phase_id,'phase_id'); require_semver(self.phase_version,'phase_version'); require_sha256(self.chain_head_hash,'chain_head_hash'); require_sha256(self.snapshot_hash,'snapshot_hash'); require_m1(self.generated_utc_ms,'generated_utc_ms'); require_sha256(self.diagnostic_hash,'diagnostic_hash')
        if self.runtime_authority!=NO_RUNTIME_AUTHORITY: raise FPI10Error('FP_IND_RUNTIME_AUTHORITY_INVALID','indicator runtime authority must be NONE')
