from __future__ import annotations
from copy import deepcopy
from .encoding import encode_domain_view
from .canonical import content_hash,stable_id

def future_suffix_audit(view,config,cutoff):
    base=encode_domain_view(view,config,cutoff);future=deepcopy(view);future['known_as_of']='2099-01-01T00:00:00Z';mut=encode_domain_view(future,config,cutoff)
    passed=mut['future_filtered'] and not mut['available'] and base['embedding']!=[]
    doc={'phase':'SAED_V4_15','view_name':view['view_name'],'passed':passed,'base_envelope_hash':base['envelope_hash'],'future_envelope_hash':mut['envelope_hash'],'future_suffix_accessed':False,'production_eligible':False};doc['audit_hash']=content_hash(doc);doc['audit_id']=stable_id('v415future',doc);return doc

def fail_closed_audits(envelopes,config,candidate,policy,support_fn,fuse_fn):
    rows=[]
    critical=config.critical_view_names[0];m=[dict(x,available=False) if x['view_name']==critical else x for x in envelopes];s=support_fn(m);o=fuse_fn(m,s);rows.append({'case':'missing_critical_view','passed':o['directive']==policy.missing_critical_action,'directive':o['directive']})
    corrupted=[dict(x,embedding=x['embedding'][:-1]) if x==envelopes[0] else x for x in envelopes];s=support_fn(corrupted);o=fuse_fn(corrupted,s);rows.append({'case':'corrupt_dimension','passed':o['directive']==policy.corrupt_action,'directive':o['directive']})
    nofoundation=[dict(x,available=False) if x['source_plane']=='foundation' else x for x in envelopes];s=support_fn(nofoundation);o=fuse_fn(nofoundation,s);expected=policy.foundation_missing_action if candidate.requires_foundation_views else 'fuse';rows.append({'case':'all_foundation_missing','passed':o['directive']==expected,'directive':o['directive']})
    doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'rows':rows,'all_passed':all(x['passed'] for x in rows),'production_eligible':False};doc['audit_hash']=content_hash(doc);doc['audit_id']=stable_id('v415failclosed',doc);return doc
