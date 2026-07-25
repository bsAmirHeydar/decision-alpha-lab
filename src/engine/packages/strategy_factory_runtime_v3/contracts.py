from __future__ import annotations
import math,re
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import canonical_sha256,stable_id
from .enums import *
from .errors import RuntimeContractError
_SHA=re.compile(r'^[0-9a-f]{64}$');_SEMVER=re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$');_ID=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:@/-]*$')
def _id(v,n):
    if not isinstance(v,str) or not _ID.fullmatch(v):raise RuntimeContractError('invalid_identifier',f'{n} is invalid',{'value':v})
def _hash(v,n):
    if not isinstance(v,str) or not _SHA.fullmatch(v):raise RuntimeContractError('invalid_sha256',f'{n} must be lowercase SHA-256')
def _semver(v,n):
    if not isinstance(v,str) or not _SEMVER.fullmatch(v):raise RuntimeContractError('invalid_semver',f'{n} must be semantic version')
def _finite(v,n):
    if not math.isfinite(float(v)):raise RuntimeContractError('non_finite',f'{n} must be finite')

@dataclass(frozen=True,slots=True)
class ArtifactRef:
    artifact_id:str; version:str; sha256:str; media_type:str; byte_size:int; role:str; required:bool=True; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        _id(self.artifact_id,'artifact_id');_semver(self.version,'version');_hash(self.sha256,'sha256');_id(self.role,'role')
        if self.byte_size<0:raise RuntimeContractError('invalid_byte_size','byte_size cannot be negative')
        if not self.media_type:raise RuntimeContractError('missing_media_type','media_type required')

@dataclass(frozen=True,slots=True)
class FeatureRule:
    name:str; kind:FeatureKind; missing:MissingPolicy=MissingPolicy.ERROR; missing_value:float=0.0; scaling:ScalingKind=ScalingKind.IDENTITY
    mean:float=0.0; scale:float=1.0; minimum:float=0.0; maximum:float=1.0; clip_min:float|None=None; clip_max:float|None=None; categories:tuple[str,...]=()
    def __post_init__(self):
        _id(self.name,'name')
        for n in ('missing_value','mean','scale','minimum','maximum'):_finite(getattr(self,n),n)
        if self.scale<=0:raise RuntimeContractError('invalid_scale','scale must be positive')
        if self.maximum<=self.minimum and self.scaling is ScalingKind.MINMAX:raise RuntimeContractError('invalid_minmax','maximum must exceed minimum')
        if self.clip_min is not None:_finite(self.clip_min,'clip_min')
        if self.clip_max is not None:_finite(self.clip_max,'clip_max')
        if self.clip_min is not None and self.clip_max is not None and self.clip_min>self.clip_max:raise RuntimeContractError('invalid_clip','clip_min exceeds clip_max')
        if self.kind is FeatureKind.CATEGORICAL:
            if not self.categories:raise RuntimeContractError('empty_categories','categorical feature requires categories')
            if len(set(self.categories))!=len(self.categories):raise RuntimeContractError('duplicate_categories','categories must be unique')

@dataclass(frozen=True,slots=True)
class PreprocessingContract:
    contract_id:str; version:str; feature_order:tuple[str,...]; rules:tuple[FeatureRule,...]; precision:Precision=Precision.FLOAT32; reject_unknown_features:bool=True
    def __post_init__(self):
        _id(self.contract_id,'contract_id');_semver(self.version,'version')
        if not self.feature_order:raise RuntimeContractError('empty_feature_order','feature order required')
        if len(set(self.feature_order))!=len(self.feature_order):raise RuntimeContractError('duplicate_feature','feature order contains duplicates')
        names=tuple(r.name for r in self.rules)
        if names!=self.feature_order:raise RuntimeContractError('feature_order_mismatch','rule order must equal feature_order',{'rules':names,'feature_order':self.feature_order})
    @property
    def preprocessing_hash(self):return canonical_sha256(asdict(self))
    @property
    def output_names(self):
        out=[]
        for r in self.rules:
            if r.kind is FeatureKind.CATEGORICAL:out.extend(f'{r.name}=={c}' for c in r.categories)
            else:out.append(r.name)
        return tuple(out)
    @property
    def output_width(self):return len(self.output_names)

