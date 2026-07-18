from __future__ import annotations
from datetime import datetime,timezone
from .canonical import verify_embedded_digest,with_digest
from .errors import AuthorityError
from .policies import ACTION
def _dt(s:str): return datetime.fromisoformat(s.replace('Z','+00:00'))
def verify_permit(permit:dict,binding:dict,at:str)->dict:
    if not verify_embedded_digest(permit,'permit_digest'): raise AuthorityError('ACL15_PERMIT_DIGEST_INVALID')
    if permit.get('phase')!='ACL-15' or permit.get('action')!=ACTION: raise AuthorityError('ACL15_PERMIT_ACTION_INVALID')
    if permit.get('pilot_run_id')!=binding.get('pilot_run_id') or permit.get('acl14_handoff_digest')!=binding.get('acl14_handoff_digest'): raise AuthorityError('ACL15_PERMIT_BINDING_INVALID')
    if not (_dt(permit['issued_at'])<=_dt(at)<=_dt(permit['expires_at'])): raise AuthorityError('ACL15_PERMIT_EXPIRED')
    caps=permit.get('capabilities',{})
    forbidden=['network_access_allowed','secret_access_allowed','pilot_execution_allowed','prospective_outcome_creation_allowed','runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed','closed_history_mutation_allowed']
    if any(caps.get(k) is not False for k in forbidden): raise AuthorityError('ACL15_CAPABILITY_ESCALATION')
    return with_digest({'schema_version':'1.0.0','permit_id':permit['permit_id'],'action':ACTION,'pilot_run_id':binding['pilot_run_id'],'acl14_handoff_digest':binding['acl14_handoff_digest'],'verified_at':at,'permit_valid':True,'reference_closure_only':True,'pilot_execution_allowed':False,'prospective_outcome_creation_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'authority_report_digest')
