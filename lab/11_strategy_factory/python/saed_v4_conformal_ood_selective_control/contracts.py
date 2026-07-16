from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .errors import ContractError

ACTIONS = {'skip', 'long', 'short'}
ROLES = {'calibration', 'selection_validation', 'drift_reference'}
REQUIRED_RECORD_FIELDS = {
    'record_id', 'cluster_id', 'regime', 'decision_time', 'feature_known_at', 'outcome_observed_at',
    'role', 'features', 'support_score', 'policy_id', 'predicted_value', 'realized_value',
    'candidate_action', 'allowed_actions', 'behavior_probability', 'candidate_probability',
    'future_suffix_accessed', 'protected_evidence_accessed'
}

def exact(mapping: Mapping[str, Any], required: set[str], label: str) -> None:
    if set(mapping) != required:
        raise ContractError(f'{label} field mismatch: {sorted(set(mapping) ^ required)}')

def text(value, label):
    value = str(value)
    if not value:
        raise ContractError(f'{label} is empty')
    return value

def positive(value, label):
    value = float(value)
    if value <= 0:
        raise ContractError(f'{label} must be positive')
    return value

def probability(value, label, open_zero=False):
    value = float(value)
    if (value <= 0 if open_zero else value < 0) or value > 1:
        raise ContractError(f'{label} outside probability domain')
    return value

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

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'required_phase', 'handoff_hash', 'certificate_hash', 'research_policy_id', 'immutable', 'hash_verified', 'research_only', 'promotion_denied', 'runtime_denied'}
        exact(value, required, 'upstream intake')
        output = cls(text(value['exact_version'], 'exact_version'), text(value['required_phase'], 'required_phase'), text(value['handoff_hash'], 'handoff_hash'), text(value['certificate_hash'], 'certificate_hash'), text(value['research_policy_id'], 'research_policy_id'), bool(value['immutable']), bool(value['hash_verified']), bool(value['research_only']), bool(value['promotion_denied']), bool(value['runtime_denied']))
        if output.required_phase != 'SAED_V4_23' or not all((output.immutable, output.hash_verified, output.research_only, output.promotion_denied, output.runtime_denied)):
            raise ContractError('unsafe V4-23 intake')
        return output

@dataclass(frozen=True)
class CalibrationDatasetContract:
    exact_version: str
    allowed_roles: tuple[str, ...]
    required_fields: tuple[str, ...]
    feature_names: tuple[str, ...]
    minimum_records: int
    minimum_clusters: int
    minimum_records_per_regime: int
    strict_decision_time_order: bool
    feature_known_by_decision: bool
    outcome_after_decision: bool
    future_suffix_forbidden: bool
    protected_evidence_forbidden: bool
    cluster_role_separation_required: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'allowed_roles', 'required_fields', 'feature_names', 'minimum_records', 'minimum_clusters', 'minimum_records_per_regime', 'strict_decision_time_order', 'feature_known_by_decision', 'outcome_after_decision', 'future_suffix_forbidden', 'protected_evidence_forbidden', 'cluster_role_separation_required'}
        exact(value, required, 'calibration dataset')
        output = cls(str(value['exact_version']), tuple(map(str, value['allowed_roles'])), tuple(map(str, value['required_fields'])), tuple(map(str, value['feature_names'])), int(value['minimum_records']), int(value['minimum_clusters']), int(value['minimum_records_per_regime']), bool(value['strict_decision_time_order']), bool(value['feature_known_by_decision']), bool(value['outcome_after_decision']), bool(value['future_suffix_forbidden']), bool(value['protected_evidence_forbidden']), bool(value['cluster_role_separation_required']))
        if set(output.allowed_roles) != ROLES or set(output.required_fields) != REQUIRED_RECORD_FIELDS or len(output.feature_names) < 5:
            raise ContractError('dataset registry mismatch')
        if output.minimum_records < 120 or output.minimum_clusters < 6 or output.minimum_records_per_regime < 20:
            raise ContractError('dataset minima too weak')
        if not all((output.strict_decision_time_order, output.feature_known_by_decision, output.outcome_after_decision, output.future_suffix_forbidden, output.protected_evidence_forbidden, output.cluster_role_separation_required)):
            raise ContractError('dataset safety controls disabled')
        return output

