from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .errors import ContractError

FAMILIES={'native_linear_baseline','timesfm_style','chronos_style','moment_style','moirai_style','sparse_moe_style'}
MODES={'causal_linear','frozen_embedding','zero_shot_distribution','masked_representation','probabilistic_multiscale','sparse_expert_features'}
NORMALIZATIONS={'causal_zscore','causal_robust','identity'}
MISSINGNESS={'mask_and_zero','carry_with_age','reject'}
CALIBRATIONS={'identity','temperature','isotonic_reference'}
OVERLAP_RISKS={'none','low','medium','high','unknown'}
INTAKE_DECISIONS={'admit_reference','quarantine','reject'}


def exact(mapping:Mapping[str,Any], required:set[str], label:str):
    if set(mapping)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(mapping)^required)}')

@dataclass(frozen=True)
class AdapterConfig:
    exact_version:str; sequence_length:int; feature_dim:int; patch_length:int; horizon:int; embedding_dim:int; quantiles:tuple[float,...]; known_time_only:bool; frozen_upstream:bool; local_execution_only:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any]):
        r={'exact_version','sequence_length','feature_dim','patch_length','horizon','embedding_dim','quantiles','known_time_only','frozen_upstream','local_execution_only'};exact(x,r,'adapter config')
        o=cls(str(x['exact_version']),int(x['sequence_length']),int(x['feature_dim']),int(x['patch_length']),int(x['horizon']),int(x['embedding_dim']),tuple(float(q) for q in x['quantiles']),bool(x['known_time_only']),bool(x['frozen_upstream']),bool(x['local_execution_only']))
        if min(o.sequence_length,o.feature_dim,o.patch_length,o.horizon,o.embedding_dim)<1: raise ContractError('adapter dimensions must be positive')
        if o.patch_length>o.sequence_length: raise ContractError('patch_length exceeds sequence_length')
        if sorted(o.quantiles)!=list(o.quantiles) or len(set(o.quantiles))!=len(o.quantiles) or any(not 0<q<1 for q in o.quantiles): raise ContractError('invalid quantiles')
        if not (o.known_time_only and o.frozen_upstream and o.local_execution_only): raise ContractError('mandatory safety flags must be true')
        return o

@dataclass(frozen=True)
class ModelIntake:
    intake_id:str; family:str; release:str; source_kind:str; weight_digest:str; code_digest:str; tokenizer_digest:str; license_id:str; license_permitted:bool; architecture_disclosed:bool; exact_corpus_disclosed:bool; market_data_possible:bool; overlap_risk:str; local_execution_only:bool; remote_inference_forbidden:bool; synthetic_reference_adapter:bool; enabled:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any]):
        r={'intake_id','family','release','source_kind','weight_digest','code_digest','tokenizer_digest','license_id','license_permitted','architecture_disclosed','exact_corpus_disclosed','market_data_possible','overlap_risk','local_execution_only','remote_inference_forbidden','synthetic_reference_adapter','enabled'};exact(x,r,'model intake')
        o=cls(str(x['intake_id']),str(x['family']),str(x['release']),str(x['source_kind']),str(x['weight_digest']),str(x['code_digest']),str(x['tokenizer_digest']),str(x['license_id']),bool(x['license_permitted']),bool(x['architecture_disclosed']),bool(x['exact_corpus_disclosed']),bool(x['market_data_possible']),str(x['overlap_risk']),bool(x['local_execution_only']),bool(x['remote_inference_forbidden']),bool(x['synthetic_reference_adapter']),bool(x['enabled']))
        if o.family not in FAMILIES or o.overlap_risk not in OVERLAP_RISKS: raise ContractError('unknown intake enum')
        if not all(v.startswith('sha256:') and len(v)==71 for v in (o.weight_digest,o.code_digest,o.tokenizer_digest)): raise ContractError('digests must be sha256:<64hex>')
        if not o.local_execution_only or not o.remote_inference_forbidden: raise ContractError('remote inference is forbidden in V4-14')
        return o

