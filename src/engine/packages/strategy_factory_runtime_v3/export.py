from __future__ import annotations
import importlib.util,json
from dataclasses import asdict
from typing import Any,Mapping
from .canonical import canonical_bytes,canonical_sha256
from .contracts import NativeModelArtifact,ExportRecord
from .enums import ExportFormat
from .errors import ExportUnavailableError,RuntimeContractError

def onnx_availability()->dict[str,Any]:
    onnx=importlib.util.find_spec('onnx') is not None;runtime=importlib.util.find_spec('onnxruntime') is not None
    return {'onnx':onnx,'onnxruntime':runtime,'available':onnx and runtime}

def export_approved_native(model:NativeModelArtifact)->tuple[ExportRecord,bytes]:
    payload={'format':'approved_native_v1','schema_version':'1.0.0','model':asdict(model)}
    data=canonical_bytes(payload);artifact_hash=canonical_sha256(payload)
    record=ExportRecord(f'export:{model.model_id}','1.0.0',ExportFormat.APPROVED_NATIVE_V1,model.model_hash,artifact_hash,model.precision,model.input_names,model.output_names,warnings=('canonical-json deterministic native representation',))
    return record,data

def export_onnx(model:NativeModelArtifact,opset:int=18)->tuple[ExportRecord,bytes]:
    probe=onnx_availability()
    if not probe['available']:raise ExportUnavailableError('onnx_unavailable','onnx and onnxruntime are required',probe)
    raise ExportUnavailableError('onnx_adapter_not_implemented','this reference pack certifies the approved native path; project-specific ONNX conversion must register an adapter',{'opset':opset})

def load_approved_native(data:bytes)->NativeModelArtifact:
    try:payload=json.loads(data.decode('utf-8'))
    except Exception as e:raise RuntimeContractError('corrupt_export','export is not valid UTF-8 JSON') from e
    if payload.get('format')!='approved_native_v1' or payload.get('schema_version')!='1.0.0':raise RuntimeContractError('unsupported_export_format','export format/version unsupported')
    m=payload.get('model',{})
    from .enums import ModelKind,Precision
    try:return NativeModelArtifact(m['model_id'],m['version'],ModelKind(m['kind']),tuple(m['input_names']),tuple(m['output_names']),tuple(tuple(float(x) for x in r) for r in m['weights']),tuple(float(x) for x in m['bias']),Precision(m['precision']),m.get('metadata',{}))
    except Exception as e:raise RuntimeContractError('corrupt_export','export model payload invalid',{'error':str(e)}) from e