@dataclass(frozen=True)
class ConformalContract:
    exact_version: str
    alpha: float
    score_type: str
    one_sided_lower: bool
    mondrian_field: str
    pooled_fallback: bool
    finite_sample_correction: bool
    minimum_group_size: int
    deterministic: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'alpha', 'score_type', 'one_sided_lower', 'mondrian_field', 'pooled_fallback', 'finite_sample_correction', 'minimum_group_size', 'deterministic'}
        exact(value, required, 'conformal contract')
        output = cls(str(value['exact_version']), probability(value['alpha'], 'alpha', True), str(value['score_type']), bool(value['one_sided_lower']), str(value['mondrian_field']), bool(value['pooled_fallback']), bool(value['finite_sample_correction']), int(value['minimum_group_size']), bool(value['deterministic']))
        if output.alpha >= 0.5 or output.score_type != 'downside_residual' or output.mondrian_field != 'regime' or output.minimum_group_size < 20:
            raise ContractError('unsafe conformal specification')
        if not all((output.one_sided_lower, output.pooled_fallback, output.finite_sample_correction, output.deterministic)):
            raise ContractError('conformal safety controls disabled')
        return output

@dataclass(frozen=True)
class OODContract:
    exact_version: str
    alpha: float
    feature_names: tuple[str, ...]
    methods: tuple[str, ...]
    robust_scale_floor: float
    nearest_neighbor_weight: float
    support_deficit_weight: float
    maximum_feature_missingness: float
    minimum_pvalue: float
    fail_closed: bool
    deterministic: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'alpha', 'feature_names', 'methods', 'robust_scale_floor', 'nearest_neighbor_weight', 'support_deficit_weight', 'maximum_feature_missingness', 'minimum_pvalue', 'fail_closed', 'deterministic'}
        exact(value, required, 'OOD contract')
        output = cls(str(value['exact_version']), probability(value['alpha'], 'alpha', True), tuple(map(str, value['feature_names'])), tuple(map(str, value['methods'])), positive(value['robust_scale_floor'], 'robust_scale_floor'), float(value['nearest_neighbor_weight']), float(value['support_deficit_weight']), probability(value['maximum_feature_missingness'], 'maximum_feature_missingness'), probability(value['minimum_pvalue'], 'minimum_pvalue', True), bool(value['fail_closed']), bool(value['deterministic']))
        if output.alpha >= 0.5 or set(output.methods) != {'robust_mad', 'nearest_neighbor', 'support_deficit'} or min(output.nearest_neighbor_weight, output.support_deficit_weight) < 0:
            raise ContractError('unsafe OOD specification')
        if not output.fail_closed or not output.deterministic:
            raise ContractError('OOD must fail closed and be deterministic')
        return output

@dataclass(frozen=True)
class SelectiveControlContract:
    exact_version: str
    safe_action: str
    minimum_value_lower_bound: float
    minimum_ood_pvalue: float
    minimum_support_score: float
    maximum_missingness: float
    require_action_mask: bool
    require_conformal_gate: bool
    require_ood_gate: bool
    require_support_gate: bool
    baseline_preserved: bool
    fail_closed: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'safe_action', 'minimum_value_lower_bound', 'minimum_ood_pvalue', 'minimum_support_score', 'maximum_missingness', 'require_action_mask', 'require_conformal_gate', 'require_ood_gate', 'require_support_gate', 'baseline_preserved', 'fail_closed'}
        exact(value, required, 'selective control')
        output = cls(str(value['exact_version']), str(value['safe_action']), float(value['minimum_value_lower_bound']), probability(value['minimum_ood_pvalue'], 'minimum_ood_pvalue', True), probability(value['minimum_support_score'], 'minimum_support_score'), probability(value['maximum_missingness'], 'maximum_missingness'), bool(value['require_action_mask']), bool(value['require_conformal_gate']), bool(value['require_ood_gate']), bool(value['require_support_gate']), bool(value['baseline_preserved']), bool(value['fail_closed']))
        if output.safe_action != 'skip' or not all((output.require_action_mask, output.require_conformal_gate, output.require_ood_gate, output.require_support_gate, output.baseline_preserved, output.fail_closed)):
            raise ContractError('unsafe selective controller')
        return output

@dataclass(frozen=True)
class CoverageRiskContract:
    exact_version: str
    risk_definition: str
    minimum_coverage: float
    maximum_selective_risk_upper: float
    threshold_grid: tuple[float, ...]
    bootstrap_draws: int
    confidence_level: float
    monotone_envelope_required: bool
    aurc_required: bool
    cluster_bootstrap_required: bool
    baseline_comparison_required: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'risk_definition', 'minimum_coverage', 'maximum_selective_risk_upper', 'threshold_grid', 'bootstrap_draws', 'confidence_level', 'monotone_envelope_required', 'aurc_required', 'cluster_bootstrap_required', 'baseline_comparison_required'}
        exact(value, required, 'coverage risk')
        output = cls(str(value['exact_version']), str(value['risk_definition']), probability(value['minimum_coverage'], 'minimum_coverage'), probability(value['maximum_selective_risk_upper'], 'maximum_selective_risk_upper'), tuple(map(float, value['threshold_grid'])), int(value['bootstrap_draws']), probability(value['confidence_level'], 'confidence_level', True), bool(value['monotone_envelope_required']), bool(value['aurc_required']), bool(value['cluster_bootstrap_required']), bool(value['baseline_comparison_required']))
        if output.risk_definition != 'negative_realized_value_rate' or len(output.threshold_grid) < 8 or any(left >= right for left, right in zip(output.threshold_grid, output.threshold_grid[1:])):
            raise ContractError('invalid coverage-risk grid')
        if output.bootstrap_draws < 200 or output.confidence_level < 0.8 or not all((output.monotone_envelope_required, output.aurc_required, output.cluster_bootstrap_required, output.baseline_comparison_required)):
            raise ContractError('coverage-risk controls disabled')
        return output

