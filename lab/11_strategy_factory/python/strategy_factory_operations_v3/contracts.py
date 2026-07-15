from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple

from .canonical import canonical_sha256, validate_sha256
from .enums import (
    ChangeClass,
    ControlDecision,
    DeploymentStage,
    EvidenceState,
    GateName,
    IncidentSeverity,
    IncidentState,
    RampVerdict,
)
from .errors import OperationsError


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise OperationsError(code, message)


def _nonempty(value: str, field: str) -> None:
    _require(bool(value.strip()), field, f"{field} is required")


def _hash(value: str, field: str) -> None:
    validate_sha256(value, field)


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    evidence_hash: str
    schema_version: str
    path: str
    produced_at_ms: int

    def __post_init__(self) -> None:
        _nonempty(self.evidence_id, "evidence_id")
        _hash(self.evidence_hash, "evidence_hash")
        _require(self.produced_at_ms >= 0, "produced_at", "produced_at_ms cannot be negative")
        parts = self.path.replace("\\", "/").split("/")
        _require(".." not in parts and not self.path.startswith(("/", "\\")), "unsafe_path", "evidence path must be repository relative")


@dataclass(frozen=True)
class DeploymentTarget:
    target_id: str
    environment_hash: str
    broker_server_hash: str
    account_hashes: Tuple[str, ...]
    allowed_symbols: Tuple[str, ...]
    terminal_instance_ids: Tuple[str, ...]
    timezone: str
    captured_at_ms: int

    def __post_init__(self) -> None:
        _nonempty(self.target_id, "target_id")
        for field_name in ("environment_hash", "broker_server_hash"):
            _hash(getattr(self, field_name), field_name)
        for index, value in enumerate(self.account_hashes):
            _hash(value, f"account_hashes[{index}]")
        _require(len(self.account_hashes) == len(set(self.account_hashes)), "duplicate_account", "account hashes must be unique")
        _require(len(self.allowed_symbols) == len(set(self.allowed_symbols)), "duplicate_symbol", "symbols must be unique")
        _require(len(self.terminal_instance_ids) == len(set(self.terminal_instance_ids)), "duplicate_terminal", "terminal instance IDs must be unique")
        _require(self.captured_at_ms >= 0, "target_time", "captured_at_ms cannot be negative")

    @property
    def target_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RiskEnvelope:
    envelope_id: str
    max_total_risk_units: float
    max_open_risk_units: float
    max_order_risk_units: float
    max_daily_loss_units: float
    max_weekly_loss_units: float
    max_positions: int
    max_orders_per_minute: int
    max_symbol_risk_units: Mapping[str, float]
    max_context_risk_units: Mapping[str, float]

    def __post_init__(self) -> None:
        _nonempty(self.envelope_id, "envelope_id")
        numeric = (
            self.max_total_risk_units,
            self.max_open_risk_units,
            self.max_order_risk_units,
            self.max_daily_loss_units,
            self.max_weekly_loss_units,
        )
        _require(min(numeric) >= 0, "negative_risk", "risk and loss limits cannot be negative")
        _require(self.max_open_risk_units <= self.max_total_risk_units, "open_risk", "open risk cannot exceed total risk")
        _require(self.max_order_risk_units <= self.max_open_risk_units, "order_risk", "single-order risk cannot exceed open risk")
        _require(self.max_positions >= 0 and self.max_orders_per_minute >= 0, "count_limit", "count limits cannot be negative")
        _require(all(value >= 0 for value in self.max_symbol_risk_units.values()), "symbol_risk", "symbol limits cannot be negative")
        _require(all(value >= 0 for value in self.max_context_risk_units.values()), "context_risk", "context limits cannot be negative")

    @property
    def envelope_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class OperationsPolicy:
    policy_id: str
    schema_version: str
    heartbeat_timeout_ms: int
    max_feature_age_ms: int
    max_p99_latency_ms: float
    max_queue_depth: int
    max_memory_growth_mb: float
    max_reject_rate: float
    max_drift_score: float
    max_reconciliation_age_ms: int
    max_lease_minutes: int
    required_flat_before_environment_change: bool
    require_distinct_operator_approver: bool
    require_manual_ramp_approval: bool
    minimum_stage_sessions: Mapping[str, int]
    minimum_stage_events: Mapping[str, int]
    minimum_stage_days: Mapping[str, int]

    def __post_init__(self) -> None:
        _nonempty(self.policy_id, "policy_id")
        _require(self.heartbeat_timeout_ms > 0 and self.max_feature_age_ms > 0, "freshness_policy", "freshness limits must be positive")
        _require(self.max_p99_latency_ms > 0 and self.max_queue_depth >= 0 and self.max_memory_growth_mb >= 0, "resource_policy", "resource limits are invalid")
        _require(0 <= self.max_reject_rate <= 1 and self.max_drift_score >= 0, "rate_policy", "rate limits are invalid")
        _require(self.max_reconciliation_age_ms > 0 and self.max_lease_minutes > 0, "time_policy", "time limits must be positive")
        for mapping, name in (
            (self.minimum_stage_sessions, "minimum_stage_sessions"),
            (self.minimum_stage_events, "minimum_stage_events"),
            (self.minimum_stage_days, "minimum_stage_days"),
        ):
            _require(all(value > 0 for value in mapping.values()), name, f"{name} values must be positive")

    @property
    def policy_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class DeploymentPlan:
    plan_id: str
    schema_version: str
    source_commit: str
    release_manifest_hash: str
    qualification_report_hash: str
    environment_hash: str
    target_hash: str
    generation_hash: str
    rollback_generation_hash: str
    stage: DeploymentStage
    authority_order: bool
    authority_broker: bool
    max_risk_units: float
    risk_envelope_hash: str
    operator_id: str
    approver_id: str
    approved_at_ms: int
    starts_at_ms: int
    expires_at_ms: int
    limitations: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in (
            "release_manifest_hash",
            "qualification_report_hash",
            "environment_hash",
            "target_hash",
            "generation_hash",
            "rollback_generation_hash",
            "risk_envelope_hash",
        ):
            _hash(getattr(self, field_name), field_name)
        _nonempty(self.operator_id, "operator_id")
        _nonempty(self.approver_id, "approver_id")
        _require(self.approved_at_ms <= self.starts_at_ms < self.expires_at_ms, "plan_time", "deployment plan timeline is invalid")
        _require(self.max_risk_units >= 0, "plan_risk", "max_risk_units cannot be negative")
        if self.stage in (DeploymentStage.PAPER, DeploymentStage.SHADOW, DeploymentStage.FROZEN):
            _require(not self.authority_order and not self.authority_broker and self.max_risk_units == 0, "no_send_stage", "non-live stages cannot carry execution authority")
        if self.authority_order or self.authority_broker:
            _require(self.stage in (DeploymentStage.MICRO_LIVE, DeploymentStage.LIMITED_LIVE, DeploymentStage.PRODUCTION), "authority_stage", "authority requires a live stage")

    @property
    def plan_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RuntimeLease:
    lease_id: str
    schema_version: str
    plan_hash: str
    environment_hash: str
    generation_hash: str
    stage: DeploymentStage
    account_hashes: Tuple[str, ...]
    allowed_symbols: Tuple[str, ...]
    max_risk_units: float
    issued_by: str
    approved_by: str
    issued_at_ms: int
    expires_at_ms: int
    revoked_at_ms: int = 0
    revocation_reason: str = ""

    def __post_init__(self) -> None:
        for field_name in ("plan_hash", "environment_hash", "generation_hash"):
            _hash(getattr(self, field_name), field_name)
        _require(self.issued_at_ms < self.expires_at_ms, "lease_time", "lease must expire after issue")
        _require(self.revoked_at_ms == 0 or self.issued_at_ms <= self.revoked_at_ms <= self.expires_at_ms, "revocation_time", "revocation time is invalid")
        _require(self.max_risk_units >= 0, "lease_risk", "lease risk cannot be negative")

    @property
    def lease_hash(self) -> str:
        return canonical_sha256(self)

    def active_at(self, now_ms: int) -> bool:
        return self.issued_at_ms <= now_ms < self.expires_at_ms and self.revoked_at_ms == 0


