from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

ACTIONS={'skip','long','short'}
ROLES={'training','calibration','selection_validation'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')
def nonempty(v,label):
    if not str(v): raise ContractError(f'{label} is empty')
    return str(v)
def positive(v,label):
    x=float(v)
    if x<=0: raise ContractError(f'{label} must be positive')
    return x

@dataclass(frozen=True)
class UpstreamIntakeContract:
    exact_version:str;required_phase:str;generative_stress_certificate_hash:str;fidelity_report_hash:str;uncertainty_map_hash:str;exploitability_report_hash:str;budget_ledger_hash:str;handoff_hash:str;immutable:bool;hash_verified:bool;research_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','required_phase','generative_stress_certificate_hash','fidelity_report_hash','uncertainty_map_hash','exploitability_report_hash','budget_ledger_hash','handoff_hash','immutable','hash_verified','research_only'};exact(x,keys,'upstream intake')
        o=cls(*[nonempty(x[k],k) for k in ['exact_version','required_phase','generative_stress_certificate_hash','fidelity_report_hash','uncertainty_map_hash','exploitability_report_hash','budget_ledger_hash','handoff_hash']],bool(x['immutable']),bool(x['hash_verified']),bool(x['research_only']))
        if o.required_phase!='SAED_V4_22' or not(o.immutable and o.hash_verified and o.research_only): raise ContractError('unsafe upstream intake')
        return o

@dataclass(frozen=True)
class LoggedDatasetContract:
    exact_version:str;allowed_roles:tuple[str,...];required_step_fields:tuple[str,...];strict_time_order:bool;known_time_required:bool;behavior_probability_required:bool;cluster_identity_required:bool;minimum_episodes:int;minimum_steps_per_episode:int;future_suffix_forbidden:bool;protected_evidence_forbidden:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','allowed_roles','required_step_fields','strict_time_order','known_time_required','behavior_probability_required','cluster_identity_required','minimum_episodes','minimum_steps_per_episode','future_suffix_forbidden','protected_evidence_forbidden'};exact(x,keys,'logged dataset contract')
        o=cls(str(x['exact_version']),tuple(map(str,x['allowed_roles'])),tuple(map(str,x['required_step_fields'])),bool(x['strict_time_order']),bool(x['known_time_required']),bool(x['behavior_probability_required']),bool(x['cluster_identity_required']),int(x['minimum_episodes']),int(x['minimum_steps_per_episode']),bool(x['future_suffix_forbidden']),bool(x['protected_evidence_forbidden']))
        required={'t','state','action','reward','next_state','done','behavior_prob','allowed_actions','known_at','reward_components'}
        if set(o.allowed_roles)!=ROLES or set(o.required_step_fields)!=required or o.minimum_episodes<4 or o.minimum_steps_per_episode<3 or not all([o.strict_time_order,o.known_time_required,o.behavior_probability_required,o.cluster_identity_required,o.future_suffix_forbidden,o.protected_evidence_forbidden]): raise ContractError('unsafe logged dataset contract')
        return o

@dataclass(frozen=True)
class ActionSpaceContract:
    exact_version:str;actions:tuple[str,...];safe_action:str;action_masks_required:bool;unknown_action_rejected:bool;safe_action_always_available:bool;runtime_action_forbidden:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','actions','safe_action','action_masks_required','unknown_action_rejected','safe_action_always_available','runtime_action_forbidden'};exact(x,keys,'action space')
        o=cls(str(x['exact_version']),tuple(map(str,x['actions'])),str(x['safe_action']),bool(x['action_masks_required']),bool(x['unknown_action_rejected']),bool(x['safe_action_always_available']),bool(x['runtime_action_forbidden']))
        if set(o.actions)!=ACTIONS or o.safe_action!='skip' or not all([o.action_masks_required,o.unknown_action_rejected,o.safe_action_always_available,o.runtime_action_forbidden]): raise ContractError('unsafe action space')
        return o

@dataclass(frozen=True)
class RewardContract:
    exact_version:str;components:tuple[str,...];minimum_reward:float;maximum_reward:float;clip_for_training:bool;audit_component_sum:bool;synthetic_reward_positive_evidence_forbidden:bool;execution_cost_required:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','components','minimum_reward','maximum_reward','clip_for_training','audit_component_sum','synthetic_reward_positive_evidence_forbidden','execution_cost_required'};exact(x,keys,'reward contract')
        o=cls(str(x['exact_version']),tuple(map(str,x['components'])),float(x['minimum_reward']),float(x['maximum_reward']),bool(x['clip_for_training']),bool(x['audit_component_sum']),bool(x['synthetic_reward_positive_evidence_forbidden']),bool(x['execution_cost_required']))
        if set(o.components)!={'gross_return','execution_cost','risk_penalty'} or o.minimum_reward>=o.maximum_reward or not all([o.clip_for_training,o.audit_component_sum,o.synthetic_reward_positive_evidence_forbidden,o.execution_cost_required]): raise ContractError('unsafe reward contract')
        return o

@dataclass(frozen=True)
class BehaviorPolicyContract:
    exact_version:str;smoothing:float;minimum_probability:float;maximum_log_ratio:float;state_conditioned:bool;cluster_aware:bool;deterministic:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','smoothing','minimum_probability','maximum_log_ratio','state_conditioned','cluster_aware','deterministic'};exact(x,keys,'behavior policy')
        o=cls(str(x['exact_version']),positive(x['smoothing'],'smoothing'),positive(x['minimum_probability'],'minimum_probability'),positive(x['maximum_log_ratio'],'maximum_log_ratio'),bool(x['state_conditioned']),bool(x['cluster_aware']),bool(x['deterministic']))
        if o.minimum_probability>=1 or not all([o.state_conditioned,o.cluster_aware,o.deterministic]): raise ContractError('unsafe behavior policy')
        return o

@dataclass(frozen=True)
class SupportContract:
    exact_version:str;minimum_state_action_count:int;minimum_behavior_probability:float;minimum_effective_sample_size:float;maximum_unsupported_mass:float;maximum_importance_weight:float;fail_closed:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','minimum_state_action_count','minimum_behavior_probability','minimum_effective_sample_size','maximum_unsupported_mass','maximum_importance_weight','fail_closed'};exact(x,keys,'support contract')
        o=cls(str(x['exact_version']),int(x['minimum_state_action_count']),positive(x['minimum_behavior_probability'],'minimum_behavior_probability'),positive(x['minimum_effective_sample_size'],'minimum_effective_sample_size'),float(x['maximum_unsupported_mass']),positive(x['maximum_importance_weight'],'maximum_importance_weight'),bool(x['fail_closed']))
        if o.minimum_state_action_count<1 or not 0<=o.maximum_unsupported_mass<1 or not o.fail_closed: raise ContractError('unsafe support contract')
        return o

@dataclass(frozen=True)
class CQLContract:
    exact_version:str;discount:float;conservative_alpha:float;iterations:int;temperature:float;minimum_count_for_unpenalized:int;deterministic:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','discount','conservative_alpha','iterations','temperature','minimum_count_for_unpenalized','deterministic'};exact(x,keys,'cql contract')
        o=cls(str(x['exact_version']),float(x['discount']),positive(x['conservative_alpha'],'conservative_alpha'),int(x['iterations']),positive(x['temperature'],'temperature'),int(x['minimum_count_for_unpenalized']),bool(x['deterministic']))
        if not 0<=o.discount<1 or o.iterations<5 or o.minimum_count_for_unpenalized<1 or not o.deterministic: raise ContractError('unsafe cql contract')
        return o

@dataclass(frozen=True)
class IQLContract:
    exact_version:str;discount:float;expectile:float;advantage_temperature:float;iterations:int;maximum_advantage_weight:float;deterministic:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','discount','expectile','advantage_temperature','iterations','maximum_advantage_weight','deterministic'};exact(x,keys,'iql contract')
        o=cls(str(x['exact_version']),float(x['discount']),float(x['expectile']),positive(x['advantage_temperature'],'advantage_temperature'),int(x['iterations']),positive(x['maximum_advantage_weight'],'maximum_advantage_weight'),bool(x['deterministic']))
        if not 0<=o.discount<1 or not 0.5<o.expectile<1 or o.iterations<5 or not o.deterministic: raise ContractError('unsafe iql contract')
        return o

@dataclass(frozen=True)
class SequencePolicyContract:
    exact_version:str;maximum_context_length:int;recency_decay:float;smoothing:float;minimum_sequence_count:int;fallback_to_behavior:bool;deterministic:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','maximum_context_length','recency_decay','smoothing','minimum_sequence_count','fallback_to_behavior','deterministic'};exact(x,keys,'sequence policy')
        o=cls(str(x['exact_version']),int(x['maximum_context_length']),float(x['recency_decay']),positive(x['smoothing'],'smoothing'),int(x['minimum_sequence_count']),bool(x['fallback_to_behavior']),bool(x['deterministic']))
        if not 1<=o.maximum_context_length<=16 or not 0<o.recency_decay<=1 or o.minimum_sequence_count<1 or not(o.fallback_to_behavior and o.deterministic): raise ContractError('unsafe sequence policy')
        return o

@dataclass(frozen=True)
class OPEContract:
    exact_version:str;estimators:tuple[str,...];discount:float;weight_clip:float;bootstrap_draws:int;confidence_level:float;minimum_lower_bound_margin:float;cluster_bootstrap:bool;synthetic_positive_evidence_forbidden:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','estimators','discount','weight_clip','bootstrap_draws','confidence_level','minimum_lower_bound_margin','cluster_bootstrap','synthetic_positive_evidence_forbidden'};exact(x,keys,'ope contract')
        o=cls(str(x['exact_version']),tuple(map(str,x['estimators'])),float(x['discount']),positive(x['weight_clip'],'weight_clip'),int(x['bootstrap_draws']),float(x['confidence_level']),float(x['minimum_lower_bound_margin']),bool(x['cluster_bootstrap']),bool(x['synthetic_positive_evidence_forbidden']))
        if set(o.estimators)!={'wis','pdis','fqe','doubly_robust'} or not 0<=o.discount<1 or o.bootstrap_draws<100 or not 0.8<=o.confidence_level<1 or not(o.cluster_bootstrap and o.synthetic_positive_evidence_forbidden): raise ContractError('unsafe ope contract')
        return o

@dataclass(frozen=True)
class ProjectionContract:
    exact_version:str;minimum_supported_probability:float;maximum_l1_from_behavior:float;maximum_kl_from_behavior:float;safe_action_floor:float;mask_enforced:bool;support_enforced:bool;fail_closed:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','minimum_supported_probability','maximum_l1_from_behavior','maximum_kl_from_behavior','safe_action_floor','mask_enforced','support_enforced','fail_closed'};exact(x,keys,'projection contract')
        o=cls(str(x['exact_version']),float(x['minimum_supported_probability']),float(x['maximum_l1_from_behavior']),float(x['maximum_kl_from_behavior']),float(x['safe_action_floor']),bool(x['mask_enforced']),bool(x['support_enforced']),bool(x['fail_closed']))
        if not 0<=o.minimum_supported_probability<1 or not 0<o.maximum_l1_from_behavior<=2 or o.maximum_kl_from_behavior<=0 or not 0<=o.safe_action_floor<1 or not all([o.mask_enforced,o.support_enforced,o.fail_closed]): raise ContractError('unsafe projection contract')
        return o

@dataclass(frozen=True)
class ResearchBudget:
    exact_version:str;max_dataset_episodes:int;max_training_trials:int;max_candidate_policies:int;max_ope_evaluations:int;max_bootstrap_draws:int;max_projection_attempts:int;max_synthetic_challenges:int;max_failures:int;max_hidden_evaluation_queries:int;protected_evidence_exposure_limit:int
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','max_dataset_episodes','max_training_trials','max_candidate_policies','max_ope_evaluations','max_bootstrap_draws','max_projection_attempts','max_synthetic_challenges','max_failures','max_hidden_evaluation_queries','protected_evidence_exposure_limit'};exact(x,keys,'research budget')
        vals=[int(x[k]) for k in ['max_dataset_episodes','max_training_trials','max_candidate_policies','max_ope_evaluations','max_bootstrap_draws','max_projection_attempts','max_synthetic_challenges','max_failures','max_hidden_evaluation_queries','protected_evidence_exposure_limit']]
        o=cls(str(x['exact_version']),*vals)
        if min(vals[:8])<1 or o.max_hidden_evaluation_queries!=0 or o.protected_evidence_exposure_limit!=0: raise ContractError('unsafe research budget')
        return o
