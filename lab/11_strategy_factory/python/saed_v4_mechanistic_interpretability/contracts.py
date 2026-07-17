from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .errors import ContractError

ROLES={"mechanism_train","mechanism_validation","mechanism_stress","mechanism_negative"}
PATHWAYS={"transfer","adaptation","calibration","view_fusion","treatment_interaction"}
REQUIRED_RECORD_FIELDS={
"record_id","model_id","model_generation","context_id","task_id","cluster_id","role","known_time","decision_time","outcome_observed_at",
"feature_names","feature_values","feature_weights","view_names","view_values","view_weights","layer_ids","layer_matrices","output_weights","bias",
"transfer_sources","adaptation_deltas","calibration_components","calibration_weights","treatment_interactions","support_score","ood_pvalue",
"baseline_score","observed_score","observed_target","future_suffix_accessed","protected_evidence_accessed","immutable_model"
}

def exact(value: Mapping[str,Any], required:set[str], label:str)->None:
    if set(value)!=required:
        raise ContractError(f"{label} field mismatch; unknown={sorted(set(value)-required)}, missing={sorted(required-set(value))}")
def text(v:Any,label:str)->str:
    x=str(v)
    if not x: raise ContractError(f"{label} empty")
    return x
def integer(v:Any,label:str,minimum:int=0)->int:
    x=int(v)
    if x<minimum: raise ContractError(f"{label} below {minimum}")
    return x
def positive(v:Any,label:str)->float:
    x=float(v)
    if x<=0: raise ContractError(f"{label} not positive")
    return x
def probability(v:Any,label:str,open_zero:bool=False)->float:
    x=float(v)
    if (x<=0 if open_zero else x<0) or x>1: raise ContractError(f"{label} outside probability")
    return x

def flags(value: Mapping[str,Any], names:tuple[str,...], label:str)->None:
    if not all(bool(value[n]) for n in names): raise ContractError(f"{label} safety flags disabled")

@dataclass(frozen=True)
class UpstreamIntakeContract:
    exact_version:str; required_phase:str; certificate_hash:str; handoff_hash:str; immutable:bool; hash_verified:bool; research_only:bool; promotion_denied:bool; runtime_denied:bool; online_policy_mutation_denied:bool
    @classmethod
    def from_mapping(cls,v:Mapping[str,Any]):
        required={"exact_version","required_phase","certificate_hash","handoff_hash","immutable","hash_verified","research_only","promotion_denied","runtime_denied","online_policy_mutation_denied"}; exact(v,required,"upstream intake")
        out=cls(text(v["exact_version"],"exact_version"),text(v["required_phase"],"required_phase"),text(v["certificate_hash"],"certificate_hash"),text(v["handoff_hash"],"handoff_hash"),bool(v["immutable"]),bool(v["hash_verified"]),bool(v["research_only"]),bool(v["promotion_denied"]),bool(v["runtime_denied"]),bool(v["online_policy_mutation_denied"]))
        if out.required_phase!="SAED_V4_25": raise ContractError("V4-26 requires exact V4-25")
        flags(v,("immutable","hash_verified","research_only","promotion_denied","runtime_denied","online_policy_mutation_denied"),"upstream intake")
        return out

@dataclass(frozen=True)
class MechanismDatasetContract:
    exact_version:str; allowed_roles:tuple[str,...]; required_fields:tuple[str,...]; minimum_records:int; minimum_models:int; minimum_contexts:int; minimum_records_per_role:int; strict_known_time:bool; cluster_role_separation_required:bool; immutable_models_required:bool; future_suffix_forbidden:bool; protected_evidence_forbidden:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","allowed_roles","required_fields","minimum_records","minimum_models","minimum_contexts","minimum_records_per_role","strict_known_time","cluster_role_separation_required","immutable_models_required","future_suffix_forbidden","protected_evidence_forbidden"}; exact(v,required,"mechanism dataset")
        out=cls(text(v["exact_version"],"exact_version"),tuple(map(str,v["allowed_roles"])),tuple(map(str,v["required_fields"])),integer(v["minimum_records"],"minimum_records",16),integer(v["minimum_models"],"minimum_models",1),integer(v["minimum_contexts"],"minimum_contexts",2),integer(v["minimum_records_per_role"],"minimum_records_per_role",2),bool(v["strict_known_time"]),bool(v["cluster_role_separation_required"]),bool(v["immutable_models_required"]),bool(v["future_suffix_forbidden"]),bool(v["protected_evidence_forbidden"]))
        if set(out.allowed_roles)!=ROLES or set(out.required_fields)!=REQUIRED_RECORD_FIELDS: raise ContractError("dataset registries mismatch")
        flags(v,("strict_known_time","cluster_role_separation_required","immutable_models_required","future_suffix_forbidden","protected_evidence_forbidden"),"mechanism dataset")
        return out

