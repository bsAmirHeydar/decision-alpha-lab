from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

DECISION_OBJECTIVES={'expected_utility','lower_confidence_utility','cvar_utility','minimax_regret','pareto_robust','hybrid'}
TIE_POLICIES={'canonical_id','baseline_first','abstain'}
ABSTENTION_POLICIES={'margin','uncertainty','support','proof','combined'}
CALIBRATION_METHODS={'identity','temperature','isotonic_reference','platt_reference'}
FALLBACKS={'skip','manual','baseline','abstain','quarantine'}


def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required:raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')

@dataclass(frozen=True)
class TreatmentUniverseContract:
    exact_version:str;treatments:tuple[dict,...];canonical_baseline:str;skip_treatment:str;closed_world:bool;runtime_mutation_allowed:bool;synthetic_only:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','treatments','canonical_baseline','skip_treatment','closed_world','runtime_mutation_allowed','synthetic_only'},'treatment universe')
        ts=tuple(dict(v) for v in x['treatments']);ids=[]
        for t in ts:
            exact(t,{'treatment_id','family','description','complexity','manual_approved','enabled','max_nominal_risk'},'treatment')
            if not t['treatment_id'] or int(t['complexity'])<0 or not 0<=float(t['max_nominal_risk'])<=1:raise ContractError('invalid treatment')
            ids.append(str(t['treatment_id']))
        o=cls(str(x['exact_version']),ts,str(x['canonical_baseline']),str(x['skip_treatment']),bool(x['closed_world']),bool(x['runtime_mutation_allowed']),bool(x['synthetic_only']))
        if len(ids)!=len(set(ids)) or o.canonical_baseline not in ids or o.skip_treatment not in ids or not(o.closed_world and o.synthetic_only) or o.runtime_mutation_allowed:raise ContractError('unsafe treatment universe')
        return o

@dataclass(frozen=True)
class DecisionProblemContract:
    exact_version:str;context_id_field:str;known_time_field:str;outcome_field:str;sample_weight_field:str;treatment_field:str;cluster_field:str;allowed_objectives:tuple[str,...];primary_objective:str;maximize:bool;future_suffix_forbidden:bool;protected_evidence_forbidden:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','context_id_field','known_time_field','outcome_field','sample_weight_field','treatment_field','cluster_field','allowed_objectives','primary_objective','maximize','future_suffix_forbidden','protected_evidence_forbidden'},'decision problem')
        o=cls(str(x['exact_version']),str(x['context_id_field']),str(x['known_time_field']),str(x['outcome_field']),str(x['sample_weight_field']),str(x['treatment_field']),str(x['cluster_field']),tuple(map(str,x['allowed_objectives'])),str(x['primary_objective']),bool(x['maximize']),bool(x['future_suffix_forbidden']),bool(x['protected_evidence_forbidden']))
        if not set(o.allowed_objectives)<=DECISION_OBJECTIVES or o.primary_objective not in o.allowed_objectives or not(o.maximize and o.future_suffix_forbidden and o.protected_evidence_forbidden):raise ContractError('unsafe decision problem')
        return o

@dataclass(frozen=True)
class UtilityContract:
    exact_version:str;reward_weight:float;cost_weight:float;tail_loss_weight:float;drawdown_weight:float;complexity_weight:float;turnover_weight:float;abstention_cost:float;skip_utility:float;utility_floor:float;utility_ceiling:float
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','reward_weight','cost_weight','tail_loss_weight','drawdown_weight','complexity_weight','turnover_weight','abstention_cost','skip_utility','utility_floor','utility_ceiling'},'utility')
        o=cls(str(x['exact_version']),*[float(x[k]) for k in ['reward_weight','cost_weight','tail_loss_weight','drawdown_weight','complexity_weight','turnover_weight','abstention_cost','skip_utility','utility_floor','utility_ceiling']])
        if min(o.reward_weight,o.cost_weight,o.tail_loss_weight,o.drawdown_weight,o.complexity_weight,o.turnover_weight,o.abstention_cost)<0 or o.utility_floor>=o.utility_ceiling:raise ContractError('invalid utility')
        return o

