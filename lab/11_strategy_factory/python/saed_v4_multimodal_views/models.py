from __future__ import annotations
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import content_hash,stable_id
from .enums import ViewKind,FeatureType,MissingnessPolicy,NormalizationKind,TransformKind,ViewStatus,SupportStatus,CompatibilityStatus,EvidenceRole

@dataclass(frozen=True)
class ViewAuthorityBoundary:
    read_twin:bool=True; read_event_projection:bool=True; read_static_metadata:bool=True; read_approved_descriptor:bool=True; build_view:bool=True; build_package:bool=True; replay:bool=True
    mutate_ucee_truth:bool=False; mutate_twin_manifest:bool=False; mutate_event_journal:bool=False; fit_adaptive_normalizer:bool=False; impute_silently:bool=False; train_model:bool=False; select_treatment:bool=False; allocate_risk:bool=False; activate_runtime:bool=False; send_order:bool=False; network_access:bool=False
    def to_dict(self):return asdict(self)

@dataclass(frozen=True)
class StaticNormalizer:
    kind:NormalizationKind=NormalizationKind.NONE; center:float|None=None; scale:float|None=None; minimum:float|None=None; maximum:float|None=None; statistics_artifact_id:str|None=None; statistics_hash:str|None=None
    def to_dict(self):
        d=asdict(self);d['kind']=self.kind.value;return d

@dataclass(frozen=True)
class InputBinding:
    alias:str; namespace:str; path:str

@dataclass(frozen=True)
class ViewFeatureDefinition:
    feature_id:str; feature_type:FeatureType; inputs:tuple[InputBinding,...]; transform:TransformKind=TransformKind.IDENTITY; required:bool=False; missingness:MissingnessPolicy=MissingnessPolicy.MASK; explicit_default:Any=None; maximum_staleness_ms:int|None=None; minimum_quality:float=0.0; normalizer:StaticNormalizer=field(default_factory=StaticNormalizer); allowed_categories:tuple[str,...]=(); minimum:float|None=None; maximum:float|None=None; vector_length:int|None=None; description:str=''
    def semantic_payload(self):
        return {'feature_id':self.feature_id,'feature_type':self.feature_type.value,'inputs':[asdict(x) for x in self.inputs],'transform':self.transform.value,'required':self.required,'missingness':self.missingness.value,'explicit_default':self.explicit_default,'maximum_staleness_ms':self.maximum_staleness_ms,'minimum_quality':self.minimum_quality,'normalizer':self.normalizer.to_dict(),'allowed_categories':sorted(self.allowed_categories),'minimum':self.minimum,'maximum':self.maximum,'vector_length':self.vector_length,'description':self.description}

@dataclass(frozen=True)
class ViewSpecification:
    view_name:str; exact_version:str; twin_id:str; kind:ViewKind; features:tuple[ViewFeatureDefinition,...]; evidence_roles:tuple[EvidenceRole,...]; required_view:bool; minimum_support_score:float; authority:ViewAuthorityBoundary; description:str; dependencies:tuple[str,...]=(); limitations:tuple[str,...]=()
    def semantic_payload(self):
        return {'view_name':self.view_name,'exact_version':self.exact_version,'twin_id':self.twin_id,'kind':self.kind.value,'features':[x.semantic_payload() for x in sorted(self.features,key=lambda x:x.feature_id)],'evidence_roles':sorted(x.value for x in self.evidence_roles),'required_view':self.required_view,'minimum_support_score':self.minimum_support_score,'authority':self.authority.to_dict(),'description':self.description,'dependencies':sorted(self.dependencies),'limitations':sorted(self.limitations)}
    @property
    def specification_id(self):return stable_id('viewspec',self.semantic_payload())
    @property
    def semantic_hash(self):return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class SourceValue:
    namespace:str; path:str; value:Any; event_time:str; known_time:str; quality:float; evidence_role:EvidenceRole; source_artifact_id:str; source_hash:str; lineage_ids:tuple[str,...]=(); conflict:bool=False
    @property
    def source_key(self):return f'{self.namespace}:{self.path}'
    @property
    def value_hash(self):return content_hash(self.value)

@dataclass(frozen=True)
class ViewBuildRequest:
    twin_id:str; known_as_of:str; event_as_of:str; evidence_role:EvidenceRole; source_values:tuple[SourceValue,...]; request_id:str

