from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

TREATMENT_ROLES={'skip','manual_baseline','candidate'}
ESTIMATORS={'difference_in_means','s_learner_ridge','t_learner_ridge','r_learner_linear','aipw_dr'}
POLICY_TYPES={'skip_all','fixed_treatment','manual_rule','uplift_argmax','conservative_lcb'}
DIRECTIVES={'continue_reference','baseline','abstain','manual','reject','quarantine','stop_family'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')
def increasing(xs): return all(a<b for a,b in zip(xs,xs[1:]))

@dataclass(frozen=True)
class TreatmentRegistry:
    exact_version:str; treatments:tuple[dict,...]; baseline_treatment_id:str; manual_treatment_id:str; finite:bool; frozen:bool; runtime_selectable:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','treatments','baseline_treatment_id','manual_treatment_id','finite','frozen','runtime_selectable'};exact(x,keys,'treatment registry')
        treatments=tuple(dict(v) for v in x['treatments']);required={'treatment_id','role','description','action_atoms','known_time_rule','synthetic_only','enabled'};ids=[]
        for v in treatments:
            exact(v,required,'treatment');ids.append(str(v['treatment_id']))
            if v['role'] not in TREATMENT_ROLES or not isinstance(v['action_atoms'],list) or not v['action_atoms'] or not v['synthetic_only']:raise ContractError('invalid treatment semantics')
        o=cls(str(x['exact_version']),treatments,str(x['baseline_treatment_id']),str(x['manual_treatment_id']),bool(x['finite']),bool(x['frozen']),bool(x['runtime_selectable']))
        if len(ids)!=len(set(ids)) or len(ids)<3 or o.baseline_treatment_id not in ids or o.manual_treatment_id not in ids:raise ContractError('invalid treatment anchors')
        if not(o.finite and o.frozen) or o.runtime_selectable:raise ContractError('treatment authority safeguards absent')
        return o

@dataclass(frozen=True)
class OutcomeSpec:
    exact_version:str; outcome_id:str; utility_unit:str; horizon_bars:int; higher_is_better:bool; cost_adjusted:bool; censored_rows_allowed:bool; known_time_rule:str; negative_control_outcome_id:str; protected_final_role:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','outcome_id','utility_unit','horizon_bars','higher_is_better','cost_adjusted','censored_rows_allowed','known_time_rule','negative_control_outcome_id','protected_final_role'};exact(x,keys,'outcome spec')
        o=cls(str(x['exact_version']),str(x['outcome_id']),str(x['utility_unit']),int(x['horizon_bars']),bool(x['higher_is_better']),bool(x['cost_adjusted']),bool(x['censored_rows_allowed']),str(x['known_time_rule']),str(x['negative_control_outcome_id']),bool(x['protected_final_role']))
        if o.horizon_bars<1 or not(o.higher_is_better and o.cost_adjusted and o.known_time_rule) or o.protected_final_role:raise ContractError('invalid outcome safeguards')
        return o

@dataclass(frozen=True)
class IdentificationPlan:
    exact_version:str; estimand:str; comparison_baseline:str; assumptions:tuple[str,...]; overlap_floor:float; propensity_clip:float; min_effective_sample_size:float; cluster_key:str; chronology_key:str; purge_rows:int; embargo_rows:int; cross_fit_folds:int; future_training_forbidden:bool; sibling_split_forbidden:bool; synthetic_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','estimand','comparison_baseline','assumptions','overlap_floor','propensity_clip','min_effective_sample_size','cluster_key','chronology_key','purge_rows','embargo_rows','cross_fit_folds','future_training_forbidden','sibling_split_forbidden','synthetic_only'};exact(x,keys,'identification plan')
        o=cls(str(x['exact_version']),str(x['estimand']),str(x['comparison_baseline']),tuple(map(str,x['assumptions'])),float(x['overlap_floor']),float(x['propensity_clip']),float(x['min_effective_sample_size']),str(x['cluster_key']),str(x['chronology_key']),int(x['purge_rows']),int(x['embargo_rows']),int(x['cross_fit_folds']),bool(x['future_training_forbidden']),bool(x['sibling_split_forbidden']),bool(x['synthetic_only']))
        if o.estimand not in {'ate','cate','policy_value'} or not 0<o.overlap_floor<0.5 or not 0<o.propensity_clip<0.5 or o.min_effective_sample_size<10 or o.cross_fit_folds<3:raise ContractError('invalid identification parameters')
        if not(o.future_training_forbidden and o.sibling_split_forbidden and o.synthetic_only) or len(o.assumptions)<4:raise ContractError('identification safeguards absent')
        return o

@dataclass(frozen=True)
class EstimatorSpec:
    estimator_id:str; algorithm:str; complexity_tier:int; ridge:float; enabled:bool; supports_multitreatment:bool; orthogonal:bool; cross_fitted:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'estimator_id','algorithm','complexity_tier','ridge','enabled','supports_multitreatment','orthogonal','cross_fitted'};exact(x,keys,'estimator')
        o=cls(str(x['estimator_id']),str(x['algorithm']),int(x['complexity_tier']),float(x['ridge']),bool(x['enabled']),bool(x['supports_multitreatment']),bool(x['orthogonal']),bool(x['cross_fitted']))
        if o.algorithm not in ESTIMATORS or o.complexity_tier<0 or o.ridge<0 or not o.supports_multitreatment:raise ContractError('invalid estimator')
        return o

@dataclass(frozen=True)
class PolicySpec:
    policy_id:str; policy_type:str; treatment_id:str; minimum_uplift:float; abstain_on_support_failure:bool; preserve_manual_fallback:bool; evaluation_only:bool; enabled:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'policy_id','policy_type','treatment_id','minimum_uplift','abstain_on_support_failure','preserve_manual_fallback','evaluation_only','enabled'};exact(x,keys,'policy')
        o=cls(str(x['policy_id']),str(x['policy_type']),str(x['treatment_id']),float(x['minimum_uplift']),bool(x['abstain_on_support_failure']),bool(x['preserve_manual_fallback']),bool(x['evaluation_only']),bool(x['enabled']))
        if o.policy_type not in POLICY_TYPES or o.minimum_uplift<0 or not(o.abstain_on_support_failure and o.preserve_manual_fallback):raise ContractError('invalid policy')
        return o

@dataclass(frozen=True)
class ComputeExposureBudget:
    max_rows:int; max_treatments:int; max_estimators:int; max_policies:int; max_cross_fit_folds:int; max_bootstrap_replicates:int; max_sensitivity_runs:int; max_failures:int; max_retries:int; protected_evidence_exposure_limit:int; hidden_evaluation_query_limit:int
    @classmethod
    def from_mapping(cls,x):
        keys={'max_rows','max_treatments','max_estimators','max_policies','max_cross_fit_folds','max_bootstrap_replicates','max_sensitivity_runs','max_failures','max_retries','protected_evidence_exposure_limit','hidden_evaluation_query_limit'};exact(x,keys,'compute exposure budget')
        vals=[int(x[k]) for k in ['max_rows','max_treatments','max_estimators','max_policies','max_cross_fit_folds','max_bootstrap_replicates','max_sensitivity_runs','max_failures','max_retries','protected_evidence_exposure_limit','hidden_evaluation_query_limit']]
        o=cls(*vals)
        if min(vals[:7])<1 or min(vals[7:])<0 or o.protected_evidence_exposure_limit!=0 or o.hidden_evaluation_query_limit!=0:raise ContractError('invalid exposure budget')
        return o
