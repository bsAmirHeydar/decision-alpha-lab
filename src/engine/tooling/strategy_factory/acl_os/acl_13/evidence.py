from __future__ import annotations
from .canonical import stable_id,with_digest
def build_evidence(binding:dict,request:dict,items:list[dict])->dict:
    refs=[]
    for item in items:
        for k,v in item.items():
            if k.endswith('_digest') and isinstance(v,str) and v.startswith('sha256:'): refs.append(v)
    refs=sorted(set(refs+[binding['binding_digest'],request['assessment_request_digest']]))
    body={'schema_version':'1.0.0','evidence_bundle_id':stable_id('TRIAGEEVID',request['assessment_request_id'],length=28),'evidence_count':len(refs),'evidence_refs':refs,'source_security_readiness_decision':'REFERENCE_SECURITY_HARDENED_PRODUCTION_NOT_READY','synthetic_reference_data':request.get('synthetic_reference_data',False),'production_attestation_present':False,'prospective_evidence_present':False,'independent_replication_present':False,'execution_economics_present':False,'reference_only':True}
    return with_digest(body,'evidence_bundle_digest')
