from .models import MultimodalViewPackage
from .compatibility import assess_compatibility
from .lineage import package_lineage_root
from .canonical import content_hash,stable_id

class MultimodalPackageBuilder:
    def build(self,views,package_version,required_view_names,optional_view_names=(),limitations=()):
        views=tuple(sorted(views,key=lambda x:(x.view_name,x.exact_version,x.view_hash)))
        compatibility=assess_compatibility(views,required_view_names)
        twin=compatibility.twin_id or views[0].twin_id;known=compatibility.known_as_of or views[0].known_as_of;event=compatibility.event_as_of or views[0].event_as_of;role=compatibility.evidence_role
        lineage=package_lineage_root(views)
        missingness=[];quality=[]
        for view in views:
            missingness.extend(f.mask for f in sorted(view.features,key=lambda x:x.feature_id));quality.extend(f.quality for f in sorted(view.features,key=lambda x:x.feature_id))
        seed={'package_version':package_version,'twin_id':twin,'known_as_of':known,'event_as_of':event,'evidence_role':role.value,'view_hashes':sorted(v.view_hash for v in views),'required_view_names':sorted(required_view_names),'optional_view_names':sorted(optional_view_names),'lineage_root':lineage,'limitations':sorted(limitations)}
        package_id=stable_id('viewpkg',seed)
        obj=MultimodalViewPackage(package_id,package_version,twin,known,event,role,views,compatibility,tuple(sorted(required_view_names)),tuple(sorted(optional_view_names)),tuple(missingness),tuple(round(x,12) for x in quality),lineage,'',tuple(sorted(limitations)))
        package_hash=content_hash(obj.semantic_payload())
        return MultimodalViewPackage(**{**obj.__dict__,'package_hash':package_hash})
