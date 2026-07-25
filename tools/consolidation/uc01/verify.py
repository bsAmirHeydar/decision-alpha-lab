"""Fail-closed verification for UC-01 static implementation and captured baseline."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from .archive import root_digest_from_rows
from .constants import (
    BASELINE_RELATIVE_ROOT,
    BASELINE_STABILIZATION_REPAIR_PATHS,
    OUTPUT_FILENAMES,
    RELEASE_RELATIVE_ROOT,
)
from .git_utils import git_available, list_repository_files, run_command
from .io_utils import iter_jsonl_gz, read_json, sha256_file


_REQUIRED_MANIFEST_KEYS = {
    "baseline_id", "program_id", "stage_id", "implementation_version", "captured_at",
    "repository_root_digest_sha256", "artifact_count", "python_symbol_count",
    "mql5_symbol_count", "documentation_count", "consumer_edge_count",
    "critical_logic_count", "unresolved_item_count", "blocking_item_count", "immutable",
}



def verify_static_patch(repo_root: Path) -> dict:
    """Verify the static UC-01 patch controls before any baseline capture."""
    repo_root = repo_root.resolve()
    release = repo_root / RELEASE_RELATIVE_ROOT
    errors: list[str] = []
    try:
        manifest = read_json(release / "UC01_PATCH_MANIFEST.json")
    except Exception as exc:
        return {"status": "FAILED", "errors": [f"invalid patch manifest: {exc}"]}
    index_path = release / "UC01_PATCH_FILE_INDEX.txt"
    paths = [line.strip().replace("\\", "/") for line in index_path.read_text(encoding="utf-8").splitlines() if line.strip()] if index_path.is_file() else []
    if len(paths) != manifest.get("total_path_count") or len(paths) != len(set(paths)):
        errors.append("static file index count or uniqueness mismatch")
    for rel in paths:
        if not (repo_root / rel).is_file():
            errors.append(f"static patch path missing: {rel}")
    ledger_path = release / "UC01_PATCH_FILE_HASHES.sha256"
    ledger_entries = {}
    if ledger_path.is_file():
        for line in ledger_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                digest, rel = line.split("  ", 1)
                ledger_entries[rel] = digest
            except ValueError:
                errors.append(f"invalid static hash ledger line: {line}")
    else:
        errors.append("static hash ledger missing")
    expected_ledger = set(paths) - {ledger_path.relative_to(repo_root).as_posix()}
    if set(ledger_entries) != expected_ledger:
        errors.append("static hash ledger path set mismatch")
    for rel, digest in ledger_entries.items():
        if (repo_root / rel).is_file() and sha256_file(repo_root / rel) != digest:
            errors.append(f"static patch hash mismatch: {rel}")
    inventory_path = release / "UC01_PATCH_ARTIFACT_INVENTORY.csv"
    if inventory_path.is_file():
        with inventory_path.open(encoding="utf-8", newline="") as handle:
            inventory = list(csv.DictReader(handle))
        if len(inventory) != len(paths) or {row.get("path") for row in inventory} != set(paths):
            errors.append("static artifact inventory path set mismatch")
    else:
        errors.append("static artifact inventory missing")
    expected_modified = set(BASELINE_STABILIZATION_REPAIR_PATHS)
    declared_modified = set(manifest.get("modified_paths", []))
    if manifest.get("deleted_file_count") != 0:
        errors.append("UC-01 static patch must be deletion-free")
    if declared_modified != expected_modified:
        errors.append("UC-01 modified-path declaration does not match the bounded baseline stabilization repair set")
    if manifest.get("modified_file_count") != len(expected_modified):
        errors.append("UC-01 modified-file count does not match the bounded repair set")
    if manifest.get("new_file_count", 0) + manifest.get("modified_file_count", 0) != len(paths):
        errors.append("UC-01 new/modified path counts do not sum to the static file index")
    if not expected_modified.issubset(set(paths)):
        errors.append("UC-01 static file index omitted one or more bounded baseline stabilization repairs")
    original_hashes = manifest.get("repair_original_sha256", {})
    patched_hashes = manifest.get("repair_patched_sha256", {})
    if set(original_hashes) != expected_modified or set(patched_hashes) != expected_modified:
        errors.append("UC-01 repair provenance hash maps do not match the bounded repair set")
    for rel in expected_modified:
        target = repo_root / rel
        if target.is_file() and patched_hashes.get(rel) != sha256_file(target):
            errors.append(f"UC-01 repaired path does not match its declared patched hash: {rel}")
        if original_hashes.get(rel) == patched_hashes.get(rel):
            errors.append(f"UC-01 repair provenance does not distinguish original and patched bytes: {rel}")
    if inventory_path.is_file():
        inventory_changes = {row.get("path"): row.get("change_type") for row in inventory}
        actual_modified = {path for path, change in inventory_changes.items() if change == "MODIFY"}
        if actual_modified != expected_modified:
            errors.append("UC-01 artifact inventory MODIFY set does not match the bounded repair set")
        unexpected_change_types = {change for change in inventory_changes.values() if change not in {"ADD", "MODIFY"}}
        if unexpected_change_types:
            errors.append(f"UC-01 artifact inventory contains forbidden change types: {sorted(unexpected_change_types)}")
    return {
        "status": "PASS" if not errors else "FAILED",
        "path_count": len(paths),
        "hash_count": len(ledger_entries),
        "errors": errors,
    }

def verify_baseline(repo_root: Path, baseline_root: Path | None = None, *, verify_current_tree: bool = True) -> dict:
    repo_root = repo_root.resolve()
    baseline_root = (baseline_root or repo_root / BASELINE_RELATIVE_ROOT).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not baseline_root.is_dir():
        return {"status": "FAILED", "errors": [f"baseline root missing: {baseline_root}"], "warnings": []}

    expected_names = set(OUTPUT_FILENAMES)
    present_names = {path.name for path in baseline_root.iterdir() if path.is_file()}
    # Full regression receipt is optional and generated only when the upstream runner exists.
    allowed_extra = {"lcm16a_regression_receipt.json"}
    missing = expected_names - present_names
    extra = present_names - expected_names - allowed_extra
    if missing:
        errors.append(f"missing baseline outputs: {sorted(missing)}")
    if extra:
        errors.append(f"unexpected baseline outputs: {sorted(extra)}")

    try:
        manifest = read_json(baseline_root / "baseline_manifest.json")
        missing_keys = _REQUIRED_MANIFEST_KEYS - set(manifest)
        if missing_keys:
            errors.append(f"baseline manifest missing keys: {sorted(missing_keys)}")
        if manifest.get("stage_id") != "UC-01" or manifest.get("program_id") != "UCPS":
            errors.append("baseline manifest program/stage identity mismatch")
        if manifest.get("immutable") is not True:
            errors.append("baseline manifest must be immutable")
    except Exception as exc:
        manifest = {}
        errors.append(f"invalid baseline manifest: {type(exc).__name__}: {exc}")

    try:
        rows = list(iter_jsonl_gz(baseline_root / "artifact_inventory.jsonl.gz"))
        if len(rows) != manifest.get("artifact_count"):
            errors.append(f"artifact count mismatch: {len(rows)} != {manifest.get('artifact_count')}")
        paths = [row.get("path") for row in rows]
        if len(paths) != len(set(paths)):
            errors.append("artifact inventory contains duplicate paths")
        if paths != sorted(paths):
            errors.append("artifact inventory is not sorted")
        root_digest = root_digest_from_rows(rows)
        if root_digest != manifest.get("repository_root_digest_sha256"):
            errors.append("artifact inventory root digest mismatch")
        if any(row.get("disposition") != "UNASSESSED_UNTIL_UC02" for row in rows):
            errors.append("UC-01 artifact disposition exceeded stage authority")
    except Exception as exc:
        rows = []
        errors.append(f"invalid artifact inventory: {type(exc).__name__}: {exc}")

    for name in (
        "python_symbol_inventory.jsonl.gz", "python_import_graph.jsonl.gz", "python_parse_issues.jsonl.gz",
        "mql5_symbol_inventory.jsonl.gz", "mql5_include_graph.jsonl.gz", "mql5_authority_surface.jsonl.gz",
        "documentation_inventory.jsonl.gz", "documentation_link_graph.jsonl.gz", "documentation_id_collisions.jsonl.gz",
        "schema_inventory.jsonl.gz", "path_reference_graph.jsonl.gz", "consumer_inventory.jsonl.gz",
        "large_object_inventory.jsonl.gz", "git_lfs_inventory.jsonl.gz", "critical_logic_inventory.jsonl.gz",
        "test_inventory.jsonl.gz", "unresolved_items.jsonl.gz",
    ):
        try:
            list(iter_jsonl_gz(baseline_root / name))
        except Exception as exc:
            errors.append(f"invalid compressed JSONL {name}: {type(exc).__name__}: {exc}")

    ledger = baseline_root / "baseline_output_hashes.sha256"
    if ledger.is_file():
        for line_number, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                expected, name = line.split("  ", 1)
                target = baseline_root / name
                if not target.is_file():
                    errors.append(f"hash ledger target missing: {name}")
                elif sha256_file(target) != expected:
                    errors.append(f"hash ledger mismatch: {name}")
            except ValueError:
                errors.append(f"invalid hash ledger line {line_number}")
    else:
        errors.append("baseline output hash ledger missing")

    decision_path = baseline_root / "stage_exit_decision.json"
    if decision_path.is_file():
        try:
            decision = read_json(decision_path)
            if decision.get("status") not in {"PENDING", "BLOCKED", "FAILED", "ACCEPTED"}:
                errors.append("invalid stage exit status")
            if decision.get("status") == "ACCEPTED" and decision.get("uc02_authorized") is not True:
                errors.append("accepted stage decision did not authorize UC-02")
            if decision.get("destructive_authority") is not False and decision.get("status") != "PENDING":
                errors.append("UC-01 created destructive authority")
        except Exception as exc:
            errors.append(f"invalid stage exit decision: {exc}")

    static_index = repo_root / RELEASE_RELATIVE_ROOT / "UC01_PATCH_FILE_INDEX.txt"
    if not static_index.is_file():
        errors.append("static patch file index missing")
    else:
        static_paths = [line.strip() for line in static_index.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(static_paths) != len(set(static_paths)):
            errors.append("static patch file index contains duplicates")
        for rel in static_paths:
            if not (repo_root / rel).is_file():
                errors.append(f"static indexed path missing: {rel}")

    if verify_current_tree and rows:
        changed = []
        baseline_prefix = BASELINE_RELATIVE_ROOT.as_posix().rstrip("/") + "/"
        current_paths, _ = list_repository_files(repo_root)
        current_set = {path for path in current_paths if not path.startswith(baseline_prefix) and "/__pycache__/" not in f"/{path}/" and not path.endswith(".pyc")}
        expected_set = {row["path"] for row in rows}
        missing_paths = sorted(expected_set - current_set)
        extra_paths = sorted(current_set - expected_set)
        if missing_paths:
            errors.append(f"current tree is missing baseline paths: {missing_paths[:50]}")
        if extra_paths:
            errors.append(f"current tree contains post-baseline paths: {extra_paths[:50]}")
        for row in rows:
            rel = row["path"]
            if rel.startswith(baseline_prefix):
                continue
            path = repo_root / rel
            if not path.is_file():
                changed.append({"path": rel, "reason": "missing"})
                continue
            actual = sha256_file(path)
            if actual != row["sha256"]:
                changed.append({"path": rel, "reason": "hash_mismatch"})
            if len(changed) >= 100:
                break
        if changed:
            errors.append(f"current tree drifted from baseline: {changed[:20]}")

    if git_available(repo_root):
        deleted = run_command(("git", "diff", "--name-only", "--diff-filter=D"), repo_root, timeout=30)
        staged_deleted = run_command(("git", "diff", "--cached", "--name-only", "--diff-filter=D"), repo_root, timeout=30)
        deleted_paths = [line for line in (deleted.stdout + "\n" + staged_deleted.stdout).splitlines() if line.strip()]
        if deleted_paths:
            errors.append(f"UC-01 worktree contains deletions: {deleted_paths[:50]}")

    return {
        "status": "PASS" if not errors else "FAILED",
        "baseline_root": str(baseline_root),
        "errors": errors,
        "warnings": warnings,
        "artifact_count": len(rows),
    }