@dataclass(frozen=True)
class TelemetrySnapshot:
    snapshot_id: str
    environment_hash: str
    generation_hash: str
    captured_at_ms: int
    last_heartbeat_ms: int
    max_feature_age_ms: int
    p99_latency_ms: float
    queue_depth: int
    memory_growth_mb: float
    broker_connected: bool
    history_synchronized: bool
    open_positions: int
    open_risk_units: float
    reserved_risk_units: float
    daily_pnl_units: float
    weekly_pnl_units: float
    reject_rate: float
    drift_score: float
    duplicate_action_count: int
    stale_action_count: int
    unreserved_action_count: int
    critical_error_count: int

    def __post_init__(self) -> None:
        for field_name in ("environment_hash", "generation_hash"):
            _hash(getattr(self, field_name), field_name)
        _require(self.last_heartbeat_ms <= self.captured_at_ms, "heartbeat_time", "heartbeat cannot be in the future")
        counts = (self.max_feature_age_ms, self.queue_depth, self.open_positions, self.duplicate_action_count, self.stale_action_count, self.unreserved_action_count, self.critical_error_count)
        _require(min(counts) >= 0, "telemetry_count", "telemetry counts cannot be negative")
        _require(min(self.p99_latency_ms, self.memory_growth_mb, self.open_risk_units, self.reserved_risk_units, self.reject_rate, self.drift_score) >= 0, "telemetry_metric", "telemetry metrics cannot be negative")
        _require(self.reject_rate <= 1, "reject_rate", "reject_rate cannot exceed one")

    @property
    def snapshot_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class HealthAssessment:
    assessment_id: str
    status: EvidenceState
    decision: ControlDecision
    evaluated_at_ms: int
    reason_codes: Tuple[str, ...]
    telemetry_hash: str
    max_allowed_risk_units: float

    def __post_init__(self) -> None:
        _hash(self.telemetry_hash, "telemetry_hash")
        _require(self.max_allowed_risk_units >= 0, "health_risk", "health risk cannot be negative")
        _require(not (self.status is EvidenceState.FAIL and self.max_allowed_risk_units > 0), "failed_health_risk", "failed health cannot authorize risk")


