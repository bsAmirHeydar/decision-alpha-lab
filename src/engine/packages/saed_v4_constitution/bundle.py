"""Evidence bundle construction and integrity verification."""
from __future__ import annotations

from typing import Any, Mapping

from .canonical import content_hash
from .errors import IntegrityViolation


REQUIRED_COMPONENTS = (
    "constitution",
    "authority_matrix",
    "evidence_role_policy",
    "objective_policy",
    "baseline_policy",
    "crosswalk",
    "core_boundary_snapshot",
    "exposure_ledger",
    "decision_ledger",
    "limitations",
)


def build_evidence_bundle(bundle_id: str, known_time: str, components: Mapping[str, Any]) -> dict[str, Any]:
    missing = [x for x in REQUIRED_COMPONENTS if x not in components]
    if missing:
        raise ValueError(f"missing evidence-bundle components: {missing}")
    component_hashes = {name: content_hash(components[name]) for name in sorted(components)}
    payload = {
        "schema_version": "4.0.0",
        "bundle_id": bundle_id,
        "known_time": known_time,
        "component_hashes": component_hashes,
        "limitations": list(components["limitations"]),
        "actual_external_evidence_attached": False,
        "production_authorized": False,
    }
    payload["bundle_hash"] = content_hash(payload)
    return payload


def verify_evidence_bundle(bundle: Mapping[str, Any], components: Mapping[str, Any]) -> bool:
    expected = {name: content_hash(components[name]) for name in sorted(components)}
    if dict(bundle.get("component_hashes", {})) != expected:
        raise IntegrityViolation("evidence-bundle component hash mismatch")
    without_hash = {k: v for k, v in bundle.items() if k != "bundle_hash"}
    if bundle.get("bundle_hash") != content_hash(without_hash):
        raise IntegrityViolation("evidence-bundle hash mismatch")
    return True
