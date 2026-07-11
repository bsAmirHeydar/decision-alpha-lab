from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from .models import OnnxModelManifest,FeatureOrder,PreprocessingManifest,CalibrationContract,TensorContract
from .hashing import sha256_bytes,fnv1a64
from .exporter import inspect_linear_scalar_onnx

@dataclass(frozen=True, slots=True)
class RuntimeCompatibilityReport:
    compatible: bool; errors: tuple[str,...]; warnings: tuple[str,...]; model_sha256: str; model_fnv1a64: str; model_size_bytes: int

def validate_release(model_path: str|Path, manifest: OnnxModelManifest, feature_order: FeatureOrder,
                     preprocessing: PreprocessingManifest, calibration: CalibrationContract,
                     input_contract: TensorContract, output_contract: TensorContract,
                     *, terminal_build: int) -> RuntimeCompatibilityReport:
    errors=[]; warnings=[]
    try: manifest.validate(); feature_order.validate(); preprocessing.validate(len(feature_order.bindings)); calibration.validate(); input_contract.validate(); output_contract.validate()
    except ValueError as exc: errors.append(str(exc))
    data=Path(model_path).read_bytes(); sha=sha256_bytes(data); fnv=fnv1a64(data)
    if sha!=manifest.onnx_sha256: errors.append("ONNX SHA-256 mismatch")
    if fnv!=manifest.onnx_fnv1a64: errors.append("ONNX FNV-1a fingerprint mismatch")
    if len(data)!=manifest.onnx_size_bytes: errors.append("ONNX size mismatch")
    if terminal_build<manifest.minimum_terminal_build: errors.append("terminal build below release minimum")
    if feature_order.feature_schema_hash!=manifest.feature_schema_hash: errors.append("feature schema mismatch")
    if feature_order.order_hash!=manifest.feature_order_hash: errors.append("feature order mismatch")
    if preprocessing.transform_hash!=manifest.transform_hash: errors.append("transform lineage mismatch")
    if preprocessing.manifest_hash!=manifest.preprocessing_manifest_hash: errors.append("preprocessing manifest mismatch")
    if calibration.calibration_hash!=manifest.calibration_hash: errors.append("calibration mismatch")
    if input_contract.contract_hash!=manifest.input_contract_hash or output_contract.contract_hash!=manifest.output_contract_hash: errors.append("tensor contract mismatch")
    try:
        info=inspect_linear_scalar_onnx(data)
        if info["opset"]!=manifest.opset or info["ir_version"]!=manifest.ir_version or info["graph_name"]!=manifest.graph_name: errors.append("ONNX graph metadata mismatch")
        if [op for _,op in info["operators"]] != ["MatMul","Add"]: errors.append("unsupported ONNX operator set")
    except ValueError as exc: errors.append(f"ONNX structural parse failed: {exc}")
    return RuntimeCompatibilityReport(not errors,tuple(errors),tuple(warnings),sha,fnv,len(data))