@dataclass(frozen=True)
class ReconciliationReport:
    report_id: str
    environment_hash: str
    generation_hash: str
    expected_reservation_hash: str
    observed_reservation_hash: str
    expected_order_hash: str
    observed_order_hash: str
    expected_position_hash: str
    observed_position_hash: str
    orphan_order_count: int
    orphan_position_count: int
    missing_order_count: int
    missing_position_count: int
    duplicate_intent_count: int
    unreserved_position_count: int
    reconciled_at_ms: int

    def __post_init__(self) -> None:
        for field_name in (
            "environment_hash",
            "generation_hash",
            "expected_reservation_hash",
            "observed_reservation_hash",
            "expected_order_hash",
            "observed_order_hash",
            "expected_position_hash",
            "observed_position_hash",
        ):
            _hash(getattr(self, field_name), field_name)
        counts = (self.orphan_order_count, self.orphan_position_count, self.missing_order_count, self.missing_position_count, self.duplicate_intent_count, self.unreserved_position_count)
        _require(min(counts) >= 0, "reconciliation_count", "reconciliation counts cannot be negative")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)

    @property
    def exact(self) -> bool:
        return (
            self.expected_reservation_hash == self.observed_reservation_hash
            and self.expected_order_hash == self.observed_order_hash
            and self.expected_position_hash == self.observed_position_hash
            and self.orphan_order_count == 0
            and self.orphan_position_count == 0
            and self.missing_order_count == 0
            and self.missing_position_count == 0
            and self.duplicate_intent_count == 0
            and self.unreserved_position_count == 0
        )


