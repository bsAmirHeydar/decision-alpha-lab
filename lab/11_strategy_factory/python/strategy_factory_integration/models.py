from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any
from .enums import CanonicalDirection, DifferentialStatus, IntegrationMode, LegacyDirection, LegacySide, LifecycleState, StageStatus
from .hashing import canonical_hash, stable_id

def _required(name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} is required")

def _positive(name: str, value: int | float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")

@dataclass(frozen=True)
class AdapterConfig:
    symbol_a: str
    symbol_b: str
    broker_utc_offset_hours: int = 3
    use_auto_new_york_dst: bool = True
    manual_new_york_utc_offset_hours: int = -5
    group_minutes: tuple[int, ...] = (3,5,9,10,15,18,20,24,30,40,45,60,72,90,120,150,180,240,300,360,720)
    require_m1_history: bool = True
    mode: IntegrationMode = IntegrationMode.AUDIT_ONLY
    live_authority: bool = False
    adapter_version: str = "1.0.0"
    def __post_init__(self):
        _required("symbol_a", self.symbol_a); _required("symbol_b", self.symbol_b)
        if self.symbol_a == self.symbol_b: raise ValueError("symbols must differ")
        if not self.group_minutes or tuple(sorted(set(self.group_minutes))) != tuple(sorted(self.group_minutes)):
            raise ValueError("group minutes must be unique")
        if any(v <= 0 for v in self.group_minutes): raise ValueError("invalid group minutes")
        if self.live_authority: raise ValueError("Phase 20 pilot cannot have live authority")
    @property
    def config_hash(self) -> str:
        return canonical_hash(self, "sf20cfg")

@dataclass(frozen=True)
class LegacyDivergenceCandidate:
    divergence_id: str
    group_name: str
    group_minutes: int
    current_cycle_index: int
    current_cycle_number: int
    reference_cycle_index: int
    reference_cycle_number: int
    trading_day_start_ny_s: int
    trading_day_end_ny_s: int
    current_cycle_start_ny_s: int
    current_cycle_end_ny_s: int
    reference_cycle_start_ny_s: int
    reference_cycle_end_ny_s: int
    direction: LegacyDirection
    side: LegacySide
    hunter_symbol: str
    clean_symbol: str
    one_sided_hunt: bool
    data_ready: bool
    hunter_reference_price: float
    clean_reference_price: float
    hunter_current_extreme: float
    clean_current_extreme: float
    clean_stop_reference_price: float
    note: str = ""
    def __post_init__(self):
        for n,v in (("divergence_id",self.divergence_id),("group_name",self.group_name),("hunter_symbol",self.hunter_symbol),("clean_symbol",self.clean_symbol)):
            _required(n,v)
        _positive("group_minutes", self.group_minutes)
        if self.hunter_symbol == self.clean_symbol: raise ValueError("hunter and clean symbols must differ")
        if not self.one_sided_hunt or not self.data_ready: raise ValueError("only ready one-sided candidates are mappable")
        if self.direction == LegacyDirection.BUY and self.side != LegacySide.LOW: raise ValueError("BUY must map from LOW side")
        if self.direction == LegacyDirection.SELL and self.side != LegacySide.HIGH: raise ValueError("SELL must map from HIGH side")
        if any(v <= 0 for v in (self.hunter_reference_price,self.clean_reference_price,self.hunter_current_extreme,self.clean_current_extreme,self.clean_stop_reference_price)):
            raise ValueError("candidate prices must be positive")
    @property
    def identity_payload(self) -> str:
        return "|".join((self.divergence_id,self.group_name,str(self.group_minutes),str(self.trading_day_start_ny_s),str(self.current_cycle_start_ny_s),str(self.reference_cycle_start_ny_s),self.direction.value,self.side.value,self.hunter_symbol,self.clean_symbol))
    @property
    def payload_hash(self) -> str:
        return canonical_hash(self, "sf20lp")

@dataclass(frozen=True)
class CanonicalAnatomyEvent:
    schema_name: str
    schema_version: str
    event_id: str
    strategy_id: str
    strategy_version: str
    producer_id: str
    producer_version: str
    symbol: str
    reference_symbol: str
    direction: CanonicalDirection
    event_time_ms: int
    known_time_ms: int
    confirmation_time_ms: int
    reference_price: float
    invalidation_price: float
    timeframe_seconds: int
    session_id: str
    parent_event_id: str
    market_event_cluster_id: str
    source_hash: str
    anatomy_state: str
    def __post_init__(self):
        for n,v in (("event_id",self.event_id),("strategy_id",self.strategy_id),("strategy_version",self.strategy_version),("producer_id",self.producer_id),("producer_version",self.producer_version),("symbol",self.symbol),("market_event_cluster_id",self.market_event_cluster_id),("source_hash",self.source_hash)):
            _required(n,v)
        if not (self.event_time_ms <= self.known_time_ms <= self.confirmation_time_ms):
            raise ValueError("known-time causality violated")
        _positive("timeframe_seconds", self.timeframe_seconds)
    @property
    def canonical_identity(self) -> str:
        return "|".join((self.strategy_id,self.strategy_version,self.symbol,self.reference_symbol,self.direction.value,str(self.event_time_ms),str(self.known_time_ms),str(self.confirmation_time_ms),str(self.timeframe_seconds),self.parent_event_id,self.market_event_cluster_id,self.source_hash))
    @property
    def derived_event_id(self) -> str:
        return stable_id("evt", self.canonical_identity)

@dataclass(frozen=True)
class MappingRecord:
    mapping_id: str
    legacy_divergence_id: str
    legacy_payload_hash: str
    canonical_event_id: str
    canonical_source_hash: str
    cluster_id: str
    mapped_at_utc_ms: int
    adapter_config_hash: str
    adapter_version: str
    reasons: tuple[str,...] = ()

@dataclass(frozen=True)
class LifecycleRecord:
    record_id: str
    event_id: str
    state: LifecycleState
    first_seen_utc_ms: int
    last_seen_utc_ms: int
    pulse_sequence: int
    reason: str

@dataclass(frozen=True)
class DifferentialRecord:
    record_id: str
    legacy_divergence_id: str
    canonical_event_id: str
    status: DifferentialStatus
    mismatched_fields: tuple[str,...]
    legacy_payload_hash: str
    canonical_payload_hash: str
    known_time_ms: int

@dataclass(frozen=True)
class DifferentialReport:
    report_id: str
    case_id: str
    legacy_count: int
    canonical_count: int
    matched_count: int
    missing_count: int
    extra_count: int
    mismatch_count: int
    records: tuple[DifferentialRecord,...]
    passed: bool

@dataclass(frozen=True)
class StageEvidence:
    stage: str
    status: StageStatus
    input_id: str
    output_id: str
    known_time_ms: int
    reason_code: str
    detail: str
    evidence_hash: str = ""
    def __post_init__(self):
        _required("stage",self.stage); _required("reason_code",self.reason_code)
        if not self.evidence_hash:
            object.__setattr__(self,"evidence_hash",canonical_hash({k:v for k,v in asdict(self).items() if k!="evidence_hash"},"sf20evd"))

@dataclass(frozen=True)
class IntegrationManifest:
    manifest_id: str
    run_id: str
    generation_id: str
    strategy_id: str
    adapter_id: str
    adapter_version: str
    adapter_config_hash: str
    legacy_source_hash: str
    engine_phase: int
    mode: IntegrationMode
    live_authority: bool
    created_at_utc_ms: int
    downstream_bindings: tuple[str,...]
    exact_contract_versions: tuple[tuple[str,str],...]
    def __post_init__(self):
        if self.engine_phase != 20: raise ValueError("engine phase must be 20")
        if self.live_authority: raise ValueError("live authority must remain disabled")
        if len(self.downstream_bindings) != len(set(self.downstream_bindings)):
            raise ValueError("duplicate binding")

@dataclass
class PilotTelemetry:
    pulses: int = 0
    legacy_candidates_seen: int = 0
    canonical_events_emitted: int = 0
    duplicate_events_suppressed: int = 0
    events_retired: int = 0
    mapping_failures: int = 0
    differential_mismatches: int = 0
    context_passes: int = 0
    candidate_passes: int = 0
    downstream_gates: int = 0
    live_authority_attempts: int = 0

@dataclass(frozen=True)
class ReplayManifest:
    replay_id: str
    case_id: str
    adapter_config_hash: str
    input_fixture_hash: str
    expected_event_ids: tuple[str,...]
    expected_cluster_ids: tuple[str,...]
    pulse_times_utc_ms: tuple[int,...]
    strict_ordering: bool = True

@dataclass(frozen=True)
class MigrationWave:
    wave_id: str
    order: int
    anatomy_family: str
    source_paths: tuple[str,...]
    target_adapter_id: str
    entry_gate: str
    exit_gate: str
    status: str
