from __future__ import annotations
from datetime import datetime
from .canonical import verify_embedded_digest,with_digest
from .errors import AuthorityError
from .policies import REQUIRED_ACTION
def dt(v:str)->datetime: return datetime.fromisoformat(v.replace('Z','+00:00'))
def validate_permit(permit:dict,binding:dict)->dict:
    if not verify_embedded_digest(permit,'permit_digest'): raise AuthorityError('ACL14_PERMIT_DIGEST_INVALID')
    if permit.get('phase')!='ACL-14' or permit.get('action')!=REQUIRED_ACTION: raise AuthorityError('ACL14_PERMIT_SCOPE_INVALID')
    if permit.get('acl13_handoff_digest')!=binding.get('acl13_handoff_digest'): raise AuthorityError('ACL14_PERMIT_HANDOFF_MISMATCH')
    if permit.get('assessment_run_id')!=binding.get('assessment_run_id'): raise AuthorityError('ACL14_PERMIT_RUN_MISMATCH')
    if dt(permit['issued_at'])>=dt(permit['expires_at']): raise AuthorityError('ACL14_PERMIT_TIME_INVALID')
    denied=['network_access_allowed','secret_access_allowed','runtime_generation_allowed','runtime_activation_allowed','pilot_execution_allowed','live_order_submission_allowed','capital_activation_allowed','post_outcome_rule_change_allowed']
    if any(permit.get(k) is not False for k in denied): raise AuthorityError('ACL14_AUTHORITY_ESCALATION_DENIED')
    return with_digest({'schema_version':'1.0.0','permit_id':permit['permit_id'],'phase':'ACL-14','action':REQUIRED_ACTION,'assessment_run_id':binding['assessment_run_id'],'acl13_handoff_digest':binding['acl13_handoff_digest'],'issuer':permit['issuer'],'issued_at':permit['issued_at'],'expires_at':permit['expires_at'],'valid':True,'pilot_contract_authoring_allowed':True,'pilot_readiness_assessment_allowed':True,'pilot_execution_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'authority_report_digest')
