from __future__ import annotations
from .models import ViewFeatureValue,ViewArtifact
from .source_frame import SourceFrame
from .missingness import resolve_missing
from .normalization import normalize,validate_static_normalizer
from .transforms import apply_transform
from .validation import validate_feature_value
from .support import assess_support
from .lineage import view_lineage_root
from .canonical import content_hash,stable_id,parse_time
from .temporal import age_ms
from .enums import ViewStatus,SupportStatus
from .errors import ViewBuildError,TemporalBoundaryError,MissingnessError

class ViewBuilder:
    def build(self,spec,request):
        if spec.twin_id!=request.twin_id:raise ViewBuildError('twin mismatch')
        if request.evidence_role not in spec.evidence_roles:raise ViewBuildError('evidence role not allowed by view spec')
        frame=SourceFrame(request.source_values);features=[]
        for definition in sorted(spec.features,key=lambda x:x.feature_id):
            features.append(self._feature(definition,frame,request))
        support=assess_support(spec,tuple(features))
        status=self._status(support,features)
        lineage_root=view_lineage_root(tuple(features))
        base={'specification_id':spec.specification_id,'specification_hash':spec.semantic_hash,'view_name':spec.view_name,'exact_version':spec.exact_version,'twin_id':spec.twin_id,'kind':spec.kind.value,'known_as_of':request.known_as_of,'event_as_of':request.event_as_of,'evidence_role':request.evidence_role.value,'features':[x.semantic_payload() for x in features],'support':{**support.__dict__,'status':support.status.value},'lineage_root':lineage_root,'limitations':sorted(spec.limitations)}
        view_id=stable_id('view',{'specification_id':spec.specification_id,'known_as_of':request.known_as_of,'event_as_of':request.event_as_of,'evidence_role':request.evidence_role.value,'feature_source_hashes':sorted(h for f in features for h in f.source_value_hashes)})
        base['view_id']=view_id;base['status']=status.value
        view_hash=content_hash(base)
        return ViewArtifact(view_id,spec.specification_id,spec.semantic_hash,spec.view_name,spec.exact_version,spec.twin_id,spec.kind,request.known_as_of,request.event_as_of,request.evidence_role,status,tuple(features),support,lineage_root,tuple(sorted(spec.limitations)),view_hash)
    def _feature(self,d,frame,request):
        validate_static_normalizer(d.normalizer)
        source_values=[];reasons=[]
        for binding in d.inputs:
            try:value=frame.visible(binding.namespace,binding.path,request.known_as_of,request.event_as_of,request.evidence_role)
            except TemporalBoundaryError:
                value=None;reasons.append('not_visible_at_boundary')
            if value is None:
                source_values=[];break
            if value.conflict:reasons.append('source_conflict')
            source_values.append(value)
        if not source_values:
            raw,mask,missing_reasons=resolve_missing(d)
            reasons.extend(missing_reasons);missing=True;stale=False;quality=0.0;last=None;keys=ids=hashes=()
        else:
            raw=apply_transform(d.transform,[x.value for x in source_values],request.event_as_of,[x.event_time for x in source_values]);mask=0;missing=False
            validate_feature_value(d,raw)
            ages=[age_ms(x.event_time,request.event_as_of) for x in source_values];stale=bool(d.maximum_staleness_ms is not None and max(ages)>d.maximum_staleness_ms)
            if stale:reasons.append('stale')
            quality=min(x.quality for x in source_values);last=max(x.event_time for x in source_values)
            keys=tuple(sorted(x.source_key for x in source_values));ids=tuple(sorted(x.source_artifact_id for x in source_values));hashes=tuple(sorted(x.value_hash for x in source_values))
        if raw is not None:
            try:validate_feature_value(d,raw)
            except ViewBuildError:
                reasons.append('out_of_range');raise
        normalized=normalize(raw,d.normalizer)
        return ViewFeatureValue(d.feature_id,raw,normalized,missing,mask,stale,round(float(quality),12),keys,ids,hashes,last,tuple(sorted(set(reasons))))
    @staticmethod
    def _status(support,features):
        if any('source_conflict' in x.reason_codes for x in features):return ViewStatus.CONFLICTED
        if support.status==SupportStatus.UNKNOWN:return ViewStatus.UNKNOWN
        if support.status==SupportStatus.UNSUPPORTED:return ViewStatus.QUARANTINED
        if support.status==SupportStatus.DEGRADED:return ViewStatus.DEGRADED
        return ViewStatus.COMPLETE
