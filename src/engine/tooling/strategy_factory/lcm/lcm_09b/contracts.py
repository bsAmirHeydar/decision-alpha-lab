from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .constants import CLAIM_CEILING,MANDATORY_RULES
from .errors import AuthorityError,ContractError
from .expressions import validate_expression

def validate_authority(doc:dict[str,Any])->None:
    for key in ("promotion_authority","runtime_authority","live_order_authority","capital_authority"):
        if doc.get(key) is not False:raise AuthorityError(f"LCM09B_AUTHORITY_MUST_BE_FALSE:{key}")
    if doc.get("consumer_cutover_authorized") is not False:raise AuthorityError("LCM09B_CONSUMER_CUTOVER_FORBIDDEN")

def validate_package(doc:dict[str,Any])->list[str]:
    failures=[]
    if doc.get("claim_ceiling")!=CLAIM_CEILING:failures.append("CLAIM_CEILING_MISMATCH")
    try:validate_authority(doc["authority_boundary"])
    except (KeyError,AuthorityError) as e:failures.append(str(e))
    rules=doc.get("rules",{})
    if set(rules)!={"eligibility","trigger","confirmation","invalidation","cancellation","expiry","abstention","entitlement"}:failures.append("RULE_SURFACE_INCOMPLETE")
    status=doc.get("package_status")
    blocked=bool(doc.get("blocker_ids"))
    if status=="REFERENCE_READY":
        for name in MANDATORY_RULES:
            rule=rules.get(name)
            if not isinstance(rule,dict):failures.append(f"MANDATORY_RULE_UNKNOWN:{name}")
            else:
                try:validate_expression(rule)
                except ContractError as e:failures.append(str(e))
        if blocked:failures.append("READY_PACKAGE_HAS_BLOCKERS")
    elif status=="REFERENCE_BLOCKED":
        if not blocked:failures.append("BLOCKED_PACKAGE_WITHOUT_BLOCKER")
        if doc.get("executable_reference") is not False:failures.append("BLOCKED_PACKAGE_EXECUTABLE")
    else:failures.append("PACKAGE_STATUS_INVALID")
    if digest_object(doc,"package_digest")!=doc.get("package_digest"):failures.append("PACKAGE_DIGEST_MISMATCH")
    return failures
