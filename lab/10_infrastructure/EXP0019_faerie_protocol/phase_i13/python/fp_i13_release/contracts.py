from __future__ import annotations
from dataclasses import dataclass,replace
from typing import Tuple
from .canonical import require_id,require_hash,sha256,stable_id,sorted_unique
from .constants import *
from .enums import *
from .errors import FPI13Error

@dataclass(frozen=True,slots=True)
class ReplayEvent:
    sequence:int; event_time:int; event_type:ReplayEventType; semantic_id:str; payload_hash:str; source_revision_id:str; kind:str=''; is_historical:bool=False; reason_codes:tuple[str,...]=(); event_id:str=''
    def __post_init__(self):
        if self.sequence<1 or self.event_time<0: raise FPI13Error('FP_REL_EVENT_SEQUENCE_INVALID','event counters invalid')
        require_id(self.semantic_id,'semantic_id');require_hash(self.payload_hash,'payload_hash');require_id(self.source_revision_id,'source_revision_id')
        if self.reason_codes!=sorted_unique(self.reason_codes): raise FPI13Error('FP_REL_REASONS_NONCANONICAL','reason codes must be sorted unique')
        if self.event_id: require_id(self.event_id,'event_id')
    @property
    def computed_event_id(self): return self.event_id or stable_id('FPEVT',{'sequence':self.sequence,'type':self.event_type.value,'semantic_id':self.semantic_id,'payload_hash':self.payload_hash,'revision':self.source_revision_id})
    @property
    def event_hash(self): return sha256({'event_id':self.computed_event_id,'sequence':self.sequence,'event_time':self.event_time,'event_type':self.event_type.value,'semantic_id':self.semantic_id,'payload_hash':self.payload_hash,'source_revision_id':self.source_revision_id,'kind':self.kind,'is_historical':self.is_historical,'reason_codes':self.reason_codes})

@dataclass(frozen=True,slots=True)
class ReplayFixture:
    fixture_id:str; config_hash:str; resolved_host_timeframe_minutes:int; events:tuple[ReplayEvent,...]; source_revision_id:str; description:str=''
    def __post_init__(self):
        require_id(self.fixture_id,'fixture_id');require_hash(self.config_hash,'config_hash');require_id(self.source_revision_id,'source_revision_id')
        if self.resolved_host_timeframe_minutes<=0: raise FPI13Error('FP_REL_HOST_TF_INVALID','host timeframe invalid')
        if len(self.events)>MAX_EVENTS_PER_FIXTURE: raise FPI13Error('FP_REL_FIXTURE_TOO_LARGE','fixture too large')
        seq=[x.sequence for x in self.events]
        if seq!=sorted(seq) or len(seq)!=len(set(seq)): raise FPI13Error('FP_REL_SEQUENCE_NONCANONICAL','event sequences must be unique ascending')
    @property
    def fixture_hash(self): return sha256(self)

@dataclass(frozen=True,slots=True)
class InstanceIdentity:
    instance_id:str; chart_id:int; terminal_path_hash:str; pair_id:str; context_epoch:str; config_hash:str; object_namespace:str; checkpoint_key:str; export_file_key:str

@dataclass(frozen=True,slots=True)
class ReplayInventory:
    semantic_ids:tuple[str,...]; semantic_payloads:tuple[tuple[str,str],...]; visual_semantic_ids:tuple[str,...]; visual_object_ids:tuple[str,...]; alert_ids:tuple[str,...]; suppressed_historical_alert_ids:tuple[str,...]; export_ids:tuple[str,...]; health_codes:tuple[str,...]; event_chain_hash:str; last_sequence:int; inventory_hash:str

@dataclass(frozen=True,slots=True)
class ReplayTelemetry:
    event_count:int; chunk_count:int; full_scan_count:int; duplicate_count:int; elapsed_ns:int; peak_memory_bytes:int; checkpoint_bytes:int; object_count:int; object_ops:int; events_per_second:float; max_chunk_ns:int; telemetry_hash:str

@dataclass(frozen=True,slots=True)
class ReplayRun:
    run_id:str; fixture_id:str; mode:ReplayMode; instance_id:str; chart_timeframe_minutes:int; resolved_host_timeframe_minutes:int; config_hash:str; inventory:ReplayInventory; telemetry:ReplayTelemetry; run_hash:str

@dataclass(frozen=True,slots=True)
class ParityReport:
    report_id:str; left_run_id:str; right_run_id:str; status:ParityStatus; compared_fields:tuple[str,...]; mismatches:tuple[str,...]; report_hash:str

