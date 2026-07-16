from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .errors import ContractError

ROLES = {"meta_train", "meta_validation", "transfer_test", "drift_reference"}
DRIFT_CLASSES = {"stationary", "gradual", "sudden", "recurring", "novel"}
REQUIRED_TASK_FIELDS = {
    "task_id",
    "context_id",
    "cluster_id",
    "regime",
    "role",
    "window_start",
    "decision_time",
    "window_end",
    "feature_known_at",
    "outcome_observed_at",
    "feature_summary",
    "support_features",
    "support_targets",
    "query_features",
    "query_targets",
    "baseline_parameters",
    "support_score",
    "ood_pvalue",
    "conformal_value_lower_bound",
    "future_suffix_accessed",
    "protected_evidence_accessed",
}


def exact(mapping: Mapping[str, Any], required: set[str], label: str) -> None:
    if set(mapping) != required:
        unknown = sorted(set(mapping) - required)
        missing = sorted(required - set(mapping))
        raise ContractError(f"{label} field mismatch; unknown={unknown}, missing={missing}")


def text(value: Any, label: str) -> str:
    output = str(value)
    if not output:
        raise ContractError(f"{label} is empty")
    return output


def integer(value: Any, label: str, minimum: int = 0) -> int:
    output = int(value)
    if output < minimum:
        raise ContractError(f"{label} below minimum {minimum}")
    return output


def positive(value: Any, label: str) -> float:
    output = float(value)
    if output <= 0:
        raise ContractError(f"{label} must be positive")
    return output


def probability(value: Any, label: str, open_zero: bool = False) -> float:
    output = float(value)
    if (output <= 0 if open_zero else output < 0) or output > 1:
        raise ContractError(f"{label} outside probability domain")
    return output


@dataclass(frozen=True)
class UpstreamIntakeContract:
    exact_version: str
    required_phase: str
    handoff_hash: str
    certificate_hash: str
    research_policy_id: str
    immutable: bool
    hash_verified: bool
    research_only: bool
    promotion_denied: bool
    runtime_denied: bool
    online_policy_mutation_denied: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "UpstreamIntakeContract":
        required = {
            "exact_version", "required_phase", "handoff_hash", "certificate_hash",
            "research_policy_id", "immutable", "hash_verified", "research_only",
            "promotion_denied", "runtime_denied", "online_policy_mutation_denied",
        }
        exact(value, required, "upstream intake")
        output = cls(
            text(value["exact_version"], "exact_version"),
            text(value["required_phase"], "required_phase"),
            text(value["handoff_hash"], "handoff_hash"),
            text(value["certificate_hash"], "certificate_hash"),
            text(value["research_policy_id"], "research_policy_id"),
            bool(value["immutable"]),
            bool(value["hash_verified"]),
            bool(value["research_only"]),
            bool(value["promotion_denied"]),
            bool(value["runtime_denied"]),
            bool(value["online_policy_mutation_denied"]),
        )
        if output.required_phase != "SAED_V4_24":
            raise ContractError("V4-25 requires exact SAED_V4_24 intake")
        if not all((
            output.immutable,
            output.hash_verified,
            output.research_only,
            output.promotion_denied,
            output.runtime_denied,
            output.online_policy_mutation_denied,
        )):
            raise ContractError("unsafe V4-24 intake")
        return output


@dataclass(frozen=True)
class MetaDatasetContract:
    exact_version: str
    allowed_roles: tuple[str, ...]
    required_fields: tuple[str, ...]
    feature_names: tuple[str, ...]
    parameter_names: tuple[str, ...]
    minimum_tasks: int
    minimum_contexts: int
    minimum_clusters: int
    minimum_tasks_per_role: int
    strict_chronology: bool
    cluster_role_separation_required: bool
    query_outcomes_protected_during_adaptation: bool
    future_suffix_forbidden: bool
    protected_evidence_forbidden: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "MetaDatasetContract":
        required = {
            "exact_version", "allowed_roles", "required_fields", "feature_names",
            "parameter_names", "minimum_tasks", "minimum_contexts", "minimum_clusters",
            "minimum_tasks_per_role", "strict_chronology", "cluster_role_separation_required",
            "query_outcomes_protected_during_adaptation", "future_suffix_forbidden",
            "protected_evidence_forbidden",
        }
        exact(value, required, "meta dataset")
        output = cls(
            text(value["exact_version"], "exact_version"),
            tuple(map(str, value["allowed_roles"])),
            tuple(map(str, value["required_fields"])),
            tuple(map(str, value["feature_names"])),
            tuple(map(str, value["parameter_names"])),
            integer(value["minimum_tasks"], "minimum_tasks", 20),
            integer(value["minimum_contexts"], "minimum_contexts", 3),
            integer(value["minimum_clusters"], "minimum_clusters", 6),
            integer(value["minimum_tasks_per_role"], "minimum_tasks_per_role", 3),
            bool(value["strict_chronology"]),
            bool(value["cluster_role_separation_required"]),
            bool(value["query_outcomes_protected_during_adaptation"]),
            bool(value["future_suffix_forbidden"]),
            bool(value["protected_evidence_forbidden"]),
        )
        if set(output.allowed_roles) != ROLES:
            raise ContractError("meta dataset roles mismatch")
        if set(output.required_fields) != REQUIRED_TASK_FIELDS:
            raise ContractError("meta dataset required fields mismatch")
        if len(output.feature_names) < 5 or len(output.parameter_names) < 2:
            raise ContractError("meta dataset registries too small")
        if not all((
            output.strict_chronology,
            output.cluster_role_separation_required,
            output.query_outcomes_protected_during_adaptation,
            output.future_suffix_forbidden,
            output.protected_evidence_forbidden,
        )):
            raise ContractError("meta dataset safety controls disabled")
        return output


