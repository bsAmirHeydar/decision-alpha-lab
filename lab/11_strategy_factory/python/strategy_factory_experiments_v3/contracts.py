"""Immutable contracts for UCE-I11 experiment orchestration.

The contracts deliberately separate declaration from execution.  The compiler
consumes only immutable declarations and emits immutable DAG/identity artifacts.
The scheduler may change node status, but it cannot reinterpret the compiled
semantics.  Every behavior-changing field participates in canonical identity.
"""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence

from .canonical import canonical_sha256, stable_id
from .enums import (
    AdmissionDecision,
    BudgetDecision,
    CacheStatus,
    FailureDisposition,
    LedgerAction,
    NodeKind,
    NodeStatus,
    ObjectiveDirection,
    ParameterKind,
    ResourceDevice,
    SchedulerEventKind,
    SearchKind,
)
from .errors import ExperimentError

_SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]*$")


def _text(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ExperimentError("required_text_missing", f"{name} is required", {"field": name})


def _identifier(value: str, name: str) -> None:
    _text(value, name)
    if not _ID_RE.match(value):
        raise ExperimentError("invalid_identifier", f"{name} contains unsupported characters", {"value": value})


def _semver(value: str, name: str) -> None:
    _text(value, name)
    if not _SEMVER_RE.match(value):
        raise ExperimentError("invalid_semver", f"{name} must be semantic version text", {"value": value})


def _hash(value: str, name: str, *, allow_blank: bool = False) -> None:
    if allow_blank and value == "":
        return
    if not isinstance(value, str) or not _SHA256_RE.match(value):
        raise ExperimentError("invalid_sha256", f"{name} must be lowercase SHA-256", {"value": value})


def _finite(value: float, name: str) -> None:
    if not math.isfinite(float(value)):
        raise ExperimentError("non_finite_value", f"{name} must be finite", {"value": repr(value)})


def _nonnegative(value: int | float, name: str) -> None:
    _finite(float(value), name)
    if value < 0:
        raise ExperimentError("negative_value", f"{name} must be non-negative", {"value": value})


def _unique(values: Sequence[Any], name: str) -> None:
    rendered = [canonical_sha256(value) for value in values]
    if len(set(rendered)) != len(rendered):
        raise ExperimentError("duplicate_values", f"{name} must contain unique values")


@dataclass(frozen=True, slots=True)
class CandidateAdmission:
    candidate_key: str
    candidate_version: str
    family: str
    trainer_key: str
    decision: AdmissionDecision
    evidence_hash: str
    baseline: bool = False
    warnings: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    capability_flags: Mapping[str, bool] = field(default_factory=dict)
    estimated_memory_mb: int = 256
    estimated_wall_seconds: float = 60.0
    requires_gpu: bool = False

    def __post_init__(self) -> None:
        _identifier(self.candidate_key, "candidate_key")
        _semver(self.candidate_version, "candidate_version")
        _identifier(self.family, "family")
        _identifier(self.trainer_key, "trainer_key")
        _hash(self.evidence_hash, "evidence_hash")
        if self.decision is AdmissionDecision.REJECT and not self.blockers:
            raise ExperimentError("rejected_candidate_without_blocker", "rejected candidates require blockers")
        if self.decision is not AdmissionDecision.REJECT and self.blockers:
            raise ExperimentError("admitted_candidate_with_blocker", "admitted candidates cannot retain blockers")
        if self.estimated_memory_mb < 1:
            raise ExperimentError("invalid_memory_estimate", "estimated_memory_mb must be positive")
        if self.estimated_wall_seconds <= 0:
            raise ExperimentError("invalid_wall_estimate", "estimated_wall_seconds must be positive")

    @property
    def key(self) -> str:
        return f"{self.candidate_key}@{self.candidate_version}"

    @property
    def schedulable(self) -> bool:
        return self.decision in (AdmissionDecision.ACCEPT, AdmissionDecision.WARN)

    @property
    def admission_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class ParameterSpec:
    name: str
    kind: ParameterKind
    values: tuple[Any, ...] = ()
    low: float | int | None = None
    high: float | int | None = None
    step: float | int | None = None
    log_scale: bool = False
    behavior_changing: bool = True

    def __post_init__(self) -> None:
        _identifier(self.name, "parameter.name")
        if not self.behavior_changing:
            raise ExperimentError(
                "non_identity_search_parameter_forbidden",
                "all search parameters must be behavior-changing and identity-bearing",
                {"name": self.name},
            )
        if self.kind in (ParameterKind.CATEGORICAL, ParameterKind.BOOLEAN):
            if not self.values:
                raise ExperimentError("empty_parameter_values", "categorical/boolean parameters require values")
            _unique(self.values, f"parameter[{self.name}].values")
            if self.kind is ParameterKind.BOOLEAN and any(not isinstance(value, bool) for value in self.values):
                raise ExperimentError("invalid_boolean_parameter", "boolean parameter values must be booleans")
            if any(value is not None for value in (self.low, self.high, self.step)):
                raise ExperimentError("mixed_parameter_domain", "discrete parameter cannot define numeric bounds")
        else:
            if self.low is None or self.high is None:
                raise ExperimentError("missing_numeric_bounds", "numeric parameter requires low and high")
            _finite(float(self.low), f"{self.name}.low")
            _finite(float(self.high), f"{self.name}.high")
            if float(self.low) > float(self.high):
                raise ExperimentError("inverted_parameter_bounds", "parameter low exceeds high")
            if self.step is not None:
                _finite(float(self.step), f"{self.name}.step")
                if float(self.step) <= 0:
                    raise ExperimentError("invalid_parameter_step", "parameter step must be positive")
            if self.values:
                raise ExperimentError("mixed_parameter_domain", "numeric parameter cannot define explicit values")
            if self.log_scale and float(self.low) <= 0:
                raise ExperimentError("invalid_log_parameter", "log-scale parameter low must be positive")

    @property
    def spec_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class ObjectiveSpec:
    name: str
    direction: ObjectiveDirection
    weight: float = 1.0
    constraint_min: float | None = None
    constraint_max: float | None = None

    def __post_init__(self) -> None:
        _identifier(self.name, "objective.name")
        _finite(self.weight, "objective.weight")
        if self.weight <= 0:
            raise ExperimentError("invalid_objective_weight", "objective weight must be positive")
        if self.constraint_min is not None:
            _finite(self.constraint_min, "objective.constraint_min")
        if self.constraint_max is not None:
            _finite(self.constraint_max, "objective.constraint_max")
        if (
            self.constraint_min is not None
            and self.constraint_max is not None
            and self.constraint_min > self.constraint_max
        ):
            raise ExperimentError("inverted_objective_constraint", "objective minimum exceeds maximum")


@dataclass(frozen=True, slots=True)
class SearchPlan:
    search_id: str
    search_version: str
    kind: SearchKind
    parameters: tuple[ParameterSpec, ...]
    max_trials: int
    seed: int
    objectives: tuple[ObjectiveSpec, ...]
    baseline_parameters: Mapping[str, Any] = field(default_factory=dict)
    eta: int = 3
    min_resource: int = 1
    max_resource: int = 27
    warmup_trials: int = 5

    def __post_init__(self) -> None:
        _identifier(self.search_id, "search_id")
        _semver(self.search_version, "search_version")
        if self.max_trials < 1:
            raise ExperimentError("invalid_max_trials", "max_trials must be positive")
        if self.seed < 0:
            raise ExperimentError("negative_search_seed", "search seed must be non-negative")
        if not self.objectives:
            raise ExperimentError("empty_objectives", "at least one objective is required")
        names = [parameter.name for parameter in self.parameters]
        if len(set(names)) != len(names):
            raise ExperimentError("duplicate_parameter_name", "search parameter names must be unique")
        objective_names = [objective.name for objective in self.objectives]
        if len(set(objective_names)) != len(objective_names):
            raise ExperimentError("duplicate_objective_name", "objective names must be unique")
        if self.eta < 2:
            raise ExperimentError("invalid_halving_eta", "eta must be at least two")
        if self.min_resource < 1 or self.max_resource < self.min_resource:
            raise ExperimentError("invalid_search_resource_range", "search resource range is invalid")
        unknown = set(self.baseline_parameters) - set(names)
        if unknown:
            raise ExperimentError(
                "unknown_baseline_parameter",
                "baseline parameters must be declared in the search space",
                {"unknown": sorted(unknown)},
            )

    @property
    def plan_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class BudgetPolicy:
    budget_id: str
    budget_version: str
    max_trials: int
    max_total_wall_seconds: float
    max_trial_wall_seconds: float
    max_memory_mb: int
    cpu_slots: int
    gpu_slots: int
    max_retries: int
    max_artifact_bytes: int
    max_seeds: int
    max_folds: int
    max_candidates: int
    per_candidate_trial_cap: int
    retain_failed_artifacts: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        _identifier(self.budget_id, "budget_id")
        _semver(self.budget_version, "budget_version")
        positive_ints = {
            "max_trials": self.max_trials,
            "max_memory_mb": self.max_memory_mb,
            "cpu_slots": self.cpu_slots,
            "max_artifact_bytes": self.max_artifact_bytes,
            "max_seeds": self.max_seeds,
            "max_folds": self.max_folds,
            "max_candidates": self.max_candidates,
            "per_candidate_trial_cap": self.per_candidate_trial_cap,
        }
        for name, value in positive_ints.items():
            if value < 1:
                raise ExperimentError("invalid_budget_limit", f"{name} must be positive", {"value": value})
        if self.gpu_slots < 0 or self.max_retries < 0:
            raise ExperimentError("invalid_budget_limit", "gpu_slots and max_retries must be non-negative")
        if self.max_total_wall_seconds <= 0 or self.max_trial_wall_seconds <= 0:
            raise ExperimentError("invalid_wall_budget", "wall-clock budgets must be positive")
        if self.max_trial_wall_seconds > self.max_total_wall_seconds:
            raise ExperimentError("trial_budget_exceeds_total", "trial wall limit cannot exceed total wall limit")
        if self.per_candidate_trial_cap > self.max_trials:
            raise ExperimentError("candidate_cap_exceeds_total", "per-candidate trial cap exceeds total trial cap")

    @property
    def policy_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class ExperimentDeclaration:
    experiment_id: str
    experiment_version: str
    dataset_id: str
    dataset_manifest_hash: str
    split_plan_id: str
    split_plan_hash: str
    transform_plan_hash: str
    target_plan_hash: str
    economics_plan_hash: str
    known_time_policy_hash: str
    candidates: tuple[CandidateAdmission, ...]
    folds: tuple[str, ...]
    seeds: tuple[int, ...]
    search_plan: SearchPlan
    budget: BudgetPolicy
    scheduler_version: str
    compiler_version: str
    baseline_first: bool = True
    hidden_test_role: str = "final_test"
    requested_roles: tuple[str, ...] = ("train", "validation")
    calibration_kinds: tuple[str, ...] = ("none",)
    threshold_kinds: tuple[str, ...] = ("default",)
    ensemble_kinds: tuple[str, ...] = ()
    export_requested: bool = True

    def __post_init__(self) -> None:
        _identifier(self.experiment_id, "experiment_id")
        _semver(self.experiment_version, "experiment_version")
        _identifier(self.dataset_id, "dataset_id")
        _hash(self.dataset_manifest_hash, "dataset_manifest_hash")
        _identifier(self.split_plan_id, "split_plan_id")
        for name, value in (
            ("split_plan_hash", self.split_plan_hash),
            ("transform_plan_hash", self.transform_plan_hash),
            ("target_plan_hash", self.target_plan_hash),
            ("economics_plan_hash", self.economics_plan_hash),
            ("known_time_policy_hash", self.known_time_policy_hash),
        ):
            _hash(value, name)
        _semver(self.scheduler_version, "scheduler_version")
        _semver(self.compiler_version, "compiler_version")
        if not self.candidates or not self.folds or not self.seeds:
            raise ExperimentError("empty_experiment_axis", "candidates, folds, and seeds must be non-empty")
        _unique(self.candidates, "candidates")
        if len(set(candidate.key for candidate in self.candidates)) != len(self.candidates):
            raise ExperimentError("duplicate_candidate_key", "candidate keys must be unique")
        if len(set(self.folds)) != len(self.folds) or any(not fold for fold in self.folds):
            raise ExperimentError("invalid_fold_set", "fold identifiers must be unique and non-empty")
        if len(set(self.seeds)) != len(self.seeds) or any(seed < 0 for seed in self.seeds):
            raise ExperimentError("invalid_seed_set", "seeds must be unique and non-negative")
        if self.hidden_test_role in self.requested_roles:
            raise ExperimentError(
                "hidden_test_role_requested",
                "hidden/final test role cannot be referenced by search nodes",
                {"role": self.hidden_test_role},
            )
        if len(set(self.requested_roles)) != len(self.requested_roles):
            raise ExperimentError("duplicate_requested_role", "requested roles must be unique")
        if not self.calibration_kinds or not self.threshold_kinds:
            raise ExperimentError("empty_postprocess_axis", "calibration and threshold axes cannot be empty")

    @property
    def declaration_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class TrialIdentity:
    trial_id: str
    experiment_id: str
    candidate_key: str
    trainer_key: str
    parameter_values: Mapping[str, Any]
    fold_id: str
    seed: int
    resource_level: int
    dataset_manifest_hash: str
    split_plan_hash: str
    transform_plan_hash: str
    target_plan_hash: str
    economics_plan_hash: str
    known_time_policy_hash: str
    search_plan_hash: str
    budget_policy_hash: str
    scheduler_version: str
    compiler_version: str
    identity_hash: str

    def __post_init__(self) -> None:
        _identifier(self.trial_id, "trial_id")
        _identifier(self.experiment_id, "experiment_id")
        _identifier(self.candidate_key, "candidate_key")
        _identifier(self.trainer_key, "trainer_key")
        _identifier(self.fold_id, "fold_id")
        if self.seed < 0 or self.resource_level < 1:
            raise ExperimentError("invalid_trial_axis", "trial seed/resource level is invalid")
        for name in (
            "dataset_manifest_hash",
            "split_plan_hash",
            "transform_plan_hash",
            "target_plan_hash",
            "economics_plan_hash",
            "known_time_policy_hash",
            "search_plan_hash",
            "budget_policy_hash",
            "identity_hash",
        ):
            _hash(getattr(self, name), name)


@dataclass(frozen=True, slots=True)
class DagNode:
    node_id: str
    kind: NodeKind
    semantic_key: str
    payload_hash: str
    dependencies: tuple[str, ...]
    priority: int
    resource_claim_hash: str = ""
    trial_id: str = ""

    def __post_init__(self) -> None:
        _identifier(self.node_id, "node_id")
        _identifier(self.semantic_key, "semantic_key")
        _hash(self.payload_hash, "payload_hash")
        if self.resource_claim_hash:
            _hash(self.resource_claim_hash, "resource_claim_hash")
        if self.priority < 0:
            raise ExperimentError("negative_node_priority", "node priority must be non-negative")
        if self.node_id in self.dependencies:
            raise ExperimentError("self_dependency", "DAG node cannot depend on itself")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ExperimentError("duplicate_dependency", "DAG node dependencies must be unique")


@dataclass(frozen=True, slots=True)
class DagEdge:
    parent_id: str
    child_id: str
    edge_type: str = "requires"

    def __post_init__(self) -> None:
        _identifier(self.parent_id, "parent_id")
        _identifier(self.child_id, "child_id")
        _identifier(self.edge_type, "edge_type")
        if self.parent_id == self.child_id:
            raise ExperimentError("self_edge", "DAG edge cannot point to itself")


@dataclass(frozen=True, slots=True)
class ResourceClaim:
    claim_id: str
    trial_id: str
    device: ResourceDevice
    cpu_slots: int
    gpu_slots: int
    memory_mb: int
    wall_seconds: float
    artifact_bytes: int
    deterministic_required: bool = True

    def __post_init__(self) -> None:
        _identifier(self.claim_id, "claim_id")
        _identifier(self.trial_id, "trial_id")
        if self.cpu_slots < 1 or self.gpu_slots < 0 or self.memory_mb < 1 or self.artifact_bytes < 0:
            raise ExperimentError("invalid_resource_claim", "resource claim contains invalid integer limits")
        if self.wall_seconds <= 0:
            raise ExperimentError("invalid_resource_claim", "resource wall_seconds must be positive")
        if self.device is ResourceDevice.GPU and self.gpu_slots < 1:
            raise ExperimentError("gpu_claim_without_slot", "GPU device requires at least one GPU slot")

    @property
    def claim_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class ExperimentManifest:
    manifest_id: str
    manifest_version: str
    declaration_hash: str
    compiler_version: str
    scheduler_version: str
    generated_sequence: int
    candidate_admission_hash: str
    nodes: tuple[DagNode, ...]
    edges: tuple[DagEdge, ...]
    trials: tuple[TrialIdentity, ...]
    resource_claims: tuple[ResourceClaim, ...]
    declared_trial_count: int
    rejected_candidate_keys: tuple[str, ...]
    hidden_test_role: str
    manifest_hash: str

    def __post_init__(self) -> None:
        _identifier(self.manifest_id, "manifest_id")
        _semver(self.manifest_version, "manifest_version")
        _semver(self.compiler_version, "compiler_version")
        _semver(self.scheduler_version, "scheduler_version")
        for name in ("declaration_hash", "candidate_admission_hash", "manifest_hash"):
            _hash(getattr(self, name), name)
        if self.generated_sequence < 0:
            raise ExperimentError("negative_generated_sequence", "generated sequence must be non-negative")
        if self.declared_trial_count != len(self.trials):
            raise ExperimentError("declared_trial_count_mismatch", "declared trial count differs from trial identities")
        node_ids = [node.node_id for node in self.nodes]
        if len(set(node_ids)) != len(node_ids):
            raise ExperimentError("duplicate_dag_node", "DAG node identifiers must be unique")
        trial_ids = [trial.trial_id for trial in self.trials]
        if len(set(trial_ids)) != len(trial_ids):
            raise ExperimentError("duplicate_trial_identity", "trial identifiers must be unique")
        claim_ids = [claim.claim_id for claim in self.resource_claims]
        if len(set(claim_ids)) != len(claim_ids):
            raise ExperimentError("duplicate_resource_claim", "resource claim identifiers must be unique")


@dataclass(frozen=True, slots=True)
class SearchObservation:
    trial_id: str
    parameter_values: Mapping[str, Any]
    metrics: Mapping[str, float]
    feasible: bool
    resource_level: int
    completed_sequence: int

    def __post_init__(self) -> None:
        _identifier(self.trial_id, "trial_id")
        if not self.metrics:
            raise ExperimentError("empty_search_metrics", "search observation requires metrics")
        for name, value in self.metrics.items():
            _identifier(name, "metric_name")
            _finite(value, f"metric[{name}]")
        if self.resource_level < 1 or self.completed_sequence < 0:
            raise ExperimentError("invalid_search_observation", "resource/sequence is invalid")

    @property
    def observation_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class BudgetUsage:
    trials_started: int = 0
    trials_completed: int = 0
    total_wall_seconds: float = 0.0
    artifact_bytes: int = 0
    memory_high_water_mb: int = 0
    per_candidate_trials: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, value in (
            ("trials_started", self.trials_started),
            ("trials_completed", self.trials_completed),
            ("artifact_bytes", self.artifact_bytes),
            ("memory_high_water_mb", self.memory_high_water_mb),
        ):
            if value < 0:
                raise ExperimentError("negative_budget_usage", f"{name} cannot be negative")
        _nonnegative(self.total_wall_seconds, "total_wall_seconds")
        if self.trials_completed > self.trials_started:
            raise ExperimentError("completed_exceeds_started", "completed trials cannot exceed started trials")


@dataclass(frozen=True, slots=True)
class BudgetAssessment:
    assessment_id: str
    decision: BudgetDecision
    reason_codes: tuple[str, ...]
    usage_before: BudgetUsage
    proposed_claim: ResourceClaim
    policy_hash: str
    assessment_hash: str

    def __post_init__(self) -> None:
        _identifier(self.assessment_id, "assessment_id")
        _hash(self.policy_hash, "policy_hash")
        _hash(self.assessment_hash, "assessment_hash")
        if self.decision is BudgetDecision.DENY and not self.reason_codes:
            raise ExperimentError("budget_denial_without_reason", "budget denial requires reason codes")


@dataclass(frozen=True, slots=True)
class SchedulerEvent:
    event_id: str
    sequence: int
    node_id: str
    trial_id: str
    kind: SchedulerEventKind
    status_before: NodeStatus
    status_after: NodeStatus
    attempt: int
    worker_id: str
    payload_hash: str
    reason_code: str = ""

    def __post_init__(self) -> None:
        _identifier(self.event_id, "event_id")
        _identifier(self.node_id, "node_id")
        if self.trial_id:
            _identifier(self.trial_id, "trial_id")
        if self.worker_id:
            _identifier(self.worker_id, "worker_id")
        _hash(self.payload_hash, "payload_hash")
        if self.sequence < 0 or self.attempt < 0:
            raise ExperimentError("negative_scheduler_counter", "scheduler sequence/attempt cannot be negative")


@dataclass(frozen=True, slots=True)
class WorkResult:
    status: NodeStatus
    metrics: Mapping[str, float] = field(default_factory=dict)
    artifact_hashes: tuple[str, ...] = ()
    elapsed_seconds: float = 0.0
    artifact_bytes: int = 0
    failure_code: str = ""
    failure_disposition: FailureDisposition = FailureDisposition.TERMINAL

    def __post_init__(self) -> None:
        if self.status not in (
            NodeStatus.SUCCEEDED,
            NodeStatus.FAILED,
            NodeStatus.PRUNED,
            NodeStatus.TIMED_OUT,
            NodeStatus.CANCELLED,
            NodeStatus.QUARANTINED,
            NodeStatus.CACHED,
        ):
            raise ExperimentError("invalid_work_result_status", "work result has unsupported terminal status")
        _nonnegative(self.elapsed_seconds, "elapsed_seconds")
        if self.artifact_bytes < 0:
            raise ExperimentError("negative_artifact_bytes", "artifact_bytes cannot be negative")
        for value in self.metrics.values():
            _finite(value, "work_result.metric")
        for value in self.artifact_hashes:
            _hash(value, "artifact_hash")
        if self.status in (NodeStatus.FAILED, NodeStatus.TIMED_OUT, NodeStatus.QUARANTINED) and not self.failure_code:
            raise ExperimentError("failure_without_code", "failed work result requires failure_code")


@dataclass(frozen=True, slots=True)
class SelectionLedgerEntry:
    entry_id: str
    sequence: int
    experiment_id: str
    manifest_hash: str
    trial_id: str
    node_id: str
    action: LedgerAction
    reason_code: str
    metrics: Mapping[str, float]
    artifact_hashes: tuple[str, ...]
    actor: str
    previous_entry_hash: str
    entry_hash: str

    def __post_init__(self) -> None:
        _identifier(self.entry_id, "entry_id")
        _identifier(self.experiment_id, "experiment_id")
        _identifier(self.trial_id, "trial_id")
        _identifier(self.node_id, "node_id")
        _identifier(self.actor, "actor")
        _hash(self.manifest_hash, "manifest_hash")
        _hash(self.previous_entry_hash, "previous_entry_hash", allow_blank=True)
        _hash(self.entry_hash, "entry_hash")
        if self.sequence < 0:
            raise ExperimentError("negative_ledger_sequence", "ledger sequence cannot be negative")
        for value in self.artifact_hashes:
            _hash(value, "artifact_hash")
        for value in self.metrics.values():
            _finite(value, "ledger_metric")


@dataclass(frozen=True, slots=True)
class CacheRecord:
    cache_key: str
    namespace: str
    artifact_kind: str
    producer_version: str
    schema_version: str
    input_hashes: tuple[str, ...]
    payload_hash: str
    provenance_hash: str
    created_sequence: int
    size_bytes: int
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _hash(self.cache_key, "cache_key")
        _identifier(self.namespace, "namespace")
        _identifier(self.artifact_kind, "artifact_kind")
        _semver(self.producer_version, "producer_version")
        _semver(self.schema_version, "schema_version")
        if not self.input_hashes:
            raise ExperimentError("empty_cache_inputs", "cache record requires input hashes")
        for value in self.input_hashes:
            _hash(value, "input_hash")
        _hash(self.payload_hash, "payload_hash")
        _hash(self.provenance_hash, "provenance_hash")
        if self.created_sequence < 0 or self.size_bytes < 0:
            raise ExperimentError("invalid_cache_counter", "cache sequence/size cannot be negative")


@dataclass(frozen=True, slots=True)
class CacheLookup:
    key: str
    status: CacheStatus
    reason_code: str
    record: CacheRecord | None

    def __post_init__(self) -> None:
        _hash(self.key, "key")
        if self.status is CacheStatus.VALID and self.record is None:
            raise ExperimentError("valid_cache_without_record", "valid cache lookup requires a record")
        if self.status is not CacheStatus.VALID and not self.reason_code:
            raise ExperimentError("cache_failure_without_reason", "non-valid cache lookup requires reason code")


@dataclass(frozen=True, slots=True)
class ArtifactComparison:
    artifact_name: str
    expected_hash: str
    actual_hash: str
    within_tolerance: bool
    max_abs_error: float
    tolerance: float

    def __post_init__(self) -> None:
        _identifier(self.artifact_name, "artifact_name")
        _hash(self.expected_hash, "expected_hash")
        _hash(self.actual_hash, "actual_hash")
        _nonnegative(self.max_abs_error, "max_abs_error")
        _nonnegative(self.tolerance, "tolerance")


@dataclass(frozen=True, slots=True)
class ReproducibilityReport:
    report_id: str
    manifest_hash: str
    rerun_manifest_hash: str
    declared_trial_count: int
    executed_trial_count: int
    selected_trial_ids_expected: tuple[str, ...]
    selected_trial_ids_actual: tuple[str, ...]
    artifact_comparisons: tuple[ArtifactComparison, ...]
    event_stream_hash_expected: str
    event_stream_hash_actual: str
    passed: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    report_hash: str

    def __post_init__(self) -> None:
        _identifier(self.report_id, "report_id")
        for name in (
            "manifest_hash",
            "rerun_manifest_hash",
            "event_stream_hash_expected",
            "event_stream_hash_actual",
            "report_hash",
        ):
            _hash(getattr(self, name), name)
        if self.declared_trial_count < 0 or self.executed_trial_count < 0:
            raise ExperimentError("negative_repro_count", "reproducibility counts cannot be negative")
        if self.passed and self.blockers:
            raise ExperimentError("passed_repro_with_blockers", "passed reproducibility report cannot contain blockers")
        if not self.passed and not self.blockers:
            raise ExperimentError("failed_repro_without_blockers", "failed reproducibility report requires blockers")


def make_trial_identity(
    *,
    declaration: ExperimentDeclaration,
    candidate: CandidateAdmission,
    parameter_values: Mapping[str, Any],
    fold_id: str,
    seed: int,
    resource_level: int,
) -> TrialIdentity:
    identity_payload = {
        "experiment_id": declaration.experiment_id,
        "experiment_version": declaration.experiment_version,
        "candidate_key": candidate.key,
        "trainer_key": candidate.trainer_key,
        "parameter_values": dict(parameter_values),
        "fold_id": fold_id,
        "seed": seed,
        "resource_level": resource_level,
        "dataset_manifest_hash": declaration.dataset_manifest_hash,
        "split_plan_hash": declaration.split_plan_hash,
        "transform_plan_hash": declaration.transform_plan_hash,
        "target_plan_hash": declaration.target_plan_hash,
        "economics_plan_hash": declaration.economics_plan_hash,
        "known_time_policy_hash": declaration.known_time_policy_hash,
        "search_plan_hash": declaration.search_plan.plan_hash,
        "budget_policy_hash": declaration.budget.policy_hash,
        "scheduler_version": declaration.scheduler_version,
        "compiler_version": declaration.compiler_version,
    }
    identity_hash = canonical_sha256(identity_payload)
    return TrialIdentity(
        trial_id=stable_id("ucetrial", identity_payload),
        experiment_id=declaration.experiment_id,
        candidate_key=candidate.key,
        trainer_key=candidate.trainer_key,
        parameter_values=dict(parameter_values),
        fold_id=fold_id,
        seed=seed,
        resource_level=resource_level,
        dataset_manifest_hash=declaration.dataset_manifest_hash,
        split_plan_hash=declaration.split_plan_hash,
        transform_plan_hash=declaration.transform_plan_hash,
        target_plan_hash=declaration.target_plan_hash,
        economics_plan_hash=declaration.economics_plan_hash,
        known_time_policy_hash=declaration.known_time_policy_hash,
        search_plan_hash=declaration.search_plan.plan_hash,
        budget_policy_hash=declaration.budget.policy_hash,
        scheduler_version=declaration.scheduler_version,
        compiler_version=declaration.compiler_version,
        identity_hash=identity_hash,
    )

@dataclass(frozen=True, slots=True)
class SearchAdapterDescriptor:
    adapter_id: str
    adapter_version: str
    kind: SearchKind
    native: bool
    deterministic: bool
    supports_constraints: bool
    supports_multi_objective: bool
    supports_pruning: bool
    dependency_profile: str = ""
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _identifier(self.adapter_id, "adapter_id")
        _semver(self.adapter_version, "adapter_version")
        if self.native and self.dependency_profile:
            raise ExperimentError("native_search_dependency_forbidden", "native search adapter cannot require dependency profile")

    @property
    def key(self) -> str:
        return f"{self.adapter_id}@{self.adapter_version}"

    @property
    def descriptor_hash(self) -> str:
        return canonical_sha256(asdict(self))


@dataclass(frozen=True, slots=True)
class SearchRegistrySnapshot:
    snapshot_id: str
    descriptors: tuple[SearchAdapterDescriptor, ...]
    frozen: bool
    evidence_hash: str

    def __post_init__(self) -> None:
        _identifier(self.snapshot_id, "snapshot_id")
        _hash(self.evidence_hash, "evidence_hash")
        keys = [descriptor.key for descriptor in self.descriptors]
        if len(set(keys)) != len(keys):
            raise ExperimentError("duplicate_search_adapter", "search registry keys must be unique")