@dataclass(frozen=True,slots=True)
class NativeModelArtifact:
    model_id:str; version:str; kind:ModelKind; input_names:tuple[str,...]; output_names:tuple[str,...]; weights:tuple[tuple[float,...],...]; bias:tuple[float,...]; precision:Precision=Precision.FLOAT32; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        _id(self.model_id,'model_id');_semver(self.version,'version')
        if not self.input_names or len(set(self.input_names))!=len(self.input_names):raise RuntimeContractError('invalid_model_inputs','model inputs must be unique and non-empty')
        if not self.output_names or len(set(self.output_names))!=len(self.output_names):raise RuntimeContractError('invalid_model_outputs','model outputs must be unique and non-empty')
        if len(self.weights)!=len(self.output_names) or len(self.bias)!=len(self.output_names):raise RuntimeContractError('model_shape_mismatch','output dimension mismatch')
        for row in self.weights:
            if len(row)!=len(self.input_names):raise RuntimeContractError('model_shape_mismatch','weight row width mismatch')
            for x in row:_finite(x,'weight')
        for x in self.bias:_finite(x,'bias')
        if self.kind is ModelKind.LINEAR_SCALAR and len(self.output_names)!=1:raise RuntimeContractError('scalar_output_mismatch','scalar model requires one output')
    @property
    def model_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ExportRecord:
    export_id:str; version:str; format:ExportFormat; model_hash:str; artifact_hash:str; precision:Precision; input_names:tuple[str,...]; output_names:tuple[str,...]; opset:int|None=None; warnings:tuple[str,...]=(); unsupported_operators:tuple[str,...]=(); available:bool=True
    def __post_init__(self):
        _id(self.export_id,'export_id');_semver(self.version,'version');_hash(self.model_hash,'model_hash');_hash(self.artifact_hash,'artifact_hash')
        if self.format is ExportFormat.ONNX and self.opset is None:raise RuntimeContractError('missing_opset','ONNX export requires opset')
        if self.available and self.unsupported_operators:raise RuntimeContractError('unsupported_export','available export cannot list unsupported operators')
    @property
    def export_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class RuntimeBundleManifest:
    bundle_id:str; version:str; generation:int; created_at_ms:int; components:tuple[ArtifactRef,...]; preprocessing_hash:str; model_hash:str; export_hash:str; policy_graph_hash:str; manual_policy_hash:str; fallback_policy_hash:str; authority_matrix_hash:str; monitoring_policy_hash:str; rollback_bundle_hash:str; allowed_modes:tuple[RuntimeMode,...]; feature_order:tuple[str,...]; output_names:tuple[str,...]; signature_key_id:str; signature:str=''; limitations:tuple[str,...]=()
    def __post_init__(self):
        _id(self.bundle_id,'bundle_id');_semver(self.version,'version');_id(self.signature_key_id,'signature_key_id')
        if self.generation<1:raise RuntimeContractError('invalid_generation','generation must be positive')
        for n in ('preprocessing_hash','model_hash','export_hash','policy_graph_hash','manual_policy_hash','fallback_policy_hash','authority_matrix_hash','monitoring_policy_hash','rollback_bundle_hash'):_hash(getattr(self,n),n)
        if not self.components:raise RuntimeContractError('empty_bundle','bundle components required')
        roles=[c.role for c in self.components]
        if len(roles)!=len(set(roles)):raise RuntimeContractError('duplicate_component_role','component roles must be unique')
        if not self.allowed_modes:raise RuntimeContractError('empty_modes','allowed modes required')
        if len(set(self.feature_order))!=len(self.feature_order):raise RuntimeContractError('duplicate_feature_order','feature order duplicated')
    @property
    def unsigned_payload(self):
        d=asdict(self);d['signature']='';return d
    @property
    def bundle_hash(self):return canonical_sha256(self.unsigned_payload)

@dataclass(frozen=True,slots=True)
class ParityTolerance:
    absolute:float=1e-6; relative:float=1e-5; decision_exact:bool=True
    def __post_init__(self):
        _finite(self.absolute,'absolute');_finite(self.relative,'relative')
        if self.absolute<0 or self.relative<0:raise RuntimeContractError('negative_tolerance','parity tolerance cannot be negative')

@dataclass(frozen=True,slots=True)
class ParityVector:
    vector_id:str; family:str; features:Mapping[str,Any]; expected_decision:str|None=None; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):_id(self.vector_id,'vector_id');_id(self.family,'family')

@dataclass(frozen=True,slots=True)
class ParityObservation:
    vector_id:str; source_outputs:tuple[float,...]; export_outputs:tuple[float,...]; mql5_outputs:tuple[float,...]; source_decision:str; export_decision:str; mql5_decision:str; max_absolute_error:float; max_relative_error:float; passed:bool; reasons:tuple[str,...]=()
    def __post_init__(self):
        _id(self.vector_id,'vector_id');_finite(self.max_absolute_error,'max_absolute_error');_finite(self.max_relative_error,'max_relative_error')

