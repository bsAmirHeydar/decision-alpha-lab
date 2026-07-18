from __future__ import annotations

from .canonical import content_id, digest_object, normalize_root_relative
from .errors import ContractViolation

SEMANTIC_CLASSIFICATIONS = {
    "NON_SEMANTIC",
    "SEMANTIC_BUG_FIX",
    "SEMANTIC_DOMAIN_CHANGE",
    "SECURITY_HOTFIX",
    "DOCUMENTATION_ONLY",
}


def build_amendment(
    baseline_id: str,
    path: str,
    old_sha256: str,
    new_sha256: str,
    classification: str,
    affected_identities: list[str],
    rationale: str,
) -> dict:
    path = normalize_root_relative(path)
    if classification not in SEMANTIC_CLASSIFICATIONS:
        raise ContractViolation("unknown amendment classification")
    if old_sha256 == new_sha256:
        raise ContractViolation("amendment old and new digests must differ")
    if not affected_identities:
        raise ContractViolation("affected identities required")
    material = {
        "baseline_id": baseline_id,
        "path": path,
        "old_sha256": old_sha256,
        "new_sha256": new_sha256,
        "classification": classification,
        "affected_identities": sorted(affected_identities),
    }
    value = {
        "schema_version": "1.0.0",
        "amendment_id": content_id("AMD", material),
        **material,
        "rationale": rationale,
        "recharacterization_required": classification in {
            "SEMANTIC_BUG_FIX", "SEMANTIC_DOMAIN_CHANGE", "SECURITY_HOTFIX"
        },
        "approval_status": "PENDING_HUMAN_APPROVAL",
        "applied_to_baseline": False,
        "amendment_digest": "",
    }
    value["amendment_digest"] = digest_object(value, "amendment_digest")
    return value


def validate_amendment(value: dict) -> None:
    expected = digest_object(value, "amendment_digest")
    if value.get("amendment_digest") != expected:
        raise ContractViolation("amendment digest mismatch")
    if value.get("classification") not in SEMANTIC_CLASSIFICATIONS:
        raise ContractViolation("amendment classification not closed")
    if value.get("old_sha256") == value.get("new_sha256"):
        raise ContractViolation("amendment must change content")