@dataclass(frozen=True)
class ConstraintContract:
    exact_version:str;minimum_support:int;minimum_overlap:float;maximum_cost:float;maximum_tail_loss_probability:float;maximum_drawdown:float;maximum_complexity:int;proof_required:bool;manual_approval_required:bool;hard_fail_to_skip:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','minimum_support','minimum_overlap','maximum_cost','maximum_tail_loss_probability','maximum_drawdown','maximum_complexity','proof_required','manual_approval_required','hard_fail_to_skip'},'constraints')
        o=cls(str(x['exact_version']),int(x['minimum_support']),float(x['minimum_overlap']),float(x['maximum_cost']),float(x['maximum_tail_loss_probability']),float(x['maximum_drawdown']),int(x['maximum_complexity']),bool(x['proof_required']),bool(x['manual_approval_required']),bool(x['hard_fail_to_skip']))
        if o.minimum_support<1 or not 0<=o.minimum_overlap<=1 or min(o.maximum_cost,o.maximum_drawdown,o.maximum_complexity)<0 or not 0<=o.maximum_tail_loss_probability<=1 or not(o.proof_required and o.manual_approval_required and o.hard_fail_to_skip):raise ContractError('unsafe constraints')
        return o

@dataclass(frozen=True)
class RiskContract:
    exact_version:str;confidence_z:float;cvar_alpha:float;ambiguity_radius:float;regret_weight:float;uncertainty_weight:float;tail_weight:float;minimum_margin:float;maximum_entropy:float;maximum_set_size:int
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','confidence_z','cvar_alpha','ambiguity_radius','regret_weight','uncertainty_weight','tail_weight','minimum_margin','maximum_entropy','maximum_set_size'},'risk')
        o=cls(str(x['exact_version']),float(x['confidence_z']),float(x['cvar_alpha']),float(x['ambiguity_radius']),float(x['regret_weight']),float(x['uncertainty_weight']),float(x['tail_weight']),float(x['minimum_margin']),float(x['maximum_entropy']),int(x['maximum_set_size']))
        if o.confidence_z<0 or not 0<o.cvar_alpha<=1 or min(o.ambiguity_radius,o.regret_weight,o.uncertainty_weight,o.tail_weight,o.minimum_margin,o.maximum_entropy)<0 or o.maximum_set_size<1:raise ContractError('invalid risk contract')
        return o

@dataclass(frozen=True)
class SelectionPolicyContract:
    exact_version:str;objective:str;tie_policy:str;abstention_policy:str;calibration_method:str;set_valued:bool;baseline_preservation:bool;pareto_required:bool;deterministic:bool;runtime_executable:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','objective','tie_policy','abstention_policy','calibration_method','set_valued','baseline_preservation','pareto_required','deterministic','runtime_executable'},'selection policy')
        o=cls(str(x['exact_version']),str(x['objective']),str(x['tie_policy']),str(x['abstention_policy']),str(x['calibration_method']),bool(x['set_valued']),bool(x['baseline_preservation']),bool(x['pareto_required']),bool(x['deterministic']),bool(x['runtime_executable']))
        if o.objective not in DECISION_OBJECTIVES or o.tie_policy not in TIE_POLICIES or o.abstention_policy not in ABSTENTION_POLICIES or o.calibration_method not in CALIBRATION_METHODS or not(o.baseline_preservation and o.pareto_required and o.deterministic) or o.runtime_executable:raise ContractError('unsafe selection policy')
        return o

@dataclass(frozen=True)
class SelectionBudget:
    max_contexts:int;max_treatments:int;max_scenarios:int;max_objective_evaluations:int;max_calibration_iterations:int;max_pareto_points:int;max_counterfactual_queries:int;max_hidden_evaluation_queries:int;protected_evidence_exposure_limit:int;max_failures:int
    @classmethod
    def from_mapping(cls,x):
        keys={'max_contexts','max_treatments','max_scenarios','max_objective_evaluations','max_calibration_iterations','max_pareto_points','max_counterfactual_queries','max_hidden_evaluation_queries','protected_evidence_exposure_limit','max_failures'};exact(x,keys,'selection budget')
        o=cls(**{k:int(x[k]) for k in keys})
        if min(o.max_contexts,o.max_treatments,o.max_scenarios,o.max_objective_evaluations,o.max_calibration_iterations,o.max_pareto_points,o.max_counterfactual_queries)<1 or o.max_hidden_evaluation_queries!=0 or o.protected_evidence_exposure_limit!=0 or o.max_failures<0:raise ContractError('unsafe budget')
        return o
