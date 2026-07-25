from __future__ import annotations
from .canonical import with_digest
def build_fast_slice(req:dict)->dict:
    rows=sorted(req['observations'],key=lambda r:(r['event_time'],r['observation_id']))
    normalized=[]
    for r in rows:
        normalized.append({k:r[k] for k in ['observation_id','event_time','available_at','label_available_at','context_present','direction','state','confirmation','x_location_score','y_state_score','optionality_score','forward_delta']})
    body={'schema_version':'1.0.0','slice_id':'ACL13_REFERENCE_FAST_SLICE_V1','context_id':req['context_id'],'assessment_cut_at':req['assessment_cut_at'],'row_count':len(normalized),'timezone':req['known_time_contract']['timezone'],'known_time_safe':True,'synthetic_reference_data':req.get('synthetic_reference_data',False),'rows':normalized}
    return with_digest(body,'slice_digest')
