from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any

from tools.repository_paths import RepositoryPaths
from tools.consolidation.uc04w1b.contracts import (
    BASELINE_COMPILE_TARGETS,
    CANDIDATE_ID,
    ENGINE_ID,
    PROGRAM_ID,
    expected_fixture_rows,
    read_json,
    sha256_file,
    with_digest,
    write_json,
)

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
CLEAN_COMPILE_RE = re.compile(r"\b0\s+errors?\s*,\s*0\s+warnings?\b", re.IGNORECASE)


class NativeReviewError(ValueError):
    """Raised when native qualification evidence is incomplete or unsafe."""


def _safe_evidence_path(evidence_root: Path, relative: str, label: str) -> Path:
    value = Path(relative.replace("\\", "/"))
    if value.is_absolute() or ".." in value.parts:
        raise NativeReviewError(f"unsafe {label} path: {relative}")
    resolved_root = evidence_root.resolve()
    resolved = (evidence_root / value).resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise NativeReviewError(f"{label} escapes evidence root: {relative}")
    return resolved


def _require_hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise NativeReviewError(f"invalid {label} SHA-256")
    return value


def _verify_compile_targets(repo: Path, evidence_root: Path, receipt: dict[str, Any]) -> list[dict[str, Any]]:
    rows = receipt.get("compile_targets")
    if not isinstance(rows, list):
        raise NativeReviewError("compile_targets must be a list")
    if receipt.get("compile_target_count") != len(BASELINE_COMPILE_TARGETS):
        raise NativeReviewError("compile_target_count drift")
    if len(rows) != len(BASELINE_COMPILE_TARGETS):
        raise NativeReviewError("compile target receipt count drift")

    actual_paths = [str(row.get("source_path", "")) for row in rows if isinstance(row, dict)]
    if actual_paths != list(BASELINE_COMPILE_TARGETS):
        raise NativeReviewError("compile target order or membership drift")

    reviewed: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise NativeReviewError("compile target row must be an object")
        source_path = str(row.get("source_path", ""))
        source = repo / source_path
        if not source.is_file():
            raise NativeReviewError(f"compile source missing: {source_path}")
        source_hash = _require_hash(row.get("source_sha256"), f"source {source_path}")
        if sha256_file(source) != source_hash:
            raise NativeReviewError(f"compile source hash mismatch: {source_path}")
        if row.get("errors") != 0 or row.get("warnings") != 0:
            raise NativeReviewError(f"compile is not clean: {source_path}")

        log = _safe_evidence_path(evidence_root, str(row.get("log_path", "")), "compile log")
        ex5 = _safe_evidence_path(evidence_root, str(row.get("ex5_path", "")), "compiled EX5")
        if not log.is_file() or not ex5.is_file():
            raise NativeReviewError(f"compile evidence missing: {source_path}")
        log_hash = _require_hash(row.get("log_sha256"), f"compile log {source_path}")
        ex5_hash = _require_hash(row.get("ex5_sha256"), f"EX5 {source_path}")
        if sha256_file(log) != log_hash or sha256_file(ex5) != ex5_hash:
            raise NativeReviewError(f"compile evidence hash mismatch: {source_path}")
        text = log.read_text(encoding="utf-8-sig", errors="replace")
        if CLEAN_COMPILE_RE.search(text) is None:
            raise NativeReviewError(f"compile log lacks 0 errors, 0 warnings: {source_path}")
        reviewed.append(
            {
                "source_path": source_path,
                "source_sha256": source_hash,
                "log_sha256": log_hash,
                "ex5_sha256": ex5_hash,
                "status": "PASS",
            }
        )
    return reviewed


