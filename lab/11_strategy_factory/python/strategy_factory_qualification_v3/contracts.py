from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple

from .canonical import canonical_sha256, validate_sha256
from .enums import EvidenceStatus, GateName, IncidentSeverity, QualificationDecision, ReleaseStage
from .errors import QualificationError


def _require(value: bool, code: str, message: str) -> None:
    if not value:
        raise QualificationError(code, message)


@dataclass(frozen=True)
class ArtifactRef:
    artifact_id: str
    schema_version: str
    artifact_hash: str
    path: str
    produced_at_ms: int

    def __post_init__(self) -> None:
        _require(bool(self.artifact_id), "artifact_id", "artifact_id is required")
        validate_sha256(self.artifact_hash, "artifact_hash")
        _require(self.produced_at_ms >= 0, "produced_at", "produced_at_ms cannot be negative")
        _require(".." not in self.path.replace("\\", "/").split("/"), "unsafe_path", "parent traversal is forbidden")


@dataclass(frozen=True)
class EnvironmentFingerprint:
    environment_id: str
    os_name: str
    os_version: str
    terminal_build: str
    metaeditor_build: str
    broker_server: str
    account_mode: str
    timezone: str
    symbol_spec_hash: str
    dependency_lock_hash: str
    captured_at_ms: int

    def __post_init__(self) -> None:
        validate_sha256(self.symbol_spec_hash, "symbol_spec_hash")
        validate_sha256(self.dependency_lock_hash, "dependency_lock_hash")
        _require(self.captured_at_ms >= 0, "captured_at", "captured_at_ms cannot be negative")

    @property
    def fingerprint_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class CompileTargetResult:
    target: str
    source_hash: str
    compiler_build: str
    exit_code: int
    errors: int
    warnings: int
    log_hash: str
    output_hash: str
    compiled_at_ms: int

    def __post_init__(self) -> None:
        for field_name in ("source_hash", "log_hash", "output_hash"):
            validate_sha256(getattr(self, field_name), field_name)
        _require(self.errors >= 0 and self.warnings >= 0, "compile_counts", "compile counts cannot be negative")

    @property
    def passed(self) -> bool:
        return self.exit_code == 0 and self.errors == 0


@dataclass(frozen=True)
class CompileEvidence:
    evidence_id: str
    schema_version: str
    environment_hash: str
    targets: Tuple[CompileTargetResult, ...]
    required_targets: Tuple[str, ...]
    warnings_allowed: int
    captured_at_ms: int

    def __post_init__(self) -> None:
        validate_sha256(self.environment_hash, "environment_hash")
        _require(len(set(x.target for x in self.targets)) == len(self.targets), "duplicate_target", "compile targets must be unique")
        _require(self.warnings_allowed >= 0, "warnings_allowed", "warnings_allowed cannot be negative")

    @property
    def evidence_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class DifferentialCase:
    case_id: str
    expected_hash: str
    observed_hash: str
    max_abs_error: float
    max_rel_error: float
    allowed_abs_error: float
    allowed_rel_error: float
    event_count: int
    mismatch_count: int

    def __post_init__(self) -> None:
        validate_sha256(self.expected_hash, "expected_hash")
        validate_sha256(self.observed_hash, "observed_hash")
        _require(self.event_count > 0, "event_count", "event_count must be positive")
        _require(0 <= self.mismatch_count <= self.event_count, "mismatch_count", "mismatch_count is outside event_count")
        _require(min(self.max_abs_error, self.max_rel_error, self.allowed_abs_error, self.allowed_rel_error) >= 0, "tolerance", "errors and tolerances cannot be negative")

    @property
    def passed(self) -> bool:
        hash_equal = self.expected_hash == self.observed_hash
        numeric_equal = self.max_abs_error <= self.allowed_abs_error and self.max_rel_error <= self.allowed_rel_error
        return self.mismatch_count == 0 and (hash_equal or numeric_equal)


