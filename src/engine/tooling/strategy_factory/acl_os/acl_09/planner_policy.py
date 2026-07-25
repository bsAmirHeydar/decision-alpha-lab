from __future__ import annotations
from .canonical import verify_embedded_digest
from .errors import PolicyError
def validate_planner_policy(doc:dict)->dict:
    if not verify_embedded_digest(doc,'policy_digest'): raise PolicyError('ACL09_PLANNER_POLICY_DIGEST_INVALID')
    if doc.get('policy_id')!='ACL09_PLANNER_POLICY_V1' or doc.get('max_selected_proposals')!=6 or doc.get('max_total_cost_units')!=100: raise PolicyError('ACL09_PLANNER_POLICY_NOT_CANONICAL')
    for field in ('research_execution_allowed','promotion_allowed','live_order_submission_allowed','capital_activation_allowed'):
        if doc.get(field) is not False: raise PolicyError('ACL09_PLANNER_AUTHORITY_INVALID')
    return doc
