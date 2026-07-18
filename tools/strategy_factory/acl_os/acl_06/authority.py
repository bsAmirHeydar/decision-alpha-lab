from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest,with_digest
from .errors import AuthorityError
from .policies import AUTHORITY_ACTION
from .schema_validation import validate_instance

def validate_authority(permit:dict[str,Any],handoff:dict[str,Any])->dict[str,Any]:
    validate_instance('authority_permit',permit)
    if not verify_embedded_digest(permit,'permit_digest'): raise AuthorityError('permit digest invalid')
    checks={
      'action_exact':permit['action']==AUTHORITY_ACTION,
      'subject_exact':permit['subject']=='ACL-06',
      'batch_exact':permit['batch_id']==handoff['batch_id'],
      'handoff_bound':permit['upstream_handoff_digest']==handoff['handoff_digest'],
      'network_denied':permit['network_access_allowed'] is False,
      'secret_denied':permit['secret_access_allowed'] is False,
      'order_denied':permit['live_order_submission_allowed'] is False,
      'capital_denied':permit['capital_activation_allowed'] is False,
    }
    if not all(checks.values()): raise AuthorityError(str([k for k,v in checks.items() if not v]))
    return with_digest({'schema_version':'1.0.0','permit_id':permit['permit_id'],'checks':checks,'passed':True},'report_digest')
