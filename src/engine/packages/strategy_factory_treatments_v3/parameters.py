from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping
from .enums import ParameterType, MonotonicDirection
from .errors import ParameterError
from .utils import safe_id, dec, canonical_value, stable_id
@dataclass(frozen=True,slots=True)
class ParameterSpec:
    name:str; parameter_type:ParameterType; default:Any
    minimum:Any|None=None; maximum:Any|None=None; allowed_values:tuple[str,...]=()
    units:str='unitless'; identity_affecting:bool=True; monotonic_direction:MonotonicDirection=MonotonicDirection.NONE
    description:str=''
    def __post_init__(self):
        safe_id(self.name,'parameter name'); safe_id(self.units,'parameter units')
        if self.parameter_type is ParameterType.ENUM and not self.allowed_values: raise ParameterError('empty_enum','enum requires allowed_values',{'name':self.name})
        self.validate(self.default)
    def validate(self,v:Any)->Any:
        t=self.parameter_type
        if t is ParameterType.BOOLEAN:
            if not isinstance(v,bool): raise ParameterError('type_mismatch','expected bool',{'name':self.name})
            return v
        if t is ParameterType.INTEGER:
            if isinstance(v,bool) or int(v)!=v: raise ParameterError('type_mismatch','expected integer',{'name':self.name,'value':v})
            x=int(v)
        elif t is ParameterType.DECIMAL: x=dec(v)
        else:
            if not isinstance(v,str): raise ParameterError('type_mismatch','expected string',{'name':self.name})
            x=v
        if t is ParameterType.ENUM and x not in self.allowed_values: raise ParameterError('enum_violation','value not allowed',{'name':self.name,'value':x})
        if t in (ParameterType.INTEGER,ParameterType.DECIMAL):
            if self.minimum is not None and x<dec(self.minimum): raise ParameterError('below_minimum','parameter below minimum',{'name':self.name})
            if self.maximum is not None and x>dec(self.maximum): raise ParameterError('above_maximum','parameter above maximum',{'name':self.name})
        return x
    def to_dict(self):
        return {'name':self.name,'parameter_type':self.parameter_type.value,'default':canonical_value(self.default),'minimum':canonical_value(self.minimum),'maximum':canonical_value(self.maximum),'allowed_values':list(self.allowed_values),'units':self.units,'identity_affecting':self.identity_affecting,'monotonic_direction':self.monotonic_direction.value,'description':self.description}
@dataclass(frozen=True,slots=True)
class ParameterSchema:
    schema_id:str; version:str; specs:tuple[ParameterSpec,...]
    def __post_init__(self):
        safe_id(self.schema_id,'schema_id'); safe_id(self.version,'version')
        names=[s.name for s in self.specs]
        if len(names)!=len(set(names)): raise ParameterError('duplicate_parameter','duplicate parameter name')
    @property
    def definition_id(self): return stable_id('ucep',self.to_dict())
    def bind(self,provided:Mapping[str,Any]|None=None)->'ParameterPacket':
        provided=dict(provided or {}); known={s.name for s in self.specs}; unknown=set(provided)-known
        if unknown: raise ParameterError('unknown_parameter','unknown parameter supplied',{'unknown':sorted(unknown)})
        values={s.name:s.validate(provided.get(s.name,s.default)) for s in self.specs}
        return ParameterPacket(self.definition_id,values)
    def to_dict(self): return {'schema_id':self.schema_id,'version':self.version,'specs':[x.to_dict() for x in self.specs]}
@dataclass(frozen=True,slots=True)
class ParameterPacket:
    schema_definition_id:str; values:Mapping[str,Any]
    @property
    def packet_id(self): return stable_id('ucepp',self.to_dict())
    def get_decimal(self,name:str)->Decimal: return dec(self.values[name])
    def get_int(self,name:str)->int: return int(self.values[name])
    def get_bool(self,name:str)->bool: return bool(self.values[name])
    def get_str(self,name:str)->str: return str(self.values[name])
    def to_dict(self): return {'schema_definition_id':self.schema_definition_id,'values':canonical_value(self.values)}
