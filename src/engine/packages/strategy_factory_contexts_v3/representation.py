"""Deterministic multi-view projection registry sharing one context occurrence identity."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any, Protocol, Sequence
from strategy_factory_contracts_v3 import CanonicalDecimal, IdentityKind, build_identity, canonical_sha256
from .enums import RepresentationKind, AvailabilityMode
from .feature import FeatureFrame
from .errors import ViewError
from .utils import safe_id, contract_safe

@dataclass(frozen=True, slots=True)
class RepresentationViewDescriptor:
    view_id: str; version: str; owner_id: str; kind: RepresentationKind; feature_ids: tuple[str,...]; shape: tuple[int,...]
    availability_modes: AvailabilityMode; runtime_exportable: bool; parameters: Mapping[str,Any]
    def __post_init__(self) -> None:
        safe_id(self.view_id,"view_id"); safe_id(self.version,"version"); safe_id(self.owner_id,"owner_id")
        if len(set(self.feature_ids))!=len(self.feature_ids): raise ViewError("duplicate_view_feature","view feature IDs must be unique")
        if any(x<1 for x in self.shape): raise ViewError("invalid_view_shape","view shape dimensions must be positive")
        if self.availability_modes==AvailabilityMode.NONE: raise ViewError("view_unavailable","view availability is empty")
    def material(self)->Mapping[str,Any]: return {"availability_modes":int(self.availability_modes),"feature_ids":list(self.feature_ids),"kind":self.kind.value,"owner_id":self.owner_id,"parameters":contract_safe(self.parameters),"runtime_exportable":self.runtime_exportable,"shape":list(self.shape),"version":self.version,"view_id":self.view_id}
    @property
    def descriptor_hash(self)->str: return canonical_sha256(self.material())

@dataclass(frozen=True, slots=True)
class RepresentationView:
    descriptor: RepresentationViewDescriptor; context_observation_id: str; feature_frame_hash: str; payload: Mapping[str,Any]
    def material(self)->Mapping[str,Any]: return {"context_observation_id":self.context_observation_id,"descriptor_hash":self.descriptor.descriptor_hash,"feature_frame_hash":self.feature_frame_hash,"payload":contract_safe(self.payload),"view_id":self.descriptor.view_id,"version":self.descriptor.version}
    @property
    def view_hash(self)->str: return canonical_sha256(self.material())
    @property
    def view_instance_id(self)->str: return build_identity(IdentityKind.REPRESENTATION_VIEW,namespace="ucee.representation_view",version=self.descriptor.version,owner_id=self.descriptor.owner_id,context_observation_id=self.context_observation_id,view_id=self.descriptor.view_id,view_hash=self.view_hash).stable_id

class ViewCompiler(Protocol):
    kind: RepresentationKind
    def compile(self, descriptor: RepresentationViewDescriptor, frame: FeatureFrame, auxiliary: Mapping[str,Any]) -> Mapping[str,Any]: ...

def _value_map(frame: FeatureFrame)->dict[str,Any]: return {value.feature_id:value.value for value in frame.values}
def _canon_number(value:Any)->Any:
    if isinstance(value,float): return CanonicalDecimal(str(value),8)
    if isinstance(value,(list,tuple)): return [_canon_number(x) for x in value]
    return value

class TabularCompiler:
    kind=RepresentationKind.TABULAR
    def compile(self,d,frame,aux):
        values=_value_map(frame); return {"columns":list(d.feature_ids),"values":[_canon_number(values[x]) for x in d.feature_ids]}
class SequenceCompiler:
    kind=RepresentationKind.SEQUENCE
    def compile(self,d,frame,aux):
        windows=aux.get("sequence_windows",{}); rows=[]
        for fid in d.feature_ids:
            if fid not in windows: raise ViewError("missing_sequence_window","sequence window is missing",{"feature_id":fid})
            rows.append([_canon_number(x) for x in windows[fid]])
        return {"feature_ids":list(d.feature_ids),"layout":"feature_major","values":rows}
class GraphCompiler:
    kind=RepresentationKind.GRAPH
    def compile(self,d,frame,aux):
        graph=aux.get("graph")
        if not isinstance(graph,Mapping): raise ViewError("missing_graph","graph auxiliary payload is missing")
        return {"edges":list(graph.get("edges",[])),"node_features":dict(graph.get("node_features",{})),"nodes":list(graph.get("nodes",[]))}
class IntermarketCompiler:
    kind=RepresentationKind.INTERMARKET
    def compile(self,d,frame,aux):
        matrix=aux.get("intermarket_matrix")
        if matrix is None: raise ViewError("missing_intermarket_matrix","intermarket matrix is missing")
        return {"symbols":list(aux.get("intermarket_symbols",[])),"values":[[_canon_number(x) for x in row] for row in matrix]}
class RasterCompiler:
    kind=RepresentationKind.RASTER
    def compile(self,d,frame,aux):
        raster=aux.get("raster")
        if raster is None: raise ViewError("missing_raster","raster payload is missing")
        return {"layout":str(aux.get("raster_layout","channels_first")),"values":[_canon_number(x) for x in raster]}
class SparseEventCompiler:
    kind=RepresentationKind.SPARSE_EVENT
    def compile(self,d,frame,aux): return {"events":list(aux.get("sparse_events",[]))}
class PathSignatureCompiler:
    kind=RepresentationKind.PATH_SIGNATURE
    def compile(self,d,frame,aux):
        signature=aux.get("path_signature")
        if signature is None: raise ViewError("missing_path_signature","path signature is missing")
        return {"order":int(aux.get("signature_order",2)),"values":[_canon_number(x) for x in signature]}
class ExecutionCompiler:
    kind=RepresentationKind.EXECUTION
    def compile(self,d,frame,aux): return {"execution_state":dict(aux.get("execution_state",{}))}
class PortfolioCompiler:
    kind=RepresentationKind.PORTFOLIO
    def compile(self,d,frame,aux): return {"portfolio_state":dict(aux.get("portfolio_state",{}))}
class FusedCompiler:
    kind=RepresentationKind.FUSED
    def compile(self,d,frame,aux):
        parts=aux.get("fused_parts")
        if not isinstance(parts,Mapping) or not parts: raise ViewError("missing_fused_parts","fused view needs named child payloads")
        return {"parts":dict(sorted(parts.items()))}

class RepresentationViewRegistry:
    def __init__(self)->None:
        self._compilers={}
        for compiler in (TabularCompiler(),SequenceCompiler(),GraphCompiler(),IntermarketCompiler(),RasterCompiler(),SparseEventCompiler(),PathSignatureCompiler(),ExecutionCompiler(),PortfolioCompiler(),FusedCompiler()): self.register(compiler)
    def register(self,compiler:ViewCompiler)->None:
        if compiler.kind in self._compilers: raise ViewError("duplicate_view_compiler","view compiler already registered",{"kind":compiler.kind.value})
        self._compilers[compiler.kind]=compiler
    def compile(self,descriptor:RepresentationViewDescriptor,frame:FeatureFrame,auxiliary:Mapping[str,Any] | None=None)->RepresentationView:
        compiler=self._compilers.get(descriptor.kind)
        if compiler is None: raise ViewError("unsupported_view_kind","view compiler is not registered",{"kind":descriptor.kind.value})
        missing=sorted(set(descriptor.feature_ids)-{d.feature_id for d in frame.descriptors})
        if missing: raise ViewError("view_feature_missing","view references features absent from frame",{"missing":missing})
        payload=compiler.compile(descriptor,frame,dict(auxiliary or {}))
        return RepresentationView(descriptor,frame.context_observation_id,frame.frame_hash,payload)
