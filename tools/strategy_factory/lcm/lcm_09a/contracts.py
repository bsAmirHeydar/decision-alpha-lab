from __future__ import annotations
from .canonical import digest_object
from .policy import validate_contract_boundary
def validate_contract(c:dict,canonical_context_ids:set[str])->list[str]:
    failures=[]
    if c["context_binding"]["canonical_context_identity_id"] not in canonical_context_ids|{None}: failures.append("NON_CANONICAL_CONTEXT_REFERENCE")
    failures.extend(validate_contract_boundary(c))
    if not c["abstention_contract"]["no_trade_is_first_class"]: failures.append("NO_TRADE_NOT_FIRST_CLASS")
    if digest_object(c,"contract_digest")!=c["contract_digest"]: failures.append("CONTRACT_DIGEST_MISMATCH")
    return failures
