from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Sequence
import math
from .enums import *
from .hashing import stable_id,cfloat,cbool

SCHEMA="alpha_lab.strategy_factory"
def req(*values: str):
    if any(not x for x in values): raise ValueError("missing identity or lineage")

@dataclass(frozen=True, slots=True)
class TensorContract:
    name: str; element_type: TensorElementType; shape: tuple[int,...]; ordinal: int=0; contract_hash: str=""
    def canonical(self)->str: return "|".join(map(str,[f"{SCHEMA}/tensor_contract@1.0.0",self.name,int(self.element_type),self.ordinal,",".join(map(str,self.shape))]))
    def with_hash(self): return type(self)(self.name,self.element_type,self.shape,self.ordinal,stable_id("tens",self.canonical()))
    def validate(self):
        req(self.name)
        if not self.shape or any(v<1 for v in self.shape): raise ValueError("invalid static tensor shape")
        if self.ordinal<0: raise ValueError("invalid tensor ordinal")
        if self.contract_hash and self.contract_hash!=stable_id("tens",self.canonical()): raise ValueError("tensor hash mismatch")

@dataclass(frozen=True, slots=True)
class FeatureBinding:
    feature_id: str; feature_version: str; ordinal: int; value_type: str="float32"; required: bool=True
    def canonical(self)->str: return ":".join(map(str,[self.ordinal,f"{self.feature_id}@{self.feature_version}",self.value_type,int(self.required)]))
    def validate(self):
        req(self.feature_id,self.feature_version,self.value_type)
        if self.ordinal<0 or self.ordinal>=4096: raise ValueError("feature ordinal outside bound")

@dataclass(frozen=True, slots=True)
class FeatureOrder:
    feature_schema_hash: str; bindings: tuple[FeatureBinding,...]; order_hash: str=""
    def canonical(self)->str: return "|".join([f"{SCHEMA}/feature_order@1.0.0",self.feature_schema_hash,*[x.canonical() for x in self.bindings]])
    def with_hash(self): return type(self)(self.feature_schema_hash,self.bindings,stable_id("ford",self.canonical()))
    def validate(self):
        req(self.feature_schema_hash)
        if not self.bindings: raise ValueError("empty feature order")
        for i,b in enumerate(self.bindings): b.validate();
        if tuple(b.ordinal for b in self.bindings)!=tuple(range(len(self.bindings))): raise ValueError("feature order is not dense and exact")
        if len({(b.feature_id,b.feature_version) for b in self.bindings})!=len(self.bindings): raise ValueError("duplicate feature")
        if self.order_hash and self.order_hash!=stable_id("ford",self.canonical()): raise ValueError("feature-order hash mismatch")

@dataclass(frozen=True, slots=True)
class PreprocessingManifest:
    feature_schema_hash: str; transform_hash: str; impute_values: tuple[float,...]; means: tuple[float,...]; scales: tuple[float,...]
    missing_policy: str="TRAIN_IMPUTE"; scale_policy: str="STANDARDIZE"; fitted_role: str="TRAIN"; fitted_rowset_hash: str=""; manifest_hash: str=""
    def canonical(self)->str:
        vec=lambda x:",".join(cfloat(v) for v in x)
        return "|".join([f"{SCHEMA}/preprocessing_manifest@1.0.0",self.feature_schema_hash,self.transform_hash,vec(self.impute_values),vec(self.means),vec(self.scales),self.missing_policy,self.scale_policy,self.fitted_role,self.fitted_rowset_hash])
    def with_hash(self): return type(self)(**{**asdict(self),"impute_values":self.impute_values,"means":self.means,"scales":self.scales,"manifest_hash":stable_id("prep",self.canonical())})
    def validate(self,width:int):
        req(self.feature_schema_hash,self.transform_hash,self.missing_policy,self.scale_policy,self.fitted_role,self.fitted_rowset_hash)
        if self.fitted_role!="TRAIN": raise ValueError("preprocessing was not fitted on training rows")
        if not (len(self.impute_values)==len(self.means)==len(self.scales)==width): raise ValueError("preprocessing width mismatch")
        if any(not math.isfinite(v) for v in (*self.impute_values,*self.means,*self.scales)): raise ValueError("non-finite preprocessing state")
        if any(v<=0 for v in self.scales): raise ValueError("non-positive scale")
        if self.manifest_hash and self.manifest_hash!=stable_id("prep",self.canonical()): raise ValueError("preprocessing hash mismatch")

