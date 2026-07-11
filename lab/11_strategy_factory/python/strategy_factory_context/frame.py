from __future__ import annotations
from dataclasses import dataclass
from strategy_factory_contracts.enums import FeatureQuality,FeatureType
from strategy_factory_contracts.hashing import stable_id
from strategy_factory_contracts.records import FeatureSnapshot
from strategy_factory_contracts.time import MarketTimestamp
from .descriptor import FeatureVectorSchema
from .enums import MissingPolicy
@dataclass(frozen=True,slots=True)
class FixedFeatureVector:
    vector_id:str;event_id:str;schema_hash:str;state_generation:int;feature_ids:tuple[str,...];values:tuple[float,...];quality:tuple[FeatureQuality,...]
    @classmethod
    def build(cls,schema:FeatureVectorSchema,snapshot:FeatureSnapshot)->"FixedFeatureVector":
        by_id={x.feature_id:x for x in snapshot.values};ids=[];values=[];qualities=[];parts=[snapshot.event_id,schema.schema_hash,str(snapshot.state_generation)]
        for field in schema.fields:
            feature=by_id.get(field.feature_id);value=field.default_value;quality=FeatureQuality.MISSING
            if feature is None:
                if field.missing_policy is MissingPolicy.FAIL:raise ValueError(f'required vector feature missing: {field.feature_id}')
                if field.missing_policy is MissingPolicy.ZERO:value=0.0
            else:
                if feature.value_type is not field.expected_type:raise ValueError(f'vector type mismatch: {field.feature_id}')
                quality=feature.quality
                if quality in {FeatureQuality.VALID,FeatureQuality.ESTIMATED}:
                    if feature.value_type is FeatureType.BOOLEAN:value=1.0 if feature.value else 0.0
                    elif feature.value_type is FeatureType.TIMESTAMP:value=float(feature.value.utc_epoch_milliseconds)
                    else:value=float(feature.value)
                elif field.missing_policy is MissingPolicy.FAIL:raise ValueError(f'required vector feature not valid: {field.feature_id}')
                elif field.missing_policy is MissingPolicy.ZERO:value=0.0
            ids.append(field.feature_id);values.append(value);qualities.append(quality);parts.extend([field.feature_id,format(value,'.10f'),quality.value])
        return cls(stable_id('fvec','|'.join(parts)),snapshot.event_id,schema.schema_hash,snapshot.state_generation,tuple(ids),tuple(values),tuple(qualities))
@dataclass(frozen=True,slots=True)
class ContextFrame:
    frame_id:str;event_id:str;snapshot_id:str;graph_hash:str;vector_schema_hash:str;vector_id:str;state_generation:int;feature_count:int;snapshot_time:MarketTimestamp;source_hash:str;schema:str='alpha_lab.strategy_factory/context_frame@1.0.0'
    @property
    def canonical(self)->str:return '|'.join([self.schema,self.event_id,self.snapshot_id,self.graph_hash,self.vector_schema_hash,self.vector_id,str(self.state_generation),str(self.feature_count),str(self.snapshot_time.utc_epoch_milliseconds),self.source_hash])
    @property
    def derived_id(self)->str:return stable_id('ctx',self.canonical)