@dataclass(frozen=True)
class DifferentialReport:
    report_id: str
    schema_version: str
    source_mode: str
    target_mode: str
    causal_cut_ms: int
    cases: Tuple[DifferentialCase, ...]
    missing_case_ids: Tuple[str, ...] = ()
    reordered_event_count: int = 0
    future_read_count: int = 0

    def __post_init__(self) -> None:
        _require(bool(self.cases), "empty_differential", "at least one differential case is required")
        _require(self.reordered_event_count >= 0 and self.future_read_count >= 0, "differential_counts", "counts cannot be negative")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class SoakReport:
    report_id: str
    schema_version: str
    environment_hash: str
    duration_minutes: int
    processed_events: int
    emitted_actions: int
    critical_errors: int
    unhandled_exceptions: int
    reconciliation_mismatches: int
    duplicate_actions: int
    stale_actions: int
    max_memory_growth_mb: float
    p99_latency_ms: float
    max_queue_depth: int
    start_ms: int
    end_ms: int

    def __post_init__(self) -> None:
        validate_sha256(self.environment_hash, "environment_hash")
        _require(self.duration_minutes >= 0 and self.processed_events >= 0, "soak_counts", "soak counts cannot be negative")
        _require(self.end_ms >= self.start_ms, "soak_time", "end_ms must not precede start_ms")
        _require(min(self.max_memory_growth_mb, self.p99_latency_ms) >= 0, "soak_metrics", "soak metrics cannot be negative")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class ChaosScenarioResult:
    scenario_id: str
    injected_at_ms: int
    detected: bool
    fail_closed: bool
    recovered: bool
    emitted_unreserved_action: bool
    duplicate_action_count: int
    recovery_seconds: float
    evidence_hash: str

    def __post_init__(self) -> None:
        validate_sha256(self.evidence_hash, "evidence_hash")
        _require(self.recovery_seconds >= 0 and self.duplicate_action_count >= 0, "chaos_metrics", "chaos metrics cannot be negative")

    @property
    def passed(self) -> bool:
        return self.detected and self.fail_closed and self.recovered and not self.emitted_unreserved_action and self.duplicate_action_count == 0


@dataclass(frozen=True)
class ChaosReport:
    report_id: str
    schema_version: str
    environment_hash: str
    scenarios: Tuple[ChaosScenarioResult, ...]
    required_scenario_ids: Tuple[str, ...]

    def __post_init__(self) -> None:
        validate_sha256(self.environment_hash, "environment_hash")
        _require(len(set(x.scenario_id for x in self.scenarios)) == len(self.scenarios), "duplicate_scenario", "chaos scenario IDs must be unique")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RecoveryReport:
    report_id: str
    schema_version: str
    environment_hash: str
    checkpoint_hash: str
    reservation_ledger_hash: str
    observed_ledger_hash: str
    restart_count: int
    replayed_event_count: int
    duplicate_action_count: int
    unreserved_action_count: int
    state_divergence_count: int
    rto_seconds: float
    rpo_seconds: float
    kill_switch_verified: bool
    rollback_verified: bool

    def __post_init__(self) -> None:
        for field_name in ("environment_hash", "checkpoint_hash", "reservation_ledger_hash", "observed_ledger_hash"):
            validate_sha256(getattr(self, field_name), field_name)
        _require(min(self.restart_count, self.replayed_event_count, self.duplicate_action_count, self.unreserved_action_count, self.state_divergence_count) >= 0, "recovery_counts", "recovery counts cannot be negative")
        _require(min(self.rto_seconds, self.rpo_seconds) >= 0, "recovery_time", "RTO and RPO cannot be negative")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class SecurityControlResult:
    control_id: str
    status: EvidenceStatus
    evidence_hash: str
    details: str

    def __post_init__(self) -> None:
        validate_sha256(self.evidence_hash, "evidence_hash")


