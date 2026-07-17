from __future__ import annotations
from pathlib import Path
from typing import Any
from .canonical import digest_object, verify_embedded_digest, digest_file
from .errors import ContractError
from .io import load_json, ensure_contained
from .schema_validation import validate_instance

REQUIRED_ALLOWED_SCOPE = {
    "DEFINE_HUMAN_SETUP_DSL",
    "GENERATE_BOUNDED_AI_SETUP_CANDIDATES",
    "CANONICALIZE_SETUP_BEHAVIOR",
    "VALIDATE_TREATMENT_ENVELOPE",
}
REQUIRED_FORBIDDEN_SCOPE = {
    "ALTER_CONTEXT_SEMANTICS",
    "BYPASS_KNOWN_TIME_GUARDS",
    "ACTIVATE_CAPITAL",
    "SUBMIT_ORDERS",
}


def load_acl03_bundle(compiled_root: Path) -> dict[str, Any]:
    root = compiled_root.resolve()
    paths = {
        "handoff": root / "handoff" / "acl04_handoff.json",
        "detector_ir": root / "ir" / "detector_ir.json",
        "occurrence_ir": root / "ir" / "occurrence_ir.json",
        "known_time_ir": root / "ir" / "known_time_ir.json",
        "feature_binding_ir": root / "ir" / "feature_binding_ir.json",
        "onboarding_report": root / "reports" / "onboarding_report.json",
        "source_snapshot": root / "source" / "source_snapshot.json",
        "output_manifest": root / "output_manifest.json",
        "compilation_receipt": root / "compilation_receipt.json",
    }
    values: dict[str, Any] = {}
    for key, path in paths.items():
        ensure_contained(root, path)
        values[key] = load_json(path)
    handoff = values["handoff"]
    validate_instance("acl03_handoff_input", handoff)
    if not verify_embedded_digest(handoff, "handoff_digest"):
        raise ContractError("ACL04_HANDOFF_DIGEST_MISMATCH")
    if handoff.get("handoff_type") != "ACL03_TO_ACL04":
        raise ContractError("ACL04_HANDOFF_TYPE_INVALID")
    if not REQUIRED_ALLOWED_SCOPE.issubset(set(handoff.get("allowed_scope", []))):
        raise ContractError("ACL04_HANDOFF_ALLOWED_SCOPE_INCOMPLETE")
    if not REQUIRED_FORBIDDEN_SCOPE.issubset(set(handoff.get("forbidden_scope", []))):
        raise ContractError("ACL04_HANDOFF_FORBIDDEN_SCOPE_INCOMPLETE")
    if handoff.get("live_order_submission_allowed") is not False or handoff.get("capital_activation_allowed") is not False:
        raise ContractError("ACL04_UPSTREAM_ILLEGAL_EXECUTION_AUTHORITY")
    digest_bindings = {
        "detector_ir_digest": values["detector_ir"].get("detector_ir_digest"),
        "occurrence_ir_digest": values["occurrence_ir"].get("occurrence_ir_digest"),
        "feature_binding_ir_digest": values["feature_binding_ir"].get("feature_binding_ir_digest"),
        "onboarding_report_digest": values["onboarding_report"].get("report_digest"),
        "source_snapshot_digest": values["source_snapshot"].get("snapshot_digest"),
    }
    for field, actual in digest_bindings.items():
        if handoff.get(field) != actual:
            raise ContractError(f"ACL04_UPSTREAM_BINDING_MISMATCH:{field}")
    values["bundle_digest"] = digest_object({k: values[k] for k in sorted(values) if k not in {"bundle_digest"}})
    values["root"] = str(root)
    values["file_digests"] = {k: digest_file(v) for k, v in paths.items()}
    return values