@dataclass(frozen=True, slots=True)
class CalibrationContract:
    method: CalibrationMethod; a: float=1.0; b: float=0.0; threshold: float=0.5; calibration_hash: str=""
    def canonical(self)->str: return "|".join(map(str,[f"{SCHEMA}/calibration_contract@1.0.0",int(self.method),cfloat(self.a),cfloat(self.b),cfloat(self.threshold)]))
    def with_hash(self): return type(self)(self.method,self.a,self.b,self.threshold,stable_id("cal",self.canonical()))
    def validate(self):
        if not all(math.isfinite(x) for x in (self.a,self.b,self.threshold)): raise ValueError("non-finite calibration")
        if not 0<=self.threshold<=1: raise ValueError("threshold outside probability range")
        if self.calibration_hash and self.calibration_hash!=stable_id("cal",self.canonical()): raise ValueError("calibration hash mismatch")

@dataclass(frozen=True, slots=True)
class OnnxModelManifest:
    export_id: str; model_id: str; model_version: str; release_hash: str; registry_scope_hash: str; model_artifact_hash: str
    onnx_sha256: str; onnx_fnv1a64: str; onnx_size_bytes: int; feature_schema_hash: str; feature_order_hash: str; transform_hash: str
    preprocessing_manifest_hash: str; calibration_hash: str; input_contract_hash: str; output_contract_hash: str
    output_semantics: OutputSemantics; opset: int; ir_version: int; graph_name: str; relative_model_path: str
    minimum_terminal_build: int; generated_at_utc_msc: int; code_revision: str; manifest_hash: str=""
    def canonical(self)->str:
        return "|".join(map(str,[f"{SCHEMA}/onnx_model_manifest@1.0.0",self.export_id,self.model_id,self.model_version,self.release_hash,self.registry_scope_hash,self.model_artifact_hash,self.onnx_sha256,self.onnx_fnv1a64,self.onnx_size_bytes,self.feature_schema_hash,self.feature_order_hash,self.transform_hash,self.preprocessing_manifest_hash,self.calibration_hash,self.input_contract_hash,self.output_contract_hash,int(self.output_semantics),self.opset,self.ir_version,self.graph_name,self.relative_model_path,self.minimum_terminal_build,self.generated_at_utc_msc,self.code_revision]))
    def with_hash(self): return type(self)(**{**asdict(self),"output_semantics":self.output_semantics,"manifest_hash":stable_id("omnf",self.canonical())})
    def validate(self):
        req(self.export_id,self.model_id,self.model_version,self.release_hash,self.registry_scope_hash,self.model_artifact_hash,self.onnx_sha256,self.onnx_fnv1a64,self.feature_schema_hash,self.feature_order_hash,self.transform_hash,self.preprocessing_manifest_hash,self.calibration_hash,self.input_contract_hash,self.output_contract_hash,self.graph_name,self.relative_model_path,self.code_revision)
        if len(self.onnx_sha256)!=64 or len(self.onnx_fnv1a64)!=16: raise ValueError("invalid model digest width")
        if self.onnx_size_bytes<1 or self.opset<7 or self.ir_version<3 or self.minimum_terminal_build<1: raise ValueError("unsupported runtime contract")
        if self.manifest_hash and self.manifest_hash!=stable_id("omnf",self.canonical()): raise ValueError("manifest hash mismatch")

@dataclass(frozen=True, slots=True)
class InferenceRequest:
    request_id: str; run_id: str; generation_id: str; context_frame_id: str; candidate_id: str; feature_schema_hash: str
    feature_order_hash: str; known_time_utc_msc: int; decision_time_utc_msc: int; values: tuple[float,...]; missing: tuple[bool,...]
    request_hash: str=""
    def canonical(self)->str:
        vals=",".join("NA" if m else cfloat(v) for v,m in zip(self.values,self.missing))
        return "|".join(map(str,[f"{SCHEMA}/inference_request@1.0.0",self.request_id,self.run_id,self.generation_id,self.context_frame_id,self.candidate_id,self.feature_schema_hash,self.feature_order_hash,self.known_time_utc_msc,self.decision_time_utc_msc,vals]))
    def with_hash(self):
        rid=self.request_id or stable_id("ireq",self.run_id,self.generation_id,self.context_frame_id,self.candidate_id,self.decision_time_utc_msc)
        x=type(self)(**{**asdict(self),"values":self.values,"missing":self.missing,"request_id":rid,"request_hash":""})
        return type(self)(**{**asdict(x),"values":x.values,"missing":x.missing,"request_hash":stable_id("ireqh",x.canonical())})
    def validate(self,width:int):
        req(self.run_id,self.generation_id,self.context_frame_id,self.candidate_id,self.feature_schema_hash,self.feature_order_hash)
        if self.decision_time_utc_msc<self.known_time_utc_msc: raise ValueError("decision precedes known time")
        if len(self.values)!=width or len(self.missing)!=width: raise ValueError("request width mismatch")
        if any((not m and not math.isfinite(v)) for v,m in zip(self.values,self.missing)): raise ValueError("non-finite observed feature")
        if self.request_hash:
            if self.request_hash!=stable_id("ireqh",type(self)(**{**asdict(self),"values":self.values,"missing":self.missing,"request_hash":""}).canonical()): raise ValueError("request hash mismatch")