@dataclass(frozen=True)
class OperationsIncident:
    incident_id: str
    severity: IncidentSeverity
    state: IncidentState
    detected_at_ms: int
    contained_at_ms: int
    resolved_at_ms: int
    closed_at_ms: int
    environment_hash: str
    generation_hash: str
    reason_code: str
    evidence_hashes: Tuple[str, ...]
    owner_id: str
    closed_by: str = ""

    def __post_init__(self) -> None:
        for field_name in ("environment_hash", "generation_hash"):
            _hash(getattr(self, field_name), field_name)
        for index, value in enumerate(self.evidence_hashes):
            _hash(value, f"evidence_hashes[{index}]")
        _require(self.detected_at_ms >= 0, "incident_time", "detected_at_ms cannot be negative")
        times = [value for value in (self.contained_at_ms, self.resolved_at_ms, self.closed_at_ms) if value > 0]
        _require(times == sorted(times), "incident_timeline", "incident timestamps must be monotonic")
        if self.state is IncidentState.CLOSED:
            _require(self.closed_at_ms > 0 and bool(self.closed_by), "incident_close", "closed incident requires close time and actor")

    @property
    def incident_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class CycleAuthorization:
    authorization_id: str
    decision: ControlDecision
    stage: DeploymentStage
    evaluated_at_ms: int
    plan_hash: str
    lease_hash: str
    health_hash: str
    reconciliation_hash: str
    authority_order: bool
    max_incremental_risk_units: float
    reason_codes: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("plan_hash", "lease_hash", "health_hash", "reconciliation_hash"):
            _hash(getattr(self, field_name), field_name)
        _require(self.max_incremental_risk_units >= 0, "authorization_risk", "incremental risk cannot be negative")
        _require(self.authority_order or self.max_incremental_risk_units == 0, "no_authority_risk", "risk requires order authority")
        _require(self.decision is ControlDecision.ALLOW_BOUNDED or not self.authority_order, "decision_authority", "only ALLOW_BOUNDED may grant order authority")

    @property
    def authorization_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class ProspectiveWindow:
    window_id: str
    stage: DeploymentStage
    environment_hash: str
    generation_hash: str
    started_at_ms: int
    ended_at_ms: int
    sessions: int
    events: int
    calendar_days: int
    reconciliations: int
    reconciliation_failures: int
    high_incidents: int
    critical_incidents: int
    policy_breaches: int
    max_drawdown_units: float
    reject_rate: float
    p99_latency_ms: float
    drift_score: float
    evidence_hashes: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("environment_hash", "generation_hash"):
            _hash(getattr(self, field_name), field_name)
        for index, value in enumerate(self.evidence_hashes):
            _hash(value, f"evidence_hashes[{index}]")
        _require(self.started_at_ms < self.ended_at_ms, "window_time", "window must have positive duration")
        counts = (self.sessions, self.events, self.calendar_days, self.reconciliations, self.reconciliation_failures, self.high_incidents, self.critical_incidents, self.policy_breaches)
        _require(min(counts) >= 0, "window_counts", "window counts cannot be negative")
        _require(min(self.max_drawdown_units, self.reject_rate, self.p99_latency_ms, self.drift_score) >= 0, "window_metrics", "window metrics cannot be negative")

    @property
    def window_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RampDecision:
    decision_id: str
    current_stage: DeploymentStage
    requested_stage: DeploymentStage
    verdict: RampVerdict
    evaluated_at_ms: int
    window_hash: str
    reason_codes: Tuple[str, ...]
    maximum_risk_units: float
    requires_human_approval: bool

    def __post_init__(self) -> None:
        _hash(self.window_hash, "window_hash")
        _require(self.maximum_risk_units >= 0, "ramp_risk", "ramp risk cannot be negative")
        _require(self.verdict is not RampVerdict.ELIGIBLE_FOR_HUMAN_APPROVAL or self.requires_human_approval, "automatic_ramp", "eligible ramp must require human approval")


@dataclass(frozen=True)
class ChangeRequest:
    change_id: str
    requested_by: str
    requested_at_ms: int
    active_plan_hash: str
    field_changes: Mapping[str, Tuple[str, str]]
    emergency: bool
    evidence_hashes: Tuple[str, ...]

    def __post_init__(self) -> None:
        _hash(self.active_plan_hash, "active_plan_hash")
        for index, value in enumerate(self.evidence_hashes):
            _hash(value, f"evidence_hashes[{index}]")
        _require(bool(self.field_changes), "empty_change", "field_changes cannot be empty")
        _require(all(old != new for old, new in self.field_changes.values()), "no_op_change", "change values must differ")

    @property
    def request_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class ChangeDecision:
    decision_id: str
    classification: ChangeClass
    approved: bool
    requalification_required: bool
    flat_required: bool
    evaluated_at_ms: int
    request_hash: str
    reason_codes: Tuple[str, ...]

    def __post_init__(self) -> None:
        _hash(self.request_hash, "request_hash")
        _require(not (self.classification is ChangeClass.FORBIDDEN_HOT_CHANGE and self.approved), "forbidden_change", "forbidden hot change cannot be approved")