@dataclass(frozen=True)
class AttributionContract:
    exact_version:str; method:str; integration_steps:int; baseline_value:float; normalize_abs_sum:bool; maximum_feature_concentration:float; future_suffix_forbidden:bool; deterministic:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","method","integration_steps","baseline_value","normalize_abs_sum","maximum_feature_concentration","future_suffix_forbidden","deterministic"}; exact(v,required,"attribution")
        out=cls(text(v["exact_version"],"exact_version"),text(v["method"],"method"),integer(v["integration_steps"],"integration_steps",4),float(v["baseline_value"]),bool(v["normalize_abs_sum"]),probability(v["maximum_feature_concentration"],"maximum_feature_concentration",True),bool(v["future_suffix_forbidden"]),bool(v["deterministic"]))
        if out.method!="integrated_gradients_plus_occlusion" or not out.future_suffix_forbidden or not out.deterministic: raise ContractError("unsafe attribution contract")
        return out

@dataclass(frozen=True)
class PathwayContract:
    exact_version:str; allowed_pathways:tuple[str,...]; ablation_method:str; minimum_pathway_count:int; maximum_pathway_concentration:float; baseline_preserved:bool; deterministic:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","allowed_pathways","ablation_method","minimum_pathway_count","maximum_pathway_concentration","baseline_preserved","deterministic"}; exact(v,required,"pathway")
        out=cls(text(v["exact_version"],"exact_version"),tuple(map(str,v["allowed_pathways"])),text(v["ablation_method"],"ablation_method"),integer(v["minimum_pathway_count"],"minimum_pathway_count",3),probability(v["maximum_pathway_concentration"],"maximum_pathway_concentration",True),bool(v["baseline_preserved"]),bool(v["deterministic"]))
        if set(out.allowed_pathways)!=PATHWAYS or out.ablation_method!="frozen_component_zero_ablation" or not out.baseline_preserved or not out.deterministic: raise ContractError("unsafe pathway contract")
        return out

@dataclass(frozen=True)
class ConceptProbeContract:
    exact_version:str; concept_names:tuple[str,...]; concept_vectors:tuple[tuple[float,...],...]; minimum_validation_records:int; random_control_required:bool; minimum_signal_over_random:float; deterministic:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","concept_names","concept_vectors","minimum_validation_records","random_control_required","minimum_signal_over_random","deterministic"}; exact(v,required,"concept probe")
        names=tuple(map(str,v["concept_names"])); vectors=tuple(tuple(map(float,x)) for x in v["concept_vectors"])
        out=cls(text(v["exact_version"],"exact_version"),names,vectors,integer(v["minimum_validation_records"],"minimum_validation_records",4),bool(v["random_control_required"]),float(v["minimum_signal_over_random"]),bool(v["deterministic"]))
        if len(names)!=len(vectors) or len(names)<3 or len({len(x) for x in vectors})!=1 or not out.random_control_required or not out.deterministic: raise ContractError("invalid concept registry")
        return out

@dataclass(frozen=True)
class CausalTraceContract:
    exact_version:str; layer_ids:tuple[str,...]; intervention:str; maximum_neurons_per_layer:int; same_model_required:bool; past_only_patch_sources:bool; baseline_preserved:bool; deterministic:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","layer_ids","intervention","maximum_neurons_per_layer","same_model_required","past_only_patch_sources","baseline_preserved","deterministic"}; exact(v,required,"causal trace")
        out=cls(text(v["exact_version"],"exact_version"),tuple(map(str,v["layer_ids"])),text(v["intervention"],"intervention"),integer(v["maximum_neurons_per_layer"],"maximum_neurons_per_layer",1),bool(v["same_model_required"]),bool(v["past_only_patch_sources"]),bool(v["baseline_preserved"]),bool(v["deterministic"]))
        if out.intervention!="zero_activation_and_past_only_patch" or len(out.layer_ids)!=2: raise ContractError("trace contract mismatch")
        flags(v,("same_model_required","past_only_patch_sources","baseline_preserved","deterministic"),"causal trace")
        return out

@dataclass(frozen=True)
class CounterfactualContract:
    exact_version:str; maximum_feature_changes:int; perturbation_grid:tuple[float,...]; decision_threshold:float; maximum_absolute_perturbation:float; immutable_model:bool; deterministic_tie_break:str; deterministic:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","maximum_feature_changes","perturbation_grid","decision_threshold","maximum_absolute_perturbation","immutable_model","deterministic_tie_break","deterministic"}; exact(v,required,"counterfactual")
        out=cls(text(v["exact_version"],"exact_version"),integer(v["maximum_feature_changes"],"maximum_feature_changes",1),tuple(map(float,v["perturbation_grid"])),probability(v["decision_threshold"],"decision_threshold",True),positive(v["maximum_absolute_perturbation"],"maximum_absolute_perturbation"),bool(v["immutable_model"]),text(v["deterministic_tie_break"],"deterministic_tie_break"),bool(v["deterministic"]))
        if out.maximum_feature_changes!=1 or not out.immutable_model or not out.deterministic or sorted(out.perturbation_grid)!=list(out.perturbation_grid): raise ContractError("counterfactual contract mismatch")
        return out