@dataclass(frozen=True,slots=True)
class ReplayCheckpoint:
    checkpoint_id:str; version:str; fixture_id:str; config_hash:str; instance_id:str; processed_sequence:int; event_chain_hash:str; event_hashes:tuple[tuple[str,str],...]; semantic_payloads:tuple[tuple[str,str],...]; visual_semantics:tuple[tuple[str,str],...]; alerts:tuple[str,...]; suppressed_alerts:tuple[str,...]; exports:tuple[str,...]; health_codes:tuple[str,...]; payload_hash:str

@dataclass(frozen=True,slots=True)
class CheckpointValidation:
    disposition:CheckpointDisposition; reason_code:str; checkpoint:ReplayCheckpoint|None

@dataclass(frozen=True,slots=True)
class RestartReport:
    report_id:str; uninterrupted_run_id:str; restarted_run_id:str; checkpoint_disposition:CheckpointDisposition; parity:ParityReport; report_hash:str

@dataclass(frozen=True,slots=True)
class TimeframeParityReport:
    report_id:str; fixture_id:str; chart_timeframes:tuple[int,...]; resolved_host_timeframe_minutes:int; status:ParityStatus; semantic_inventory_hashes:tuple[str,...]; run_ids:tuple[str,...]; mismatches:tuple[str,...]; report_hash:str

@dataclass(frozen=True,slots=True)
class MultiInstanceReport:
    report_id:str; instance_ids:tuple[str,...]; namespaces:tuple[str,...]; checkpoint_keys:tuple[str,...]; export_keys:tuple[str,...]; semantic_inventory_hashes:tuple[str,...]; status:IsolationStatus; collisions:tuple[str,...]; report_hash:str

@dataclass(frozen=True,slots=True)
class BudgetLimit:
    metric:str; soft_limit:float; hard_limit:float; unit:str
    def __post_init__(self):
        if self.soft_limit<0 or self.hard_limit<0: raise FPI13Error('FP_REL_BUDGET_INVALID','budget limits invalid')
        if self.metric.startswith('minimum_'):
            if self.soft_limit<self.hard_limit: raise FPI13Error('FP_REL_BUDGET_INVALID','minimum metric soft limit must be >= hard limit')
        elif self.hard_limit<self.soft_limit:
            raise FPI13Error('FP_REL_BUDGET_INVALID','maximum metric hard limit must be >= soft limit')

@dataclass(frozen=True,slots=True)
class PerformanceBudget:
    budget_id:str; limits:tuple[BudgetLimit,...]; profile_id:ReleaseProfileId

@dataclass(frozen=True,slots=True)
class BudgetObservation:
    metric:str; value:float; unit:str; status:BudgetStatus; soft_limit:float; hard_limit:float; reason_code:str

@dataclass(frozen=True,slots=True)
class PerformanceReport:
    report_id:str; budget_id:str; observations:tuple[BudgetObservation,...]; status:BudgetStatus; report_hash:str

@dataclass(frozen=True,slots=True)
class ProjectionFact:
    object_id:str; semantic_id:str; priority:ObjectPriority; is_historical:bool; immutable:bool=True

@dataclass(frozen=True,slots=True)
class DegradationDecision:
    decision_id:str; health:HealthState; semantic_count:int; projected_object_ids:tuple[str,...]; deferred_object_ids:tuple[str,...]; reason_codes:tuple[str,...]; decision_hash:str

@dataclass(frozen=True,slots=True)
class ReleaseProfile:
    profile_id:ReleaseProfileId; history_days:int; max_objects:int; max_object_ops_per_frame:int; chunk_size:int; alerts_enabled:bool; audit_export_enabled:bool; visual_mode:str; diagnostics_enabled:bool; profile_hash:str=''
    @property
    def computed_hash(self): return sha256(replace(self,profile_hash=''))

@dataclass(frozen=True,slots=True)
class GateResult:
    gate_id:str; status:GateStatus; reason_codes:tuple[str,...]; evidence_hash:str

@dataclass(frozen=True,slots=True)
class ReleaseManifest:
    manifest_id:str; manifest_version:str; product_name:str; phase_id:str; phase_version:str; composition_versions:tuple[tuple[str,str],...]; release_profiles:tuple[ReleaseProfile,...]; indicator_path:str; self_test_path:str; user_guide_path:str; open_decision_id:str; open_decision_state:str; metaeditor_compile_status:GateStatus; source_file_hashes:tuple[tuple[str,str],...]; manifest_hash:str

@dataclass(frozen=True,slots=True)
class AcceptanceReport:
    report_id:str; status:AcceptanceStatus; gates:tuple[GateResult,...]; release_manifest_id:str; production_release_ready:bool; pending_external_gates:tuple[str,...]; report_hash:str
