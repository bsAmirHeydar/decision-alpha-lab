from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

OBJECTIVES={'maximin_utility','minimax_regret','distributionally_robust','robust_cvar','lexicographic'}
AMBIGUITY_FAMILIES={'scenario_convex_hull','wasserstein_l1','kl_ball_reference','moment_box','hybrid'}
REGRET_MODES={'absolute','relative','baseline_relative'}
TIE_POLICIES={'canonical_id','baseline_first','abstain'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')

def _nonempty(s,label):
    if not str(s): raise ContractError(f'{label} is empty')
    return str(s)

@dataclass(frozen=True)
class UpstreamIntakeContract:
    exact_version:str;required_phase:str;selection_certificate_hash:str;selection_registry_hash:str;exposure_ledger_hash:str;immutable:bool;hash_verified:bool;research_only:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','required_phase','selection_certificate_hash','selection_registry_hash','exposure_ledger_hash','immutable','hash_verified','research_only'},'upstream intake')
        o=cls(*[_nonempty(x[k],k) for k in ['exact_version','required_phase','selection_certificate_hash','selection_registry_hash','exposure_ledger_hash']],bool(x['immutable']),bool(x['hash_verified']),bool(x['research_only']))
        if o.required_phase!='SAED_V4_20' or not(o.immutable and o.hash_verified and o.research_only): raise ContractError('unsafe upstream intake')
        return o

@dataclass(frozen=True)
class AmbiguitySetContract:
    exact_version:str;family:str;radius:float;probability_floor:float;mean_shift_bound:float;cost_shock_bound:float;tail_shock_bound:float;support_shock_bound:float;closed_support:bool;data_dependent_radius:bool;synthetic_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','family','radius','probability_floor','mean_shift_bound','cost_shock_bound','tail_shock_bound','support_shock_bound','closed_support','data_dependent_radius','synthetic_only'};exact(x,keys,'ambiguity set')
        o=cls(str(x['exact_version']),str(x['family']),*[float(x[k]) for k in ['radius','probability_floor','mean_shift_bound','cost_shock_bound','tail_shock_bound','support_shock_bound']],bool(x['closed_support']),bool(x['data_dependent_radius']),bool(x['synthetic_only']))
        if o.family not in AMBIGUITY_FAMILIES or min(o.radius,o.probability_floor,o.mean_shift_bound,o.cost_shock_bound,o.tail_shock_bound,o.support_shock_bound)<0 or o.probability_floor>=1 or not(o.closed_support and o.synthetic_only) or o.data_dependent_radius: raise ContractError('unsafe ambiguity set')
        return o

@dataclass(frozen=True)
class ScenarioContract:
    exact_version:str;native_scenarios:tuple[str,...];shock_axes:tuple[str,...];max_scenarios:int;include_joint_adverse:bool;include_benign_control:bool;include_leave_one_out:bool;future_suffix_forbidden:bool;protected_evidence_forbidden:bool;deterministic:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','native_scenarios','shock_axes','max_scenarios','include_joint_adverse','include_benign_control','include_leave_one_out','future_suffix_forbidden','protected_evidence_forbidden','deterministic'};exact(x,keys,'scenario')
        o=cls(str(x['exact_version']),tuple(map(str,x['native_scenarios'])),tuple(map(str,x['shock_axes'])),int(x['max_scenarios']),bool(x['include_joint_adverse']),bool(x['include_benign_control']),bool(x['include_leave_one_out']),bool(x['future_suffix_forbidden']),bool(x['protected_evidence_forbidden']),bool(x['deterministic']))
        allowed={'cost','tail','support','latency','calibration','joint','benign'}
        if not o.native_scenarios or not set(o.shock_axes)<=allowed or o.max_scenarios<1 or not(o.include_joint_adverse and o.include_benign_control and o.future_suffix_forbidden and o.protected_evidence_forbidden and o.deterministic): raise ContractError('unsafe scenario contract')
        return o

@dataclass(frozen=True)
class RobustOptimizationContract:
    exact_version:str;objective:str;mixture_allowed:bool;grid_step:float;max_active_treatments:int;diversification_penalty:float;complexity_penalty:float;baseline_preservation:bool;fail_closed:bool;deterministic:bool;runtime_executable:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','objective','mixture_allowed','grid_step','max_active_treatments','diversification_penalty','complexity_penalty','baseline_preservation','fail_closed','deterministic','runtime_executable'};exact(x,keys,'optimization')
        o=cls(str(x['exact_version']),str(x['objective']),bool(x['mixture_allowed']),float(x['grid_step']),int(x['max_active_treatments']),float(x['diversification_penalty']),float(x['complexity_penalty']),bool(x['baseline_preservation']),bool(x['fail_closed']),bool(x['deterministic']),bool(x['runtime_executable']))
        if o.objective not in OBJECTIVES or not 0<o.grid_step<=1 or o.max_active_treatments<1 or min(o.diversification_penalty,o.complexity_penalty)<0 or not(o.baseline_preservation and o.fail_closed and o.deterministic) or o.runtime_executable: raise ContractError('unsafe optimization contract')
        return o

@dataclass(frozen=True)
class RegretContract:
    exact_version:str;mode:str;maximum_regret_limit:float;mean_regret_limit:float;baseline_regret_limit:float;dynamic_regret_budget:float;robust_margin:float;tie_tolerance:float;abstain_on_violation:bool;baseline_first_on_tie:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','mode','maximum_regret_limit','mean_regret_limit','baseline_regret_limit','dynamic_regret_budget','robust_margin','tie_tolerance','abstain_on_violation','baseline_first_on_tie'};exact(x,keys,'regret')
        o=cls(str(x['exact_version']),str(x['mode']),*[float(x[k]) for k in ['maximum_regret_limit','mean_regret_limit','baseline_regret_limit','dynamic_regret_budget','robust_margin','tie_tolerance']],bool(x['abstain_on_violation']),bool(x['baseline_first_on_tie']))
        if o.mode not in REGRET_MODES or min(o.maximum_regret_limit,o.mean_regret_limit,o.baseline_regret_limit,o.dynamic_regret_budget,o.robust_margin,o.tie_tolerance)<0 or not(o.abstain_on_violation and o.baseline_first_on_tie): raise ContractError('unsafe regret contract')
        return o

@dataclass(frozen=True)
class BaselineContract:
    exact_version:str;canonical_baseline:str;skip_treatment:str;minimum_worst_case_delta:float;minimum_cvar_delta:float;maximum_complexity_increase:float;preserve_manual_baseline:bool;preserve_skip:bool;fail_to_skip:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','canonical_baseline','skip_treatment','minimum_worst_case_delta','minimum_cvar_delta','maximum_complexity_increase','preserve_manual_baseline','preserve_skip','fail_to_skip'};exact(x,keys,'baseline')
        o=cls(str(x['exact_version']),str(x['canonical_baseline']),str(x['skip_treatment']),float(x['minimum_worst_case_delta']),float(x['minimum_cvar_delta']),float(x['maximum_complexity_increase']),bool(x['preserve_manual_baseline']),bool(x['preserve_skip']),bool(x['fail_to_skip']))
        if not o.canonical_baseline or not o.skip_treatment or o.maximum_complexity_increase<0 or not(o.preserve_manual_baseline and o.preserve_skip and o.fail_to_skip): raise ContractError('unsafe baseline contract')
        return o

@dataclass(frozen=True)
class OptimizationBudget:
    max_candidates:int;max_scenarios:int;max_ambiguity_distributions:int;max_allocations:int;max_objective_evaluations:int;max_adversarial_steps:int;max_stability_resamples:int;max_hidden_evaluation_queries:int;protected_evidence_exposure_limit:int;max_failures:int
    @classmethod
    def from_mapping(cls,x):
        keys={'max_candidates','max_scenarios','max_ambiguity_distributions','max_allocations','max_objective_evaluations','max_adversarial_steps','max_stability_resamples','max_hidden_evaluation_queries','protected_evidence_exposure_limit','max_failures'};exact(x,keys,'optimization budget')
        o=cls(**{k:int(x[k]) for k in keys})
        if min(o.max_candidates,o.max_scenarios,o.max_ambiguity_distributions,o.max_allocations,o.max_objective_evaluations,o.max_adversarial_steps,o.max_stability_resamples)<1 or o.max_hidden_evaluation_queries!=0 or o.protected_evidence_exposure_limit!=0 or o.max_failures<0: raise ContractError('unsafe optimization budget')
        return o
