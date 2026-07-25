from __future__ import annotations
import math,re
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import canonical_sha256,stable_id
from .enums import *
from .errors import TournamentError
SHA=re.compile(r'^[0-9a-f]{64}$'); SEMVER=re.compile(r'^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$'); IDENT=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:@/-]*$')
def _id(v,n):
 if not isinstance(v,str) or not IDENT.fullmatch(v):raise TournamentError('invalid_identifier',f'{n} invalid',{'value':v})
def _hash(v,n):
 if not isinstance(v,str) or not SHA.fullmatch(v):raise TournamentError('invalid_hash',f'{n} must be lowercase sha256')
def _ver(v,n):
 if not isinstance(v,str) or not SEMVER.fullmatch(v):raise TournamentError('invalid_semver',f'{n} invalid')
def _finite(v,n):
 if not math.isfinite(float(v)):raise TournamentError('non_finite',f'{n} must be finite')

@dataclass(frozen=True,slots=True)
class DataInventory:
 inventory_id:str;version:str;dataset_id:str;dataset_hash:str;mode:DataMode;row_count:int;symbols:tuple[str,...];start_time_ms:int;end_time_ms:int;known_time_field:str;source_uri:str;causal_cut_ms:int;schema_hash:str;limitations:tuple[str,...]=()
 def __post_init__(self):
  _id(self.inventory_id,'inventory_id');_ver(self.version,'version');_id(self.dataset_id,'dataset_id');_hash(self.dataset_hash,'dataset_hash');_hash(self.schema_hash,'schema_hash')
  if self.row_count<1:raise TournamentError('empty_dataset','row_count must be positive')
  if not self.symbols or len(set(self.symbols))!=len(self.symbols):raise TournamentError('invalid_symbols','symbols unique and non-empty')
  if self.start_time_ms>self.end_time_ms or self.causal_cut_ms<self.end_time_ms:raise TournamentError('invalid_time_range','causal cut must be at or after end')
  _id(self.known_time_field,'known_time_field')
 @property
 def inventory_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ContextOccurrence:
 occurrence_id:str;context_id:str;context_version:str;known_time_ms:int;event_time_ms:int;symbol_scope:tuple[str,...];features:Mapping[str,Any];lifecycle_state:str;source_ids:tuple[str,...];matured:bool=True
 def __post_init__(self):
  _id(self.occurrence_id,'occurrence_id');_id(self.context_id,'context_id');_ver(self.context_version,'context_version');_id(self.lifecycle_state,'lifecycle_state')
  if self.event_time_ms>self.known_time_ms:raise TournamentError('future_known_time','event after known time')
  if not self.symbol_scope:raise TournamentError('empty_symbol_scope','symbol scope required')
 @property
 def occurrence_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ContextPackageFreeze:
 freeze_id:str;version:str;context_id:str;context_version:str;doctrine_hash:str;feature_schema_hash:str;cluster_rule_hash:str;lifecycle_hash:str;known_time_policy_hash:str;allowed_feature_ids:tuple[str,...];forbidden_feature_ids:tuple[str,...];personal_setup_ids:tuple[str,...];source_inventory_hash:str
 def __post_init__(self):
  for n in ('freeze_id','context_id'):_id(getattr(self,n),n)
  _ver(self.version,'version');_ver(self.context_version,'context_version')
  for n in ('doctrine_hash','feature_schema_hash','cluster_rule_hash','lifecycle_hash','known_time_policy_hash','source_inventory_hash'):_hash(getattr(self,n),n)
  if len(set(self.allowed_feature_ids))!=len(self.allowed_feature_ids):raise TournamentError('duplicate_feature','allowed features duplicated')
  overlap=set(self.allowed_feature_ids)&set(self.forbidden_feature_ids)
  if overlap:raise TournamentError('feature_policy_conflict','feature both allowed and forbidden',{'overlap':sorted(overlap)})
 @property
 def freeze_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class TreatmentSpec:
 treatment_id:str;version:str;family:TreatmentFamily;parameters:Mapping[str,Any];max_loss_r:float;requires_confirmation:bool;entry_kind:str;exit_kind:str;capital_policy_id:str
 def __post_init__(self):
  _id(self.treatment_id,'treatment_id');_ver(self.version,'version');_id(self.entry_kind,'entry_kind');_id(self.exit_kind,'exit_kind');_id(self.capital_policy_id,'capital_policy_id');_finite(self.max_loss_r,'max_loss_r')
  if self.max_loss_r<=0:raise TournamentError('invalid_max_loss','max loss must be positive')
 @property
 def spec_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class TreatmentUniverseFreeze:
 universe_id:str;version:str;declared_at_ms:int;outcome_cut_ms:int;treatments:tuple[TreatmentSpec,...];locked:bool=True
 def __post_init__(self):
  _id(self.universe_id,'universe_id');_ver(self.version,'version')
  ids=[x.treatment_id for x in self.treatments]
  if not ids or len(ids)!=len(set(ids)):raise TournamentError('invalid_treatment_universe','treatments unique and non-empty')
  if self.declared_at_ms>self.outcome_cut_ms:raise TournamentError('post_outcome_freeze','treatment universe declared after outcome cut')
  if not self.locked:raise TournamentError('unlocked_treatment_universe','treatment universe must be locked')
 @property
 def universe_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class AlgorithmSpec:
 algorithm_id:str;version:str;family:AlgorithmFamily;task_kind:str;view_ids:tuple[str,...];seed:int;budget_units:int;qualified:bool;dependency_flags:Mapping[str,bool]=field(default_factory=dict)
 def __post_init__(self):
  _id(self.algorithm_id,'algorithm_id');_ver(self.version,'version');_id(self.task_kind,'task_kind')
  if not self.view_ids:raise TournamentError('empty_views','algorithm requires views')
  if self.seed<0 or self.budget_units<1:raise TournamentError('invalid_algorithm_budget','seed/budget invalid')
  if self.family is AlgorithmFamily.DEEP and not self.qualified:raise TournamentError('unqualified_deep','deep algorithm must be qualified')
 @property
 def spec_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class AlgorithmUniverseFreeze:
 universe_id:str;version:str;declared_at_ms:int;outcome_cut_ms:int;algorithms:tuple[AlgorithmSpec,...];locked:bool=True
 def __post_init__(self):
  _id(self.universe_id,'universe_id');_ver(self.version,'version')
  ids=[x.algorithm_id for x in self.algorithms]
  if not ids or len(ids)!=len(set(ids)):raise TournamentError('invalid_algorithm_universe','algorithms unique and non-empty')
  if self.declared_at_ms>self.outcome_cut_ms:raise TournamentError('post_outcome_freeze','algorithm universe declared after outcome cut')
  if not self.locked:raise TournamentError('unlocked_algorithm_universe','algorithm universe must be locked')
 @property
 def universe_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class FoldSpec:
 fold_id:str;train_start_ms:int;train_end_ms:int;validation_end_ms:int;test_end_ms:int;embargo_ms:int;purge_ms:int
 def __post_init__(self):
  _id(self.fold_id,'fold_id')
  if not(self.train_start_ms<self.train_end_ms<self.validation_end_ms<self.test_end_ms):raise TournamentError('invalid_fold_order','fold times must strictly increase')
  if self.embargo_ms<0 or self.purge_ms<0:raise TournamentError('invalid_fold_gap','embargo/purge non-negative')
 @property
 def fold_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class TournamentFreeze:
 tournament_id:str;version:str;inventory_hash:str;context_freeze_hashes:tuple[str,...];treatment_universe_hash:str;algorithm_universe_hash:str;folds:tuple[FoldSpec,...];metric_ids:tuple[str,...];critical_gate_ids:tuple[str,...];max_challengers:int;seed:int;budget_units:int;final_test_sealed:bool=True
 def __post_init__(self):
  _id(self.tournament_id,'tournament_id');_ver(self.version,'version');_hash(self.inventory_hash,'inventory_hash');_hash(self.treatment_universe_hash,'treatment_universe_hash');_hash(self.algorithm_universe_hash,'algorithm_universe_hash')
  for x in self.context_freeze_hashes:_hash(x,'context_freeze_hash')
  if not self.folds or len({f.fold_id for f in self.folds})!=len(self.folds):raise TournamentError('invalid_folds','folds unique and non-empty')
  if not self.metric_ids or not self.critical_gate_ids:raise TournamentError('missing_evaluation_contract','metrics and critical gates required')
  if self.max_challengers<0 or self.budget_units<1 or self.seed<0:raise TournamentError('invalid_tournament_limits','limits invalid')
  if not self.final_test_sealed:raise TournamentError('unsealed_final_test','final test must be sealed')
 @property
 def freeze_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class TrialResult:
 trial_id:str;context_id:str;treatment_id:str;algorithm_id:str;fold_id:str;status:TrialStatus;metrics:Mapping[str,float];decision_count:int;failure_code:str='none';artifact_hash:str='0'*64
 def __post_init__(self):
  for n in ('trial_id','context_id','treatment_id','algorithm_id','fold_id','failure_code'):_id(getattr(self,n),n)
  _hash(self.artifact_hash,'artifact_hash')
  if self.decision_count<0:raise TournamentError('negative_decisions','decision_count invalid')
  for k,v in self.metrics.items():_id(k,'metric_id');_finite(v,'metric')
  if self.status is TrialStatus.SUCCEEDED and not self.metrics:raise TournamentError('missing_metrics','successful trial requires metrics')
 @property
 def result_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class LedgerEntry:
 entry_id:str;sequence:int;stage:Stage;event_type:str;payload_hash:str;previous_hash:str;timestamp_ms:int;actor_id:str='system'
 def __post_init__(self):
  _id(self.entry_id,'entry_id');_id(self.event_type,'event_type');_id(self.actor_id,'actor_id');_hash(self.payload_hash,'payload_hash');_hash(self.previous_hash,'previous_hash')
  if self.sequence<0:raise TournamentError('invalid_sequence','sequence invalid')
 @property
 def entry_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class TournamentReport:
 report_id:str;version:str;freeze_hash:str;trial_results:tuple[TrialResult,...];ledger_tail_hash:str;declared_trial_count:int;executed_trial_count:int;succeeded_trial_count:int;failed_trial_count:int;candidate_ids:tuple[str,...];critical_findings:tuple[str,...];reference_only:bool
 def __post_init__(self):
  _id(self.report_id,'report_id');_ver(self.version,'version');_hash(self.freeze_hash,'freeze_hash');_hash(self.ledger_tail_hash,'ledger_tail_hash')
  if self.declared_trial_count<len(self.trial_results):raise TournamentError('trial_count_underflow','declared count below result count')
  if self.executed_trial_count!=self.succeeded_trial_count+self.failed_trial_count:raise TournamentError('execution_count_mismatch','executed count mismatch')
  if self.executed_trial_count>self.declared_trial_count:raise TournamentError('execution_count_overflow','executed exceeds declared')
 @property
 def report_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ProspectivePaperPlan:
 plan_id:str;version:str;frozen_bundle_hash:str;start_time_ms:int;end_time_ms:int;minimum_decisions:int;retraining_allowed:bool;tuning_allowed:bool;expected_cost_model_hash:str;reconciliation_tolerance:float;required_fields:tuple[str,...]
 def __post_init__(self):
  _id(self.plan_id,'plan_id');_ver(self.version,'version');_hash(self.frozen_bundle_hash,'frozen_bundle_hash');_hash(self.expected_cost_model_hash,'expected_cost_model_hash');_finite(self.reconciliation_tolerance,'reconciliation_tolerance')
  if self.start_time_ms>=self.end_time_ms:raise TournamentError('invalid_paper_window','paper window invalid')
  if self.minimum_decisions<1:raise TournamentError('invalid_minimum_decisions','minimum decisions positive')
  if self.retraining_allowed or self.tuning_allowed:raise TournamentError('paper_mutation_forbidden','retraining/tuning forbidden during frozen paper')
  if self.reconciliation_tolerance<0:raise TournamentError('negative_tolerance','tolerance invalid')
 @property
 def plan_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class PaperObservation:
 observation_id:str;decision_hash:str;occurrence_id:str;known_time_ms:int;expected_entry:float;observed_entry:float|None;expected_cost:float;observed_cost:float|None;disposition:str;reason:str
 def __post_init__(self):
  _id(self.observation_id,'observation_id');_hash(self.decision_hash,'decision_hash');_id(self.occurrence_id,'occurrence_id');_id(self.disposition,'disposition');_id(self.reason,'reason')
  for n in ('expected_entry','expected_cost'):_finite(getattr(self,n),n)
  if self.observed_entry is not None:_finite(self.observed_entry,'observed_entry')
  if self.observed_cost is not None:_finite(self.observed_cost,'observed_cost')

