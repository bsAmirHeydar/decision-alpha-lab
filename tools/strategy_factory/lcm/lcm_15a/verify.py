from __future__ import annotations

from pathlib import Path

from tools.strategy_factory.lcm.portable_integrity import (
    current_matches_expected_or_amended,
    load_verified_lcm16a_amendments,
    matches_expected_digest,
)

from .canonical import object_digest
from .io import load_json, load_jsonl
from .models import VerificationResult


def _check_digest(obj: dict, field: str) -> None:
    if obj.get(field) != object_digest(obj, field):
        raise ValueError(f"digest mismatch: {field}")


def _downstream_changes(repo_root: Path) -> dict[str, dict]:
    base = repo_root / "registry/legacy_context_migration/root_release_reorganizations"
    if not base.is_dir():
        return {}
    packages = sorted(path for path in base.iterdir() if path.is_dir())
    if not packages:
        return {}
    package = packages[-1]
    changes: dict[str, dict] = {}
    registry = load_json(package / "documentation_relocation_receipts.json")
    for row in load_jsonl(package / registry["records_path"]):
        changes[row["legacy_path"]] = {"kind": "DOCUMENT_REDIRECT", **row}
    rewrite = load_json(package / "reference_rewrite_receipt.json")
    for row in load_jsonl(package / rewrite["records_path"]):
        if row.get("rewrite_performed"):
            changes.setdefault(row["reference_path"], {"kind": "REFERENCE_REWRITE", **row})
    return changes


def verify_package(repo_root: Path, package_root: Path) -> VerificationResult:
    ledger = load_json(package_root / "deletion_candidate_ledger.json")
    references = load_json(package_root / "reference_proof_registry.json")
    approvals = load_json(package_root / "deletion_approval_registry.json")
    blockers = load_json(package_root / "deletion_blocker_registry.json")
    handoff = load_json(package_root / "LCM15A_TO_LCM15B_HANDOFF.json")
    manifest = load_json(package_root / "output_manifest.json")
    for obj, field in (
        (ledger, "registry_digest"),
        (references, "registry_digest"),
        (approvals, "registry_digest"),
        (blockers, "registry_digest"),
        (handoff, "handoff_digest"),
        (manifest, "output_manifest_digest"),
    ):
        _check_digest(obj, field)

    rows = load_jsonl(package_root / ledger["records_path"])
    approval_rows = load_jsonl(package_root / approvals["records_path"])
    blocker_rows = load_jsonl(package_root / blockers["records_path"])
    if len(rows) != 2168 or len(approval_rows) != 2168:
        raise ValueError("candidate/approval count mismatch")
    if any(row["future_deletion_approved"] for row in rows):
        raise ValueError("future deletion approved")
    if any(row["deletion_performed"] for row in rows):
        raise ValueError("deletion performed")
    if approvals["future_deletion_approved_count"] != 0 or handoff["approved_future_deletion_count"] != 0:
        raise ValueError("authority boundary violated")
    if (package_root / "approved_future_deletion_pathspec.txt").read_text(encoding="utf-8") != "":
        raise ValueError("future deletion pathspec must be empty")

    downstream = _downstream_changes(repo_root)
    amendments = load_verified_lcm16a_amendments(repo_root)
    for row in rows:
        relative = row["candidate_path"]
        expected = row["candidate_sha256"]
        if current_matches_expected_or_amended(repo_root, relative, expected, amendments):
            continue
        moved = downstream.get(relative)
        if not moved:
            raise ValueError(f"candidate drift: {relative}")
        source = repo_root / relative
        if moved["kind"] == "DOCUMENT_REDIRECT":
            target_relative = moved["canonical_target_path"]
            target = repo_root / target_relative
            if not source.is_file() or not target.is_file():
                raise ValueError(f"downstream locator missing: {relative}")
            if not current_matches_expected_or_amended(
                repo_root, relative, moved["redirect_stub_sha256"], amendments
            ):
                raise ValueError(f"downstream redirect mismatch: {relative}")
            if not current_matches_expected_or_amended(repo_root, target_relative, expected, amendments):
                raise ValueError(f"downstream relocation mismatch: {relative}")
        elif moved["kind"] == "REFERENCE_REWRITE":
            if moved["before_sha256"] != expected:
                raise ValueError(f"downstream rewrite source mismatch: {relative}")
            if not matches_expected_digest(source, moved["after_sha256"]):
                raise ValueError(f"downstream rewrite mismatch: {relative}")
        else:
            raise ValueError(f"unsupported downstream change: {relative}")

    for relative, meta in {item["path"]: item for item in manifest["files"]}.items():
        path = package_root / relative
        if not matches_expected_digest(path, meta["sha256"]):
            raise ValueError(f"manifest mismatch: {relative}")
    return VerificationResult(
        len(rows),
        approvals["approved_relocation_count"],
        blockers["deletion_blocked_candidate_count"],
        "PASS",
    )