def _verify_runtime(evidence_root: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    runtime = receipt.get("runtime")
    if not isinstance(runtime, dict) or runtime.get("status") != "PASS":
        raise NativeReviewError("native runtime status is not PASS")
    if runtime.get("fixture_rows") != 13 or runtime.get("failed_rows") != 0 or runtime.get("summary") != "PASS":
        raise NativeReviewError("native runtime summary drift")
    csv_path = _safe_evidence_path(
        evidence_root,
        str(runtime.get("runtime_csv_path", "")),
        "runtime CSV",
    )
    if not csv_path.is_file():
        raise NativeReviewError("runtime CSV missing")
    csv_hash = _require_hash(runtime.get("runtime_csv_sha256"), "runtime CSV")
    if sha256_file(csv_path) != csv_hash:
        raise NativeReviewError("runtime CSV hash mismatch")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    fixtures = [row for row in rows if re.fullmatch(r"UC04W1_DT_[0-9]{3}", row.get("fixture_id", ""))]
    summaries = [row for row in rows if row.get("fixture_id") == "SUMMARY"]
    if len(fixtures) != 13 or len(summaries) != 1:
        raise NativeReviewError("runtime CSV must contain 13 fixtures and one summary")

    expected = {row["fixture_id"]: row for row in expected_fixture_rows()}
    observed_ids = [row.get("fixture_id") for row in fixtures]
    if observed_ids != list(expected):
        raise NativeReviewError("runtime fixture identity or order drift")
    for row in fixtures:
        fixture_id = str(row["fixture_id"])
        contract = expected[fixture_id]
        output = str(row.get("expected", ""))
        if str(row.get("unix_seconds", "")) != str(contract["unix_seconds"]):
            raise NativeReviewError(f"runtime unix second drift: {fixture_id}")
        if output != contract["expected"]:
            raise NativeReviewError(f"runtime expected output drift: {fixture_id}")
        if row.get("legacy_output") != output or row.get("reference_output") != output:
            raise NativeReviewError(f"runtime byte equivalence failed: {fixture_id}")
        if row.get("status") != "PASS" or len(output) != 19:
            raise NativeReviewError(f"runtime fixture failed: {fixture_id}")
        try:
            output.encode("ascii")
        except UnicodeEncodeError as exc:
            raise NativeReviewError(f"runtime output is not ASCII: {fixture_id}") from exc
    if summaries[0].get("status") != "PASS":
        raise NativeReviewError("runtime summary row is not PASS")

    return {
        "runtime_csv_sha256": csv_hash,
        "fixture_count": len(fixtures),
        "failed_fixture_count": 0,
        "summary": "PASS",
        "comparison": "BYTE_EXACT_ASCII",
        "status": "PASS",
    }


def review_native_receipt(repo: Path, receipt_path: Path) -> dict[str, Any]:
    root = RepositoryPaths.discover(repo).root
    receipt_path = receipt_path.resolve()
    receipt = read_json(receipt_path)
    evidence_root = receipt_path.parent

    if receipt.get("program_id") != PROGRAM_ID:
        raise NativeReviewError("native receipt program_id drift")
    if receipt.get("stage_id") != "UC04-W1B-Q-NATIVE":
        raise NativeReviewError("native receipt stage_id drift")
    if receipt.get("status") != "PASS":
        raise NativeReviewError("native receipt is not PASS")
    if receipt.get("candidate_id") != CANDIDATE_ID or receipt.get("engine_id") != ENGINE_ID:
        raise NativeReviewError("native receipt candidate identity drift")
    if receipt.get("isolated_compile_workspace") is not True or receipt.get("tracked_source_mutation") is not False:
        raise NativeReviewError("native capture isolation contract failed")
    for field in (
        "implementation_authority",
        "consumer_cutover_authority",
        "deletion_authority",
        "runtime_authority",
        "order_authority",
        "capital_authority",
    ):
        if receipt.get(field) is not False:
            raise NativeReviewError(f"native receipt grants forbidden authority: {field}")

    reviewed_targets = _verify_compile_targets(root, evidence_root, receipt)
    runtime_review = _verify_runtime(evidence_root, receipt)
    receipt_hash = sha256_file(receipt_path)
    return with_digest(
        {
            "$schema": "../../../../schemas/consolidation/uc04/w1b/independent_native_review.schema.json",
            "schema_version": "1.0.0",
            "program_id": PROGRAM_ID,
            "stage_id": "UC04-W1B-Q",
            "review_id": "UC04_W1B_INDEPENDENT_NATIVE_REVIEW_V1",
            "status": "PASS",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "receipt_path": receipt_path.name,
            "receipt_sha256": receipt_hash,
            "reviewer": "UC04W1B_DETERMINISTIC_INDEPENDENT_REVIEWER_V1",
            "review_method": "RECOMPUTE_HASHES_REPLAY_FIXTURE_CONTRACT_VERIFY_CLEAN_COMPILE",
            "compile_target_count": len(reviewed_targets),
            "compile_targets": reviewed_targets,
            "runtime": runtime_review,
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
            "next_action": "CONDITIONAL_CUTOVER_CANDIDATE_GENERATION_ALLOWED_NOT_APPLY_AUTHORIZED",
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Independently review UC04-W1B native evidence.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    receipt_path = Path(args.receipt)
    review = review_native_receipt(Path(args.repo_root), receipt_path)
    output = Path(args.output) if args.output else receipt_path.parent / "independent_native_review.json"
    write_json(output, review)
    print(f"UC04-W1B native review: PASS\nReview: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