@dataclass(frozen=True,slots=True)
class ProspectivePaperReport:
 report_id:str;version:str;plan_hash:str;mode:DataMode;observations:tuple[PaperObservation,...];decision_count:int;matched_count:int;mismatch_count:int;drift_score:float;untouched:bool;completed:bool;critical_findings:tuple[str,...]
 def __post_init__(self):
  _id(self.report_id,'report_id');_ver(self.version,'version');_hash(self.plan_hash,'plan_hash');_finite(self.drift_score,'drift_score')
  if self.decision_count!=len(self.observations):raise TournamentError('paper_count_mismatch','decision count mismatch')
  if self.matched_count+self.mismatch_count>self.decision_count:raise TournamentError('reconciliation_overflow','reconciliation counts overflow')
  if self.completed and self.mode is not DataMode.PROSPECTIVE_PAPER:raise TournamentError('fake_prospective_completion','completed report must use prospective paper mode')
  if not self.untouched:raise TournamentError('paper_period_touched','paper period was tuned or retrained')
 @property
 def report_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ChampionDecision:
 decision_id:str;version:str;tournament_report_hash:str;paper_report_hash:str;status:DecisionStatus;champion_id:str;challenger_ids:tuple[str,...];reasons:tuple[str,...];critical_gates:Mapping[str,bool];promotion_bundle_hash:str|None=None
 def __post_init__(self):
  _id(self.decision_id,'decision_id');_ver(self.version,'version');_hash(self.tournament_report_hash,'tournament_report_hash');_hash(self.paper_report_hash,'paper_report_hash');_id(self.champion_id,'champion_id')
  if self.promotion_bundle_hash is not None:_hash(self.promotion_bundle_hash,'promotion_bundle_hash')
  if self.status is DecisionStatus.PROMOTE:
   if not all(self.critical_gates.values()):raise TournamentError('critical_gate_veto','promotion cannot bypass critical gate')
   if not self.promotion_bundle_hash:raise TournamentError('missing_promotion_bundle','promotion requires bundle hash')
  if self.status is not DecisionStatus.PROMOTE and self.promotion_bundle_hash is not None:raise TournamentError('unexpected_promotion_bundle','non-promotion cannot carry bundle')
 @property
 def decision_hash(self):return canonical_sha256(asdict(self))
