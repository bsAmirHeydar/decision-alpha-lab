from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import canonical_sha256
from .enums import *
from .errors import OrchestrationError,ResourceBudgetError

def req(v,n):
 if not isinstance(v,str) or not v.strip():raise ValueError(f'{n} required')
@dataclass(frozen=True,slots=True)
class TrainerCapabilityDescriptor:
 trainer_id:str;trainer_version:str;family:str;supported_tasks:tuple[TaskKind,...];supported_views:tuple[ViewKind,...];supported_target_shapes:tuple[TargetShape,...];supported_tensors:tuple[TensorKind,...]=(TensorKind.DENSE_FLOAT64,);missingness_support:MissingnessSupport=MissingnessSupport.REJECT;censoring_support:tuple[CensoringSupport,...]=(CensoringSupport.NONE,);supports_sample_weight:bool=True;supports_multi_output:bool=False;calibration_kinds:tuple[CalibrationKind,...]=(CalibrationKind.NONE,);explainability_kinds:tuple[ExplainabilityKind,...]=(ExplainabilityKind.NONE,);export_formats:tuple[ExportFormat,...]=(ExportFormat.NATIVE_JSON,);devices:tuple[DeviceKind,...]=(DeviceKind.CPU,);precisions:tuple[PrecisionKind,...]=(PrecisionKind.FLOAT64,);determinism:DeterminismLevel=DeterminismLevel.BIT_EXACT;supports_warm_start:bool=False;supports_checkpoint:bool=False;supports_cancel:bool=True;min_rows:int=1;max_features:int=100000;max_outputs:int=1;tags:tuple[str,...]=()
 def __post_init__(self):
  req(self.trainer_id,'trainer_id');req(self.trainer_version,'trainer_version');req(self.family,'family')
  if not self.supported_tasks or not self.supported_views or not self.supported_target_shapes:raise ValueError('empty capability')
 @property
 def key(self):return f'{self.trainer_id}@{self.trainer_version}'
 @property
 def descriptor_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class TaskContract:
 task_id:str;task_version:str;task_kind:TaskKind;view_kind:ViewKind;target_shape:TargetShape;prediction_kind:PredictionKind;primary_metric:str;maximize_metric:bool;output_names:tuple[str,...]=('output',);class_names:tuple[str,...]=();quantile_levels:tuple[float,...]=();bounded_min:float|None=None;bounded_max:float|None=None;censoring:CensoringSupport=CensoringSupport.NONE;sample_weight_required:bool=False;calibration_required:bool=False;threshold_selection_required:bool=False;ranking_group_required:bool=False;treatment_set_required:bool=False
 def __post_init__(self):
  req(self.task_id,'task_id');req(self.task_version,'task_version');req(self.primary_metric,'metric')
 @property
 def key(self):return f'{self.task_id}@{self.task_version}'
 @property
 def contract_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class DatasetSchema:
 dataset_id:str;dataset_manifest_hash:str;feature_order:tuple[str,...];view_kind:ViewKind;tensor_kind:TensorKind;target_shape:TargetShape;output_count:int=1;has_missing_values:bool=False;has_sample_weights:bool=True;has_censoring:bool=False;row_count:int=0
 @property
 def schema_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class TrainerConfig:
 trainer_id:str;trainer_version:str;hyperparameters:Mapping[str,Any];seed:int;calibration_kind:CalibrationKind=CalibrationKind.NONE;threshold_metric:str='';threshold_grid:tuple[float,...]=();notes:str=''
 @property
 def key(self):return f'{self.trainer_id}@{self.trainer_version}'
 @property
 def config_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class ResourceBudget:
 seed:int;max_rows:int=2000000;max_features:int=100000;max_outputs:int=128;max_memory_mb:int=8192;max_wall_seconds:float=3600.;max_workers:int=1;device:DeviceKind=DeviceKind.CPU;precision:PrecisionKind=PrecisionKind.FLOAT64;deterministic_required:bool=True;checkpoint_interval_seconds:float=0.;numeric_tolerance:float=1e-12
 def __post_init__(self):
  if min(self.max_rows,self.max_features,self.max_outputs,self.max_memory_mb,self.max_workers)<1 or self.max_wall_seconds<=0:raise ResourceBudgetError('invalid_budget','resource budget invalid')
 @property
 def budget_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class TrainingRow:
 row_id:str;features:tuple[float,...];target:tuple[float,...];role:SplitRole;fold_id:str;cluster_id:str;event_time_ms:int;known_time_ms:int;sample_weight:float=1.;ranking_group:str='';treatment_id:str='';censor_event:int=0;censor_duration_ms:int=0
