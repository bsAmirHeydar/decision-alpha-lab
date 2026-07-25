"""Feature availability, missingness, staleness and immutable frame contracts."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any, Sequence
from strategy_factory_contracts_v3 import CanonicalDecimal, IdentityKind, UtcInstant, build_identity, canonical_sha256
from .enums import FeatureDataType, MissingnessPolicy, StalenessPolicy, AvailabilityMode, FreshnessState
from .errors import FeatureError
from .utils import safe_id

@dataclass(frozen=True, slots=True)
class FeatureDescriptor:
    feature_id: str; version: str; owner_id: str; data_type: FeatureDataType; units: str; shape: tuple[int,...]
    missingness_policy: MissingnessPolicy; staleness_policy: StalenessPolicy; max_staleness_ms: int
    dependencies: tuple[str,...]; availability_modes: AvailabilityMode; runtime_exportable: bool; category_values: tuple[str,...]=(); description: str=""
    def __post_init__(self) -> None:
        for n in ("feature_id","version","owner_id","units"): safe_id(getattr(self,n),n)
        if self.max_staleness_ms<0: raise FeatureError("negative_staleness","max_staleness_ms may not be negative")
        if any(x<1 for x in self.shape): raise FeatureError("invalid_shape","feature shape dimensions must be positive")
        if self.data_type==FeatureDataType.CATEGORY and not self.category_values: raise FeatureError("category_without_domain","categorical feature requires category_values")
        if self.availability_modes==AvailabilityMode.NONE: raise FeatureError("feature_unavailable","feature availability is empty")
        if len(set(self.dependencies))!=len(self.dependencies): raise FeatureError("duplicate_dependency","feature dependencies contain duplicates")
    def material(self) -> Mapping[str,Any]:
        return {"availability_modes":int(self.availability_modes),"category_values":list(self.category_values),"data_type":self.data_type.value,"dependencies":list(self.dependencies),"description":self.description,"feature_id":self.feature_id,"max_staleness_ms":self.max_staleness_ms,"missingness_policy":self.missingness_policy.value,"owner_id":self.owner_id,"runtime_exportable":self.runtime_exportable,"shape":list(self.shape),"staleness_policy":self.staleness_policy.value,"units":self.units,"version":self.version}
    @property
    def descriptor_hash(self) -> str: return canonical_sha256(self.material())

@dataclass(frozen=True, slots=True)
class FeatureValue:
    feature_id: str; feature_version: str; value: Any; known_time: UtcInstant; source_time: UtcInstant; is_missing: bool=False; missing_reason: str="none"
    def __post_init__(self) -> None:
        safe_id(self.feature_id,"feature_id"); safe_id(self.feature_version,"feature_version"); safe_id(self.missing_reason,"missing_reason")
        if self.is_missing and self.value is not None: raise FeatureError("missing_with_value","missing feature value must be None")
        if not self.is_missing and self.value is None: raise FeatureError("present_without_value","present feature needs value")
        if self.known_time.epoch_ms < self.source_time.epoch_ms: raise FeatureError("feature_known_before_source","feature known_time precedes source_time")

@dataclass(frozen=True, slots=True)
class FeatureFrame:
    context_observation_id: str; context_package_id: str; context_package_version: str; observation_cut: UtcInstant; descriptors: tuple[FeatureDescriptor,...]; values: tuple[FeatureValue,...]
    def __post_init__(self) -> None:
        safe_id(self.context_observation_id,"context_observation_id"); safe_id(self.context_package_id,"context_package_id"); safe_id(self.context_package_version,"context_package_version")
        descriptor_ids=[x.feature_id for x in self.descriptors]; value_ids=[x.feature_id for x in self.values]
        if descriptor_ids != sorted(descriptor_ids): raise FeatureError("unordered_descriptors","descriptors must be sorted by feature_id")
        if value_ids != descriptor_ids: raise FeatureError("descriptor_value_mismatch","value order and IDs must exactly match descriptors",{"descriptors":descriptor_ids,"values":value_ids})
        for descriptor,value in zip(self.descriptors,self.values):
            if descriptor.version!=value.feature_version: raise FeatureError("feature_version_mismatch","feature value version differs from descriptor",{"feature_id":descriptor.feature_id})
            if value.known_time.epoch_ms>self.observation_cut.epoch_ms: raise FeatureError("future_feature","feature became known after observation_cut",{"feature_id":value.feature_id})
            age=self.observation_cut.epoch_ms-value.known_time.epoch_ms
            if age>descriptor.max_staleness_ms and descriptor.staleness_policy==StalenessPolicy.REJECT: raise FeatureError("stale_feature","feature exceeds staleness limit",{"feature_id":value.feature_id,"age_ms":age})
            if value.is_missing and descriptor.missingness_policy==MissingnessPolicy.REJECT: raise FeatureError("missing_required_feature","feature is missing under reject policy",{"feature_id":value.feature_id})
    def freshness(self, feature_id: str) -> FreshnessState:
        idx=next((i for i,d in enumerate(self.descriptors) if d.feature_id==feature_id),None)
        if idx is None: return FreshnessState.INVALID
        descriptor,value=self.descriptors[idx],self.values[idx]
        if value.is_missing: return FreshnessState.MISSING
        age=self.observation_cut.epoch_ms-value.known_time.epoch_ms
        return FreshnessState.STALE if age>descriptor.max_staleness_ms else FreshnessState.FRESH
    def material(self) -> Mapping[str,Any]:
        def safe_value(v:Any)->Any:
            if isinstance(v,float): return CanonicalDecimal(str(v),8)
            if isinstance(v,(list,tuple)): return [safe_value(x) for x in v]
            return v
        rows=[]
        for d,v in zip(self.descriptors,self.values):
            rows.append({"descriptor_hash":d.descriptor_hash,"feature_id":v.feature_id,"feature_version":v.feature_version,"freshness":self.freshness(v.feature_id).value,"is_missing":v.is_missing,"known_time_ms":v.known_time.epoch_ms,"missing_reason":v.missing_reason,"source_time_ms":v.source_time.epoch_ms,"value":safe_value(v.value)})
        return {"context_observation_id":self.context_observation_id,"context_package_id":self.context_package_id,"context_package_version":self.context_package_version,"features":rows,"observation_cut_ms":self.observation_cut.epoch_ms}
    @property
    def frame_hash(self) -> str: return canonical_sha256(self.material())
    @property
    def frame_id(self) -> str: return build_identity(IdentityKind.REPRESENTATION_VIEW,namespace="ucee.feature_frame",version=self.context_package_version,owner_id=self.context_package_id,context_observation_id=self.context_observation_id,frame_hash=self.frame_hash).stable_id
