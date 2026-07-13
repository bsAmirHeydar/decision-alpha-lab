from dataclasses import dataclass,field,asdict
from typing import Mapping,Any
from .canonical import canonical_sha256,stable_id
from .enums import *

@dataclass(frozen=True,slots=True)
class AdvancedAlgorithmDescriptor:
 algorithm_id:str;algorithm_version:str;family:AdvancedTaskFamily;formulation:str;tasks:tuple[str,...];native:bool;deterministic_level:str;required_fields:tuple[str,...];output_semantics:tuple[str,...];export_formats:tuple[str,...]=('native_json',);optional_dependency:str='';default_parameters:Mapping[str,Any]=field(default_factory=dict);limitations:tuple[str,...]=()
 @property
 def key(self):return f'{self.algorithm_id}@{self.algorithm_version}'
 @property
 def descriptor_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class RankingPair:pair_id:str;group_id:str;preferred_row_id:str;other_row_id:str;weight:float;utility_gap:float
@dataclass(frozen=True,slots=True)
class RankingMetricReport:
 report_id:str;group_count:int;row_count:int;pair_count:int;pairwise_accuracy:float;mean_ndcg_at_k:float;mean_map_at_k:float;mean_top_k_utility:float;k:int;group_weights_hash:str;evidence_hash:str

@dataclass(frozen=True,slots=True)
class TreatmentAction:
 action_id:str;action_version:str;compatible:bool;minimum_support:int;economic_max_loss:float;tags:tuple[str,...]=()
 @property
 def key(self):return f'{self.action_id}@{self.action_version}'
@dataclass(frozen=True,slots=True)
class ActionMask:
 mask_id:str;opportunity_id:str;allowed_action_keys:tuple[str,...];blocked_reasons:Mapping[str,str];known_time_ms:int;evidence_hash:str
@dataclass(frozen=True,slots=True)
class TreatmentSupportEntry:
 action_key:str;count:int;effective_sample_size:float;minimum_propensity:float;maximum_propensity:float;state:SupportState;reason:str
@dataclass(frozen=True,slots=True)
class TreatmentSupportAudit:
 audit_id:str;dataset_id:str;entries:tuple[TreatmentSupportEntry,...];all_declared_actions_observed:bool;overlap_sufficient:bool;blockers:tuple[str,...];warnings:tuple[str,...];evidence_hash:str
@dataclass(frozen=True,slots=True)
class TreatmentChoicePrediction:
 prediction_id:str;row_id:str;allowed_action_keys:tuple[str,...];utility_by_action:Mapping[str,float];uncertainty_by_action:Mapping[str,float];chosen_action_key:str;decision:PolicyDecision;reason:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class DoublyRobustReport:
 report_id:str;policy_id:str;row_count:int;estimated_value:float;standard_error:float;effective_sample_size:float;clipped_propensity_count:int;support_audit_id:str;evidence_hash:str

@dataclass(frozen=True,slots=True)
class SurvivalObservation:
 row_id:str;duration_ms:int;event:int;cause:int;weight:float;known_time_ms:int
@dataclass(frozen=True,slots=True)
class SurvivalCurve:
 curve_id:str;row_id:str;horizons_ms:tuple[int,...];survival:tuple[float,...];cumulative_hazard:tuple[float,...];model_key:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class CompetingRiskCurve:
 curve_id:str;row_id:str;horizons_ms:tuple[int,...];cause_ids:tuple[int,...];cumulative_incidence:tuple[tuple[float,...],...];overall_survival:tuple[float,...];evidence_hash:str
@dataclass(frozen=True,slots=True)
class SurvivalMetricReport:
 report_id:str;concordance_index:float;integrated_brier_score:float;time_dependent_calibration_error:float;event_count:int;censored_count:int;comparable_pairs:int;horizons_ms:tuple[int,...];evidence_hash:str

@dataclass(frozen=True,slots=True)
class QuantilePrediction:
 prediction_id:str;row_id:str;levels:tuple[float,...];values:tuple[float,...];monotone:bool;evidence_hash:str
