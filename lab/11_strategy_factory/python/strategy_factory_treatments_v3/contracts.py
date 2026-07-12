from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
from .enums import TreatmentKind,AtomOwner,RuntimeMode,TradeSide
from .parameters import ParameterSchema,ParameterPacket
from .utils import safe_id,stable_id,canonical_value
@dataclass(frozen=True,slots=True)
class AtomCompatibility:
    supported_sides:tuple[TradeSide,...]=(TradeSide.LONG,TradeSide.SHORT)
    supported_modes:tuple[RuntimeMode,...]=(RuntimeMode.RESEARCH,RuntimeMode.TESTER,RuntimeMode.PAPER,RuntimeMode.SHADOW,RuntimeMode.LIVE)
    required_context_fields:tuple[str,...]=()
    incompatible_atom_ids:tuple[str,...]=()
    tags:tuple[str,...]=()
    def to_dict(self): return {'supported_sides':[x.value for x in self.supported_sides],'supported_modes':[x.value for x in self.supported_modes],'required_context_fields':list(self.required_context_fields),'incompatible_atom_ids':list(self.incompatible_atom_ids),'tags':list(self.tags)}
@dataclass(frozen=True,slots=True)
class TreatmentAtomDescriptor:
    atom_id:str; version:str; kind:TreatmentKind; family:str; owner:AtomOwner; implementation_id:str
    parameter_schema:ParameterSchema; compatibility:AtomCompatibility; description:str=''
    def __post_init__(self):
        for f,v in [('atom_id',self.atom_id),('version',self.version),('family',self.family),('implementation_id',self.implementation_id)]: safe_id(v,f)
    @property
    def exact_key(self): return f'{self.atom_id}@{self.version}'
    @property
    def definition_id(self): return stable_id('ucea',self.to_dict())
    def to_dict(self): return {'atom_id':self.atom_id,'version':self.version,'kind':self.kind.value,'family':self.family,'owner':self.owner.value,'implementation_id':self.implementation_id,'parameter_schema':self.parameter_schema.to_dict(),'compatibility':self.compatibility.to_dict(),'description':self.description}
@dataclass(frozen=True,slots=True)
class TreatmentAtomInvocation:
    descriptor_definition_id:str; exact_key:str; context_occurrence_id:str; feature_frame_hash:str; side:TradeSide; decision_time_ms:int; parameters:ParameterPacket; provenance:Mapping[str,str]
    @property
    def invocation_id(self): return stable_id('ucei',self.to_dict())
    def to_dict(self): return {'descriptor_definition_id':self.descriptor_definition_id,'exact_key':self.exact_key,'context_occurrence_id':self.context_occurrence_id,'feature_frame_hash':self.feature_frame_hash,'side':self.side.value,'decision_time_ms':self.decision_time_ms,'parameters':self.parameters.to_dict(),'provenance':canonical_value(self.provenance)}