@dataclass(frozen=True)
class CandidateSpec:
    candidate_id:str; intake_id:str; family:str; adapter_mode:str; seed:int; normalization:str; missingness_policy:str; calibration_method:str; expert_count:int; trainable_parameter_budget:int; enabled:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any]):
        r={'candidate_id','intake_id','family','adapter_mode','seed','normalization','missingness_policy','calibration_method','expert_count','trainable_parameter_budget','enabled'};exact(x,r,'candidate')
        o=cls(str(x['candidate_id']),str(x['intake_id']),str(x['family']),str(x['adapter_mode']),int(x['seed']),str(x['normalization']),str(x['missingness_policy']),str(x['calibration_method']),int(x['expert_count']),int(x['trainable_parameter_budget']),bool(x['enabled']))
        if o.family not in FAMILIES or o.adapter_mode not in MODES or o.normalization not in NORMALIZATIONS or o.missingness_policy not in MISSINGNESS or o.calibration_method not in CALIBRATIONS: raise ContractError('unknown candidate enum')
        if o.expert_count<1 or o.trainable_parameter_budget<0: raise ContractError('invalid candidate budget')
        return o

@dataclass(frozen=True)
class Disclosure:
    disclosure_id:str; intake_id:str; training_cutoff:str; exact_corpus_disclosed:bool; market_data_possible:bool; evaluation_period_overlap_possible:bool; contamination_reviewed:bool; unresolved_risks:tuple[str,...]
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any]):
        r={'disclosure_id','intake_id','training_cutoff','exact_corpus_disclosed','market_data_possible','evaluation_period_overlap_possible','contamination_reviewed','unresolved_risks'};exact(x,r,'pretraining disclosure')
        return cls(str(x['disclosure_id']),str(x['intake_id']),str(x['training_cutoff']),bool(x['exact_corpus_disclosed']),bool(x['market_data_possible']),bool(x['evaluation_period_overlap_possible']),bool(x['contamination_reviewed']),tuple(str(v) for v in x['unresolved_risks']))

@dataclass(frozen=True)
class DomainShiftPolicy:
    max_mean_shift:float; max_scale_ratio:float; max_missing_rate:float; max_router_concentration:float; unsupported_action:str; min_support_tokens:int
    @classmethod
    def from_mapping(cls,x):
        r={'max_mean_shift','max_scale_ratio','max_missing_rate','max_router_concentration','unsupported_action','min_support_tokens'};exact(x,r,'domain shift policy')
        o=cls(float(x['max_mean_shift']),float(x['max_scale_ratio']),float(x['max_missing_rate']),float(x['max_router_concentration']),str(x['unsupported_action']),int(x['min_support_tokens']))
        if min(o.max_mean_shift,o.max_scale_ratio,o.max_missing_rate,o.max_router_concentration)<0 or o.unsupported_action not in {'abstain','quarantine','reject'} or o.min_support_tokens<1: raise ContractError('invalid domain shift policy')
        return o

@dataclass(frozen=True)
class ComputeExposureBudget:
    max_candidates:int; max_adapter_calls:int; max_total_tokens:int; max_trainable_parameters:int; max_exposure_events:int; max_failures:int; max_retries:int
    @classmethod
    def from_mapping(cls,x):
        r={'max_candidates','max_adapter_calls','max_total_tokens','max_trainable_parameters','max_exposure_events','max_failures','max_retries'};exact(x,r,'compute exposure budget')
        o=cls(*(int(x[k]) for k in ['max_candidates','max_adapter_calls','max_total_tokens','max_trainable_parameters','max_exposure_events','max_failures','max_retries']))
        if min(o.max_candidates,o.max_adapter_calls,o.max_total_tokens,o.max_exposure_events)<1 or min(o.max_trainable_parameters,o.max_failures,o.max_retries)<0: raise ContractError('invalid compute/exposure budget')
        return o
