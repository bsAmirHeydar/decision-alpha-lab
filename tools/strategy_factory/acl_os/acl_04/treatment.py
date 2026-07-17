from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest
from .errors import ContractError
from .schema_validation import validate_instance


def validate_treatment_envelope(envelope: dict[str, Any], handoff: dict[str, Any]) -> dict[str, Any]:
    validate_instance("treatment_envelope", envelope)
    failures=[]
    if not verify_embedded_digest(envelope, "envelope_digest"): failures.append("ACL04_TREATMENT_ENVELOPE_DIGEST_MISMATCH")
    if envelope.get("context_id") != handoff.get("context_id") or envelope.get("context_version") != handoff.get("context_version"):
        failures.append("ACL04_TREATMENT_ENVELOPE_CONTEXT_MISMATCH")
    if envelope.get("upstream_handoff_digest") != handoff.get("handoff_digest"):
        failures.append("ACL04_TREATMENT_ENVELOPE_HANDOFF_MISMATCH")
    if envelope.get("live_order_submission_allowed") is not False or envelope.get("capital_activation_allowed") is not False:
        failures.append("ACL04_TREATMENT_ILLEGAL_EXECUTION_SCOPE")
    if failures: raise ContractError(",".join(failures))
    return envelope


def action_allowed(action: str, envelope: dict[str, Any]) -> bool:
    return action in set(envelope.get("allowed_actions", []))
