from __future__ import annotations
from dataclasses import dataclass
from strategy_factory_contracts.enums import FeatureType
from strategy_factory_contracts.hashing import stable_id
from strategy_factory_contracts.validation import validate_safe_identifier, require, validate_finite
from .enums import UpdateScope, MissingPolicy
@dataclass(frozen=True,slots=True)
class FeatureDescriptor:
    feature_id:str; feature_version:str; owner_id:str; value_type:FeatureType
    update_scope:UpdateScope=UpdateScope.EVENT; required:bool=True; numeric:bool=False
    max_age_milliseconds:int=0; dependencies:tuple[str,...]=()
    def __post_init__(self):
        validate_safe_identifier(self.feature_id,"feature_id",128);validate_safe_identifier(self.feature_version,"feature_version",64);validate_safe_identifier(self.owner_id,"owner_id",128)
        require(self.value_type is not FeatureType.NULL,"NULL feature type is not allowed");require(self.max_age_milliseconds>=0,"negative max age");require(len(self.dependencies)<=16,"too many dependencies")
        require(len(set(self.dependencies))==len(self.dependencies),"duplicate dependency");require(self.feature_id not in self.dependencies,"self dependency")
        for dep in self.dependencies: validate_safe_identifier(dep,"dependency",128)
    @property
    def canonical(self)->str:
        return '|'.join([self.feature_id,self.feature_version,self.owner_id,str(self.value_type.value),str(int(self.update_scope)),str(self.required).lower(),str(self.numeric).lower(),str(self.max_age_milliseconds),*self.dependencies])
    @property
    def descriptor_hash(self)->str:return stable_id('fdsc',self.canonical)
@dataclass(frozen=True,slots=True)
class VectorField:
    feature_id:str; expected_type:FeatureType; missing_policy:MissingPolicy=MissingPolicy.FAIL; default_value:float=0.0
    def __post_init__(self):
        validate_safe_identifier(self.feature_id,"feature_id",128);require(self.expected_type in {FeatureType.DOUBLE,FeatureType.INTEGER,FeatureType.BOOLEAN,FeatureType.TIMESTAMP},"numeric-compatible type required");validate_finite(self.default_value,"default_value")
@dataclass(frozen=True,slots=True)
class FeatureVectorSchema:
    schema_id:str; schema_version:str; fields:tuple[VectorField,...]
    def __post_init__(self):
        validate_safe_identifier(self.schema_id,"schema_id",128);validate_safe_identifier(self.schema_version,"schema_version",64);require(bool(self.fields),"empty vector schema");ids=[x.feature_id for x in self.fields];require(len(ids)==len(set(ids)),"duplicate vector field")
    @property
    def canonical(self)->str:
        parts=[self.schema_id,self.schema_version]
        for f in self.fields:parts.extend([f.feature_id,f.expected_type.value,str(int(f.missing_policy)),format(f.default_value,'.10f')])
        return '|'.join(parts)
    @property
    def schema_hash(self)->str:return stable_id('vsch',self.canonical)