@dataclass(frozen=True,slots=True)
class FoldDefinition:
 fold_id:str;train_row_ids:tuple[str,...];calibration_row_ids:tuple[str,...];threshold_row_ids:tuple[str,...];holdout_row_ids:tuple[str,...];purged_row_ids:tuple[str,...]=();embargo_row_ids:tuple[str,...]=()
 def __post_init__(self):
  groups=[set(self.train_row_ids),set(self.calibration_row_ids),set(self.threshold_row_ids),set(self.holdout_row_ids),set(self.purged_row_ids),set(self.embargo_row_ids)]
  if any(a&b for i,a in enumerate(groups) for b in groups[i+1:]):raise OrchestrationError('fold_role_overlap','fold roles overlap')
@dataclass(frozen=True,slots=True)
class OOFProtocol:
 protocol_id:str;protocol_version:str;folds:tuple[FoldDefinition,...];final_train_row_ids:tuple[str,...];final_calibration_row_ids:tuple[str,...];final_threshold_row_ids:tuple[str,...];final_test_row_ids:tuple[str,...];test_sealed:bool=True;purge_ms:int=0;embargo_ms:int=0
 @property
 def protocol_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class OrchestrationPlan:
 plan_id:str;plan_version:str;task:TaskContract;trainer:TrainerConfig;resources:ResourceBudget;oof:OOFProtocol;retain_failed_trials:bool=True;package_artifact:bool=True;require_serialization_parity:bool=True;require_deterministic_rerun:bool=True
 @property
 def plan_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class PredictionLineage:
 dataset_id:str;dataset_manifest_hash:str;task_key:str;trainer_key:str;trainer_config_hash:str;fold_id:str;seed:int;model_state_hash:str;role:SplitRole;orchestration_phase:OrchestrationPhase
@dataclass(frozen=True,slots=True)
class PredictionRecord:
 prediction_id:str;row_id:str;outputs:tuple[float,...];prediction_kind:PredictionKind;lineage:PredictionLineage;threshold:float|None=None;predicted_class:int|None=None
@dataclass(frozen=True,slots=True)
class PredictionBatch:
 batch_id:str;records:tuple[PredictionRecord,...];output_names:tuple[str,...];prediction_kind:PredictionKind;complete:bool;evidence_hash:str
@dataclass(frozen=True,slots=True)
class ThresholdSelection:
 threshold:float;metric_name:str;metric_value:float;maximize:bool;row_ids_hash:str
@dataclass(frozen=True,slots=True)
class TrialLedgerEntry:
 trial_id:str;plan_hash:str;trainer_key:str;fold_id:str;status:TrialStatus;started_sequence:int;finished_sequence:int;elapsed_ms:int;metrics:Mapping[str,float];model_state_hash:str;prediction_batch_hash:str;error_code:str='';error_message:str='';checkpoint_hash:str=''
@dataclass(frozen=True,slots=True)
class TrainerTelemetry:
 telemetry_id:str;sequence:int;phase:OrchestrationPhase;trainer_key:str;fold_id:str;event_code:str;severity:str;elapsed_ms:int;row_count:int;feature_count:int;memory_estimate_mb:float;details:Mapping[str,Any]=field(default_factory=dict)
@dataclass(frozen=True,slots=True)
class AccessAuditRecord:
 sequence:int;row_ids_hash:str;role:SplitRole;purpose:AccessPurpose;phase:OrchestrationPhase;trainer_key:str;allowed:bool;reason:str
@dataclass(frozen=True,slots=True)
class ModelStateBundle:
 trainer_key:str;state_format:str;state_payload:str;state_hash:str;fitted_feature_order:tuple[str,...];fitted_output_names:tuple[str,...]
@dataclass(frozen=True,slots=True)
class ModelArtifactManifest:
 artifact_id:str;artifact_version:str;trainer_descriptor_hash:str;trainer_config_hash:str;task_contract_hash:str;dataset_manifest_hash:str;oof_protocol_hash:str;resource_budget_hash:str;feature_order:tuple[str,...];output_names:tuple[str,...];state_hash:str;calibration_hash:str;threshold_hash:str;environment_hash:str;code_hash:str;metrics:Mapping[str,float];limitations:tuple[str,...];export_formats:tuple[ExportFormat,...];risk_level:ArtifactRiskLevel
@dataclass(frozen=True,slots=True)
class ModelCard:
 model_id:str;title:str;summary:str;intended_uses:tuple[str,...];prohibited_uses:tuple[str,...];training_data_summary:str;evaluation_summary:str;limitations:tuple[str,...];economic_assumptions:tuple[str,...];fairness_scope:str;operational_requirements:tuple[str,...];rollback_conditions:tuple[str,...];residual_risks:tuple[str,...];artifact_manifest_hash:str
@dataclass(frozen=True,slots=True)
class OrchestrationResult:
 run_id:str;plan_hash:str;oof_predictions:PredictionBatch;final_test_predictions:PredictionBatch;threshold:ThresholdSelection|None;fold_trials:tuple[TrialLedgerEntry,...];final_trial:TrialLedgerEntry;artifact_manifest:ModelArtifactManifest|None;model_card:ModelCard|None;access_audit:tuple[AccessAuditRecord,...];telemetry:tuple[TrainerTelemetry,...];selection_locked:bool