@dataclass(frozen=True,slots=True)
class ConformalInterval:
 interval_id:str;row_id:str;alpha:float;lower:float;upper:float;kind:IntervalKind;calibration_size:int;group_key:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class DistributionalRiskSummary:
 summary_id:str;row_id:str;expected_value:float;probability_positive:float;value_at_risk:float;conditional_value_at_risk:float;probability_target_first:float;probability_stop_first:float;tail_level:float;evidence_hash:str
@dataclass(frozen=True,slots=True)
class DistributionalMetricReport:
 report_id:str;pinball_by_level:Mapping[str,float];interval_coverage:float;interval_width:float;tail_calibration_error:float;row_count:int;evidence_hash:str

@dataclass(frozen=True,slots=True)
class MultiTaskHeadResult:
 task_key:str;loss:float;weight:float;prediction_hash:str
@dataclass(frozen=True,slots=True)
class MultiTaskLossReport:
 report_id:str;heads:tuple[MultiTaskHeadResult,...];weighted_loss:float;gradient_balance_score:float;shared_representation_hash:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class RegimeAssignment:
 assignment_id:str;row_id:str;regime_id:str;probability:float;support_count:int;fallback_used:bool;fallback_reason:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class ExpertGateResult:
 result_id:str;row_id:str;selected_expert_key:str;global_model_used:bool;regime_id:str;support_count:int;decision:GateDecision;reason:str;evidence_hash:str

@dataclass(frozen=True,slots=True)
class LoggedPolicyRow:
 row_id:str;state_features:tuple[float,...];logged_action_key:str;reward:float;propensity:float;allowed_action_keys:tuple[str,...];cluster_id:str;known_time_ms:int
@dataclass(frozen=True,slots=True)
class PolicySupportAudit:
 audit_id:str;declared_action_keys:tuple[str,...];observed_action_keys:tuple[str,...];unseen_action_keys:tuple[str,...];masked_violation_count:int;minimum_action_count:int;minimum_propensity:float;decision:GateDecision;blockers:tuple[str,...];evidence_hash:str
@dataclass(frozen=True,slots=True)
class PolicyActionScore:
 action_key:str;mean_utility:float;uncertainty:float;conservative_value:float;support_count:int;support_state:SupportState
@dataclass(frozen=True,slots=True)
class ConservativePolicyDecision:
 decision_id:str;row_id:str;scores:tuple[PolicyActionScore,...];selected_action_key:str;baseline_action_key:str;decision:PolicyDecision;improvement_lower_bound:float;reason:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class LoggedPolicyComparison:
 report_id:str;candidate_policy_id:str;baseline_policy_id:str;candidate_value:float;baseline_value:float;improvement:float;improvement_standard_error:float;lower_confidence_bound:float;effective_sample_size:float;support_audit_id:str;decision:GateDecision;evidence_hash:str

@dataclass(frozen=True,slots=True)
class TaskComparisonObservation:
 observation_id:str;context_id:str;task_family:AdvancedTaskFamily;algorithm_key:str;status:str;primary_metric:str;primary_value:float;economic_utility:float;calibration_value:float;support_gate:GateDecision;deterministic:bool;fit_ms:int;predict_ms:int;artifact_hash:str;limitations:tuple[str,...]=()
@dataclass(frozen=True,slots=True)
class TaskComparisonReport:
 report_id:str;context_id:str;dataset_manifest_hash:str;observations:tuple[TaskComparisonObservation,...];attempted_families:tuple[AdvancedTaskFamily,...];missing_families:tuple[AdvancedTaskFamily,...];best_by_family:Mapping[str,str];promotion_ready:bool;blockers:tuple[str,...];warnings:tuple[str,...];evidence_hash:str
@dataclass(frozen=True,slots=True)
class AdvancedTaskRegistrySnapshot:
 snapshot_id:str;descriptors:tuple[AdvancedAlgorithmDescriptor,...];frozen:bool;evidence_hash:str
