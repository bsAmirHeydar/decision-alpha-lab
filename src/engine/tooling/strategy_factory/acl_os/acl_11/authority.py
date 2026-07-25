from __future__ import annotations
from .canonical import verify_embedded_digest,with_digest
from .errors import AuthorityError
from .policies import REQUIRED_ACTION
def validate_permit(p: dict,binding: dict) -> dict:
    if not verify_embedded_digest(p,'permit_digest'): raise AuthorityError('ACL11_PERMIT_DIGEST_INVALID')
    if p.get('phase')!='ACL-11' or p.get('action')!=REQUIRED_ACTION: raise AuthorityError('ACL11_PERMIT_SCOPE_INVALID')
    if p.get('promotion_run_id')!=binding.get('promotion_run_id') or p.get('acl10_handoff_digest')!=binding.get('handoff_digest'): raise AuthorityError('ACL11_PERMIT_BINDING_MISMATCH')
    denied=['network_access_allowed','secret_access_allowed','runtime_generation_allowed','signing_key_access_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']
    if any(p.get(k) is not False for k in denied): raise AuthorityError('ACL11_PERMIT_AUTHORITY_ESCALATION')
    body={'schema_version':'1.0.0','permit_id':p['permit_id'],'action':p['action'],'promotion_run_id':p['promotion_run_id'],'acl10_handoff_digest':p['acl10_handoff_digest'],'validated':True,'denied_capabilities':denied}
    return with_digest(body,'authority_report_digest')
