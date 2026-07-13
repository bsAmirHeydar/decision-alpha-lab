from enum import Enum
class AlgorithmFamily(str,Enum):
 BASELINE='baseline';LINEAR='linear';TREE='tree';BOOSTING='boosting';KERNEL='kernel';NEIGHBORHOOD='neighborhood';PROBABILISTIC='probabilistic';ADDITIVE='additive';OPTIONAL_EXTERNAL='optional_external'
class DependencyMode(str,Enum):REQUIRED='required';OPTIONAL='optional';BUILTIN='builtin'
class AvailabilityState(str,Enum):AVAILABLE='available';UNAVAILABLE='unavailable';INCOMPATIBLE='incompatible';DISABLED='disabled'
class CalibrationDisclosure(str,Enum):CALIBRATED='calibrated';UNCALIBRATED='uncalibrated';NOT_APPLICABLE='not_applicable'
class BenchmarkStatus(str,Enum):SUCCEEDED='succeeded';FAILED='failed';SKIPPED_UNAVAILABLE='skipped_unavailable';REJECTED='rejected'
class ExplanationScope(str,Enum):FOLD_HOLDOUT='fold_holdout';CALIBRATION='calibration';FINAL_TEST_AUDIT_ONLY='final_test_audit_only'
class ImportanceKind(str,Enum):COEFFICIENT='coefficient';IMPURITY='impurity';PERMUTATION='permutation';ABLATION='ablation';PARTIAL_DEPENDENCE='partial_dependence';ALE='ale';SHAP_HOOK='shap_hook'
class ComparisonGateState(str,Enum):PASS='pass';BLOCK='block';REVIEW='review'
class PortabilityLevel(str,Enum):NATIVE_JSON='native_json';PARAMETER_SNAPSHOT='parameter_snapshot';LIBRARY_ARTIFACT_REQUIRED='library_artifact_required';RESEARCH_ONLY='research_only'