@dataclass(frozen=True)
class ViewFeatureValue:
    feature_id:str; value:Any; normalized_value:Any; missing:bool; mask:int; stale:bool; quality:float; source_keys:tuple[str,...]; source_artifact_ids:tuple[str,...]; source_value_hashes:tuple[str,...]; last_event_time:str|None; reason_codes:tuple[str,...]
    def semantic_payload(self):
        return {'feature_id':self.feature_id,'value':self.value,'normalized_value':self.normalized_value,'missing':self.missing,'mask':self.mask,'stale':self.stale,'quality':self.quality,'source_keys':sorted(self.source_keys),'source_artifact_ids':sorted(self.source_artifact_ids),'source_value_hashes':sorted(self.source_value_hashes),'last_event_time':self.last_event_time,'reason_codes':sorted(self.reason_codes)}

@dataclass(frozen=True)
class ViewSupportAssessment:
    status:SupportStatus; score:float; required_total:int; required_passed:int; optional_total:int; optional_passed:int; missing_features:tuple[str,...]; stale_features:tuple[str,...]; low_quality_features:tuple[str,...]; out_of_range_features:tuple[str,...]; reasons:tuple[str,...]
    @property
    def assessment_id(self):return stable_id('viewsupport',{**asdict(self),'status':self.status.value})

@dataclass(frozen=True)
class ViewArtifact:
    view_id:str; specification_id:str; specification_hash:str; view_name:str; exact_version:str; twin_id:str; kind:ViewKind; known_as_of:str; event_as_of:str; evidence_role:EvidenceRole; status:ViewStatus; features:tuple[ViewFeatureValue,...]; support:ViewSupportAssessment; lineage_root:str; limitations:tuple[str,...]; view_hash:str
    def semantic_payload(self):
        return {'view_id':self.view_id,'specification_id':self.specification_id,'specification_hash':self.specification_hash,'view_name':self.view_name,'exact_version':self.exact_version,'twin_id':self.twin_id,'kind':self.kind.value,'known_as_of':self.known_as_of,'event_as_of':self.event_as_of,'evidence_role':self.evidence_role.value,'status':self.status.value,'features':[x.semantic_payload() for x in sorted(self.features,key=lambda x:x.feature_id)],'support':{**asdict(self.support),'status':self.support.status.value},'lineage_root':self.lineage_root,'limitations':sorted(self.limitations)}

@dataclass(frozen=True)
class CrossViewCompatibility:
    status:CompatibilityStatus; twin_id:str; known_as_of:str; event_as_of:str; evidence_role:EvidenceRole; view_ids:tuple[str,...]; missing_required_views:tuple[str,...]; degraded_views:tuple[str,...]; reasons:tuple[str,...]
    @property
    def compatibility_id(self):return stable_id('compat',{**asdict(self),'status':self.status.value,'evidence_role':self.evidence_role.value})

@dataclass(frozen=True)
class MultimodalViewPackage:
    package_id:str; package_version:str; twin_id:str; known_as_of:str; event_as_of:str; evidence_role:EvidenceRole; views:tuple[ViewArtifact,...]; compatibility:CrossViewCompatibility; required_view_names:tuple[str,...]; optional_view_names:tuple[str,...]; missingness_vector:tuple[int,...]; quality_vector:tuple[float,...]; lineage_root:str; package_hash:str; limitations:tuple[str,...]
    def semantic_payload(self):
        return {'package_id':self.package_id,'package_version':self.package_version,'twin_id':self.twin_id,'known_as_of':self.known_as_of,'event_as_of':self.event_as_of,'evidence_role':self.evidence_role.value,'view_hashes':sorted(x.view_hash for x in self.views),'compatibility_id':self.compatibility.compatibility_id,'required_view_names':sorted(self.required_view_names),'optional_view_names':sorted(self.optional_view_names),'missingness_vector':list(self.missingness_vector),'quality_vector':list(self.quality_vector),'lineage_root':self.lineage_root,'limitations':sorted(self.limitations)}

@dataclass(frozen=True)
class ViewDiff:
    left_view_hash:str; right_view_hash:str; changed_features:tuple[str,...]; added_features:tuple[str,...]; removed_features:tuple[str,...]; status_changed:bool; support_changed:bool
    @property
    def diff_id(self):return stable_id('viewdiff',asdict(self))

@dataclass(frozen=True)
class ViewReplayReceipt:
    specification_id:str; known_as_of:str; event_as_of:str; expected_view_hash:str; observed_view_hash:str; status:str
    @property
    def receipt_id(self):return stable_id('viewreplay',asdict(self))

@dataclass(frozen=True)
class ViewIntegrityReceipt:
    package_id:str; package_hash:str; view_hashes:tuple[str,...]; specification_hashes:tuple[str,...]; lineage_root:str; component_root:str; status:str
    @property
    def receipt_id(self):return stable_id('viewintegrity',asdict(self))
