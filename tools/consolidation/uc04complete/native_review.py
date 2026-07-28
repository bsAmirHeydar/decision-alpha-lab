from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.consolidation.uc04complete.build import REGISTRY_ROOT, SCHEMA_ROOT, canonical_json, document_digest
from tools.repository_paths import RepositoryPaths

RECEIPT_SCHEMA = "native_seal_receipt.schema.json"
REVIEW_SCHEMA = "native_seal_review.schema.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object expected: {path}")
    return value


def validate_schema(root: Path, value: dict[str, Any], schema_name: str) -> list[str]:
    schema = read_json(root / SCHEMA_ROOT / schema_name)
    Draft202012Validator.check_schema(schema)
    errors: list[str] = []
    for issue in Draft202012Validator(schema).iter_errors(value):
        location = "/".join(str(part) for part in issue.path) or "<root>"
        errors.append(f"schema violation {schema_name}@{location}: {issue.message}")
    return errors


def review(repo: Path, receipt_path: Path, output_path: Path | None = None) -> tuple[dict[str, Any], list[str]]:
    root = RepositoryPaths.discover(repo).root
    receipt_path = receipt_path.resolve()
    receipt = read_json(receipt_path)
    errors = validate_schema(root, receipt, RECEIPT_SCHEMA)

    contract = read_json(root / REGISTRY_ROOT / "native_acceptance_contract.json")
    targets = contract["compile_targets"]
    target_map = {item.get("source_path"): item for item in receipt.get("compile_targets", [])}

    if receipt.get("status") != "PASS":
        errors.append("native receipt status is not PASS")
    if receipt.get("compile_target_count") != len(targets):
        errors.append("compile target count does not match the canonical contract")
    if set(target_map) != set(targets):
        missing = sorted(set(targets) - set(target_map))
        extra = sorted(set(target_map) - set(targets))
        errors.append(f"compile target membership mismatch; missing={missing}, extra={extra}")

    evidence_root = receipt_path.parent
    for relative in targets:
        item = target_map.get(relative)
        if not item:
            continue
        source = root / relative
        if not source.is_file():
            errors.append(f"compile source missing from repository: {relative}")
            continue
        if item.get("source_sha256") != sha256_file(source):
            errors.append(f"source hash mismatch: {relative}")
        if item.get("errors") != 0 or item.get("warnings") != 0:
            errors.append(f"compile was not clean: {relative}")
        for key, digest_key in (("log_path", "log_sha256"), ("ex5_path", "ex5_sha256")):
            artifact = evidence_root / str(item.get(key, ""))
            if not artifact.is_file():
                errors.append(f"missing evidence artifact for {relative}: {key}")
                continue
            if item.get(digest_key) != sha256_file(artifact):
                errors.append(f"evidence hash mismatch for {relative}: {key}")
        log = evidence_root / str(item.get("log_path", ""))
        if log.is_file():
            text = log.read_text(encoding="utf-8-sig", errors="replace")
            normalized = " ".join(text.lower().split())
            if "0 errors, 0 warnings" not in normalized and "0 error(s), 0 warning(s)" not in normalized:
                errors.append(f"clean compile marker missing from log: {relative}")

    runtime = receipt.get("runtime", {})
    runtime_csv = evidence_root / str(runtime.get("runtime_csv_path", ""))
    if not runtime_csv.is_file():
        errors.append("runtime CSV is missing")
    elif runtime.get("runtime_csv_sha256") != sha256_file(runtime_csv):
        errors.append("runtime CSV hash mismatch")
    if runtime.get("status") != "PASS" or runtime.get("summary") != "PASS":
        errors.append("runtime self-test is not PASS")
    if int(runtime.get("failed_rows", -1)) != 0:
        errors.append("runtime self-test has failed rows")
    if int(runtime.get("test_rows", 0)) < 20:
        errors.append("runtime self-test did not execute the complete primitive corpus")

    for field in (
        "production_source_mutation",
        "semantic_change_authority",
        "deletion_authority",
        "runtime_authority",
        "order_authority",
        "capital_authority",
    ):
        if receipt.get(field) is not False:
            errors.append(f"forbidden authority or mutation in receipt: {field}")

    review_record: dict[str, Any] = {
        "$schema": "../../../../schemas/consolidation/uc04/complete/native_seal_review.schema.json",
        "program_id": "UCPS",
        "stage_id": "UC04-COMPLETE-NATIVE-SEAL",
        "schema_version": "1.0.0",
        "receipt_sha256": sha256_file(receipt_path),
        "contract_sha256": sha256_file(root / REGISTRY_ROOT / "native_acceptance_contract.json"),
        "compile_target_count": len(targets),
        "compile_membership_exact": set(target_map) == set(targets),
        "compile_all_zero_errors_zero_warnings": not any("compile" in error for error in errors),
        "runtime_summary_pass": runtime.get("status") == "PASS" and runtime.get("summary") == "PASS",
        "runtime_failed_rows": int(runtime.get("failed_rows", -1)),
        "production_source_mutation": False,
        "semantic_change_authority": False,
        "deletion_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "capital_authority": False,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    review_record["document_digest"] = document_digest(review_record)
    errors.extend(validate_schema(root, review_record, REVIEW_SCHEMA))
    if errors and review_record["status"] == "PASS":
        review_record["status"] = "FAIL"
        review_record["errors"] = errors
        review_record["document_digest"] = document_digest(review_record)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(json.dumps(review_record, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    return review_record, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently review UC-04 complete native seal evidence.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    record, errors = review(Path(args.repo_root), Path(args.receipt), Path(args.output))
    if errors or record.get("status") != "PASS":
        print(f"UC04 native seal review failed: {len(errors)} error(s)")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("UC04 native seal independent review: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
