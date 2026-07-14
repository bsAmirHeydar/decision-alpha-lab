from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Any
from .canonical import require_hash,require_id,sha256,stable_id,sorted_unique
from .constants import MAX_REASON_CODES,TRACE_CONTRACT_VERSION
from .enums import *
from .errors import FPI14Error

@dataclass(frozen=True,slots=True)
class ProductManifest:
    product:ProductKind; product_version:str; context_id:str; context_epoch:str; pair_id:str; config_hash:str; source_revision_id:str; resolved_host_timeframe_minutes:int; module_versions:tuple[tuple[str,str],...]; trace_contract_version:str=TRACE_CONTRACT_VERSION; manifest_id:str=""
    def __post_init__(self):
        require_id(self.product_version,"product_version");require_id(self.context_id,"context_id");require_id(self.context_epoch,"context_epoch");require_id(self.pair_id,"pair_id");require_hash(self.config_hash,"config_hash");require_id(self.source_revision_id,"source_revision_id")
        if self.resolved_host_timeframe_minutes<=0: raise FPI14Error("FP_DIAG_HOST_TF_INVALID","host timeframe must be positive")
        if tuple(sorted(self.module_versions))!=self.module_versions or len(set(k for k,_ in self.module_versions))!=len(self.module_versions): raise FPI14Error("FP_DIAG_MODULES_NONCANONICAL","module versions must be sorted unique")
    @property
    def computed_manifest_id(self): return self.manifest_id or stable_id("FPMAN",{"product":self.product.value,"version":self.product_version,"context":self.context_id,"epoch":self.context_epoch,"pair":self.pair_id,"config":self.config_hash,"revision":self.source_revision_id,"host_tf":self.resolved_host_timeframe_minutes,"modules":self.module_versions,"trace":self.trace_contract_version})
    @property
    def semantic_manifest_hash(self): return sha256({"context_id":self.context_id,"context_epoch":self.context_epoch,"pair_id":self.pair_id,"config_hash":self.config_hash,"source_revision_id":self.source_revision_id,"host_tf":self.resolved_host_timeframe_minutes,"module_versions":self.module_versions,"trace_contract_version":self.trace_contract_version})

@dataclass(frozen=True,slots=True)
class TraceEvent:
    sequence:int; event_time_utc_ms:int; product:ProductKind; event_type:TraceEventType; semantic_id:str; payload_hash:str; config_hash:str; source_revision_id:str; state:str=""; relation:str=""; direction:str=""; owner_session_id:str=""; buffer_index:int=-1; numeric_value:float=0.0; reason_codes:tuple[str,...]=(); event_id:str=""
    def __post_init__(self):
        if self.sequence<1 or self.event_time_utc_ms<0: raise FPI14Error("FP_DIAG_SEQUENCE_INVALID","event sequence/time invalid")
        require_id(self.semantic_id,"semantic_id");require_hash(self.payload_hash,"payload_hash");require_hash(self.config_hash,"config_hash");require_id(self.source_revision_id,"source_revision_id")
        if len(self.reason_codes)>MAX_REASON_CODES or self.reason_codes!=sorted_unique(self.reason_codes): raise FPI14Error("FP_DIAG_REASONS_NONCANONICAL","reason codes must be sorted unique")
        if self.event_id: require_id(self.event_id,"event_id")
    @property
    def canonical_key(self): return (self.sequence,self.event_type.value,self.semantic_id)
    @property
    def computed_event_id(self): return self.event_id or stable_id("FPTRC",{"sequence":self.sequence,"type":self.event_type.value,"semantic_id":self.semantic_id,"payload_hash":self.payload_hash,"config":self.config_hash,"revision":self.source_revision_id})
    @property
    def semantic_hash(self): return sha256({"sequence":self.sequence,"time":self.event_time_utc_ms,"type":self.event_type.value,"semantic_id":self.semantic_id,"payload_hash":self.payload_hash,"config_hash":self.config_hash,"source_revision_id":self.source_revision_id,"state":self.state,"relation":self.relation,"direction":self.direction,"owner_session_id":self.owner_session_id,"buffer_index":self.buffer_index,"numeric_value":round(self.numeric_value,10),"reason_codes":self.reason_codes})
    @property
    def event_hash(self): return sha256({"product":self.product.value,"event_id":self.computed_event_id,"semantic_hash":self.semantic_hash})

