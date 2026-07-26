from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .portable_hash import hash_matches


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value



def _check_authority_false(errors: list[str], label: str, payload: dict[str, Any]) -> None:
    for key in (
        "deletion_authority",
        "semantic_merge_authority",
        "runtime_authority",
        "order_authority",
        "broker_authority",
        "capital_authority",
    ):
        if payload.get(key) is True:
            errors.append(f"{label} unexpectedly grants {key}")


def verify(repo_root: Path) -> dict[str, Any]:
    repo = repo_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    required_files = {
        "UC-01 static manifest": repo / "releases/unified_consolidation/uc01/UC01_PATCH_MANIFEST.json",
        "UC-02 static manifest": repo / "releases/unified_consolidation/uc02/UC02_PATCH_MANIFEST.json",
        "UC-03 Part 1 decision": repo / "registry/consolidation/uc03/part1/part1_exit_decision.json",
        "UC-03 Part 2 decision": repo / "registry/consolidation/uc03/part2/part2_exit_decision.json",
        "UC-03 Part 2 relocation receipt": repo / "registry/consolidation/uc03/part2/code_relocation_receipt.json",
        "UC-03 Part 2 rewrite receipt": repo / "registry/consolidation/uc03/part2/compatibility_rewrite_receipt.json",
        "UC-01 migration amendment": repo / "releases/unified_consolidation/uc03/part2/UC01_STATIC_AMENDMENT.json",
        "UC-02 migration amendment": repo / "releases/unified_consolidation/uc03/part2/UC02_STATIC_AMENDMENT.json",
        "CI recovery amendment": repo / "releases/unified_consolidation/ci_recovery_01/UC02_STATIC_AMENDMENT.json",
    }
    for label, path in required_files.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(repo)}")

    if errors:
        return {"status": "FAILED", "errors": errors, "warnings": warnings}

    part1 = _read_json(required_files["UC-03 Part 1 decision"])
    part2 = _read_json(required_files["UC-03 Part 2 decision"])
    relocation = _read_json(required_files["UC-03 Part 2 relocation receipt"])
    rewrite = _read_json(required_files["UC-03 Part 2 rewrite receipt"])
    part3_path = repo / "registry/consolidation/uc03/part3/part3_exit_decision.json"
    part3 = _read_json(part3_path) if part3_path.is_file() else None
    part3_rewrite_path = repo / "registry/consolidation/uc03/part3/reference_rewrite_receipt.json"
    part3_rewrites: dict[str, dict[str, Any]] = {}
    if part3_rewrite_path.is_file():
        payload = _read_json(part3_rewrite_path)
        if payload.get("status") != "PASS":
            errors.append("UC-03 Part 3 rewrite receipt is not PASS")
        part3_rewrites = {str(row.get("path", "")): row for row in payload.get("files", []) if isinstance(row, dict)}
    part3_relocations: dict[str, str] = {}
    for relative in (
        "registry/consolidation/uc03/part3/documentation_relocation_receipt.json",
        "registry/consolidation/uc03/part3/registry_relocation_receipt.json",
    ):
        receipt_path = repo / relative
        if not receipt_path.is_file():
            continue
        payload = _read_json(receipt_path)
        if payload.get("status") != "PASS":
            errors.append(f"UC-03 Part 3 relocation receipt is not PASS: {relative}")
            continue
        for row in payload.get("relocations", []):
            if not isinstance(row, dict):
                continue
            source = str(row.get("source", "")).replace("\\", "/")
            destination = str(row.get("destination", "")).replace("\\", "/")
            if source and destination:
                part3_relocations[source] = destination

    if part1.get("status") != "ACCEPTED":
        errors.append("UC-03 Part 1 decision is not ACCEPTED")
    if part2.get("status") != "ACCEPTED" or part2.get("uc03_part3_authorized") is not True:
        errors.append("UC-03 Part 2 decision is not ACCEPTED or does not authorize Part 3")
    if part2.get("uc04_authorized") is True:
        errors.append("UC-03 Part 2 must not authorize UC-04")
    if part3 is not None:
        if part3.get("status") != "ACCEPTED" or part3.get("uc04_authorized") is not True:
            errors.append("UC-03 Part 3 is not ACCEPTED or does not authorize UC-04")
        _check_authority_false(errors, "UC-03 Part 3 decision", part3)
    if relocation.get("status") != "PASS" or int(relocation.get("file_relocation_count", 0)) <= 0:
        errors.append("UC-03 Part 2 relocation receipt is not PASS")
    if int(relocation.get("conflict_count", 0)) != 0:
        errors.append("UC-03 Part 2 relocation receipt contains unresolved conflicts")
    if rewrite.get("status") != "PASS" or int(rewrite.get("modified_file_count", 0)) <= 0:
        errors.append("UC-03 Part 2 rewrite receipt is not PASS")

    for label, payload in (
        ("UC-03 Part 1 decision", part1),
        ("UC-03 Part 2 decision", part2),
        ("UC-03 Part 2 relocation receipt", relocation),
    ):
        _check_authority_false(errors, label, payload)

    verified_amendment_paths = 0
    expected_by_path: dict[str, tuple[str, str]] = {}
    amendment_sources = [
        ("UC-01 migration amendment", required_files["UC-01 migration amendment"]),
        ("UC-02 migration amendment", required_files["UC-02 migration amendment"]),
        ("CI recovery amendment", required_files["CI recovery amendment"]),
    ]
    recovery_v2 = repo / "releases/unified_consolidation/ci_recovery_02/UC02_STATIC_AMENDMENT.json"
    if recovery_v2.is_file():
        amendment_sources.append(("CI recovery 02 amendment", recovery_v2))
    part3_static = repo / "releases/unified_consolidation/uc03/part3/UC02_STATIC_AMENDMENT.json"
    if part3_static.is_file():
        amendment_sources.append(("UC-03 Part 3 static amendment", part3_static))
    for label, amendment_path in amendment_sources:
        amendment = _read_json(amendment_path)
        if amendment.get("stage_id") != "UC-03":
            errors.append(f"{label} has the wrong stage identity")
        _check_authority_false(errors, label, amendment)
        rows = amendment.get("amended_paths", [])
        if not isinstance(rows, list) or not rows:
            errors.append(f"{label} contains no amended paths")
            continue
        for row in rows:
            if not isinstance(row, dict):
                errors.append(f"{label} has an invalid amended path row")
                continue
            relative = str(row.get("path", ""))
            expected = str(row.get("sha256", "")).lower()
            if not relative or not expected:
                errors.append(f"{label} has an incomplete amended path row")
                continue
            # Later bounded amendments supersede earlier hashes for the same path.
            expected_by_path[relative] = (expected, label)

    for relative, (expected, label) in sorted(expected_by_path.items()):
        resolved_rel = part3_relocations.get(relative, relative)
        path = repo / resolved_rel
        if not path.is_file():
            errors.append(f"{label} path is missing after relocation: {relative}")
            continue
        if not hash_matches(path, expected):
            successor = part3_rewrites.get(resolved_rel)
            before = str(successor.get("before_sha256", "")).lower() if successor else ""
            after = str(successor.get("after_sha256", "")).lower() if successor else ""
            if before != expected.lower() or not after or not hash_matches(path, after):
                errors.append(f"{label} hash mismatch: {relative}")
                continue
        verified_amendment_paths += 1

    result = {
        "status": "PASS" if not errors else "FAILED",
        "errors": errors,
        "warnings": warnings,
        "relocation_count": int(relocation.get("file_relocation_count", 0)),
        "rewrite_file_count": int(rewrite.get("modified_file_count", 0)),
        "verified_amendment_path_count": verified_amendment_paths,
        "historical_dynamic_uc01_uc02_package_required": False,
        "continuity_basis": "UC-03 accepted decisions, relocation receipts, chained rewrite receipts and bounded static amendments",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = verify(Path(args.repo_root))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
