from __future__ import annotations

from pathlib import Path

from .canonical import object_digest
from .constants import (
    PACKAGE_RELATIVE,
    PHASE_SEQUENCE,
    PROGRAM_CLOSURE_ID,
    REQUIRED_EXTERNAL_DIMENSIONS,
    UPSTREAM_HANDOFF_DIGEST,
)
from .io import file_digest, load_json, load_jsonl
from .models import ProgramClosureVerificationResult

DIGEST_FIELDS = {
    "upstream_binding.json": "binding_digest",
    "recovery_drill_plan.json": "program_plan_digest",
    "recovery_drill_receipt.json": "receipt_digest",
    "external_evidence_contract.json": "contract_digest",
    "external_evidence_status.json": "program_status_digest",
    "final_locator_snapshot.json": "locator_digest",
    "final_migration_ledger.json": "ledger_digest",
    "authority_final_state.json": "authority_digest",
    "deletion_final_state.json": "deletion_state_digest",
    "residual_risk_register.json": "risk_register_digest",
    "program_closure_decision.json": "program_decision_digest",
    "program_closure_certificate.json": "program_certificate_digest",
    "post_program_continuity_handoff.json": "handoff_digest",
    "rollback_manifest.json": "rollback_manifest_digest",
    "reports/acceptance_report.json": "report_digest",
    "reports/hostile_review_report.json": "report_digest",
    "reports/determinism_report.json": "report_digest",
    "reports/program_state_report.json": "report_digest",
    "output_manifest.json": "output_manifest_digest",
}


def _verify_digest(path: Path, field: str) -> dict:
    document = load_json(path)
    if document.get(field) != object_digest(document, field):
        raise ValueError(f"object digest mismatch: {path}")
    return document


def verify_program_closure_package(
    repo_root: Path,
    package_root: Path | None = None,
) -> ProgramClosureVerificationResult:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / PACKAGE_RELATIVE).resolve()
    if package_root.name != PROGRAM_CLOSURE_ID:
        raise ValueError("unexpected LCM-16B program closure identity")

    documents = {relative: _verify_digest(package_root / relative, field) for relative, field in DIGEST_FIELDS.items()}
    binding = documents["upstream_binding.json"]
    if binding["upstream_handoff_digest"] != UPSTREAM_HANDOFF_DIGEST:
        raise ValueError("LCM-16B upstream handoff mismatch")

    phases = load_jsonl(package_root / "records/phase_register.jsonl")
    if [item["phase_id"] for item in phases] != list(PHASE_SEQUENCE):
        raise ValueError("final phase sequence is incomplete or reordered")

    snapshot = load_jsonl(package_root / "records/control_plane_snapshot.jsonl")
    if not snapshot or len({item["path"] for item in snapshot}) != len(snapshot):
        raise ValueError("control-plane snapshot is empty or duplicated")
    for row in snapshot:
        path = repo_root / row["path"]
        if not path.is_file() or file_digest(path) != row["sha256"]:
            raise ValueError(f"current control-plane mismatch: {row['path']}")

    receipt = documents["recovery_drill_receipt.json"]
    if receipt["local_control_plane_status"] != "PASS" or receipt["lcm16a_rehydration_status"] != "PASS":
        raise ValueError("local recovery drill is not complete")
    if receipt["repository_mutated"]:
        raise ValueError("recovery drill mutated the repository")

    evidence = documents["external_evidence_status.json"]
    dimensions = {item["dimension"]: item["status"] for item in evidence["dimensions"]}
    if set(dimensions) != set(REQUIRED_EXTERNAL_DIMENSIONS):
        raise ValueError("external evidence dimension set is incomplete")

    decision = documents["program_closure_decision.json"]
    certificate = documents["program_closure_certificate.json"]
    blocked = [gate for gate in decision["gates"] if gate["status"] in {"UNKNOWN", "BLOCKED", "PARTIAL"}]
    if blocked:
        if decision["decision"] != "BLOCKED" or certificate["certificate_status"] != "NOT_ISSUED":
            raise ValueError("blocked gate was compensated or certificate was over-issued")
    elif decision["decision"] != "ACCEPTED" or certificate["certificate_status"] != "ISSUED":
        raise ValueError("fully satisfied closure did not produce accepted certificate")

    for document_name in ("authority_final_state.json", "deletion_final_state.json"):
        document = documents[document_name]
        for key, value in document.items():
            if key.endswith("authority") or key.endswith("authority_created"):
                if value is True:
                    raise ValueError(f"forbidden authority in {document_name}: {key}")

    deletion = documents["deletion_final_state.json"]
    if deletion["approved_deletion_count"] != 0 or deletion["executed_deletion_count"] != 0:
        raise ValueError("LCM-16B changed the deletion disposition")

    manifest = documents["output_manifest.json"]
    for metadata in manifest["files"]:
        path = package_root / metadata["path"]
        if not path.is_file() or file_digest(path) != metadata["sha256"]:
            raise ValueError(f"output manifest mismatch: {metadata['path']}")

    return ProgramClosureVerificationResult(
        closure_id=PROGRAM_CLOSURE_ID,
        phase_count=len(phases),
        control_plane_path_count=len(snapshot),
        local_recovery_status="PASS",
        external_evidence_status=("PASS" if all(value == "PASS" for value in dimensions.values()) else "BLOCKED_OR_UNKNOWN"),
        approval_status=evidence["approval_status"],
        program_closure_decision=decision["decision"],
        certificate_status=certificate["certificate_status"],
        validation_status="PASS",
    )
