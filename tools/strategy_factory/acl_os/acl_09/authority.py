from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest,with_digest
from .errors import AuthorityError
from .policies import REQUIRED_ACTION
def validate_authority(permit:dict[str,Any],handoff:dict[str,Any])->dict[str,Any]:
    if not verify_embedded_digest(permit,'permit_digest'): raise AuthorityError('ACL09_PERMIT_DIGEST_INVALID')
    checks={
      'phase':permit.get('phase')=='ACL-09',
      'action':permit.get('action')==REQUIRED_ACTION,
      'report_bound':permit.get('report_id')==handoff.get('report_id'),
      'handoff_bound':permit.get('upstream_handoff_digest')==handoff.get('handoff_digest'),
      'network_denied':permit.get('network_access_allowed') is False,
      'secret_denied':permit.get('secret_access_allowed') is False,
      'research_execution_denied':permit.get('research_execution_allowed') is False,
      'order_denied':permit.get('live_order_submission_allowed') is False,
      'capital_denied':permit.get('capital_activation_allowed') is False,
      'doctrine_denied':permit.get('doctrine_amendment_allowed') is False,
    }
    if not all(checks.values()): raise AuthorityError(str([k for k,v in checks.items() if not v]))
    return with_digest({'schema_version':'1.0.0','permit_id':permit['permit_id'],'checks':checks,'passed':True},'authority_report_digest')
