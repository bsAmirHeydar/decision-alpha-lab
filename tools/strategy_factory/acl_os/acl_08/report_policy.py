from __future__ import annotations
from .canonical import verify_embedded_digest
from .errors import PolicyError
from .policies import AUDIENCES
from .report_registry import registry_snapshot
def validate_policy(doc:dict)->dict:
    if not verify_embedded_digest(doc,'policy_digest'): raise PolicyError('invalid report policy digest')
    if doc.get('policy_id')!='ACL08_REPORT_POLICY_V1' or doc.get('report_version')!='1.0.0': raise PolicyError('unsupported report policy')
    if set(doc.get('audiences',[]))!=AUDIENCES: raise PolicyError('audience set changed')
    expected=[x['block_id'] for x in registry_snapshot()['entries']]
    if doc.get('report_blocks')!=expected: raise PolicyError('report block set/order changed')
    if doc.get('decision_semantics_mutable') is not False or doc.get('diagnostic_selectable') is not False: raise PolicyError('unsafe report policy')
    if doc.get('alpha_claim_allowed') is not False or doc.get('promotion_allowed') is not False: raise PolicyError('claim authority escalation')
    return doc
