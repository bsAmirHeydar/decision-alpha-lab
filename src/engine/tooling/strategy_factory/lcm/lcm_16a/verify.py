from __future__ import annotations

from pathlib import Path

from .baseline import verify_baseline_amendment
from .canonical import object_digest
from .constants import (
    AUDIT_ID,
    PACKAGE_RELATIVE,
    UPSTREAM_HANDOFF_DIGEST,
    UPSTREAM_PACKAGE_RELATIVE,
)
from .io import file_digest, load_json
from .models import AuditVerificationResult

DIGEST_FIELDS = {
    "baseline_amendment.json": "amendment_digest",
    "closure_test_matrix.json": "matrix_digest",
    "registry_conformance_report.json": "report_digest",
    "python_regression_report.json": "report_digest",
    "schema_validation_report.json": "report_digest",
    "mql5_compile_matrix.json": "matrix_digest",
    "strategy_tester_matrix.json": "matrix_digest",
    "cross_language_parity_report.json": "report_digest",
    "security_authority_audit.json": "report_digest",
    "documentation_integrity_report.json": "report_digest",
    "rollback_manifest.json": "rollback_manifest_digest",
    "output_manifest.json": "output_manifest_digest",
    "LCM16A_TO_LCM16B_HANDOFF.json": "handoff_digest",
    "reports/acceptance_report.json": "report_digest",
    "reports/determinism_report.json": "report_digest",
    "reports/hostile_review_report.json": "report_digest",
}


def _verify_digest(path: Path, field: str) -> dict:
    document = load_json(path)
    if document.get(field) != object_digest(document, field):
        raise ValueError(f"object digest mismatch: {path}")
    return document


def verify_package(repo_root: Path, package_root: Path | None = None) -> AuditVerificationResult:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / PACKAGE_RELATIVE).resolve()
    if package_root.name != AUDIT_ID:
        raise ValueError("unexpected LCM-16A audit identity")

    documents = {
        relative: _verify_digest(package_root / relative, field)
        for relative, field in DIGEST_FIELDS.items()
    }

    handoff = documents["LCM16A_TO_LCM16B_HANDOFF.json"]
    if handoff["source_handoff_digest"] != UPSTREAM_HANDOFF_DIGEST:
        raise ValueError("LCM-16A upstream handoff mismatch")
    if handoff["closure_decision"] != "BLOCKED":
        raise ValueError("LCM-16A must not infer closure from unavailable evidence")
    if handoff["allowed_next_actions"] != [
        "LCM16B_RECOVERY_DRILL_PREPARATION",
        "CAPTURE_EXTERNAL_METAEDITOR_AND_STRATEGY_TESTER_EVIDENCE",
        "RESOLVE_EXTERNAL_CONSUMER_REACHABILITY",
    ]:
        raise ValueError("unexpected next-action boundary")
    for key in (
        "runtime_authority_created",
        "live_order_authority_created",
        "capital_authority_created",
        "deletion_authority_created",
    ):
        if handoff[key]:
            raise ValueError(f"forbidden authority created: {key}")

    matrix = documents["closure_test_matrix.json"]
    if matrix["phase_decision"] != "BLOCKED":
        raise ValueError("closure matrix did not preserve blocking UNKNOWNs")
    mandatory_unknowns = {
        item["gate_id"]
        for item in matrix["gates"]
        if item["mandatory"] and item["status"] in {"UNKNOWN", "BLOCKED"}
    }
    if not {
        "MQL5_METAEDITOR_COMPILE",
        "STRATEGY_TESTER_GOLDEN_REPLAY",
        "OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS",
    }.issubset(mandatory_unknowns):
        raise ValueError("mandatory external UNKNOWN set is incomplete")

    compile_matrix = documents["mql5_compile_matrix.json"]
    tester_matrix = documents["strategy_tester_matrix.json"]
    if compile_matrix["metaeditor_status"] != "UNKNOWN":
        raise ValueError("static MQL5 scan was overstated as compilation")
    if tester_matrix["strategy_tester_status"] != "UNKNOWN":
        raise ValueError("Strategy Tester evidence was overstated")

    baseline_count, amendment_count, unchanged_count, missing_count = verify_baseline_amendment(
        repo_root,
        repo_root / UPSTREAM_PACKAGE_RELATIVE,
        package_root,
    )

    manifest = documents["output_manifest.json"]
    for metadata in manifest["files"]:
        path = package_root / metadata["path"]
        if not path.is_file() or file_digest(path) != metadata["sha256"]:
            raise ValueError(f"output manifest mismatch: {metadata['path']}")

    return AuditVerificationResult(
        audit_id=AUDIT_ID,
        baseline_count=baseline_count,
        amendment_count=amendment_count,
        unchanged_count=unchanged_count,
        missing_count=missing_count,
        deterministic_gate_status="PASS",
        external_evidence_status="UNKNOWN_BLOCKING",
        closure_decision="BLOCKED",
        validation_status="PASS",
    )
