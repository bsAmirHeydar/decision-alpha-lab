from __future__ import annotations
from .catalog import institutional_view_catalog
from .models import SourceValue,ViewBuildRequest
from .enums import EvidenceRole
from .service import MultimodalViewService
from .integrity import verify_integrity

def run_vectors(vectors):
    out=[]
    for vector in vectors:
        try:
            specs=institutional_view_catalog(vector.get('twin_id','twin_golden'));service=MultimodalViewService()
            for s in specs:service.register_specification(s)
            sources=tuple(SourceValue(x['namespace'],x['path'],x['value'],x['event_time'],x['known_time'],x.get('quality',1.0),EvidenceRole(x.get('evidence_role','development')),x['source_artifact_id'],x['source_hash'],tuple(x.get('lineage_ids',[])),x.get('conflict',False)) for x in vector['sources'])
            request=ViewBuildRequest(vector.get('twin_id','twin_golden'),vector['known_as_of'],vector['event_as_of'],EvidenceRole(vector.get('evidence_role','development')),sources,vector['id'])
            selected=[s for s in specs if s.view_name in vector['view_names']]
            views=tuple(service.build_view(s,request) for s in selected)
            package=service.build_package(views,'1.0.0',tuple(vector.get('required_view_names',vector['view_names'])))
            receipt=service.integrity_receipt(package);verify_integrity(package,receipt)
            observed={'package_hash':package.package_hash,'compatibility':package.compatibility.status.value,'statuses':{v.view_name:v.status.value for v in views}}
            passed=all(observed.get(k)==v for k,v in vector.get('expect',{}).items())
            out.append({'id':vector['id'],'passed':passed,'observed':observed})
        except Exception as exc:
            out.append({'id':vector['id'],'passed':vector.get('expect_error') in type(exc).__name__ if vector.get('expect_error') else False,'error':type(exc).__name__+': '+str(exc)})
    return out
