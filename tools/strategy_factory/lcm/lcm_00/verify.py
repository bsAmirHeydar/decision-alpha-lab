from __future__ import annotations

from pathlib import Path

from .canonical import digest_object, normalize_root_relative, sha256_file
from .errors import IntegrityError
from .event_ledger import verify_event_ledger
from .io import read_json


def verify_output_manifest(package_root: Path) -> None:
    manifest = read_json(package_root / "output_manifest.json")
    if manifest.get("output_manifest_digest") != digest_object(manifest, "output_manifest_digest"):
        raise IntegrityError("output manifest digest mismatch")
    declared = set()
    for item in manifest.get("artifacts", []):
        rel = normalize_root_relative(item["path"])
        declared.add(rel)
        path = package_root / rel
        if not path.is_file():
            raise IntegrityError(f"missing output artifact: {rel}")
        if path.stat().st_size != item["size_bytes"]:
            raise IntegrityError(f"output artifact size mismatch: {rel}")
        if sha256_file(path) != item["sha256"]:
            raise IntegrityError(f"output artifact hash mismatch: {rel}")
    actual = {p.relative_to(package_root).as_posix() for p in package_root.rglob("*") if p.is_file() and p.name != "output_manifest.json"}
    if actual != declared:
        raise IntegrityError(f"output artifact set mismatch: missing={sorted(declared-actual)[:5]} extra={sorted(actual-declared)[:5]}")


def verify_baseline_package(package_root: Path) -> dict:
    verify_output_manifest(package_root)
    manifest = read_json(package_root / "baseline_manifest.json")
    if manifest.get("manifest_digest") != digest_object(manifest, "manifest_digest"):
        raise IntegrityError("baseline manifest digest mismatch")
    paths = [item["path"] for item in manifest.get("records", [])]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise IntegrityError("baseline paths not unique and sorted")
    verify_event_ledger(read_json(package_root / "events/freeze_event_ledger.json"))
    receipt = read_json(package_root / "baseline_receipt.json")
    if receipt.get("receipt_digest") != digest_object(receipt, "receipt_digest"):
        raise IntegrityError("receipt digest mismatch")
    if receipt.get("baseline_manifest_digest") != manifest.get("manifest_digest"):
        raise IntegrityError("receipt baseline binding mismatch")
    rehearsal = read_json(package_root / "restoration/restore_rehearsal_report.json")
    if not rehearsal.get("passed"):
        raise IntegrityError("reference restore rehearsal did not pass")
    return {
        "passed": True,
        "baseline_id": manifest["baseline_id"],
        "record_count": manifest["record_count"],
        "package_artifact_count": read_json(package_root / "output_manifest.json")["artifact_count"],
    }


def verify_repository_against_baseline(repo_root: Path, package_root: Path, allowed_additions: set[str] | None = None) -> dict:
    manifest = read_json(package_root / "baseline_manifest.json")
    mismatches: list[dict] = []
    baseline_paths = set()
    for item in manifest["records"]:
        rel = item["path"]
        baseline_paths.add(rel)
        path = repo_root / rel
        if item["kind"] == "FILE":
            if not path.is_file():
                mismatches.append({"path": rel, "reason": "MISSING"})
            else:
                actual = sha256_file(path)
                if actual != item["sha256"]:
                    mismatches.append({"path": rel, "reason": "HASH_MISMATCH", "actual": actual})
        elif not path.is_symlink():
            mismatches.append({"path": rel, "reason": "SYMLINK_MISSING"})
    undeclared: list[str] = []
    if allowed_additions is not None:
        allowed = set(allowed_additions)
        for path in repo_root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(repo_root).as_posix()
            if any(part in {".git", ".pytest_cache", "__pycache__"} for part in path.relative_to(repo_root).parts):
                continue
            if path.suffix.lower() in {".pyc", ".pyo"}:
                continue
            if rel not in baseline_paths and rel not in allowed:
                undeclared.append(rel)
    return {
        "passed": not mismatches and not undeclared,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "undeclared_addition_count": len(undeclared),
        "undeclared_additions": sorted(undeclared),
    }
