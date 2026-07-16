from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import CertificateError

def build_selection_certificate(context_id,universe,mask,ranked,pareto_ids,decision,baseline,upstream_hashes,authority):
    body={'phase':'SAED_V4_20','context_id':context_id,'universe_hash':universe['universe_hash'],'mask_hash':mask['mask_hash'],'candidate_ranking':[{k:r[k] for k in ['treatment_id','rank','objective_score','selection_probability','allowed']} for r in ranked],'pareto_treatments':list(pareto_ids),'decision':decision,'baseline_report':baseline,'upstream_hashes':dict(sorted(upstream_hashes.items())),'research_only':True,'runtime_executable':False,'decision_authority':False,'promotion_authority':False,'execution_authority':False,'authority_hash':content_hash(authority)}
    body['certificate_id']=stable_id('selection_certificate',body);body['certificate_hash']=content_hash(body)
    return body

def verify_selection_certificate(c):
    x=dict(c);h=x.pop('certificate_hash',None)
    if h!=content_hash(x):raise CertificateError('certificate hash mismatch')
    if not c['research_only'] or c['runtime_executable'] or c['decision_authority'] or c['promotion_authority'] or c['execution_authority']:raise CertificateError('authority escalation')
    return True