@dataclass(frozen=True, slots=True)
class InferenceResult:
    result_id: str; request_id: str; model_id: str; model_version: str; release_hash: str; manifest_hash: str
    status: InferenceStatus; raw_score: float; calibrated_score: float; predicted_class: int; threshold: float
    inference_time_utc_msc: int; latency_micros: int; backend: RuntimeBackend; error_code: int=0; error_message: str=""; result_hash: str=""
    def canonical(self)->str:
        return "|".join(map(str,[f"{SCHEMA}/inference_result@1.0.0",self.result_id,self.request_id,self.model_id,self.model_version,self.release_hash,self.manifest_hash,int(self.status),cfloat(self.raw_score),cfloat(self.calibrated_score),self.predicted_class,cfloat(self.threshold),self.inference_time_utc_msc,self.latency_micros,int(self.backend),self.error_code,self.error_message]))
    def with_hash(self):
        rid=self.result_id or stable_id("ires",self.request_id,self.model_id,self.model_version)
        x=type(self)(**{**asdict(self),"status":self.status,"backend":self.backend,"result_id":rid,"result_hash":""})
        return type(self)(**{**asdict(x),"status":x.status,"backend":x.backend,"result_hash":stable_id("iresh",x.canonical())})
    def validate(self):
        req(self.request_id,self.model_id,self.model_version,self.release_hash,self.manifest_hash)
        if not all(math.isfinite(x) for x in (self.raw_score,self.calibrated_score,self.threshold)): raise ValueError("non-finite result")
        if self.status==InferenceStatus.ACCEPTED and not 0<=self.calibrated_score<=1: raise ValueError("accepted probability outside range")
        if self.latency_micros<0: raise ValueError("negative latency")

@dataclass(frozen=True, slots=True)
class ParityVector:
    vector_id: str; values: tuple[float,...]; missing: tuple[bool,...]; expected_transformed: tuple[float,...]
    expected_raw_score: float; expected_calibrated_score: float; expected_class: int; vector_hash: str=""
    def canonical(self)->str:
        enc=lambda xs:",".join(cfloat(v) for v in xs)
        return "|".join(map(str,[f"{SCHEMA}/parity_vector@1.0.0",self.vector_id,enc(self.values),",".join(cbool(x) for x in self.missing),enc(self.expected_transformed),cfloat(self.expected_raw_score),cfloat(self.expected_calibrated_score),self.expected_class]))
    def with_hash(self): return type(self)(**{**asdict(self),"values":self.values,"missing":self.missing,"expected_transformed":self.expected_transformed,"vector_hash":stable_id("pvec",self.canonical())})

@dataclass(frozen=True, slots=True)
class ParityReport:
    report_id: str; manifest_hash: str; backend: RuntimeBackend; vector_count: int; passed_count: int; failed_count: int
    maximum_raw_abs_error: float; maximum_calibrated_abs_error: float; raw_tolerance: float; calibrated_tolerance: float
    verdict: ParityVerdict; report_hash: str=""
    def canonical(self)->str: return "|".join(map(str,[f"{SCHEMA}/parity_report@1.0.0",self.report_id,self.manifest_hash,int(self.backend),self.vector_count,self.passed_count,self.failed_count,cfloat(self.maximum_raw_abs_error),cfloat(self.maximum_calibrated_abs_error),cfloat(self.raw_tolerance),cfloat(self.calibrated_tolerance),int(self.verdict)]))
    def with_hash(self): return type(self)(**{**asdict(self),"backend":self.backend,"verdict":self.verdict,"report_hash":stable_id("prep",self.canonical())})
