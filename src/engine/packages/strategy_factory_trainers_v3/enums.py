from enum import Enum
class TaskKind(str,Enum):
 BINARY_CLASSIFICATION='binary_classification'; MULTICLASS_CLASSIFICATION='multiclass_classification'; REGRESSION='regression'; RANKING='ranking'; TREATMENT_CHOICE='treatment_choice'; SURVIVAL='survival'; COMPETING_RISK='competing_risk'; QUANTILE='quantile'; MULTI_TASK='multi_task'; NOVELTY='novelty'; REGIME_GATING='regime_gating'; BOUNDED_POLICY='bounded_policy'
class ViewKind(str,Enum):
 TABULAR='tabular'; SEQUENCE='sequence'; IMAGE='image'; GRAPH='graph'; EVENT_SET='event_set'; MULTI_VIEW='multi_view'; SPARSE_TABULAR='sparse_tabular'; PANEL='panel'; TREATMENT_MATRIX='treatment_matrix'; POLICY_STATE='policy_state'
class TargetShape(str,Enum):
 SCALAR='scalar'; CLASS_INDEX='class_index'; VECTOR='vector'; PAIRWISE='pairwise'; LISTWISE='listwise'; DURATION_EVENT='duration_event'; DURATION_CAUSE='duration_cause'; QUANTILE_VECTOR='quantile_vector'; TREATMENT_UTILITY_VECTOR='treatment_utility_vector'; BOUNDED_ACTION='bounded_action'
class TensorKind(str,Enum):
 DENSE_FLOAT32='dense_float32'; DENSE_FLOAT64='dense_float64'; SPARSE_CSR_FLOAT32='sparse_csr_float32'; INTEGER_INDEX='integer_index'; BOOLEAN_MASK='boolean_mask'; RAGGED_SEQUENCE='ragged_sequence'
class MissingnessSupport(str,Enum): REJECT='reject'; MASK_REQUIRED='mask_required'; NATIVE='native'; PREIMPUTED='preimputed'
class CensoringSupport(str,Enum): NONE='none'; RIGHT='right'; INTERVAL='interval'; COMPETING_RISK='competing_risk'
class CalibrationKind(str,Enum): NONE='none'; IDENTITY='identity'; PLATT='platt'; ISOTONIC='isotonic'; TEMPERATURE='temperature'; CONFORMAL='conformal'
class ExplainabilityKind(str,Enum): NONE='none'; GLOBAL_IMPORTANCE='global_importance'; LOCAL_CONTRIBUTION='local_contribution'; COUNTERFACTUAL='counterfactual'; PARTIAL_DEPENDENCE='partial_dependence'
class ExportFormat(str,Enum): NATIVE_JSON='native_json'; PICKLE_FORBIDDEN='pickle_forbidden'; ONNX='onnx'; MQL5_LINEAR='mql5_linear'; TREELITE='treelite'
class DeviceKind(str,Enum): CPU='cpu'; GPU='gpu'; AUTO='auto'
class PrecisionKind(str,Enum): FLOAT64='float64'; FLOAT32='float32'; MIXED_FLOAT16='mixed_float16'
class DeterminismLevel(str,Enum): BIT_EXACT='bit_exact'; NUMERIC_TOLERANCE='numeric_tolerance'; STATISTICAL='statistical'; NONDETERMINISTIC='nondeterministic'
class TrainerLifecycleState(str,Enum): CREATED='created'; CONFIGURED='configured'; VALIDATED='validated'; FITTED='fitted'; CALIBRATED='calibrated'; EXPORTED='exported'; DISPOSED='disposed'; FAILED='failed'
class SplitRole(str,Enum): TRAIN='train'; CALIBRATION='calibration'; THRESHOLD='threshold'; OOF_HOLDOUT='oof_holdout'; FINAL_TRAIN='final_train'; FINAL_CALIBRATION='final_calibration'; FINAL_THRESHOLD='final_threshold'; FINAL_TEST='final_test'; PURGED='purged'; EMBARGO='embargo'
class OrchestrationPhase(str,Enum): PREFLIGHT='preflight'; FOLD_TRAINING='fold_training'; FOLD_CALIBRATION='fold_calibration'; FOLD_THRESHOLD='fold_threshold'; OOF_PREDICTION='oof_prediction'; SELECTION_LOCK='selection_lock'; FINAL_TRAINING='final_training'; FINAL_CALIBRATION='final_calibration'; FINAL_THRESHOLD='final_threshold'; FINAL_TEST='final_test'; ARTIFACT_PACKAGING='artifact_packaging'
class PredictionKind(str,Enum): SCORE='score'; PROBABILITY='probability'; CLASS='class'; VALUE='value'; RANK_SCORE='rank_score'; QUANTILES='quantiles'; SURVIVAL_CURVE='survival_curve'; CAUSE_HAZARD='cause_hazard'; TREATMENT_UTILITY='treatment_utility'; NOVELTY_SCORE='novelty_score'; ACTION='action'
class TrialStatus(str,Enum): PLANNED='planned'; RUNNING='running'; SUCCEEDED='succeeded'; FAILED='failed'; PRUNED='pruned'; TIMED_OUT='timed_out'; CANCELLED='cancelled'; REJECTED='rejected'
class AccessPurpose(str,Enum): VALIDATE_SCHEMA='validate_schema'; FIT='fit'; CALIBRATE='calibrate'; SELECT_THRESHOLD='select_threshold'; PREDICT_OOF='predict_oof'; PREDICT_FINAL_TEST='predict_final_test'; EXPLAIN='explain'
class ArtifactRiskLevel(str,Enum): LOW='low'; MODERATE='moderate'; HIGH='high'; BLOCKED='blocked'
