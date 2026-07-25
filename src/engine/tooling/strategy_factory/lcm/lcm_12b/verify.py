from __future__ import annotations
from pathlib import Path
from .canonical import verify_embedded_digest
from .io import load_json

REQUIRED = (
    "documentation_move_manifest.json",
    "documentation_redirect_registry.json",
    "obsidian_link_report.json",
    "obsidian_orphan_report.json",
    "generated_document_registry.json",
    "canonical_knowledge_registry.json",
    "residual_documentation_issues.json",
    "documentation_closure_report.md",
    "LCM12B_TO_LCM13A_HANDOFF.json",
    "output_manifest.json",
    "rollback_manifest.json",
    "reports/acceptance_report.json",
    "reports/hostile_review_report.json",
    "records/documentation_move_records.jsonl",
    "records/documentation_redirect_records.jsonl",
    "records/documentation_link_rewrite_records.jsonl",
    "records/documentation_orphan_records.jsonl",
    "records/generated_document_records.jsonl",
    "records/canonical_knowledge_records.jsonl",
)
DIGEST_FIELDS = {
    "documentation_move_manifest.json": "manifest_digest",
    "documentation_redirect_registry.json": "registry_digest",
    "obsidian_link_report.json": "report_digest",
    "obsidian_orphan_report.json": "report_digest",
    "generated_document_registry.json": "registry_digest",
    "canonical_knowledge_registry.json": "registry_digest",
    "residual_documentation_issues.json": "registry_digest",
    "LCM12B_TO_LCM13A_HANDOFF.json": "handoff_digest",
    "output_manifest.json": "output_manifest_digest",
    "rollback_manifest.json": "rollback_digest",
    "reports/acceptance_report.json": "report_digest",
    "reports/hostile_review_report.json": "report_digest",
}

def verify_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"MISSING:{relative}")
    for relative, field in DIGEST_FIELDS.items():
        path = root / relative
        if path.is_file() and not verify_embedded_digest(load_json(path), field):
            errors.append(f"DIGEST:{relative}")
    if errors:
        return errors
    move = load_json(root / "documentation_move_manifest.json")
    links = load_json(root / "obsidian_link_report.json")
    generated = load_json(root / "generated_document_registry.json")
    acceptance = load_json(root / "reports/acceptance_report.json")
    hostile = load_json(root / "reports/hostile_review_report.json")
    handoff = load_json(root / "LCM12B_TO_LCM13A_HANDOFF.json")
    if move["source_delete_count"] != 0:
        errors.append("DOCUMENT_DELETE")
    if not move["all_targets_exist"] or not move["all_legacy_paths_exist"]:
        errors.append("LOCATOR_MISSING")
    if links["new_broken_reference_count"] != 0 or links["canonical_basename_collision_count"] != 0:
        errors.append("LINK_GATE")
    if not generated["all_generated_documents_source_bound"] or not generated["all_generated_documents_producer_bound"]:
        errors.append("GENERATED_BINDING")
    if not acceptance["passed"] or hostile["result"] != "PASS":
        errors.append("ACCEPTANCE")
    if handoff["runtime_authority_created"] or handoff["live_order_authority_created"] or handoff["capital_authority_created"]:
        errors.append("AUTHORITY_ESCALATION")
    return errors
