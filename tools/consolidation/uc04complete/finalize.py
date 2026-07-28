from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.consolidation.uc04complete.build import REGISTRY_ROOT, SCHEMA_ROOT, document_digest, sha256_file
from tools.consolidation.uc04complete.native_review import read_json
from tools.repository_paths import RepositoryPaths


def validate(root: Path, value: dict[str, Any], schema_name: str) -> None:
    schema = read_json(root / SCHEMA_ROOT / schema_name)
    Draft202012Validator.check_schema(schema)
    issues = list(Draft202012Validator(schema).iter_errors(value))
    if issues:
        raise ValueError("; ".join(issue.message for issue in issues))


def finalize(repo: Path, receipt_path: Path, review_path: Path) -> list[Path]:
    root = RepositoryPaths.discover(repo).root
    receipt_path = receipt_path.resolve()
    review_path = review_path.resolve()
    receipt = read_json(receipt_path)
    review = read_json(review_path)
    validate(root, receipt, "native_seal_receipt.schema.json")
    validate(root, review, "native_seal_review.schema.json")
    if receipt.get("status") != "PASS" or review.get("status") != "PASS":
        raise ValueError("native receipt and independent review must both be PASS")
    if review.get("receipt_sha256") != sha256_file(receipt_path):
        raise ValueError("review is not bound to the supplied receipt")

    acceptance: dict[str, Any] = {
        "$schema": "../../../../schemas/consolidation/uc04/complete/uc04_acceptance.schema.json",
        "program_id": "UCPS",
        "stage_id": "UC-04",
        "schema_version": "1.0.0",
        "implementation_status": "COMPLETE",
        "native_seal_status": "PASS",
        "selected_shared_capability_count": 14,
        "explicit_variant_count": 191,
        "consumer_adapter_count": 109,
        "compile_target_count": receipt["compile_target_count"],
        "runtime_test_rows": receipt["runtime"]["test_rows"],
        "runtime_failed_rows": 0,
        "native_receipt_sha256": sha256_file(receipt_path),
        "independent_review_sha256": sha256_file(review_path),
        "evidence_bundle_sha256": receipt["evidence_bundle_sha256"],
        "production_source_mutation": False,
        "unexplained_behavior_delta_count": 0,
        "active_internal_imports_from_retired_engines": 0,
        "context_specific_branch_in_shared_kernel": False,
        "semantic_change_authority": False,
        "deletion_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "capital_authority": False,
        "status": "ACCEPTED",
    }
    acceptance["document_digest"] = document_digest(acceptance)
    validate(root, acceptance, "uc04_acceptance.schema.json")

    handoff: dict[str, Any] = {
        "$schema": "../../../../schemas/consolidation/uc04/complete/uc05_handoff_decision.schema.json",
        "program_id": "UCPS",
        "stage_id": "UC04-TO-UC05",
        "schema_version": "1.0.0",
        "uc04_acceptance_digest": acceptance["document_digest"],
        "uc04_implementation_complete": True,
        "uc04_native_seal_pass": True,
        "uc05_handoff_authorized": True,
        "uc05_implementation_authority": False,
        "semantic_change_authority": False,
        "deletion_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "capital_authority": False,
        "status": "HANDOFF_AUTHORIZED_ONLY",
    }
    handoff["document_digest"] = document_digest(handoff)
    validate(root, handoff, "uc05_handoff_decision.schema.json")

    target = root / REGISTRY_ROOT
    target.mkdir(parents=True, exist_ok=True)
    outputs = [target / "uc04_acceptance.json", target / "uc05_handoff_decision.json"]
    for path, value in zip(outputs, (acceptance, handoff), strict=True):
        path.write_bytes(json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8") + b"\n")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize the UC-04 accepted exit and UC-05 handoff after native seal PASS.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--review", required=True)
    args = parser.parse_args()
    try:
        outputs = finalize(Path(args.repo_root), Path(args.receipt), Path(args.review))
    except Exception as exc:
        print(f"UC04 finalization failed: {exc}")
        return 1
    print("UC04 finalization: PASS")
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