@dataclass(frozen=True)
class AbstentionContract:
    exact_version: str
    target_risk_upper: float
    minimum_coverage: float
    safe_action: str
    objective: str
    tie_break: str
    empty_feasible_set_falls_back: bool
    deterministic: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'target_risk_upper', 'minimum_coverage', 'safe_action', 'objective', 'tie_break', 'empty_feasible_set_falls_back', 'deterministic'}
        exact(value, required, 'abstention')
        output = cls(str(value['exact_version']), probability(value['target_risk_upper'], 'target_risk_upper'), probability(value['minimum_coverage'], 'minimum_coverage'), str(value['safe_action']), str(value['objective']), str(value['tie_break']), bool(value['empty_feasible_set_falls_back']), bool(value['deterministic']))
        if output.safe_action != 'skip' or output.objective != 'maximize_coverage_subject_to_risk_upper' or output.tie_break != 'higher_threshold_then_lower_risk':
            raise ContractError('invalid abstention objective')
        if not output.empty_feasible_set_falls_back or not output.deterministic:
            raise ContractError('abstention must fail closed')
        return output

@dataclass(frozen=True)
class DriftContract:
    exact_version: str
    maximum_ood_rate: float
    maximum_psi: float
    maximum_mean_score_ratio: float
    minimum_window_records: int
    action_on_breach: str
    runtime_mutation_forbidden: bool
    fail_closed: bool

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'maximum_ood_rate', 'maximum_psi', 'maximum_mean_score_ratio', 'minimum_window_records', 'action_on_breach', 'runtime_mutation_forbidden', 'fail_closed'}
        exact(value, required, 'drift')
        output = cls(str(value['exact_version']), probability(value['maximum_ood_rate'], 'maximum_ood_rate'), positive(value['maximum_psi'], 'maximum_psi'), positive(value['maximum_mean_score_ratio'], 'maximum_mean_score_ratio'), int(value['minimum_window_records']), str(value['action_on_breach']), bool(value['runtime_mutation_forbidden']), bool(value['fail_closed']))
        if output.minimum_window_records < 20 or output.action_on_breach != 'research_abstention_only' or not output.runtime_mutation_forbidden or not output.fail_closed:
            raise ContractError('unsafe drift contract')
        return output

@dataclass(frozen=True)
class ResearchBudget:
    exact_version: str
    max_records: int
    max_conformal_fits: int
    max_ood_fits: int
    max_selective_evaluations: int
    max_frontier_points: int
    max_bootstrap_draws: int
    max_drift_windows: int
    max_failures: int
    max_hidden_evaluation_queries: int
    protected_evidence_exposure_limit: int
    runtime_compilation_limit: int
    order_submission_limit: int

    @classmethod
    def from_mapping(cls, value):
        required = {'exact_version', 'max_records', 'max_conformal_fits', 'max_ood_fits', 'max_selective_evaluations', 'max_frontier_points', 'max_bootstrap_draws', 'max_drift_windows', 'max_failures', 'max_hidden_evaluation_queries', 'protected_evidence_exposure_limit', 'runtime_compilation_limit', 'order_submission_limit'}
        exact(value, required, 'research budget')
        positive_keys = ('max_records', 'max_conformal_fits', 'max_ood_fits', 'max_selective_evaluations', 'max_frontier_points', 'max_bootstrap_draws', 'max_drift_windows', 'max_failures')
        output = cls(str(value['exact_version']), int(value['max_records']), int(value['max_conformal_fits']), int(value['max_ood_fits']), int(value['max_selective_evaluations']), int(value['max_frontier_points']), int(value['max_bootstrap_draws']), int(value['max_drift_windows']), int(value['max_failures']), int(value['max_hidden_evaluation_queries']), int(value['protected_evidence_exposure_limit']), int(value['runtime_compilation_limit']), int(value['order_submission_limit']))
        if min(int(value[key]) for key in positive_keys) < 1:
            raise ContractError('positive research budgets required')
        if any((output.max_hidden_evaluation_queries, output.protected_evidence_exposure_limit, output.runtime_compilation_limit, output.order_submission_limit)):
            raise ContractError('authority-bearing budgets must be zero')
        return output