@dataclass(frozen=True)
class EndOfDayReport:
    report_id: str
    environment_hash: str
    generation_hash: str
    trading_day: str
    reservation_hash: str
    order_hash: str
    position_hash: str
    ledger_hash: str
    all_events_persisted: bool
    all_intents_terminal: bool
    exact_reconciliation: bool
    unresolved_high_incidents: int
    unresolved_critical_incidents: int
    daily_loss_units: float
    evidence_hashes: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("environment_hash", "generation_hash", "reservation_hash", "order_hash", "position_hash", "ledger_hash"):
            _hash(getattr(self, field_name), field_name)
        for index, value in enumerate(self.evidence_hashes):
            _hash(value, f"evidence_hashes[{index}]")
        _require(self.unresolved_high_incidents >= 0 and self.unresolved_critical_incidents >= 0, "eod_incident_count", "incident counts cannot be negative")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RollbackExecution:
    rollback_id: str
    plan_hash: str
    from_generation_hash: str
    to_generation_hash: str
    initiated_at_ms: int
    completed_at_ms: int
    max_allowed_seconds: float
    orders_blocked: bool
    positions_reconciled: bool
    reservations_reconciled: bool
    target_generation_active: bool
    evidence_hashes: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("plan_hash", "from_generation_hash", "to_generation_hash"):
            _hash(getattr(self, field_name), field_name)
        for index, value in enumerate(self.evidence_hashes):
            _hash(value, f"evidence_hashes[{index}]")
        _require(self.initiated_at_ms <= self.completed_at_ms, "rollback_time", "rollback timeline is invalid")
        _require(self.max_allowed_seconds > 0, "rollback_budget", "rollback budget must be positive")

    @property
    def duration_seconds(self) -> float:
        return (self.completed_at_ms - self.initiated_at_ms) / 1000.0

    @property
    def execution_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RetirementManifest:
    retirement_id: str
    release_manifest_hash: str
    plan_hash: str
    environment_hash: str
    generation_hash: str
    retired_at_ms: int
    retired_by: str
    approved_by: str
    positions_flat: bool
    reservations_zero: bool
    leases_revoked: bool
    evidence_archive_hash: str
    retention_until_ms: int
    reason: str

    def __post_init__(self) -> None:
        for field_name in ("release_manifest_hash", "plan_hash", "environment_hash", "generation_hash", "evidence_archive_hash"):
            _hash(getattr(self, field_name), field_name)
        _require(self.retention_until_ms > self.retired_at_ms, "retention_time", "retention must extend beyond retirement")
        _require(self.retired_by != self.approved_by, "retirement_sod", "retirement actor and approver must be distinct")
        _require(self.positions_flat and self.reservations_zero and self.leases_revoked, "retirement_safety", "retirement requires flat, zero reservation and revoked leases")

    @property
    def retirement_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class GateResult:
    gate: GateName
    status: EvidenceState
    evaluated_at_ms: int
    reason_codes: Tuple[str, ...]
    evidence_hashes: Tuple[str, ...]

    def __post_init__(self) -> None:
        for index, value in enumerate(self.evidence_hashes):
            _hash(value, f"evidence_hashes[{index}]")


@dataclass(frozen=True)
class OperationsEvidenceBundle:
    bundle_id: str
    schema_version: str
    source_commit: str
    release_manifest_hash: str
    deployment_plan_hash: str
    policy_hash: str
    environment_hash: str
    generated_at_ms: int
    gates: Tuple[GateResult, ...]
    evidence_refs: Tuple[EvidenceRef, ...]
    activation_allowed: bool
    maximum_stage: DeploymentStage
    maximum_risk_units: float
    blocking_reasons: Tuple[str, ...]
    limitations: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("release_manifest_hash", "deployment_plan_hash", "policy_hash", "environment_hash"):
            _hash(getattr(self, field_name), field_name)
        _require(self.maximum_risk_units >= 0, "bundle_risk", "maximum risk cannot be negative")
        _require(self.activation_allowed or self.maximum_risk_units == 0, "blocked_bundle_risk", "blocked bundle cannot authorize risk")
        _require(not self.activation_allowed or not self.blocking_reasons, "bundle_blockers", "active bundle cannot contain blockers")

    @property
    def bundle_hash(self) -> str:
        return canonical_sha256(self)