@dataclass(frozen=True)
class DriftTaxonomyContract:
    exact_version: str
    allowed_classes: tuple[str, ...]
    stationary_threshold: float
    gradual_threshold: float
    sudden_threshold: float
    recurrence_similarity_threshold: float
    minimum_segment_tasks: int
    deterministic: bool
    fail_closed_to_novel: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "DriftTaxonomyContract":
        required = {
            "exact_version", "allowed_classes", "stationary_threshold", "gradual_threshold",
            "sudden_threshold", "recurrence_similarity_threshold", "minimum_segment_tasks",
            "deterministic", "fail_closed_to_novel",
        }
        exact(value, required, "drift taxonomy")
        output = cls(
            text(value["exact_version"], "exact_version"),
            tuple(map(str, value["allowed_classes"])),
            positive(value["stationary_threshold"], "stationary_threshold"),
            positive(value["gradual_threshold"], "gradual_threshold"),
            positive(value["sudden_threshold"], "sudden_threshold"),
            probability(value["recurrence_similarity_threshold"], "recurrence_similarity_threshold"),
            integer(value["minimum_segment_tasks"], "minimum_segment_tasks", 2),
            bool(value["deterministic"]),
            bool(value["fail_closed_to_novel"]),
        )
        if set(output.allowed_classes) != DRIFT_CLASSES:
            raise ContractError("drift class registry mismatch")
        if not (output.stationary_threshold < output.gradual_threshold < output.sudden_threshold):
            raise ContractError("drift thresholds must be strictly increasing")
        if not output.deterministic or not output.fail_closed_to_novel:
            raise ContractError("drift taxonomy must be deterministic and fail closed")
        return output


@dataclass(frozen=True)
class TransferContract:
    exact_version: str
    maximum_sources: int
    minimum_source_support: float
    minimum_source_ood_pvalue: float
    maximum_meta_distance: float
    same_cluster_forbidden: bool
    future_source_forbidden: bool
    source_query_outcomes_forbidden: bool
    negative_transfer_guard_required: bool
    safe_fallback: str
    deterministic: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TransferContract":
        required = {
            "exact_version", "maximum_sources", "minimum_source_support",
            "minimum_source_ood_pvalue", "maximum_meta_distance", "same_cluster_forbidden",
            "future_source_forbidden", "source_query_outcomes_forbidden",
            "negative_transfer_guard_required", "safe_fallback", "deterministic",
        }
        exact(value, required, "transfer")
        output = cls(
            text(value["exact_version"], "exact_version"),
            integer(value["maximum_sources"], "maximum_sources", 1),
            probability(value["minimum_source_support"], "minimum_source_support"),
            probability(value["minimum_source_ood_pvalue"], "minimum_source_ood_pvalue", True),
            positive(value["maximum_meta_distance"], "maximum_meta_distance"),
            bool(value["same_cluster_forbidden"]),
            bool(value["future_source_forbidden"]),
            bool(value["source_query_outcomes_forbidden"]),
            bool(value["negative_transfer_guard_required"]),
            text(value["safe_fallback"], "safe_fallback"),
            bool(value["deterministic"]),
        )
        if output.maximum_sources > 16 or output.safe_fallback != "scratch_baseline":
            raise ContractError("unsafe transfer fallback or source count")
        if not all((
            output.same_cluster_forbidden,
            output.future_source_forbidden,
            output.source_query_outcomes_forbidden,
            output.negative_transfer_guard_required,
            output.deterministic,
        )):
            raise ContractError("transfer safety controls disabled")
        return output


