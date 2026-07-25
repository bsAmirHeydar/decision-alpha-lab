from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .enums import *
from strategy_factory_trainers_v3.canonical import canonical_sha256,stable_id
@dataclass(frozen=True,slots=True)
class DependencyRequirement:module:str;distribution:str;version_spec:str;mode:DependencyMode;feature:str=''
@dataclass(frozen=True,slots=True)
class DependencyStatus:module:str;state:AvailabilityState;installed_version:str='';reason:str='';evidence_hash:str=''
@dataclass(frozen=True,slots=True)
class AlgorithmDescriptor:
 algorithm_id:str;algorithm_version:str;family:AlgorithmFamily;trainer_id:str;trainer_version:str;tasks:tuple[str,...];probability_output:bool;supports_sample_weight:bool;supports_missing_values:bool;supports_multiclass:bool;deterministic_level:str;portability:PortabilityLevel;export_formats:tuple[str,...];dependencies:tuple[DependencyRequirement,...]=();default_hyperparameters:Mapping[str,Any]=field(default_factory=dict);bounded_hyperparameters:Mapping[str,tuple[float|int|str,...]]=field(default_factory=dict);tags:tuple[str,...]=();limitations:tuple[str,...]=()
 @property
 def key(self):return f'{self.algorithm_id}@{self.algorithm_version}'
 @property
 def descriptor_hash(self):return canonical_sha256(asdict(self))
@dataclass(frozen=True,slots=True)
class AlgorithmAvailability:descriptor_key:str;available:bool;dependencies:tuple[DependencyStatus,...];reason:str;evidence_hash:str
@dataclass(frozen=True,slots=True)
class CalibrationRecord:model_state_hash:str;disclosure:CalibrationDisclosure;method:str;fitted_role:str;row_ids_hash:str;parameters:Mapping[str,Any];evidence_hash:str
@dataclass(frozen=True,slots=True)
class ExplanationRequest:request_id:str;model_state_hash:str;dataset_id:str;fold_id:str;role:str;scope:ExplanationScope;kinds:tuple[ImportanceKind,...];for_selection:bool;seed:int;max_rows:int=5000;max_features:int=512
@dataclass(frozen=True,slots=True)
class FeatureImportanceRecord:feature_name:str;feature_index:int;kind:ImportanceKind;mean_importance:float;std_importance:float;direction:float;fold_id:str;role:str;model_state_hash:str;rank:int
@dataclass(frozen=True,slots=True)
class ExplanationArtifact:explanation_id:str;request_id:str;algorithm_key:str;dataset_manifest_hash:str;fold_id:str;role:str;selection_safe:bool;records:tuple[FeatureImportanceRecord,...];partial_dependence:Mapping[str,tuple[tuple[float,float],...]];shap_hook:Mapping[str,Any];limitations:tuple[str,...];evidence_hash:str
@dataclass(frozen=True,slots=True)
class BenchmarkCase:case_id:str;context_id:str;dataset_id:str;dataset_manifest_hash:str;task_key:str;trainer_key:str;trainer_config_hash:str;seed:int;required_family:AlgorithmFamily
@dataclass(frozen=True,slots=True)
class BenchmarkObservation:
 observation_id:str;case_id:str;algorithm_key:str;family:AlgorithmFamily;status:BenchmarkStatus;primary_metric:str;primary_value:float;calibration_metric:str;calibration_value:float;fit_ms:int;predict_ms:int;peak_memory_mb:float;deterministic_rerun:bool;serializable:bool;exportable:bool;explanation_available:bool;oof_evidence_hash:str;final_test_evidence_hash:str;error_code:str='';error_message:str='';warnings:tuple[str,...]=()
@dataclass(frozen=True,slots=True)
class BenchmarkReport:report_id:str;plan_id:str;observations:tuple[BenchmarkObservation,...];required_families:tuple[AlgorithmFamily,...];missing_required_families:tuple[AlgorithmFamily,...];all_probability_disclosed:bool;all_optional_failures_clean:bool;classical_comparison_ready:bool;evidence_hash:str
@dataclass(frozen=True,slots=True)
class ClassicalComparisonGate:gate_id:str;context_id:str;report_id:str;state:ComparisonGateState;required_families:tuple[AlgorithmFamily,...];present_families:tuple[AlgorithmFamily,...];blockers:tuple[str,...];warnings:tuple[str,...];evidence_hash:str
@dataclass(frozen=True,slots=True)
class AlgorithmRegistrySnapshot:snapshot_id:str;descriptors:tuple[AlgorithmDescriptor,...];availability:tuple[AlgorithmAvailability,...];frozen:bool;evidence_hash:str
def make_explanation_id(material):return stable_id('ucexplain',material)
