from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest
from .errors import AuthorityError
from .schema_validation import validate_instance

ALLOWED_ACTION = "ACL04_BUILD_SETUP_UNIVERSE"


def validate_authority(permit: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    validate_instance("authority_permit", permit)
    failures: list[str] = []
    if permit.get("decision") != "ALLOW": failures.append("ACL04_AUTHORITY_DENIED")
    if permit.get("action") != ALLOWED_ACTION: failures.append("ACL04_AUTHORITY_ACTION_MISMATCH")
    if permit.get("subject_context_id") != handoff.get("context_id"): failures.append("ACL04_AUTHORITY_CONTEXT_MISMATCH")
    if permit.get("upstream_handoff_digest") != handoff.get("handoff_digest"): failures.append("ACL04_AUTHORITY_HANDOFF_MISMATCH")
    if permit.get("live_order_submission_allowed") is not False: failures.append("ACL04_ILLEGAL_ORDER_AUTHORITY")
    if permit.get("capital_activation_allowed") is not False: failures.append("ACL04_ILLEGAL_CAPITAL_AUTHORITY")
    if not verify_embedded_digest(permit, "permit_digest"): failures.append("ACL04_AUTHORITY_DIGEST_MISMATCH")
    if failures:
        raise AuthorityError(",".join(failures))
    return {"passed": True, "permit_id": permit["permit_id"], "action": permit["action"], "reason_codes": []}
