from __future__ import annotations

from pathlib import Path

from src.engine.tooling.strategy_factory.lcm.portable_integrity import (
    current_matches_expected_or_amended,
    load_verified_lcm16a_amendments,
    matches_expected_digest,
)

from .canonical import object_digest
from .io import load_json, load_jsonl
from .models import VerificationResult


def _digest(obj: dict, field: str) -> None:
    if obj.get(field) != object_digest(obj, field):
        raise ValueError(f"digest mismatch: {field}")


def verify_package(repo_root: Path, package_root: Path) -> VerificationResult:
    names = {
        "root_relocation_manifest.json": "registry_digest",
        "release_registry_index.json": "registry_digest",
        "installer_locator_registry.json": "registry_digest",
        "documentation_relocation_receipts.json": "registry_digest",
        "reference_rewrite_receipt.json": "registry_digest",
        "root_allowlist.json": "registry_digest",
        "revalidated_deletion_ledger.json": "registry_digest",
        "post_relocation_reference_report.json": "report_digest",
        "root_before_after_map.json": "map_digest",
        "rollback_manifest.json": "rollback_manifest_digest",
        "LCM15B_TO_LCM15C_HANDOFF.json": "handoff_digest",
        "output_manifest.json": "output_manifest_digest",
        "reports/acceptance_report.json": "report_digest",
        "reports/hostile_review_report.json": "report_digest",
    }
    for relative, field in names.items():
        path = package_root / relative
        if not path.is_file():
            raise ValueError(f"missing: {relative}")
        _digest(load_json(path), field)

    root = load_json(package_root / "root_relocation_manifest.json")
    docs = load_json(package_root / "documentation_relocation_receipts.json")
    refs = load_json(package_root / "post_relocation_reference_report.json")
    revalidated = load_json(package_root / "revalidated_deletion_ledger.json")
    handoff = load_json(package_root / "LCM15B_TO_LCM15C_HANDOFF.json")
    root_rows = load_jsonl(package_root / root["records_path"])
    doc_rows = load_jsonl(package_root / docs["records_path"])
    revalidated_rows = load_jsonl(package_root / revalidated["records_path"])
    if len(root_rows) != 6 or len(doc_rows) != 934 or len(revalidated_rows) != 2168:
        raise ValueError("count mismatch")
    if refs["active_residual_reference_count"] != 0:
        raise ValueError("active references remain")
    if revalidated["future_deletion_approved_count"] != 0 or any(
        row["future_deletion_approved"] for row in revalidated_rows
    ):
        raise ValueError("deletion approval created")
    if any(row["deletion_performed"] for row in revalidated_rows):
        raise ValueError("deletion performed")

    amendments = load_verified_lcm16a_amendments(repo_root)
    for row in root_rows:
        source_relative = row["source_path"]
        target_relative = row["canonical_target_path"]
        if not (repo_root / source_relative).is_file() or not (repo_root / target_relative).is_file():
            raise ValueError(f"root relocation missing: {source_relative}")
        if not current_matches_expected_or_amended(
            repo_root, source_relative, row["source_sha256_before"], amendments
        ):
            raise ValueError(f"root source hash mismatch: {source_relative}")
        if not current_matches_expected_or_amended(
            repo_root, target_relative, row["target_sha256_after"], amendments
        ):
            raise ValueError(f"root target hash mismatch: {target_relative}")

    for row in doc_rows:
        legacy_relative = row["legacy_path"]
        target_relative = row["canonical_target_path"]
        legacy = repo_root / legacy_relative
        target = repo_root / target_relative
        if not legacy.is_file() or not target.is_file():
            raise ValueError("documentation locator missing")
        if not current_matches_expected_or_amended(
            repo_root, legacy_relative, row["redirect_stub_sha256"], amendments
        ):
            raise ValueError(f"documentation redirect hash mismatch: {legacy_relative}")
        if not current_matches_expected_or_amended(
            repo_root, target_relative, row["canonical_target_sha256"], amendments
        ):
            raise ValueError(f"documentation target hash mismatch: {target_relative}")
        text = legacy.read_text(encoding="utf-8")
        if target_relative not in text or "compatibility-redirect" not in text:
            raise ValueError("redirect malformed")

    manifest = load_json(package_root / "output_manifest.json")
    for meta in manifest["files"]:
        path = package_root / meta["path"]
        if not matches_expected_digest(path, meta["sha256"]):
            raise ValueError(f"manifest mismatch: {meta['path']}")
    if handoff["deletion_performed"] or handoff["future_deletion_approved_count"] != 0:
        raise ValueError("handoff authority violation")
    return VerificationResult(6, 934, 2168, 0, "PASS")