@dataclass(frozen=True,slots=True)
class ParityCertificate:
    certificate_id:str; version:str; bundle_hash:str; vector_set_hash:str; status:ParityStatus; observations:tuple[ParityObservation,...]; tolerance:ParityTolerance; python_version:str; export_runtime:str; mql5_contract_version:str; created_at_ms:int
    def __post_init__(self):
        _id(self.certificate_id,'certificate_id');_semver(self.version,'version');_hash(self.bundle_hash,'bundle_hash');_hash(self.vector_set_hash,'vector_set_hash');_semver(self.mql5_contract_version,'mql5_contract_version')
        if not self.observations:raise RuntimeContractError('empty_parity_certificate','parity observations required')
        if self.status is ParityStatus.PASS and not all(o.passed for o in self.observations):raise RuntimeContractError('invalid_parity_status','PASS certificate contains failed observation')
    @property
    def certificate_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class RuntimeRequest:
    request_id:str; occurrence_id:str; symbol:str; known_time_ms:int; received_at_ms:int; features:Mapping[str,Any]; mode:RuntimeMode; kill_switch:bool=False; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        for n in ('request_id','occurrence_id','symbol'):_id(getattr(self,n),n)
        if self.known_time_ms>self.received_at_ms:raise RuntimeContractError('future_known_time','known_time exceeds receipt time')

@dataclass(frozen=True,slots=True)
class RuntimeDecision:
    decision_id:str; request_id:str; occurrence_id:str; bundle_hash:str; generation:int; disposition:RuntimeDisposition; label:str; scores:Mapping[str,float]; known_time_ms:int; completed_at_ms:int; latency_us:int; reasons:tuple[str,...]; order_authority:bool=False; trace_hash:str='0'*64
    def __post_init__(self):
        for n in ('decision_id','request_id','occurrence_id'):_id(getattr(self,n),n)
        _hash(self.bundle_hash,'bundle_hash');_hash(self.trace_hash,'trace_hash')
        if self.generation<1 or self.latency_us<0:raise RuntimeContractError('invalid_runtime_counter','generation and latency must be non-negative')
        if self.order_authority:raise RuntimeContractError('order_authority_forbidden','bounded runtime decision cannot carry order authority')
        for k,v in self.scores.items():_id(k,'score_label');_finite(v,'score')
    @property
    def decision_hash(self):
        payload=asdict(self);payload.pop('completed_at_ms',None);payload.pop('latency_us',None);return canonical_sha256(payload)

@dataclass(frozen=True,slots=True)
class GenerationRecord:
    bundle_hash:str; generation:int; state:GenerationState; previous_bundle_hash:str; activated_at_ms:int|None=None; retired_at_ms:int|None=None; parity_certificate_hash:str|None=None; failure_reasons:tuple[str,...]=()
    def __post_init__(self):
        _hash(self.bundle_hash,'bundle_hash');_hash(self.previous_bundle_hash,'previous_bundle_hash')
        if self.parity_certificate_hash is not None:_hash(self.parity_certificate_hash,'parity_certificate_hash')

@dataclass(frozen=True,slots=True)
class ActivationReceipt:
    activation_id:str; bundle_hash:str; generation:int; previous_bundle_hash:str; activated_at_ms:int; idempotency_key:str; state:GenerationState
    def __post_init__(self):
        _id(self.activation_id,'activation_id');_hash(self.bundle_hash,'bundle_hash');_hash(self.previous_bundle_hash,'previous_bundle_hash');_id(self.idempotency_key,'idempotency_key')
    @property
    def receipt_hash(self):return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class FailureFinding:
    code:FailureCode; severity:str; detected:bool; disposition:str; evidence:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        if self.severity not in ('info','warning','critical'):raise RuntimeContractError('invalid_severity','severity invalid')
        _id(self.disposition,'disposition')
@dataclass(frozen=True,slots=True)
class RuntimeFailureReport:
    report_id:str; bundle_hash:str; findings:tuple[FailureFinding,...]; passed:bool; created_at_ms:int
    def __post_init__(self):
        _id(self.report_id,'report_id');_hash(self.bundle_hash,'bundle_hash')
        if self.passed and any(f.detected and f.severity=='critical' for f in self.findings):raise RuntimeContractError('invalid_failure_report','critical finding cannot pass')
    @property
    def report_hash(self):return canonical_sha256(asdict(self))
