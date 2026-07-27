from __future__ import annotations

import csv
from pathlib import Path

import pytest

from tools.consolidation.uc04w1b.contracts import (
    BASELINE_COMPILE_TARGETS,
    CANDIDATE_ID,
    ENGINE_ID,
    expected_fixture_rows,
    sha256_file,
    write_json,
)
from tools.consolidation.uc04w1b.native_review import NativeReviewError, review_native_receipt


def build_native_evidence(repo: Path, root: Path) -> Path:
    logs = root / "metaeditor_logs"
    binaries = root / "compiled_ex5"
    logs.mkdir(parents=True)
    binaries.mkdir(parents=True)
    compile_rows = []
    for index, source_path in enumerate(BASELINE_COMPILE_TARGETS, start=1):
        log = logs / f"target_{index:02d}.log"
        ex5 = binaries / f"target_{index:02d}.ex5"
        log.write_text("Result: 0 errors, 0 warnings\n", encoding="utf-8")
        ex5.write_bytes(f"synthetic-ex5-{index}".encode("ascii"))
        compile_rows.append(
            {
                "source_path": source_path,
                "source_sha256": sha256_file(repo / source_path),
                "errors": 0,
                "warnings": 0,
                "log_path": log.relative_to(root).as_posix(),
                "log_sha256": sha256_file(log),
                "ex5_path": ex5.relative_to(root).as_posix(),
                "ex5_sha256": sha256_file(ex5),
            }
        )

    runtime = root / "UC04W1B_DeterministicDateTimeFormatNativeRunner.csv"
    with runtime.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["fixture_id", "unix_seconds", "expected", "legacy_output", "reference_output", "status"])
        for row in expected_fixture_rows():
            writer.writerow(
                [
                    row["fixture_id"],
                    row["unix_seconds"],
                    row["expected"],
                    row["expected"],
                    row["expected"],
                    "PASS",
                ]
            )
        writer.writerow(["SUMMARY", 13, "BYTE_EXACT_ASCII", "LEGACY_REFERENCE", "TEST_ONLY_REFERENCE_ENGINE", "PASS"])

    receipt = root / "native_acceptance_receipt.json"
    write_json(
        receipt,
        {
            "schema_version": "1.0.0",
            "program_id": "UCPS",
            "stage_id": "UC04-W1B-Q-NATIVE",
            "receipt_id": "UC04_W1B_NATIVE_ACCEPTANCE_TEST",
            "status": "PASS",
            "candidate_id": CANDIDATE_ID,
            "engine_id": ENGINE_ID,
            "captured_at_utc": "2026-07-27T00:00:00Z",
            "isolated_compile_workspace": True,
            "tracked_source_mutation": False,
            "compile_target_count": len(compile_rows),
            "compile_status": "PASS",
            "compile_targets": compile_rows,
            "runtime": {
                "status": "PASS",
                "runtime_csv_path": runtime.relative_to(root).as_posix(),
                "runtime_csv_sha256": sha256_file(runtime),
                "fixture_rows": 13,
                "failed_rows": 0,
                "summary": "PASS",
                "runtime_symbol": "EURUSD",
            },
            "implementation_authority": False,
            "consumer_cutover_authority": False,
            "deletion_authority": False,
            "runtime_authority": False,
            "order_authority": False,
            "capital_authority": False,
        },
    )
    return receipt


def test_native_review_recomputes_all_evidence(repo_root: Path, tmp_path: Path) -> None:
    receipt = build_native_evidence(repo_root, tmp_path / "evidence")
    review = review_native_receipt(repo_root, receipt)
    assert review["status"] == "PASS"
    assert review["compile_target_count"] == 12
    assert review["runtime"]["fixture_count"] == 13
    assert review["consumer_cutover_authority"] is False


def test_native_review_rejects_runtime_byte_drift(repo_root: Path, tmp_path: Path) -> None:
    receipt = build_native_evidence(repo_root, tmp_path / "evidence")
    document = __import__("json").loads(receipt.read_text(encoding="utf-8"))
    runtime = receipt.parent / document["runtime"]["runtime_csv_path"]
    text = runtime.read_text(encoding="utf-8").replace("1970.01.01 00:00:00", "1970.01.01 00:00:09", 1)
    runtime.write_text(text, encoding="utf-8")
    document["runtime"]["runtime_csv_sha256"] = sha256_file(runtime)
    write_json(receipt, document)
    with pytest.raises(NativeReviewError, match="expected output drift|byte equivalence failed"):
        review_native_receipt(repo_root, receipt)


def test_native_review_rejects_authority_grant(repo_root: Path, tmp_path: Path) -> None:
    receipt = build_native_evidence(repo_root, tmp_path / "evidence")
    document = __import__("json").loads(receipt.read_text(encoding="utf-8"))
    document["consumer_cutover_authority"] = True
    write_json(receipt, document)
    with pytest.raises(NativeReviewError, match="forbidden authority"):
        review_native_receipt(repo_root, receipt)
