from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest, with_digest
from .errors import AuthorityError
from .policies import REQUIRED_ACTION

def verify_authority_permit(permit: dict[str,Any], binding: dict[str,Any]) -> dict[str,Any]:
    checks = {
        'digest': verify_embedded_digest(permit,'permit_digest'),
        'phase': permit.get('phase') == 'ACL-10',
        'action': permit.get('action') == REQUIRED_ACTION,
        'memory_run_bound': permit.get('memory_run_id') == binding['memory_run_id'],
        'handoff_bound': permit.get('upstream_handoff_digest') == binding['handoff_digest'],
        'network_denied': permit.get('network_access_allowed') is False,
        'secret_denied': permit.get('secret_access_allowed') is False,
        'research_execution_denied': permit.get('research_execution_allowed') is False,
        'promotion_execution_denied': permit.get('promotion_execution_allowed') is False,
        'runtime_generation_denied': permit.get('runtime_generation_allowed') is False,
        'order_denied': permit.get('live_order_submission_allowed') is False,
        'capital_denied': permit.get('capital_activation_allowed') is False,
        'self_approval_denied': permit.get('self_approval_allowed') is False,
    }
    if not all(checks.values()): raise AuthorityError('ACL10_AUTHORITY_PERMIT_REJECTED')
    return with_digest({'schema_version':'1.0.0','permit_id':permit['permit_id'],'passed':True,'checks':checks},'authority_report_digest')
