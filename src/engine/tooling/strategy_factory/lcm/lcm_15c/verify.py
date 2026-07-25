from __future__ import annotations

from pathlib import Path

from tools.strategy_factory.lcm.portable_integrity import (
    current_matches_expected_or_amended,
    load_verified_lcm16a_amendments,
    matches_expected_digest,
)

from .canonical import object_digest
from .constants import EMPTY_SHA256, EXPECTED_UPSTREAM
from .io import load_json, load_jsonl
from .models import VerificationResult


def _digest(obj: dict, field: str) -> None:
    if obj.get(field) != object_digest(obj, field):
        raise ValueError(f"digest mismatch: {field}")


def verify_package(repo_root: Path, package_root: Path) -> VerificationResult:
    names = {
        "pre_delete_receipt.json": "receipt_digest",
        "blocked_deletion_registry.json": "registry_digest",
        "deletion_ledger.json": "ledger_digest",
        "post_delete_reference_report.json": "report_digest",
        "clean_clone_verification.json": "report_digest",
        "archive_restore_sample.json": "report_digest",
        "repository_hygiene_report.json": "report_digest",
        "final_active_inventory.json": "inventory_digest",
        "rollback_manifest.json": "rollback_manifest_digest",
        "output_manifest.json": "output_manifest_digest",
        "LCM15C_TO_LCM16A_HANDOFF.json": "handoff_digest",
        "reports/acceptance_report.json": "report_digest",
        "reports/hostile_review_report.json": "report_digest",
        "reports/determinism_report.json": "report_digest",
    }
    for relative, field in names.items():
        path = package_root / relative
        if not path.is_file():
            raise ValueError(f"missing: {relative}")
        _digest(load_json(path), field)

    pathspec = package_root / "final_deletion_pathspec.txt"
    if (
        not pathspec.is_file()
        or pathspec.read_bytes() != b""
        or not matches_expected_digest(pathspec, EMPTY_SHA256)
    ):
        raise ValueError("deletion pathspec is not exact empty set")

    pre = load_json(package_root / "pre_delete_receipt.json")
    ledger = load_json(package_root / "deletion_ledger.json")
    blocked = load_json(package_root / "blocked_deletion_registry.json")
    clone = load_json(package_root / "clean_clone_verification.json")
    restore = load_json(package_root / "archive_restore_sample.json")
    handoff = load_json(package_root / "LCM15C_TO_LCM16A_HANDOFF.json")
    lock_rows = load_jsonl(package_root / "records/pre_delete_lock_records.jsonl")
    blocked_rows = load_jsonl(package_root / "records/blocked_deletion_records.jsonl")
    deletion_rows = load_jsonl(package_root / "records/deletion_records.jsonl")
    restore_rows = load_jsonl(package_root / "records/archive_restore_sample_records.jsonl")
    if len(lock_rows) != 2168 or len(blocked_rows) != 2168 or deletion_rows:
        raise ValueError("record count mismatch")
    if pre["approved_deletion_count"] != 0 or pre["final_deletion_path_count"] != 0:
        raise ValueError("approval created")
    if ledger["deleted_path_count"] != 0 or ledger["deletion_record_count"] != 0:
        raise ValueError("deletion recorded")
    if blocked["blocked_count"] != 2168 or any(
        row["deletion_approved"] or row["deletion_performed"] for row in blocked_rows
    ):
        raise ValueError("blocked set violation")

    amendments = load_verified_lcm16a_amendments(repo_root)
    for row in lock_rows:
        relative = row["candidate_path"]
        if not current_matches_expected_or_amended(
            repo_root, relative, row["locked_sha256"], amendments
        ):
            raise ValueError(f"candidate changed: {relative}")

    if clone["clean_clone_result"] != "PASS" or clone["source_manifest_digest"] != clone["clone_manifest_digest"]:
        raise ValueError("clean clone proof failed")
    if clone["verified_path_count"] < 50000 or clone["direct_test_count"] != 20:
        raise ValueError("clean clone scope incomplete")
    if restore["pass_count"] != 12 or restore["fail_count"] != 0 or any(
        row["restore_result"] != "PASS" for row in restore_rows
    ):
        raise ValueError("restore sample failed")
    if handoff["source_handoff_digest"] != EXPECTED_UPSTREAM or handoff["deleted_path_count"] != 0:
        raise ValueError("handoff mismatch")
    if handoff["allowed_next_actions"] != ["LCM16A_FULL_SYSTEM_AUDIT"]:
        raise ValueError("next action mismatch")

    manifest = load_json(package_root / "output_manifest.json")
    for meta in manifest["files"]:
        path = package_root / meta["path"]
        if not matches_expected_digest(path, meta["sha256"]):
            raise ValueError(f"manifest mismatch: {meta['path']}")
    return VerificationResult(2168, 0, 0, 2168, "PASS", restore["archive_restore_result"], "PASS")
