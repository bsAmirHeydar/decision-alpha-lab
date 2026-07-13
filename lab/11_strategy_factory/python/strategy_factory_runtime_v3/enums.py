from enum import Enum
class ExportFormat(str,Enum):
    APPROVED_NATIVE_V1='approved_native_v1'; ONNX='onnx'
class Precision(str,Enum): FLOAT32='float32'; FLOAT64='float64'; INT8='int8'
class RuntimeMode(str,Enum): RESEARCH='research'; TESTER='tester'; SHADOW='shadow'; PAPER='paper'; LIVE='live'
class GenerationState(str,Enum): BUILT='built'; WARMED='warmed'; VALIDATED='validated'; ACTIVE='active'; RETIRED='retired'; QUARANTINED='quarantined'
class ParityStatus(str,Enum): PASS='pass'; FAIL='fail'; NOT_RUN='not_run'
class FeatureKind(str,Enum): NUMERIC='numeric'; CATEGORICAL='categorical'; BOOLEAN='boolean'
class MissingPolicy(str,Enum): ERROR='error'; CONSTANT='constant'; ZERO='zero'
class ScalingKind(str,Enum): IDENTITY='identity'; ZSCORE='zscore'; MINMAX='minmax'
class ModelKind(str,Enum): LINEAR_SOFTMAX='linear_softmax'; LINEAR_SCALAR='linear_scalar'
class RuntimeDisposition(str,Enum): DECIDED='decided'; ABSTAINED='abstained'; REJECTED='rejected'; DUPLICATE='duplicate'; FAILED='failed'
class FailureCode(str,Enum):
    CORRUPT_ARTIFACT='corrupt_artifact'; FEATURE_ORDER_MISMATCH='feature_order_mismatch'; STALE_CONTEXT='stale_context'; SYMBOL_UNAVAILABLE='symbol_unavailable'; INFERENCE_FAILURE='inference_failure'; LATENCY_BREACH='latency_breach'; QUEUE_PRESSURE='queue_pressure'; RESTART_RECONCILIATION='restart_reconciliation'; KILL_SWITCH='kill_switch'; PARTIAL_BUNDLE='partial_bundle'; SIGNATURE_FAILURE='signature_failure'; PARITY_FAILURE='parity_failure'; UNSUPPORTED_OPERATOR='unsupported_operator'
