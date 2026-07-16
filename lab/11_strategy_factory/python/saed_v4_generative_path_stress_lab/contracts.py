from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

GENERATOR_FAMILIES={'moving_block_bootstrap','regime_markov','latent_linear_ensemble','residual_flow_reference'}
STRESS_FAMILIES={'gap_down','gap_up','volatility_burst','liquidity_collapse','spread_blowout','chop_reversal','regime_break','execution_degradation'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')
def nonempty(v,label):
    if not str(v): raise ContractError(f'{label} is empty')
    return str(v)

@dataclass(frozen=True)
class UpstreamIntakeContract:
    exact_version:str;required_phase:str;robust_certificate_hash:str;scenario_set_hash:str;ambiguity_set_hash:str;budget_ledger_hash:str;handoff_hash:str;immutable:bool;hash_verified:bool;research_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','required_phase','robust_certificate_hash','scenario_set_hash','ambiguity_set_hash','budget_ledger_hash','handoff_hash','immutable','hash_verified','research_only'};exact(x,keys,'upstream intake')
        o=cls(*[nonempty(x[k],k) for k in ['exact_version','required_phase','robust_certificate_hash','scenario_set_hash','ambiguity_set_hash','budget_ledger_hash','handoff_hash']],bool(x['immutable']),bool(x['hash_verified']),bool(x['research_only']))
        if o.required_phase!='SAED_V4_21' or not(o.immutable and o.hash_verified and o.research_only): raise ContractError('unsafe upstream intake')
        return o

@dataclass(frozen=True)
class StateSchemaContract:
    exact_version:str;required_row_fields:tuple[str,...];known_time_fields:tuple[str,...];action_fields_forbidden:tuple[str,...];minimum_history:int;maximum_history:int;strict_timestamp_order:bool;future_suffix_forbidden:bool;protected_evidence_forbidden:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','required_row_fields','known_time_fields','action_fields_forbidden','minimum_history','maximum_history','strict_timestamp_order','future_suffix_forbidden','protected_evidence_forbidden'};exact(x,keys,'state schema')
        o=cls(str(x['exact_version']),tuple(map(str,x['required_row_fields'])),tuple(map(str,x['known_time_fields'])),tuple(map(str,x['action_fields_forbidden'])),int(x['minimum_history']),int(x['maximum_history']),bool(x['strict_timestamp_order']),bool(x['future_suffix_forbidden']),bool(x['protected_evidence_forbidden']))
        required={'timestamp','open','high','low','close','bid','ask','volume','liquidity','regime'}
        if set(o.required_row_fields)!=required or o.minimum_history<16 or o.maximum_history<o.minimum_history or not(o.strict_timestamp_order and o.future_suffix_forbidden and o.protected_evidence_forbidden): raise ContractError('unsafe state schema')
        return o

@dataclass(frozen=True)
class GeneratorProgramContract:
    exact_version:str;families:tuple[str,...];paths_per_family:int;horizon:int;block_length:int;ensemble_members:int;seed_namespace:str;deterministic:bool;watermark_required:bool;action_masked:bool;synthetic_positive_evidence_forbidden:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','families','paths_per_family','horizon','block_length','ensemble_members','seed_namespace','deterministic','watermark_required','action_masked','synthetic_positive_evidence_forbidden'};exact(x,keys,'generator program')
        o=cls(str(x['exact_version']),tuple(map(str,x['families'])),int(x['paths_per_family']),int(x['horizon']),int(x['block_length']),int(x['ensemble_members']),nonempty(x['seed_namespace'],'seed_namespace'),bool(x['deterministic']),bool(x['watermark_required']),bool(x['action_masked']),bool(x['synthetic_positive_evidence_forbidden']))
        if not o.families or not set(o.families)<=GENERATOR_FAMILIES or o.paths_per_family<1 or not 16<=o.horizon<=2048 or not 2<=o.block_length<=o.horizon or not 2<=o.ensemble_members<=64 or not(o.deterministic and o.watermark_required and o.action_masked and o.synthetic_positive_evidence_forbidden): raise ContractError('unsafe generator program')
        return o

@dataclass(frozen=True)
class PathInvariantContract:
    exact_version:str;minimum_price:float;maximum_relative_spread:float;maximum_step_return:float;minimum_liquidity:float;maximum_liquidity:float;enforce_ohlc_geometry:bool;enforce_bid_ask_order:bool;enforce_finite:bool;fail_closed:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','minimum_price','maximum_relative_spread','maximum_step_return','minimum_liquidity','maximum_liquidity','enforce_ohlc_geometry','enforce_bid_ask_order','enforce_finite','fail_closed'};exact(x,keys,'path invariant')
        o=cls(str(x['exact_version']),*[float(x[k]) for k in ['minimum_price','maximum_relative_spread','maximum_step_return','minimum_liquidity','maximum_liquidity']],bool(x['enforce_ohlc_geometry']),bool(x['enforce_bid_ask_order']),bool(x['enforce_finite']),bool(x['fail_closed']))
        if o.minimum_price<=0 or not 0<o.maximum_relative_spread<1 or not 0<o.maximum_step_return<1 or o.minimum_liquidity<0 or o.maximum_liquidity<=o.minimum_liquidity or not(o.enforce_ohlc_geometry and o.enforce_bid_ask_order and o.enforce_finite and o.fail_closed): raise ContractError('unsafe path invariants')
        return o

@dataclass(frozen=True)
class StressProgramContract:
    exact_version:str;families:tuple[str,...];severity_levels:tuple[float,...];maximum_stress_paths:int;preserve_timestamp_grid:bool;preserve_watermark:bool;market_invariants_required:bool;adversarial_search_steps:int;deterministic:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','families','severity_levels','maximum_stress_paths','preserve_timestamp_grid','preserve_watermark','market_invariants_required','adversarial_search_steps','deterministic'};exact(x,keys,'stress program')
        o=cls(str(x['exact_version']),tuple(map(str,x['families'])),tuple(float(v) for v in x['severity_levels']),int(x['maximum_stress_paths']),bool(x['preserve_timestamp_grid']),bool(x['preserve_watermark']),bool(x['market_invariants_required']),int(x['adversarial_search_steps']),bool(x['deterministic']))
        if not o.families or not set(o.families)<=STRESS_FAMILIES or not o.severity_levels or min(o.severity_levels)<=0 or max(o.severity_levels)>1 or o.maximum_stress_paths<1 or o.adversarial_search_steps<1 or not(o.preserve_timestamp_grid and o.preserve_watermark and o.market_invariants_required and o.deterministic): raise ContractError('unsafe stress program')
        return o

@dataclass(frozen=True)
class FidelityContract:
    exact_version:str;maximum_composite_distance:float;maximum_return_mean_error:float;maximum_return_std_error:float;maximum_tail_quantile_error:float;maximum_autocorrelation_error:float;maximum_spread_error:float;maximum_liquidity_error:float;maximum_regime_occupancy_l1:float;maximum_distinguishability_proxy:float;minimum_trusted_horizon:int
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','maximum_composite_distance','maximum_return_mean_error','maximum_return_std_error','maximum_tail_quantile_error','maximum_autocorrelation_error','maximum_spread_error','maximum_liquidity_error','maximum_regime_occupancy_l1','maximum_distinguishability_proxy','minimum_trusted_horizon'};exact(x,keys,'fidelity')
        o=cls(str(x['exact_version']),*[float(x[k]) for k in ['maximum_composite_distance','maximum_return_mean_error','maximum_return_std_error','maximum_tail_quantile_error','maximum_autocorrelation_error','maximum_spread_error','maximum_liquidity_error','maximum_regime_occupancy_l1','maximum_distinguishability_proxy']],int(x['minimum_trusted_horizon']))
        if min(o.maximum_composite_distance,o.maximum_return_mean_error,o.maximum_return_std_error,o.maximum_tail_quantile_error,o.maximum_autocorrelation_error,o.maximum_spread_error,o.maximum_liquidity_error,o.maximum_regime_occupancy_l1,o.maximum_distinguishability_proxy)<=0 or o.minimum_trusted_horizon<1: raise ContractError('unsafe fidelity contract')
        return o

@dataclass(frozen=True)
class ExploitabilityContract:
    exact_version:str;synthetic_advantage_threshold:float;real_transfer_floor:float;maximum_exploitation_score:float;baseline_policy_id:str;candidate_policy_id:str;real_replay_required:bool;synthetic_gain_is_positive_evidence:bool;fail_closed:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','synthetic_advantage_threshold','real_transfer_floor','maximum_exploitation_score','baseline_policy_id','candidate_policy_id','real_replay_required','synthetic_gain_is_positive_evidence','fail_closed'};exact(x,keys,'exploitability')
        o=cls(str(x['exact_version']),float(x['synthetic_advantage_threshold']),float(x['real_transfer_floor']),float(x['maximum_exploitation_score']),nonempty(x['baseline_policy_id'],'baseline_policy_id'),nonempty(x['candidate_policy_id'],'candidate_policy_id'),bool(x['real_replay_required']),bool(x['synthetic_gain_is_positive_evidence']),bool(x['fail_closed']))
        if o.synthetic_advantage_threshold<0 or o.maximum_exploitation_score<0 or not(o.real_replay_required and o.fail_closed) or o.synthetic_gain_is_positive_evidence: raise ContractError('unsafe exploitability contract')
        return o

@dataclass(frozen=True)
class RolloutBudget:
    exact_version:str;max_real_paths:int;max_generated_paths:int;max_stress_paths:int;max_generator_trials:int;max_adversarial_steps:int;max_fidelity_evaluations:int;max_failures:int;max_hidden_evaluation_queries:int;protected_evidence_exposure_limit:int
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','max_real_paths','max_generated_paths','max_stress_paths','max_generator_trials','max_adversarial_steps','max_fidelity_evaluations','max_failures','max_hidden_evaluation_queries','protected_evidence_exposure_limit'};exact(x,keys,'rollout budget')
        o=cls(str(x['exact_version']),*[int(x[k]) for k in ['max_real_paths','max_generated_paths','max_stress_paths','max_generator_trials','max_adversarial_steps','max_fidelity_evaluations','max_failures','max_hidden_evaluation_queries','protected_evidence_exposure_limit']])
        if min(o.max_real_paths,o.max_generated_paths,o.max_stress_paths,o.max_generator_trials,o.max_adversarial_steps,o.max_fidelity_evaluations,o.max_failures)<1 or o.max_hidden_evaluation_queries!=0 or o.protected_evidence_exposure_limit!=0: raise ContractError('unsafe rollout budget')
        return o
