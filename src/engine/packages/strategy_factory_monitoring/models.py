from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from .enums import AlertState, DriftKind, HealthState, LifecycleAction, MetricKind, Severity
from .hashing import canonical_hash, stable_id

def _req_text(name: str, value: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} is required")

def _nonneg(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")

@dataclass(frozen=True)
class TelemetrySchemaEntry:
    metric_name: str
    schema_version: str
    metric_kind: MetricKind
    unit: str
    stage: str
    description: str
    lower_bound: float | None=None
    upper_bound: float | None=None
    tags: tuple[str,...]=()
    def __post_init__(self):
        for n,v in (("metric_name",self.metric_name),("schema_version",self.schema_version),("unit",self.unit),("stage",self.stage),("description",self.description)):
            _req_text(n,v)
        if self.lower_bound is not None and self.upper_bound is not None and self.lower_bound>self.upper_bound:
            raise ValueError("invalid bounds")
    @property
    def schema_id(self)->str:
        return stable_id("sf19-schema",self.metric_name,self.schema_version,self.metric_kind.value,self.unit,self.stage)

@dataclass(frozen=True)
class TelemetrySchemaManifest:
    manifest_version: str
    entries: tuple[TelemetrySchemaEntry,...]
    def __post_init__(self):
        _req_text("manifest_version",self.manifest_version)
        names=[e.metric_name for e in self.entries]
        if len(names)!=len(set(names)):
            raise ValueError("duplicate metric name")
    @property
    def manifest_id(self)->str:
        return canonical_hash(self)
    def by_name(self)->dict[str,TelemetrySchemaEntry]:
        return {e.metric_name:e for e in self.entries}

@dataclass(frozen=True)
class TelemetryEvent:
    metric_name: str
    schema_id: str
    run_id: str
    generation_id: str
    strategy_id: str
    model_id: str
    correlation_id: str
    causation_id: str
    observed_time_ms: int
    known_time_ms: int
    sequence: int
    value: float
    tags: tuple[tuple[str,str],...]=()
    payload_hash: str=""
    event_id: str=""
    def __post_init__(self):
        for n,v in (("metric_name",self.metric_name),("schema_id",self.schema_id),("run_id",self.run_id),("generation_id",self.generation_id),("correlation_id",self.correlation_id)):
            _req_text(n,v)
        if self.known_time_ms < self.observed_time_ms:
            raise ValueError("known time precedes observed time")
        if self.sequence<1:
            raise ValueError("sequence must be positive")
        if len({k for k,_ in self.tags})!=len(self.tags):
            raise ValueError("duplicate tag key")
        if not self.payload_hash:
            object.__setattr__(self,"payload_hash",canonical_hash({"metric_name":self.metric_name,"value":self.value,"tags":self.tags}))
        if not self.event_id:
            object.__setattr__(self,"event_id",stable_id("sf19-event",self.run_id,self.sequence,self.metric_name,self.known_time_ms,self.payload_hash))

@dataclass(frozen=True)
class LatencySloPolicy:
    policy_id: str
    stage: str
    bucket_edges_us: tuple[int,...]
    p50_limit_us: int
    p95_limit_us: int
    p99_limit_us: int
    minimum_samples: int=30
    def __post_init__(self):
        _req_text("policy_id",self.policy_id); _req_text("stage",self.stage)
        if tuple(sorted(set(self.bucket_edges_us)))!=self.bucket_edges_us or not self.bucket_edges_us or self.bucket_edges_us[0]<=0:
            raise ValueError("bucket edges must be unique positive ascending")
        if not (0<self.p50_limit_us<=self.p95_limit_us<=self.p99_limit_us):
            raise ValueError("invalid percentile limits")
        if self.minimum_samples<1:
            raise ValueError("minimum_samples must be positive")

@dataclass(frozen=True)
class LatencyHistogramSnapshot:
    stage: str
    policy_id: str
    sample_count: int
    bucket_edges_us: tuple[int,...]
    bucket_counts: tuple[int,...]
    overflow_count: int
    minimum_us: int
    maximum_us: int
    mean_us: float
    p50_us: int
    p95_us: int
    p99_us: int
    slo_breached: bool
    snapshot_time_ms: int
    snapshot_id: str=""
    def __post_init__(self):
        if self.sample_count<0 or self.overflow_count<0:
            raise ValueError("negative counts")
        if len(self.bucket_edges_us)!=len(self.bucket_counts):
            raise ValueError("bucket mismatch")
        if not self.snapshot_id:
            object.__setattr__(self,"snapshot_id",canonical_hash(self))

@dataclass(frozen=True)
class DriftBaseline:
    baseline_id: str
    kind: DriftKind
    feature_name: str
    model_id: str
    bin_edges: tuple[float,...]
    probabilities: tuple[float,...]
    mean: float
    standard_deviation: float
    sample_count: int
    window_start_ms: int
    window_end_ms: int
    def __post_init__(self):
        _req_text("baseline_id",self.baseline_id); _req_text("feature_name",self.feature_name)
        if len(self.probabilities)!=len(self.bin_edges)+1:
            raise ValueError("probability/bin mismatch")
        if any(p<0 for p in self.probabilities) or abs(sum(self.probabilities)-1.0)>1e-6:
            raise ValueError("baseline probabilities must sum to one")
        if self.standard_deviation<0 or self.sample_count<1 or self.window_end_ms<self.window_start_ms:
            raise ValueError("invalid baseline")

@dataclass(frozen=True)
class DriftObservation:
    observation_id: str
    baseline_id: str
    kind: DriftKind
    feature_name: str
    model_id: str
    bin_counts: tuple[int,...]
    mean: float
    standard_deviation: float
    sample_count: int
    missing_count: int
    invalid_count: int
    window_start_ms: int
    window_end_ms: int
    def __post_init__(self):
        if self.sample_count<1 or sum(self.bin_counts)!=self.sample_count:
            raise ValueError("observation counts inconsistent")
        if self.missing_count<0 or self.invalid_count<0 or self.window_end_ms<self.window_start_ms:
            raise ValueError("invalid observation")

@dataclass(frozen=True)
class DriftThresholdPolicy:
    policy_id: str
    kind: DriftKind
    psi_warning: float
    psi_critical: float
    js_warning: float
    js_critical: float
    mean_z_warning: float
    mean_z_critical: float
    missing_rate_critical: float
    invalid_rate_critical: float
    minimum_samples: int
    def __post_init__(self):
        values=(self.psi_warning,self.psi_critical,self.js_warning,self.js_critical,self.mean_z_warning,self.mean_z_critical,self.missing_rate_critical,self.invalid_rate_critical)
        if any(v<0 for v in values) or self.psi_warning>self.psi_critical or self.js_warning>self.js_critical or self.mean_z_warning>self.mean_z_critical:
            raise ValueError("invalid thresholds")
        if self.minimum_samples<1:
            raise ValueError("minimum_samples must be positive")

@dataclass(frozen=True)
class DriftResult:
    result_id: str
    baseline_id: str
    observation_id: str
    policy_id: str
    kind: DriftKind
    psi: float
    jensen_shannon: float
    mean_z_shift: float
    missing_rate: float
    invalid_rate: float
    severity: Severity
    sufficient_samples: bool
    reasons: tuple[str,...]

@dataclass(frozen=True)
class ExecutionDriftObservation:
    observation_id: str
    window_start_ms: int
    window_end_ms: int
    order_count: int
    fill_count: int
    reject_count: int
    mismatch_count: int
    mean_slippage_points: float
    p95_slippage_points: float
    mean_fill_latency_us: float
    p95_fill_latency_us: float
    missing_transaction_count: int=0
    def __post_init__(self):
        for name,value in (("order_count",self.order_count),("fill_count",self.fill_count),("reject_count",self.reject_count),("mismatch_count",self.mismatch_count),("missing_transaction_count",self.missing_transaction_count)):
            if value<0: raise ValueError(f"{name} cannot be negative")
        if self.window_end_ms<self.window_start_ms:
            raise ValueError("invalid window")

@dataclass(frozen=True)
class ExecutionDriftPolicy:
    policy_id: str
    minimum_orders: int
    reject_rate_warning: float
    reject_rate_critical: float
    mismatch_rate_critical: float
    p95_slippage_warning: float
    p95_slippage_critical: float
    p95_fill_latency_warning_us: float
    p95_fill_latency_critical_us: float
    def __post_init__(self):
        if self.minimum_orders<1: raise ValueError("minimum_orders must be positive")

@dataclass(frozen=True)
class ExecutionDriftResult:
    result_id: str
    observation_id: str
    policy_id: str
    reject_rate: float
    mismatch_rate: float
    severity: Severity
    sufficient_samples: bool
    reasons: tuple[str,...]

@dataclass(frozen=True)
class AlertPolicy:
    policy_id: str
    metric_name: str
    warning_threshold: float
    critical_threshold: float
    comparison: str="HIGH"
    consecutive_breaches: int=2
    consecutive_recoveries: int=2
    cooldown_ms: int=60000
    reminder_ms: int=300000
    def __post_init__(self):
        if self.comparison not in {"HIGH","LOW","ABS_HIGH"}: raise ValueError("invalid comparison")
        if min(self.consecutive_breaches,self.consecutive_recoveries)<1 or min(self.cooldown_ms,self.reminder_ms)<0:
            raise ValueError("invalid alert policy")

@dataclass(frozen=True)
class AlertEvent:
    alert_id: str
    policy_id: str
    metric_name: str
    state: AlertState
    severity: Severity
    value: float
    threshold: float
    known_time_ms: int
    occurrence: int
    correlation_id: str
    message: str

@dataclass(frozen=True)
class HealthSnapshot:
    snapshot_id: str
    known_time_ms: int
    state: HealthState
    active_alert_count: int
    critical_alert_count: int
    dropped_telemetry_count: int
    duplicate_telemetry_count: int
    schema_rejection_count: int
    reasons: tuple[str,...]

@dataclass(frozen=True)
class LifecycleRecommendation:
    recommendation_id: str
    action: LifecycleAction
    scope_id: str
    model_id: str
    generation_id: str
    known_time_ms: int
    reason_codes: tuple[str,...]
    evidence_ids: tuple[str,...]
    requires_operator_approval: bool=True
    automatic_mutation_allowed: bool=False
    def __post_init__(self):
        if not self.requires_operator_approval or self.automatic_mutation_allowed:
            raise ValueError("Phase 19 recommendations cannot mutate runtime automatically")

@dataclass(frozen=True)
class DashboardPanel:
    panel_id: str
    title: str
    metric_names: tuple[str,...]
    visualization: str
    refresh_ms: int

@dataclass(frozen=True)
class DashboardSpec:
    dashboard_id: str
    version: str
    panels: tuple[DashboardPanel,...]
    generated_time_ms: int

@dataclass(frozen=True)
class MonitoringRunManifest:
    run_id: str
    generation_id: str
    strategy_id: str
    model_id: str
    telemetry_manifest_id: str
    dashboard_id: str
    started_time_ms: int
    ring_capacity: int
    manifest_id: str=""
    def __post_init__(self):
        if self.ring_capacity<1: raise ValueError("ring capacity must be positive")
        if not self.manifest_id: object.__setattr__(self,"manifest_id",canonical_hash(self))

@dataclass(frozen=True)
class MonitoringReport:
    report_id: str
    manifest_id: str
    generated_time_ms: int
    health: HealthSnapshot
    latency: tuple[LatencyHistogramSnapshot,...]
    drift: tuple[DriftResult,...]
    execution_drift: tuple[ExecutionDriftResult,...]
    alerts: tuple[AlertEvent,...]
    recommendation: LifecycleRecommendation
    telemetry_count: int
    report_hash: str=""
    def __post_init__(self):
        if not self.report_hash: object.__setattr__(self,"report_hash",canonical_hash(self))
