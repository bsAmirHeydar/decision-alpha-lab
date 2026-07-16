from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from .errors import ContractError

ALGORITHMS={'late_mean_baseline','quality_gated','masked_cross_attention_reference','evidential_product_of_experts','disagreement_aware_mixture'}
ACTIONS={'fuse','baseline','abstain','manual','reject','quarantine'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')

@dataclass(frozen=True)
class FusionConfig:
    exact_version:str; common_dim:int; required_view_names:tuple[str,...]; optional_view_names:tuple[str,...]; critical_view_names:tuple[str,...]; max_view_age_seconds:int; min_view_quality:float; max_gate_concentration:float; disagreement_threshold:float; uncertainty_inflation:float; modality_dropout_rate:float; known_time_only:bool; frozen_upstream:bool
    @classmethod
    def from_mapping(cls,x):
        r={'exact_version','common_dim','required_view_names','optional_view_names','critical_view_names','max_view_age_seconds','min_view_quality','max_gate_concentration','disagreement_threshold','uncertainty_inflation','modality_dropout_rate','known_time_only','frozen_upstream'};exact(x,r,'fusion config')
        o=cls(str(x['exact_version']),int(x['common_dim']),tuple(map(str,x['required_view_names'])),tuple(map(str,x['optional_view_names'])),tuple(map(str,x['critical_view_names'])),int(x['max_view_age_seconds']),float(x['min_view_quality']),float(x['max_gate_concentration']),float(x['disagreement_threshold']),float(x['uncertainty_inflation']),float(x['modality_dropout_rate']),bool(x['known_time_only']),bool(x['frozen_upstream']))
        allv=o.required_view_names+o.optional_view_names
        if o.common_dim<4 or o.max_view_age_seconds<0: raise ContractError('invalid fusion dimensions or age')
        if len(allv)!=len(set(allv)) or not set(o.critical_view_names)<=set(o.required_view_names): raise ContractError('invalid view taxonomy')
        if not 0<=o.min_view_quality<=1 or not 0<o.max_gate_concentration<=1 or o.disagreement_threshold<0 or o.uncertainty_inflation<1 or not 0<=o.modality_dropout_rate<1: raise ContractError('invalid thresholds')
        if not o.known_time_only or not o.frozen_upstream: raise ContractError('mandatory safety flags must be true')
        return o

@dataclass(frozen=True)
class CandidateSpec:
    candidate_id:str; algorithm:str; seed:int; requires_foundation_views:bool; min_foundation_views:int; min_domain_views:int; dropout_enabled:bool; enabled:bool
    @classmethod
    def from_mapping(cls,x):
        r={'candidate_id','algorithm','seed','requires_foundation_views','min_foundation_views','min_domain_views','dropout_enabled','enabled'};exact(x,r,'candidate')
        o=cls(str(x['candidate_id']),str(x['algorithm']),int(x['seed']),bool(x['requires_foundation_views']),int(x['min_foundation_views']),int(x['min_domain_views']),bool(x['dropout_enabled']),bool(x['enabled']))
        if o.algorithm not in ALGORITHMS or min(o.min_foundation_views,o.min_domain_views)<0: raise ContractError('invalid candidate')
        if o.algorithm=='late_mean_baseline' and o.requires_foundation_views: raise ContractError('baseline cannot require foundation views')
        return o

@dataclass(frozen=True)
class SupportPolicy:
    missing_required_action:str; missing_critical_action:str; stale_required_action:str; corrupt_action:str; foundation_missing_action:str; ood_action:str; baseline_candidate_id:str
    @classmethod
    def from_mapping(cls,x):
        r={'missing_required_action','missing_critical_action','stale_required_action','corrupt_action','foundation_missing_action','ood_action','baseline_candidate_id'};exact(x,r,'support policy')
        o=cls(*(str(x[k]) for k in ['missing_required_action','missing_critical_action','stale_required_action','corrupt_action','foundation_missing_action','ood_action','baseline_candidate_id']))
        if any(v not in ACTIONS for v in [o.missing_required_action,o.missing_critical_action,o.stale_required_action,o.corrupt_action,o.foundation_missing_action,o.ood_action]): raise ContractError('unknown support action')
        return o

@dataclass(frozen=True)
class MissingnessPolicy:
    exhaustive_domain_subsets:bool; exhaustive_foundation_subsets:bool; certify_only_trained_subsets:bool; max_missing_optional:int; structured_patterns:tuple[str,...]
    @classmethod
    def from_mapping(cls,x):
        r={'exhaustive_domain_subsets','exhaustive_foundation_subsets','certify_only_trained_subsets','max_missing_optional','structured_patterns'};exact(x,r,'missingness policy')
        o=cls(bool(x['exhaustive_domain_subsets']),bool(x['exhaustive_foundation_subsets']),bool(x['certify_only_trained_subsets']),int(x['max_missing_optional']),tuple(map(str,x['structured_patterns'])))
        if not(o.exhaustive_domain_subsets and o.exhaustive_foundation_subsets and o.certify_only_trained_subsets) or o.max_missing_optional<0 or not o.structured_patterns: raise ContractError('invalid missingness policy')
        return o

@dataclass(frozen=True)
class ComputeExposureBudget:
    max_candidates:int; max_fusion_calls:int; max_domain_subset_evaluations:int; max_foundation_subset_evaluations:int; max_dropout_patterns:int; max_total_vector_dimensions:int; max_failures:int; max_retries:int
    @classmethod
    def from_mapping(cls,x):
        keys=['max_candidates','max_fusion_calls','max_domain_subset_evaluations','max_foundation_subset_evaluations','max_dropout_patterns','max_total_vector_dimensions','max_failures','max_retries'];exact(x,set(keys),'compute exposure budget')
        o=cls(*(int(x[k]) for k in keys))
        if min(o.max_candidates,o.max_fusion_calls,o.max_domain_subset_evaluations,o.max_foundation_subset_evaluations,o.max_dropout_patterns,o.max_total_vector_dimensions)<1 or min(o.max_failures,o.max_retries)<0: raise ContractError('invalid budget')
        return o