@dataclass(frozen=True)
class SecurityReport:
    report_id: str
    schema_version: str
    controls: Tuple[SecurityControlResult, ...]
    required_control_ids: Tuple[str, ...]
    plaintext_secret_findings: int
    unsigned_artifacts: int
    hash_mismatches: int
    backup_restore_verified: bool
    retention_policy_verified: bool

    def __post_init__(self) -> None:
        _require(min(self.plaintext_secret_findings, self.unsigned_artifacts, self.hash_mismatches) >= 0, "security_counts", "security counts cannot be negative")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class ProspectiveStageEvidence:
    evidence_id: str
    schema_version: str
    stage: ReleaseStage
    environment_hash: str
    start_ms: int
    end_ms: int
    sessions: int
    decision_events: int
    order_intents: int
    broker_rejections: int
    reconciliation_mismatches: int
    duplicate_actions: int
    critical_incidents: int
    max_realized_risk_units: float
    max_allowed_risk_units: float
    human_approval_id: str = ""

    def __post_init__(self) -> None:
        validate_sha256(self.environment_hash, "environment_hash")
        _require(self.end_ms >= self.start_ms, "stage_time", "end_ms must not precede start_ms")
        _require(min(self.sessions, self.decision_events, self.order_intents, self.broker_rejections, self.reconciliation_mismatches, self.duplicate_actions, self.critical_incidents) >= 0, "stage_counts", "stage counts cannot be negative")
        _require(0 <= self.max_realized_risk_units <= self.max_allowed_risk_units, "stage_risk", "realized risk exceeds allowed risk")

    @property
    def evidence_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class RollbackDrillReport:
    report_id: str
    schema_version: str
    from_generation_hash: str
    to_generation_hash: str
    initiated_at_ms: int
    completed_at_ms: int
    max_allowed_seconds: float
    orders_blocked_during_transition: bool
    state_reconciled: bool
    old_generation_restored: bool
    evidence_hash: str

    def __post_init__(self) -> None:
        for field_name in ("from_generation_hash", "to_generation_hash", "evidence_hash"):
            validate_sha256(getattr(self, field_name), field_name)
        _require(self.completed_at_ms >= self.initiated_at_ms, "rollback_time", "rollback completion precedes initiation")
        _require(self.max_allowed_seconds > 0, "rollback_budget", "rollback budget must be positive")

    @property
    def duration_seconds(self) -> float:
        return (self.completed_at_ms - self.initiated_at_ms) / 1000.0


@dataclass(frozen=True)
class IncidentRecord:
    incident_id: str
    severity: IncidentSeverity
    detected_at_ms: int
    contained_at_ms: int
    closed_at_ms: int
    root_cause: str
    corrective_action: str
    evidence_hash: str

    def __post_init__(self) -> None:
        validate_sha256(self.evidence_hash, "evidence_hash")
        _require(self.detected_at_ms <= self.contained_at_ms <= self.closed_at_ms, "incident_time", "incident timeline is invalid")