@dataclass(frozen=True,slots=True)
class TraceInventory:
    event_count:int; semantic_ids:tuple[str,...]; event_semantic_hashes:tuple[tuple[str,str],...]; signal_ids:tuple[str,...]; ww_context_ids:tuple[str,...]; quota_winner_ids:tuple[str,...]; buffer_values:tuple[tuple[int,float],...]; visual_ids:tuple[str,...]; health_codes:tuple[str,...]; chain_hash:str; inventory_hash:str

@dataclass(frozen=True,slots=True)
class TraceRun:
    run_id:str; fixture_id:str; product:ProductKind; manifest:ProductManifest; events:tuple[TraceEvent,...]; inventory:TraceInventory; duplicate_count:int; run_hash:str

@dataclass(frozen=True,slots=True)
class DifferentialMismatch:
    mismatch_id:str; kind:MismatchKind; left_product:ProductKind; right_product:ProductKind; sequence:int; semantic_id:str; field_name:str; left_value_hash:str; right_value_hash:str; reason_code:str

@dataclass(frozen=True,slots=True)
class PairwiseDifferentialReport:
    report_id:str; left_run_id:str; right_run_id:str; status:DifferentialStatus; compared_event_count:int; mismatches:tuple[DifferentialMismatch,...]; report_hash:str

@dataclass(frozen=True,slots=True)
class CrossProductReport:
    report_id:str; fixture_id:str; status:DifferentialStatus; products:tuple[ProductKind,...]; pairwise_reports:tuple[PairwiseDifferentialReport,...]; consensus_inventory_hash:str; mismatch_count:int; report_hash:str

@dataclass(frozen=True,slots=True)
class TraceCheckpoint:
    checkpoint_id:str; version:str; product:ProductKind; fixture_id:str; config_hash:str; processed_sequence:int; chain_hash:str; event_hashes:tuple[tuple[str,str],...]; events:tuple[TraceEvent,...]; payload_hash:str

@dataclass(frozen=True,slots=True)
class CheckpointValidation:
    disposition:CheckpointDisposition; reason_code:str; checkpoint:TraceCheckpoint|None

@dataclass(frozen=True,slots=True)
class StressScenario:
    scenario_id:str; kind:ScenarioKind; seed:int; duplicate_every:int=0; disconnect_after:int=0; reconnect_skip:int=0; restart_after:int=0; chart_timeframe_minutes:int=1; scenario_hash:str=""
    @property
    def computed_hash(self): return sha256(replace(self,scenario_hash=""))

@dataclass(frozen=True,slots=True)
class StressResult:
    result_id:str; scenario_id:str; product:ProductKind; baseline_run_id:str; stressed_run_id:str; status:DifferentialStatus; mismatch_count:int; duplicate_count:int; reconnect_count:int; restart_count:int; result_hash:str

@dataclass(frozen=True,slots=True)
class ExportReceipt:
    receipt_id:str; format:ExportFormat; path:str; appended_records:int; duplicate_records:int; last_sequence:int; payload_hash:str

@dataclass(frozen=True,slots=True)
class HealthSnapshot:
    snapshot_id:str; state:HealthState; product_states:tuple[tuple[str,str],...]; mismatch_count:int; trace_lag_events:int; export_backlog:int; reason_codes:tuple[str,...]; snapshot_hash:str

@dataclass(frozen=True,slots=True)
class AcceptanceGate:
    gate_id:str; status:GateStatus; reason_codes:tuple[str,...]; evidence_hash:str

@dataclass(frozen=True,slots=True)
class DiagnosticAcceptance:
    acceptance_id:str; status:GateStatus; gates:tuple[AcceptanceGate,...]; source_accepted:bool; production_ready:bool; pending_external_gates:tuple[str,...]; acceptance_hash:str
