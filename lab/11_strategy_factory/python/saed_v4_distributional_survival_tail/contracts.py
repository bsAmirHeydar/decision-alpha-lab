from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from .errors import ContractError

EVENT_CAUSES={'fill','stop','target','trail_exit','invalidation','cancellation','expiry'}
ALGORITHMS={'empirical_km_baseline','monotone_quantile_hazard','zero_inflated_mixture','competing_risk_ensemble','tail_robust_reference'}
DIRECTIVES={'estimate_reference','baseline','abstain','manual','reject','quarantine'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')

def _strictly_increasing(xs):return all(a<b for a,b in zip(xs,xs[1:]))

@dataclass(frozen=True)
class EventDefinitionRegistry:
    exact_version:str; time_origin:str; causes:tuple[str,...]; censor_label:str; interval_censoring_enabled:bool; mutually_exclusive_terminal_causes:bool; known_time_only:bool; frozen:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','time_origin','causes','censor_label','interval_censoring_enabled','mutually_exclusive_terminal_causes','known_time_only','frozen'};exact(x,keys,'event registry')
        o=cls(str(x['exact_version']),str(x['time_origin']),tuple(map(str,x['causes'])),str(x['censor_label']),bool(x['interval_censoring_enabled']),bool(x['mutually_exclusive_terminal_causes']),bool(x['known_time_only']),bool(x['frozen']))
        if set(o.causes)!=EVENT_CAUSES or len(o.causes)!=len(EVENT_CAUSES):raise ContractError('event cause registry must be exact')
        if o.censor_label in EVENT_CAUSES or not o.time_origin or not(o.mutually_exclusive_terminal_causes and o.known_time_only and o.frozen):raise ContractError('invalid event registry safety semantics')
        return o

@dataclass(frozen=True)
class CensoringPolicy:
    exact_version:str; administrative_horizon_seconds:int; observation_interval_seconds:int; allow_right_censoring:bool; allow_interval_censoring:bool; ipcw_floor:float; ipcw_ceiling:float; informative_sensitivity_factors:tuple[float,...]; censored_is_never_outcome:bool; known_time_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','administrative_horizon_seconds','observation_interval_seconds','allow_right_censoring','allow_interval_censoring','ipcw_floor','ipcw_ceiling','informative_sensitivity_factors','censored_is_never_outcome','known_time_only'};exact(x,keys,'censoring policy')
        o=cls(str(x['exact_version']),int(x['administrative_horizon_seconds']),int(x['observation_interval_seconds']),bool(x['allow_right_censoring']),bool(x['allow_interval_censoring']),float(x['ipcw_floor']),float(x['ipcw_ceiling']),tuple(float(v) for v in x['informative_sensitivity_factors']),bool(x['censored_is_never_outcome']),bool(x['known_time_only']))
        if o.administrative_horizon_seconds<=0 or o.observation_interval_seconds<=0 or not 0<o.ipcw_floor<=1<=o.ipcw_ceiling or not o.informative_sensitivity_factors:raise ContractError('invalid censoring policy')
        if not(o.allow_right_censoring and o.censored_is_never_outcome and o.known_time_only):raise ContractError('mandatory censoring safeguards absent')
        return o

@dataclass(frozen=True)
class DatasetSpec:
    exact_version:str; row_count:int; feature_dim:int; seed:int; start_time:str; spacing_seconds:int; train_rows:int; calibration_rows:int; selection_validation_rows:int; synthetic_only:bool; chronological_split:bool; frozen_fusion_features:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','row_count','feature_dim','seed','start_time','spacing_seconds','train_rows','calibration_rows','selection_validation_rows','synthetic_only','chronological_split','frozen_fusion_features'};exact(x,keys,'dataset spec')
        o=cls(str(x['exact_version']),int(x['row_count']),int(x['feature_dim']),int(x['seed']),str(x['start_time']),int(x['spacing_seconds']),int(x['train_rows']),int(x['calibration_rows']),int(x['selection_validation_rows']),bool(x['synthetic_only']),bool(x['chronological_split']),bool(x['frozen_fusion_features']))
        if o.row_count!=o.train_rows+o.calibration_rows+o.selection_validation_rows or min(o.row_count,o.feature_dim,o.spacing_seconds,o.train_rows,o.calibration_rows,o.selection_validation_rows)<1:raise ContractError('invalid dataset partition')
        if not(o.synthetic_only and o.chronological_split and o.frozen_fusion_features):raise ContractError('dataset safeguards required')
        return o

@dataclass(frozen=True)
class ModelConfig:
    exact_version:str; horizons_seconds:tuple[int,...]; quantiles:tuple[float,...]; tail_levels:tuple[float,...]; interval_levels:tuple[float,...]; min_tail_effective_samples:int; monotone_quantiles:bool; separate_zero_mass:bool; preserve_empirical_baseline:bool; calibration_split_only:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','horizons_seconds','quantiles','tail_levels','interval_levels','min_tail_effective_samples','monotone_quantiles','separate_zero_mass','preserve_empirical_baseline','calibration_split_only'};exact(x,keys,'model config')
        o=cls(str(x['exact_version']),tuple(int(v) for v in x['horizons_seconds']),tuple(float(v) for v in x['quantiles']),tuple(float(v) for v in x['tail_levels']),tuple(float(v) for v in x['interval_levels']),int(x['min_tail_effective_samples']),bool(x['monotone_quantiles']),bool(x['separate_zero_mass']),bool(x['preserve_empirical_baseline']),bool(x['calibration_split_only']))
        if not(_strictly_increasing(o.horizons_seconds) and _strictly_increasing(o.quantiles) and _strictly_increasing(o.tail_levels) and _strictly_increasing(o.interval_levels)):raise ContractError('model axes must be strictly increasing')
        if min(o.quantiles)<=0 or max(o.quantiles)>=1 or min(o.tail_levels)<=0 or max(o.tail_levels)>=.5 or min(o.interval_levels)<=.5 or max(o.interval_levels)>=1:raise ContractError('invalid probability levels')
        if o.min_tail_effective_samples<5 or not all([o.monotone_quantiles,o.separate_zero_mass,o.preserve_empirical_baseline,o.calibration_split_only]):raise ContractError('mandatory model safeguards absent')
        return o

@dataclass(frozen=True)
class CandidateSpec:
    candidate_id:str; algorithm:str; seed:int; distribution_family:str; survival_family:str; feature_scale:float; tail_shrinkage:float; enabled:bool
    @classmethod
    def from_mapping(cls,x):
        keys={'candidate_id','algorithm','seed','distribution_family','survival_family','feature_scale','tail_shrinkage','enabled'};exact(x,keys,'candidate')
        o=cls(str(x['candidate_id']),str(x['algorithm']),int(x['seed']),str(x['distribution_family']),str(x['survival_family']),float(x['feature_scale']),float(x['tail_shrinkage']),bool(x['enabled']))
        if o.algorithm not in ALGORITHMS or o.feature_scale<0 or not 0<=o.tail_shrinkage<=1:raise ContractError('invalid candidate')
        return o

@dataclass(frozen=True)
class TailPolicy:
    exact_version:str; lower_tail_levels:tuple[float,...]; expected_shortfall_required:bool; cluster_bootstrap_required:bool; best_trade_removal_required:bool; tail_event_holdout_required:bool; heavy_tail_benchmark_required:bool; insufficient_sample_action:str; unsupported_extreme_action:str
    @classmethod
    def from_mapping(cls,x):
        keys={'exact_version','lower_tail_levels','expected_shortfall_required','cluster_bootstrap_required','best_trade_removal_required','tail_event_holdout_required','heavy_tail_benchmark_required','insufficient_sample_action','unsupported_extreme_action'};exact(x,keys,'tail policy')
        o=cls(str(x['exact_version']),tuple(float(v) for v in x['lower_tail_levels']),bool(x['expected_shortfall_required']),bool(x['cluster_bootstrap_required']),bool(x['best_trade_removal_required']),bool(x['tail_event_holdout_required']),bool(x['heavy_tail_benchmark_required']),str(x['insufficient_sample_action']),str(x['unsupported_extreme_action']))
        if not _strictly_increasing(o.lower_tail_levels) or any(not 0<v<.5 for v in o.lower_tail_levels):raise ContractError('invalid tail levels')
        if not all([o.expected_shortfall_required,o.cluster_bootstrap_required,o.best_trade_removal_required,o.tail_event_holdout_required,o.heavy_tail_benchmark_required]):raise ContractError('tail stress suite incomplete')
        if o.insufficient_sample_action not in DIRECTIVES or o.unsupported_extreme_action not in DIRECTIVES:raise ContractError('invalid tail directive')
        return o

@dataclass(frozen=True)
class ComputeExposureBudget:
    max_rows:int; max_candidates:int; max_horizons:int; max_quantiles:int; max_tail_levels:int; max_predictions:int; max_stress_runs:int; max_failures:int; max_retries:int; protected_evidence_exposure_limit:int
    @classmethod
    def from_mapping(cls,x):
        keys={'max_rows','max_candidates','max_horizons','max_quantiles','max_tail_levels','max_predictions','max_stress_runs','max_failures','max_retries','protected_evidence_exposure_limit'};exact(x,keys,'compute exposure budget')
        o=cls(*(int(x[k]) for k in ['max_rows','max_candidates','max_horizons','max_quantiles','max_tail_levels','max_predictions','max_stress_runs','max_failures','max_retries','protected_evidence_exposure_limit']))
        if min(o.max_rows,o.max_candidates,o.max_horizons,o.max_quantiles,o.max_tail_levels,o.max_predictions,o.max_stress_runs)<1 or min(o.max_failures,o.max_retries,o.protected_evidence_exposure_limit)<0:raise ContractError('invalid compute exposure budget')
        if o.protected_evidence_exposure_limit!=0:raise ContractError('protected evidence exposure must remain zero')
        return o
