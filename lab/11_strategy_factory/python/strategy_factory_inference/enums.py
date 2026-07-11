from enum import IntEnum
class TensorElementType(IntEnum): FLOAT32=1
class OutputSemantics(IntEnum): SCALAR_SCORE=1; BINARY_LOGIT=2; BINARY_PROBABILITY=3
class CalibrationMethod(IntEnum): IDENTITY=0; SIGMOID=1; PLATT=2
class InferenceStatus(IntEnum): ACCEPTED=1; REJECTED=2; RUNTIME_ERROR=3; NON_FINITE=4; LINEAGE_MISMATCH=5
class RuntimeBackend(IntEnum): PYTHON_REFERENCE=1; ONNX_RUNTIME=2; MQL5_ONNX=3
class ParityVerdict(IntEnum): PASS=1; FAIL=2; NOT_RUN=3