@dataclass(frozen=True)
class QualificationPolicy:
    policy_id: str
    schema_version: str
    required_compile_targets: Tuple[str, ...]
    max_compile_warnings: int
    required_differential_cases: Tuple[str, ...]
    min_soak_minutes: int
    min_soak_events: int
    max_memory_growth_mb: float
    max_p99_latency_ms: float
    required_chaos_scenarios: Tuple[str, ...]
    max_recovery_seconds: float
    max_rpo_seconds: float
    required_security_controls: Tuple[str, ...]
    min_paper_sessions: int
    min_paper_events: int
    min_shadow_sessions: int
    min_shadow_events: int
    min_micro_live_sessions: int
    min_micro_live_events: int
    min_limited_live_sessions: int
    min_limited_live_events: int
    min_production_sessions: int
    min_production_events: int
    max_broker_reject_rate: float
    max_micro_live_risk_units: float
    max_limited_live_risk_units: float
    max_production_risk_units: float
    require_human_approval: bool = True

    def __post_init__(self) -> None:
        _require(self.max_compile_warnings >= 0, "compile_warning_policy", "max warnings cannot be negative")
        _require(self.min_soak_minutes > 0 and self.min_soak_events > 0, "soak_policy", "soak minimums must be positive")
        stage_minimums = (
            self.min_paper_sessions, self.min_paper_events, self.min_shadow_sessions, self.min_shadow_events,
            self.min_micro_live_sessions, self.min_micro_live_events, self.min_limited_live_sessions,
            self.min_limited_live_events, self.min_production_sessions, self.min_production_events,
        )
        _require(min(stage_minimums) > 0, "stage_policy", "prospective stage minimums must be positive")
        _require(0 <= self.max_broker_reject_rate <= 1, "reject_rate", "reject rate must be between zero and one")
        _require(0 < self.max_micro_live_risk_units <= self.max_limited_live_risk_units <= self.max_production_risk_units, "live_risk_tiers", "live risk tiers must be positive and monotonic")

    @property
    def policy_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class GateResult:
    gate: GateName
    status: EvidenceStatus
    reason_codes: Tuple[str, ...]
    evidence_hashes: Tuple[str, ...]
    evaluated_at_ms: int

    def __post_init__(self) -> None:
        for index, value in enumerate(self.evidence_hashes):
            validate_sha256(value, f"evidence_hashes[{index}]")


@dataclass(frozen=True)
class QualificationReport:
    report_id: str
    schema_version: str
    policy_hash: str
    environment_hash: str
    source_commit: str
    evaluated_at_ms: int
    gates: Tuple[GateResult, ...]
    decision: QualificationDecision
    activation_allowed: bool
    maximum_stage: ReleaseStage
    max_authorized_risk_units: float
    blocking_reasons: Tuple[str, ...]
    limitations: Tuple[str, ...]

    def __post_init__(self) -> None:
        validate_sha256(self.policy_hash, "policy_hash")
        validate_sha256(self.environment_hash, "environment_hash")
        _require(self.max_authorized_risk_units >= 0, "qualification_risk", "authorized risk cannot be negative")
        _require(not self.activation_allowed or self.decision is QualificationDecision.QUALIFIED, "unsafe_activation", "activation requires qualified decision")
        _require(not self.activation_allowed or not self.blocking_reasons, "unsafe_blockers", "activation cannot coexist with blockers")
        _require(self.activation_allowed or self.max_authorized_risk_units == 0.0, "inactive_risk", "inactive qualification cannot authorize risk")

    @property
    def report_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True)
class ReleaseManifest:
    manifest_id: str
    schema_version: str
    release_version: str
    source_commit: str
    qualification_report_hash: str
    environment_hash: str
    generation_hash: str
    stage: ReleaseStage
    authority_order: bool
    authority_broker: bool
    max_risk_units: float
    approved_by: str
    approved_at_ms: int
    artifact_refs: Tuple[ArtifactRef, ...]
    rollback_generation_hash: str
    expires_at_ms: int

    def __post_init__(self) -> None:
        for field_name in ("qualification_report_hash", "environment_hash", "generation_hash", "rollback_generation_hash"):
            validate_sha256(getattr(self, field_name), field_name)
        _require(self.max_risk_units >= 0, "release_risk", "max risk cannot be negative")
        _require(self.expires_at_ms > self.approved_at_ms, "release_expiry", "release must expire after approval")
        _require(bool(self.approved_by), "release_approval", "approved_by is required")
        if self.stage in (ReleaseStage.PAPER, ReleaseStage.SHADOW):
            _require(not self.authority_order and not self.authority_broker, "shadow_authority", "paper/shadow stages cannot have order authority")
        if self.authority_order or self.authority_broker:
            _require(self.stage in (ReleaseStage.MICRO_LIVE, ReleaseStage.LIMITED_LIVE, ReleaseStage.PRODUCTION), "authority_stage", "order authority requires a live stage")

    @property
    def manifest_hash(self) -> str:
        return canonical_sha256(self)
