from __future__ import annotations
from .canonical import verify_embedded_digest
from .errors import PolicyError
REQUIRED_CLASSES={'BASELINE_REFERENCE','INSUFFICIENT_EVIDENCE','NEGATIVE_VALIDATION','REPORTABLE_EVIDENCE','DIAGNOSTIC_EXCLUSION'}
def validate_memory_policy(doc:dict)->dict:
    if not verify_embedded_digest(doc,'policy_digest'): raise PolicyError('ACL09_MEMORY_POLICY_DIGEST_INVALID')
    if doc.get('policy_id')!='ACL09_MEMORY_POLICY_V1' or set(doc.get('accepted_experience_classes',[]))!=REQUIRED_CLASSES: raise PolicyError('ACL09_MEMORY_POLICY_NOT_CANONICAL')
    if doc.get('append_only') is not True or doc.get('diagnostic_quarantine_required') is not True or doc.get('doctrine_amendment_allowed') is not False or doc.get('promotion_allowed') is not False: raise PolicyError('ACL09_MEMORY_POLICY_AUTHORITY_INVALID')
    if doc.get('near_duplicate_threshold_bps')!=7500: raise PolicyError('ACL09_NEAR_DUPLICATE_THRESHOLD_INVALID')
    return doc
