from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Mapping
from .canonical import canonical_sha256
from .enums import *
from .errors import CompatibilityError

def _req(value,name):
    if not isinstance(value,str) or not value.strip(): raise CompatibilityError('required_field',f'{name} required')
def _sha(value,name):
    if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value): raise CompatibilityError('invalid_sha256',f'{name} must be lowercase SHA-256')

@dataclass(frozen=True,slots=True)
class DependencyPin:
    dependency_id:str; semantic_owner:str; source_context:SourceContext; reuse_mode:ReuseMode; relative_root:str; file_globs:tuple[str,...]; expected_file_count:int; expected_aggregate_sha256:str; exact_version:str; mutation_allowed:bool=False
    def __post_init__(self):
        for v,n in ((self.dependency_id,'dependency_id'),(self.semantic_owner,'semantic_owner'),(self.relative_root,'relative_root'),(self.exact_version,'exact_version')):_req(v,n)
        _sha(self.expected_aggregate_sha256,'expected_aggregate_sha256')
        if self.expected_file_count<1: raise CompatibilityError('invalid_file_count','expected_file_count must be positive')
        if self.mutation_allowed: raise CompatibilityError('shared_core_mutation_forbidden','FP-I01 dependencies are read-only')
    @property
    def pin_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class AdapterDescriptor:
    adapter_id:str; adapter_version:str; source_context:SourceContext; source_type:str; family:AdapterFamily; reuse_mode:ReuseMode; dependency_id:str; input_fields:tuple[str,...]; output_fields:tuple[str,...]; semantic_delta:tuple[str,...]; mutation_allowed:bool=False; authority:tuple[str,...]=()
    def __post_init__(self):
        for v,n in ((self.adapter_id,'adapter_id'),(self.adapter_version,'adapter_version'),(self.source_type,'source_type'),(self.dependency_id,'dependency_id')):_req(v,n)
        if not self.input_fields or not self.output_fields: raise CompatibilityError('empty_adapter_contract','input/output fields required')
        if self.mutation_allowed: raise CompatibilityError('adapter_mutation_forbidden','adapters are read-only')
        forbidden={'BROKER','ORDER','POSITION','NETWORK'} & {x.upper() for x in self.authority}
        if forbidden: raise CompatibilityError('forbidden_authority','adapter authority is forbidden',{'authority':sorted(forbidden)})
    @property
    def key(self): return f'{self.adapter_id}@{self.adapter_version}'
    @property
    def descriptor_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CanonicalTimeSnapshot:
    source_context:SourceContext; source_type:str; source_fingerprint:str; broker_time:int; utc_time:int; new_york_time:int; trading_day_start_ny:int; trading_day_end_ny:int; inside_trading_day:bool; ny_utc_offset_hours:int; trading_day_key:str; health:HealthState; reason_code:str
    @property
    def snapshot_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CanonicalReferencePair:
    source_context:SourceContext; source_type:str; source_fingerprint:str; reference_id:str; window_code:str; window_start:int; window_end:int; complete:bool; ready:bool; symbol_a:str; symbol_b:str; high_a:float; low_a:float; high_b:float; low_b:float; high_time_a:int; low_time_a:int; high_time_b:int; low_time_b:int; data_ready_a:bool; data_ready_b:bool; health:HealthState; reason_code:str
    @property
    def snapshot_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CanonicalHuntObservation:
    source_context:SourceContext; source_type:str; source_fingerprint:str; observation_id:str; reference_id:str; opportunity_id:str; side:HuntSide; pair_state:PairState; hunter_symbol:str; protected_symbol:str; reference_price_a:float; reference_price_b:float; current_extreme_a:float; current_extreme_b:float; event_time_utc:int; availability_time_utc:int; replay_safe:bool; health:HealthState; reason_code:str
    @property
    def snapshot_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CanonicalDivergenceCandidate:
    source_context:SourceContext; source_type:str; source_fingerprint:str; candidate_id:str; reference_id:str; opportunity_id:str; direction:Direction; side:HuntSide; hunter_symbol:str; protected_symbol:str; one_sided:bool; symmetric:bool; data_ready:bool; hunter_reference_price:float; protected_reference_price:float; event_time_utc:int; health:HealthState; reason_code:str
    @property
    def snapshot_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CanonicalConfirmationResult:
    source_context:SourceContext; source_type:str; source_fingerprint:str; result_id:str; candidate_id:str; observation_id:str; opportunity_id:str; outcome:ConfirmationOutcome; direction:Direction; side:HuntSide; hunter_symbol:str; protected_symbol:str; host_timeframe_seconds:int; host_bar_open_utc:int; host_bar_close_utc:int; confirmation_price:float; final:bool; immutable:bool; replay_safe:bool; health:HealthState; reason_code:str
    @property
    def snapshot_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CanonicalLifecycleRecord:
    source_context:SourceContext; source_type:str; source_fingerprint:str; reference_id:str; side:HuntSide; protected_symbol:str; first_hunter_symbol:str; state:str; retired:bool; accepted_use_count:int; duplicate_use_count:int; rejected_use_count:int; activation_time_utc:int; retirement_time_utc:int; immutable:bool; replay_safe:bool; health:HealthState; reason_code:str
    @property
    def snapshot_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class AdapterRunEvidence:
    fixture_id:str; adapter_key:str; source_hash_before:str; source_hash_after:str; output_hash:str; repeated_output_hash:str; source_unchanged:bool; deterministic:bool; status:CompatibilityStatus; blockers:tuple[str,...]=(); warnings:tuple[str,...]=()
    @property
    def evidence_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class DependencyVerification:
    dependency_id:str; expected_file_count:int; actual_file_count:int; expected_hash:str; actual_hash:str; status:CompatibilityStatus; reason_code:str
    @property
    def evidence_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CompatibilityReport:
    report_id:str; phase_id:str; dependency_results:tuple[DependencyVerification,...]; adapter_results:tuple[AdapterRunEvidence,...]; duplicate_findings:tuple[Mapping[str,Any],...]; previous_context_tests:tuple[Mapping[str,Any],...]; status:CompatibilityStatus; blockers:tuple[str,...]; warnings:tuple[str,...]; metaeditor_status:str
    @property
    def report_hash(self): return canonical_sha256(asdict(self))