@dataclass(frozen=True)
class AdaptationContract:
    exact_version: str
    method: str
    prior_strength: float
    ridge_penalty: float
    maximum_parameter_delta: float
    minimum_support_rows: int
    query_outcomes_forbidden: bool
    baseline_preserved: bool
    deterministic: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AdaptationContract":
        required = {
            "exact_version", "method", "prior_strength", "ridge_penalty",
            "maximum_parameter_delta", "minimum_support_rows", "query_outcomes_forbidden",
            "baseline_preserved", "deterministic",
        }
        exact(value, required, "adaptation")
        output = cls(
            text(value["exact_version"], "exact_version"),
            text(value["method"], "method"),
            positive(value["prior_strength"], "prior_strength"),
            positive(value["ridge_penalty"], "ridge_penalty"),
            positive(value["maximum_parameter_delta"], "maximum_parameter_delta"),
            integer(value["minimum_support_rows"], "minimum_support_rows", 2),
            bool(value["query_outcomes_forbidden"]),
            bool(value["baseline_preserved"]),
            bool(value["deterministic"]),
        )
        if output.method != "regularized_empirical_bayes_linear":
            raise ContractError("unsupported adaptation method")
        if not all((output.query_outcomes_forbidden, output.baseline_preserved, output.deterministic)):
            raise ContractError("adaptation safety controls disabled")
        return output


@dataclass(frozen=True)
class ContinualCalibrationContract:
    exact_version: str
    window_tasks: int
    minimum_residuals: int
    alpha: float
    finite_sample_correction: bool
    past_only: bool
    no_runtime_mutation: bool
    fail_closed: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ContinualCalibrationContract":
        required = {
            "exact_version", "window_tasks", "minimum_residuals", "alpha",
            "finite_sample_correction", "past_only", "no_runtime_mutation", "fail_closed",
        }
        exact(value, required, "continual calibration")
        output = cls(
            text(value["exact_version"], "exact_version"),
            integer(value["window_tasks"], "window_tasks", 2),
            integer(value["minimum_residuals"], "minimum_residuals", 10),
            probability(value["alpha"], "alpha", True),
            bool(value["finite_sample_correction"]),
            bool(value["past_only"]),
            bool(value["no_runtime_mutation"]),
            bool(value["fail_closed"]),
        )
        if output.alpha >= 0.5 or not all((
            output.finite_sample_correction,
            output.past_only,
            output.no_runtime_mutation,
            output.fail_closed,
        )):
            raise ContractError("unsafe continual calibration contract")
        return output


@dataclass(frozen=True)
class ReplayContract:
    exact_version: str
    capacity: int
    minimum_per_context: int
    minimum_per_drift_class: int
    recency_weight: float
    diversity_weight: float
    protected_query_outcomes_forbidden: bool
    deterministic: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ReplayContract":
        required = {
            "exact_version", "capacity", "minimum_per_context", "minimum_per_drift_class",
            "recency_weight", "diversity_weight", "protected_query_outcomes_forbidden",
            "deterministic",
        }
        exact(value, required, "replay")
        output = cls(
            text(value["exact_version"], "exact_version"),
            integer(value["capacity"], "capacity", 4),
            integer(value["minimum_per_context"], "minimum_per_context", 1),
            integer(value["minimum_per_drift_class"], "minimum_per_drift_class", 1),
            positive(value["recency_weight"], "recency_weight"),
            positive(value["diversity_weight"], "diversity_weight"),
            bool(value["protected_query_outcomes_forbidden"]),
            bool(value["deterministic"]),
        )
        if output.minimum_per_context > output.capacity or output.minimum_per_drift_class > output.capacity:
            raise ContractError("replay minima exceed capacity")
        if not output.protected_query_outcomes_forbidden or not output.deterministic:
            raise ContractError("unsafe replay contract")
        return output


@dataclass(frozen=True)
class ForgettingContract:
    exact_version: str
    maximum_mean_forgetting: float
    maximum_worst_task_forgetting: float
    minimum_forward_transfer: float
    minimum_backward_transfer: float
    bootstrap_draws: int
    confidence_level: float
    cluster_bootstrap_required: bool
    negative_transfer_fails_closed: bool

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ForgettingContract":
        required = {
            "exact_version", "maximum_mean_forgetting", "maximum_worst_task_forgetting",
            "minimum_forward_transfer", "minimum_backward_transfer", "bootstrap_draws",
            "confidence_level", "cluster_bootstrap_required", "negative_transfer_fails_closed",
        }
        exact(value, required, "forgetting")
        output = cls(
            text(value["exact_version"], "exact_version"),
            float(value["maximum_mean_forgetting"]),
            float(value["maximum_worst_task_forgetting"]),
            float(value["minimum_forward_transfer"]),
            float(value["minimum_backward_transfer"]),
            integer(value["bootstrap_draws"], "bootstrap_draws", 200),
            probability(value["confidence_level"], "confidence_level", True),
            bool(value["cluster_bootstrap_required"]),
            bool(value["negative_transfer_fails_closed"]),
        )
        if output.maximum_mean_forgetting < 0 or output.maximum_worst_task_forgetting < output.maximum_mean_forgetting:
            raise ContractError("invalid forgetting thresholds")
        if output.confidence_level < 0.8 or not output.cluster_bootstrap_required or not output.negative_transfer_fails_closed:
            raise ContractError("forgetting controls disabled")
        return output


