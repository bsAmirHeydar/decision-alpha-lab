from __future__ import annotations
from .canonical import verify_embedded_digest,with_digest
from .errors import AuthorityError
from .policies import REQUIRED_ACTION
def validate_permit(p:dict,binding:dict)->dict:
    if not verify_embedded_digest(p,'permit_digest'): raise AuthorityError('ACL12_PERMIT_DIGEST_INVALID')
    if p.get('phase')!='ACL-12' or p.get('action')!=REQUIRED_ACTION: raise AuthorityError('ACL12_PERMIT_SCOPE_INVALID')
    if p.get('runtime_custody_run_id')!=binding.get('runtime_custody_run_id') or p.get('acl11_handoff_digest')!=binding.get('acl11_handoff_digest'): raise AuthorityError('ACL12_PERMIT_BINDING_MISMATCH')
    denied=['network_access_allowed','secret_access_allowed','production_key_access_allowed','runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed']
    if any(p.get(k) is not False for k in denied): raise AuthorityError('ACL12_PERMIT_AUTHORITY_ESCALATION')
    body={'schema_version':'1.0.0','permit_id':p['permit_id'],'action':p['action'],'runtime_custody_run_id':p['runtime_custody_run_id'],'acl11_handoff_digest':p['acl11_handoff_digest'],'validated':True,'denied_capabilities':denied}
    return with_digest(body,'authority_report_digest')
