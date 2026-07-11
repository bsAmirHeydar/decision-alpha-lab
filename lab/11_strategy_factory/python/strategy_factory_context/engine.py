from __future__ import annotations
from dataclasses import dataclass,replace
from strategy_factory_contracts.enums import FeatureQuality
from strategy_factory_contracts.records import AnatomyEvent,FeatureSnapshot
from .registry import FeatureRegistry
from .state import ContextState
from .descriptor import FeatureVectorSchema
from .frame import FixedFeatureVector,ContextFrame
class ContextBuildError(RuntimeError):pass
@dataclass(slots=True)
class ContextTelemetry:
    build_count:int=0;build_failures:int=0;feature_computations:int=0;feature_cache_hits:int=0;vector_builds:int=0
class ContextEngine:
    def __init__(self,registry:FeatureRegistry,vector_schema:FeatureVectorSchema,capacity:int=256):
        self.registry=registry;self.vector_schema=vector_schema;self.state=ContextState(capacity);self.telemetry=ContextTelemetry();self.registry.compile();self.registry.validate_vector_fields(vector_schema.fields);self.last_frame=None;self.last_vector=None
    def build(self,event:AnatomyEvent,generation:int)->tuple[FeatureSnapshot,ContextFrame,FixedFeatureVector]:
        try:
            self.state.begin_generation(generation,event.event_id,event.confirmation_time);self.state.mark_all_dirty('EVENT');values=[]
            for feature_id in self.registry.order:
                node=self.registry.node(feature_id);descriptor=node.descriptor
                feature=node.compute(event,self.state);self.telemetry.feature_computations+=1
                if feature.feature_id!=descriptor.feature_id or feature.feature_version!=descriptor.feature_version or feature.value_type is not descriptor.value_type:raise ContextBuildError(f'feature contract mismatch: {feature_id}')
                if feature.known_time>event.confirmation_time:raise ContextBuildError(f'future feature: {feature_id}')
                if descriptor.required and feature.quality not in {FeatureQuality.VALID,FeatureQuality.ESTIMATED}:raise ContextBuildError(f'invalid required feature: {feature_id}')
                self.state.put(feature,descriptor.max_age_milliseconds);values.append(feature)
            snapshot=FeatureSnapshot('',event.event_id,event.strategy_id,event.confirmation_time,'sf07.context_engine','1.0.0',self.registry.graph_hash,generation,tuple(values)).with_derived_id()
            vector=FixedFeatureVector.build(self.vector_schema,snapshot);self.telemetry.vector_builds+=1
            frame=ContextFrame('',event.event_id,snapshot.snapshot_id,self.registry.graph_hash,self.vector_schema.schema_hash,vector.vector_id,generation,len(values),snapshot.snapshot_time,event.source_hash)
            frame=replace(frame,frame_id=frame.derived_id);self.last_frame=frame;self.last_vector=vector;self.telemetry.build_count+=1;return snapshot,frame,vector
        except Exception as exc:
            self.telemetry.build_failures+=1
            if isinstance(exc,ContextBuildError):raise
            raise ContextBuildError(str(exc)) from exc