@dataclass(frozen=True)
class RecalibrationExperimentContract:
    exact_version: str
    candidate_window_grid: tuple[int, ...]
    candidate_prior_strength_grid: tuple[float, ...]
    candidate_ridge_grid: tuple[float, ...]
    maximum_trials: int
    selection_role: str
    hidden_evaluation_queries: int
    online_mutation_forbidden: bool
    deterministic_tie_break: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "RecalibrationExperimentContract":
        required = {
            "exact_version", "candidate_window_grid", "candidate_prior_strength_grid",
            "candidate_ridge_grid", "maximum_trials", "selection_role",
            "hidden_evaluation_queries", "online_mutation_forbidden", "deterministic_tie_break",
        }
        exact(value, required, "recalibration experiment")
        output = cls(
            text(value["exact_version"], "exact_version"),
            tuple(int(item) for item in value["candidate_window_grid"]),
            tuple(float(item) for item in value["candidate_prior_strength_grid"]),
            tuple(float(item) for item in value["candidate_ridge_grid"]),
            integer(value["maximum_trials"], "maximum_trials", 1),
            text(value["selection_role"], "selection_role"),
            integer(value["hidden_evaluation_queries"], "hidden_evaluation_queries", 0),
            bool(value["online_mutation_forbidden"]),
            text(value["deterministic_tie_break"], "deterministic_tie_break"),
        )
        if not output.candidate_window_grid or not output.candidate_prior_strength_grid or not output.candidate_ridge_grid:
            raise ContractError("recalibration grids cannot be empty")
        if output.selection_role != "meta_validation" or output.hidden_evaluation_queries != 0:
            raise ContractError("unsafe recalibration role or hidden evaluation access")
        if not output.online_mutation_forbidden or output.deterministic_tie_break != "lower_complexity_then_lexicographic":
            raise ContractError("recalibration safety controls disabled")
        total = len(output.candidate_window_grid) * len(output.candidate_prior_strength_grid) * len(output.candidate_ridge_grid)
        if total > output.maximum_trials:
            raise ContractError("candidate grid exceeds maximum trials")
        return output


@dataclass(frozen=True)
class ResearchBudget:
    exact_version: str
    maximum_tasks: int
    maximum_source_evaluations: int
    maximum_adaptations: int
    maximum_replay_entries: int
    maximum_recalibration_trials: int
    maximum_bootstrap_draws: int
    maximum_hidden_evaluation_queries: int
    maximum_protected_evidence_exposures: int
    maximum_runtime_compilations: int
    maximum_order_submissions: int
    maximum_online_policy_mutations: int
    failure_budget: int

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ResearchBudget":
        required = {
            "exact_version", "maximum_tasks", "maximum_source_evaluations", "maximum_adaptations",
            "maximum_replay_entries", "maximum_recalibration_trials", "maximum_bootstrap_draws",
            "maximum_hidden_evaluation_queries", "maximum_protected_evidence_exposures",
            "maximum_runtime_compilations", "maximum_order_submissions",
            "maximum_online_policy_mutations", "failure_budget",
        }
        exact(value, required, "research budget")
        output = cls(
            text(value["exact_version"], "exact_version"),
            integer(value["maximum_tasks"], "maximum_tasks", 1),
            integer(value["maximum_source_evaluations"], "maximum_source_evaluations", 1),
            integer(value["maximum_adaptations"], "maximum_adaptations", 1),
            integer(value["maximum_replay_entries"], "maximum_replay_entries", 1),
            integer(value["maximum_recalibration_trials"], "maximum_recalibration_trials", 1),
            integer(value["maximum_bootstrap_draws"], "maximum_bootstrap_draws", 1),
            integer(value["maximum_hidden_evaluation_queries"], "maximum_hidden_evaluation_queries", 0),
            integer(value["maximum_protected_evidence_exposures"], "maximum_protected_evidence_exposures", 0),
            integer(value["maximum_runtime_compilations"], "maximum_runtime_compilations", 0),
            integer(value["maximum_order_submissions"], "maximum_order_submissions", 0),
            integer(value["maximum_online_policy_mutations"], "maximum_online_policy_mutations", 0),
            integer(value["failure_budget"], "failure_budget", 0),
        )
        if any((
            output.maximum_hidden_evaluation_queries,
            output.maximum_protected_evidence_exposures,
            output.maximum_runtime_compilations,
            output.maximum_order_submissions,
            output.maximum_online_policy_mutations,
        )):
            raise ContractError("forbidden authority exposure budget must remain zero")
        return output