@dataclass(frozen=True)
class SparseDictionaryContract:
    exact_version:str; dictionary_size:int; top_k:int; minimum_records:int; maximum_reconstruction_error:float; randomized_control_required:bool; deterministic:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","dictionary_size","top_k","minimum_records","maximum_reconstruction_error","randomized_control_required","deterministic"}; exact(v,required,"sparse dictionary")
        out=cls(text(v["exact_version"],"exact_version"),integer(v["dictionary_size"],"dictionary_size",2),integer(v["top_k"],"top_k",1),integer(v["minimum_records"],"minimum_records",8),positive(v["maximum_reconstruction_error"],"maximum_reconstruction_error"),bool(v["randomized_control_required"]),bool(v["deterministic"]))
        if out.top_k>out.dictionary_size or not out.randomized_control_required or not out.deterministic: raise ContractError("dictionary contract mismatch")
        return out

@dataclass(frozen=True)
class FaithfulnessContract:
    exact_version:str; minimum_deletion_drop:float; minimum_attribution_score_correlation:float; randomization_rank_correlation_ceiling:float; stability_cosine_floor:float; critical_shortcuts_forbidden:bool; fail_closed:bool
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","minimum_deletion_drop","minimum_attribution_score_correlation","randomization_rank_correlation_ceiling","stability_cosine_floor","critical_shortcuts_forbidden","fail_closed"}; exact(v,required,"faithfulness")
        out=cls(text(v["exact_version"],"exact_version"),float(v["minimum_deletion_drop"]),float(v["minimum_attribution_score_correlation"]),float(v["randomization_rank_correlation_ceiling"]),float(v["stability_cosine_floor"]),bool(v["critical_shortcuts_forbidden"]),bool(v["fail_closed"]))
        if not out.critical_shortcuts_forbidden or not out.fail_closed: raise ContractError("faithfulness must fail closed")
        return out

@dataclass(frozen=True)
class ResearchBudget:
    exact_version:str; maximum_records:int; maximum_feature_ablations:int; maximum_pathway_ablations:int; maximum_concept_probes:int; maximum_trace_interventions:int; maximum_patch_interventions:int; maximum_counterfactual_trials:int; maximum_dictionary_trials:int; maximum_hidden_evaluation_queries:int; maximum_protected_evidence_exposures:int; maximum_runtime_compilations:int; maximum_order_submissions:int; maximum_online_policy_mutations:int
    @classmethod
    def from_mapping(cls,v):
        required={"exact_version","maximum_records","maximum_feature_ablations","maximum_pathway_ablations","maximum_concept_probes","maximum_trace_interventions","maximum_patch_interventions","maximum_counterfactual_trials","maximum_dictionary_trials","maximum_hidden_evaluation_queries","maximum_protected_evidence_exposures","maximum_runtime_compilations","maximum_order_submissions","maximum_online_policy_mutations"}; exact(v,required,"research budget")
        vals=[text(v["exact_version"],"exact_version")]+[integer(v[k],k,0) for k in sorted(required-{"exact_version"})]
        # Explicit construction avoids dependence on sorted field order.
        out=cls(text(v["exact_version"],"exact_version"),*[integer(v[k],k,0) for k in ["maximum_records","maximum_feature_ablations","maximum_pathway_ablations","maximum_concept_probes","maximum_trace_interventions","maximum_patch_interventions","maximum_counterfactual_trials","maximum_dictionary_trials","maximum_hidden_evaluation_queries","maximum_protected_evidence_exposures","maximum_runtime_compilations","maximum_order_submissions","maximum_online_policy_mutations"]])
        if any(getattr(out,k)!=0 for k in ["maximum_hidden_evaluation_queries","maximum_protected_evidence_exposures","maximum_runtime_compilations","maximum_order_submissions","maximum_online_policy_mutations"]): raise ContractError("forbidden budget is nonzero")
        return out

def parse_config(config:Mapping[str,Any])->dict[str,Any]:
    required={"upstream_intake","mechanism_dataset_contract","attribution_contract","pathway_contract","concept_probe_contract","causal_trace_contract","counterfactual_contract","sparse_dictionary_contract","faithfulness_contract","research_budget"}; exact(config,required,"full config")
    return {
      "upstream_intake":UpstreamIntakeContract.from_mapping(config["upstream_intake"]),
      "mechanism_dataset_contract":MechanismDatasetContract.from_mapping(config["mechanism_dataset_contract"]),
      "attribution_contract":AttributionContract.from_mapping(config["attribution_contract"]),
      "pathway_contract":PathwayContract.from_mapping(config["pathway_contract"]),
      "concept_probe_contract":ConceptProbeContract.from_mapping(config["concept_probe_contract"]),
      "causal_trace_contract":CausalTraceContract.from_mapping(config["causal_trace_contract"]),
      "counterfactual_contract":CounterfactualContract.from_mapping(config["counterfactual_contract"]),
      "sparse_dictionary_contract":SparseDictionaryContract.from_mapping(config["sparse_dictionary_contract"]),
      "faithfulness_contract":FaithfulnessContract.from_mapping(config["faithfulness_contract"]),
      "research_budget":ResearchBudget.from_mapping(config["research_budget"]),
    }
