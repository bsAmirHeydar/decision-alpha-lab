from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

CLAIM_TIERS={'descriptive','associational','mechanism_compatible_synthetic','falsified','abstain'}
ALGORITHMS={'correlation_baseline','temporal_pc_reference','invariant_mechanism_reference','structural_equation_reference','orthogonal_score_reference'}
DIRECTIVES={'continue_reference','baseline','abstain','manual','reject','quarantine','stop_family'}
ROLES={'exogenous','context','mechanism','treatment_proxy','mediator','outcome_proxy','negative_control_exposure','negative_control_outcome','environment'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')
def increasing(xs): return all(a<b for a,b in zip(xs,xs[1:]))

@dataclass(frozen=True)
class VariableRegistry:
    exact_version:str; variables:tuple[dict,...]; treatment_proxy_id:str; outcome_proxy_id:str; environment_id:str; known_time_only:bool; frozen:bool; latent_variables_claimable:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','variables','treatment_proxy_id','outcome_proxy_id','environment_id','known_time_only','frozen','latent_variables_claimable'};exact(x,keys,'variable registry')
        variables=tuple(dict(v) for v in x['variables']);required={'variable_id','role','temporal_tier','observed','manipulable','negative_control','measurement_unit','known_time_rule'}
        ids=[]
        for v in variables:
            exact(v,required,'variable');ids.append(str(v['variable_id']))
            if v['role'] not in ROLES or int(v['temporal_tier'])<0 or not str(v['known_time_rule']):raise ContractError('invalid variable semantics')
            if v['role'] in {'negative_control_exposure','negative_control_outcome'} and not v['negative_control']:raise ContractError('negative control not declared')
        if len(ids)!=len(set(ids)) or not variables:raise ContractError('duplicate or empty variables')
        o=cls(str(x['exact_version']),variables,str(x['treatment_proxy_id']),str(x['outcome_proxy_id']),str(x['environment_id']),bool(x['known_time_only']),bool(x['frozen']),bool(x['latent_variables_claimable']))
        if any(v not in ids for v in [o.treatment_proxy_id,o.outcome_proxy_id,o.environment_id]):raise ContractError('registry anchor missing')
        if not(o.known_time_only and o.frozen) or o.latent_variables_claimable:raise ContractError('variable authority safeguards absent')
        return o

@dataclass(frozen=True)
class EnvironmentRegistry:
    exact_version:str; environments:tuple[dict,...]; assignment_rule:str; minimum_rows:int; immutable:bool; future_suffix_forbidden:bool; transport_claims_allowed:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','environments','assignment_rule','minimum_rows','immutable','future_suffix_forbidden','transport_claims_allowed'};exact(x,keys,'environment registry')
        envs=tuple(dict(v) for v in x['environments']);required={'environment_id','description','start_ordinal','end_ordinal','synthetic_intervention_tag','protected'}
        ids=[]
        for e in envs:exact(e,required,'environment');ids.append(e['environment_id'])
        o=cls(str(x['exact_version']),envs,str(x['assignment_rule']),int(x['minimum_rows']),bool(x['immutable']),bool(x['future_suffix_forbidden']),bool(x['transport_claims_allowed']))
        if len(ids)!=len(set(ids)) or o.minimum_rows<10 or not(o.immutable and o.future_suffix_forbidden) or o.transport_claims_allowed:raise ContractError('invalid environment safeguards')
        return o

@dataclass(frozen=True)
class GraphConstraints:
    exact_version:str; required_edges:tuple[tuple[str,str],...]; forbidden_edges:tuple[tuple[str,str],...]; temporal_tiers:dict; max_parents:int; acyclic_required:bool; no_future_to_past:bool; negative_controls_disconnected_from_target:bool; latent_edges_sensitivity_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','required_edges','forbidden_edges','temporal_tiers','max_parents','acyclic_required','no_future_to_past','negative_controls_disconnected_from_target','latent_edges_sensitivity_only'};exact(x,keys,'graph constraints')
        req=tuple(tuple(v) for v in x['required_edges']);forb=tuple(tuple(v) for v in x['forbidden_edges']);tiers={str(k):int(v) for k,v in x['temporal_tiers'].items()}
        o=cls(str(x['exact_version']),req,forb,tiers,int(x['max_parents']),bool(x['acyclic_required']),bool(x['no_future_to_past']),bool(x['negative_controls_disconnected_from_target']),bool(x['latent_edges_sensitivity_only']))
        if set(req)&set(forb) or o.max_parents<1 or not all([o.acyclic_required,o.no_future_to_past,o.negative_controls_disconnected_from_target,o.latent_edges_sensitivity_only]):raise ContractError('invalid graph constraints')
        return o

@dataclass(frozen=True)
class DiscoveryConfig:
    exact_version:str; seed:int; algorithms:tuple[str,...]; association_threshold:float; conditional_independence_threshold:float; invariance_mean_tolerance:float; invariance_scale_tolerance:float; negative_control_threshold:float; bootstrap_replicates:int; hidden_confounder_grid:tuple[float,...]; claim_ceiling:str; synthetic_only:bool; preserve_baseline:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','seed','algorithms','association_threshold','conditional_independence_threshold','invariance_mean_tolerance','invariance_scale_tolerance','negative_control_threshold','bootstrap_replicates','hidden_confounder_grid','claim_ceiling','synthetic_only','preserve_baseline'};exact(x,keys,'discovery config')
        o=cls(str(x['exact_version']),int(x['seed']),tuple(map(str,x['algorithms'])),float(x['association_threshold']),float(x['conditional_independence_threshold']),float(x['invariance_mean_tolerance']),float(x['invariance_scale_tolerance']),float(x['negative_control_threshold']),int(x['bootstrap_replicates']),tuple(float(v) for v in x['hidden_confounder_grid']),str(x['claim_ceiling']),bool(x['synthetic_only']),bool(x['preserve_baseline']))
        if set(o.algorithms)!=ALGORITHMS or not 0<o.association_threshold<1 or not 0<o.conditional_independence_threshold<1 or o.bootstrap_replicates<20 or not increasing(o.hidden_confounder_grid):raise ContractError('invalid discovery config')
        if o.claim_ceiling!='mechanism_compatible_synthetic_not_causal' or not(o.synthetic_only and o.preserve_baseline):raise ContractError('claim ceiling or safeguards invalid')
        return o

@dataclass(frozen=True)
class CandidateSpec:
    candidate_id:str; algorithm:str; seed:int; complexity_tier:int; edge_penalty:float; invariance_weight:float; falsification_weight:float; enabled:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'candidate_id','algorithm','seed','complexity_tier','edge_penalty','invariance_weight','falsification_weight','enabled'};exact(x,keys,'candidate')
        o=cls(str(x['candidate_id']),str(x['algorithm']),int(x['seed']),int(x['complexity_tier']),float(x['edge_penalty']),float(x['invariance_weight']),float(x['falsification_weight']),bool(x['enabled']))
        if o.algorithm not in ALGORITHMS or o.complexity_tier<0 or min(o.edge_penalty,o.invariance_weight,o.falsification_weight)<0:raise ContractError('invalid candidate')
        return o

@dataclass(frozen=True)
class ComputeExposureBudget:
    max_rows:int; max_variables:int; max_candidates:int; max_edges_evaluated:int; max_conditional_tests:int; max_bootstrap_replicates:int; max_stress_runs:int; max_failures:int; max_retries:int; protected_evidence_exposure_limit:int; hidden_evaluation_query_limit:int
    @classmethod
    def from_mapping(cls,x):
        keys={'max_rows','max_variables','max_candidates','max_edges_evaluated','max_conditional_tests','max_bootstrap_replicates','max_stress_runs','max_failures','max_retries','protected_evidence_exposure_limit','hidden_evaluation_query_limit'};exact(x,keys,'compute exposure budget')
        vals=[int(x[k]) for k in ['max_rows','max_variables','max_candidates','max_edges_evaluated','max_conditional_tests','max_bootstrap_replicates','max_stress_runs','max_failures','max_retries','protected_evidence_exposure_limit','hidden_evaluation_query_limit']]
        o=cls(*vals)
        if min(vals[:7])<1 or min(vals[7:])<0 or o.protected_evidence_exposure_limit!=0 or o.hidden_evaluation_query_limit!=0:raise ContractError('invalid exposure budget')
        return o
