"""UC-02 static and dynamic package verification."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import jsonschema

from .constants import AUTHORITY_DOMAINS, AUTHORITY_ROOT, DYNAMIC_OUTPUTS, PLANNING_DISPOSITIONS, RELEASE_ROOT, SCHEMA_ROOT
from .contracts import validate_contracts
from .io_utils import iter_jsonl_gz, read_json, sha256_file
from tools.consolidation.ci.portable_hash import hash_matches


def _part3_relocations(repo_root: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for relative in (
        "registry/consolidation/uc03/part3/documentation_relocation_receipt.json",
        "registry/consolidation/uc03/part3/registry_relocation_receipt.json",
    ):
        path = repo_root / relative
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if payload.get("status") != "PASS":
            continue
        for row in payload.get("relocations", []):
            if not isinstance(row, dict):
                continue
            source = str(row.get("source", "")).replace("\\", "/")
            destination = str(row.get("destination", "")).replace("\\", "/")
            if source and destination:
                output[source] = destination
    return output


def _part3_rewrites(repo_root: Path) -> dict[str, dict]:
    path = repo_root / "registry/consolidation/uc03/part3/reference_rewrite_receipt.json"
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    if payload.get("status") != "PASS":
        return {}
    return {str(row.get("path", "")): row for row in payload.get("files", []) if isinstance(row, dict)}


def _matches_with_part3(path: Path, relative: str, expected_values: list[str], rewrites: dict[str, dict]) -> bool:
    if any(value and hash_matches(path, value) for value in expected_values):
        return True
    row = rewrites.get(relative)
    if not row:
        return False
    before = str(row.get("before_sha256", "")).lower()
    after = str(row.get("after_sha256", "")).lower()
    if before not in {value.lower() for value in expected_values if value}:
        return False
    return bool(after and hash_matches(path, after))


def verify_static_patch(repo_root: Path) -> dict:
    repo_root = repo_root.resolve()
    release = repo_root / RELEASE_ROOT
    errors: list[str] = []
    part3_rewrites = _part3_rewrites(repo_root)
    part3_relocations = _part3_relocations(repo_root)
    amendment_paths = (
        repo_root / "releases/unified_consolidation/uc03/part2/UC02_STATIC_AMENDMENT.json",
        repo_root / "releases/unified_consolidation/ci_recovery_01/UC02_STATIC_AMENDMENT.json",
        repo_root / "releases/unified_consolidation/ci_recovery_02/UC02_STATIC_AMENDMENT.json",
        repo_root / "releases/unified_consolidation/uc03/part3/UC02_STATIC_AMENDMENT.json",
    )
    amendment_hashes: dict[str, str] = {}
    for amendment_path in amendment_paths:
        if not amendment_path.is_file():
            continue
        try:
            amendment = json.loads(amendment_path.read_text(encoding="utf-8"))
            if amendment.get("program_id") != "UCPS" or amendment.get("upstream_stage") != "UC-02":
                errors.append(f"invalid UC-02 amendment identity: {amendment_path.relative_to(repo_root)}")
            for row in amendment.get("amended_paths", []):
                amendment_hashes[str(row["path"])] = str(row["sha256"])
        except Exception as exc:
            errors.append(f"invalid UC-02 amendment {amendment_path.relative_to(repo_root)}: {exc}")
    index = release / "UC02_PATCH_FILE_INDEX.txt"
    ledger = release / "UC02_PATCH_FILE_HASHES.sha256"
    manifest_path = release / "UC02_PATCH_MANIFEST.json"
    inventory_path = release / "UC02_ARTIFACT_INVENTORY.csv"
    required = {"UC02_PATCH_FILE_INDEX.txt", "UC02_PATCH_FILE_HASHES.sha256", "UC02_PATCH_MANIFEST.json", "UC02_ARTIFACT_INVENTORY.csv", "UC02_QA_REPORT.json", "COMMIT_MESSAGE.txt"}
    present = {p.name for p in release.iterdir() if p.is_file()} if release.is_dir() else set()
    if present != required:
        errors.append(f"release control set mismatch: missing={sorted(required-present)} extra={sorted(present-required)}")
    paths = [line.strip().replace("\\", "/") for line in index.read_text(encoding="utf-8").splitlines() if line.strip()] if index.is_file() else []
    if len(paths) != len(set(paths)):
        errors.append("static file index contains duplicates")
    for rel in paths:
        resolved_rel = part3_relocations.get(rel, rel)
        if not (repo_root / resolved_rel).is_file():
            errors.append(f"static indexed file missing after relocation: {rel}")
    ledger_rows = []
    if ledger.is_file():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                expected, rel = line.split("  ", 1)
            except ValueError:
                errors.append(f"invalid hash ledger line: {line}")
                continue
            ledger_rows.append(rel)
            resolved_rel = part3_relocations.get(rel, rel)
            target = repo_root / resolved_rel
            if not target.is_file():
                errors.append(f"static hash target missing after relocation: {rel}")
            else:
                amendment_expected = amendment_hashes.get(rel) or amendment_hashes.get(resolved_rel)
                expected_values = [expected]
                if amendment_expected:
                    expected_values.append(amendment_expected)
                if not _matches_with_part3(target, resolved_rel, expected_values, part3_rewrites):
                    errors.append(f"static hash mismatch: {rel}")
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("total_path_count") != len(paths):
            errors.append("static manifest path count mismatch")
        if manifest.get("deleted_file_count") != 0 or manifest.get("modified_file_count") != 0:
            errors.append("UC-02 static patch must be add-only")
    if inventory_path.is_file():
        with inventory_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != len(paths):
            errors.append("static artifact inventory count mismatch")
        if any(row.get("change_type") != "ADD" for row in rows):
            errors.append("UC-02 static artifact inventory must contain ADD only")
    contract_result = validate_contracts(repo_root)
    if contract_result["status"] != "PASS":
        errors.extend(contract_result["errors"])
    return {"status": "PASS" if not errors else "FAILED", "errors": errors, "path_count": len(paths), "hash_count": len(ledger_rows)}


def verify_authority_package(repo_root: Path, package_root: Path | None = None) -> dict:
    repo_root = repo_root.resolve()
    package_root = (package_root or repo_root / AUTHORITY_ROOT).resolve()
    errors: list[str] = []
    if not package_root.is_dir():
        return {"status": "FAILED", "errors": [f"authority package missing: {package_root}"]}
    present = {p.name for p in package_root.iterdir() if p.is_file()}
    expected = set(DYNAMIC_OUTPUTS)
    if present != expected:
        errors.append(f"dynamic output set mismatch: missing={sorted(expected-present)} extra={sorted(present-expected)}")

    manifest = read_json(package_root / "authority_manifest.json")
    coverage = read_json(package_root / "authority_coverage_report.json")
    if manifest.get("program_id") != "UCPS" or manifest.get("stage_id") != "UC-02":
        errors.append("authority manifest identity mismatch")
    if coverage.get("unresolved_count") != 0:
        errors.append(f"authority package has unresolved items: {coverage.get('unresolved_count')}")
    if coverage.get("artifact_coverage_ratio") != 1.0:
        errors.append("artifact authority coverage is not complete")

    row_schema = json.loads((repo_root / SCHEMA_ROOT / "authority_ledger_row.schema.json").read_text(encoding="utf-8"))
    artifact_rows = list(iter_jsonl_gz(package_root / "repository_authority_ledger.jsonl.gz"))
    if len(artifact_rows) != coverage.get("artifact_count"):
        errors.append("artifact authority ledger count mismatch")
    paths = [row.get("path") for row in artifact_rows]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        errors.append("artifact authority ledger is not unique and sorted")
    for index, row in enumerate(artifact_rows):
        if row.get("canonical_owner") not in AUTHORITY_DOMAINS:
            errors.append(f"invalid canonical owner at row {index}: {row.get('canonical_owner')}")
            break
        if row.get("planning_disposition") not in PLANNING_DISPOSITIONS:
            errors.append(f"invalid planning disposition at row {index}")
            break
        if index < 100:
            try:
                jsonschema.validate(row, row_schema)
            except Exception as exc:
                errors.append(f"authority row schema failure at row {index}: {exc}")
                break

    unresolved = list(iter_jsonl_gz(package_root / "unresolved_authority_items.jsonl.gz"))
    if unresolved:
        errors.append(f"unresolved authority items are not empty: {len(unresolved)}")

    ledger_path = package_root / "authority_output_hashes.sha256"
    if ledger_path.is_file():
        for line in ledger_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                expected_hash, name = line.split("  ", 1)
            except ValueError:
                errors.append(f"invalid dynamic hash ledger line: {line}")
                continue
            target = package_root / name
            if not target.is_file() or sha256_file(target) != expected_hash:
                errors.append(f"dynamic hash mismatch: {name}")

    decision = read_json(package_root / "stage_exit_decision.json")
    schema = json.loads((repo_root / SCHEMA_ROOT / "stage_exit_decision.schema.json").read_text(encoding="utf-8"))
    try:
        jsonschema.validate(decision, schema)
    except Exception as exc:
        errors.append(f"stage exit decision schema failure: {exc}")
    handoff = read_json(package_root / "uc03_handoff.json")
    handoff_schema = json.loads((repo_root / SCHEMA_ROOT / "uc03_handoff.schema.json").read_text(encoding="utf-8"))
    try:
        jsonschema.validate(handoff, handoff_schema)
    except Exception as exc:
        errors.append(f"UC-03 handoff schema failure: {exc}")

    return {"status": "PASS" if not errors else "FAILED", "errors": errors, "artifact_count": len(artifact_rows), "unresolved_count": len(unresolved), "decision": decision.get("status")}
