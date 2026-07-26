from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .canonical import canonical_json

SNAPSHOT_ROOT = Path("registry/history/lcm/lcm_14a")
SNAPSHOT_FILE = "reference_scan_snapshot.jsonl"
SUMMARY_FILE = "reference_scan_snapshot_summary.json"


def _sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def scan_references(repo_root: Path, candidates: list[dict]) -> tuple[list[dict], dict]:
    root = repo_root / SNAPSHOT_ROOT
    snapshot_path = root / SNAPSHOT_FILE
    summary_path = root / SUMMARY_FILE
    if not snapshot_path.is_file() or not summary_path.is_file():
        raise ValueError("REFERENCE_SCAN_SNAPSHOT_MISSING")
    text = snapshot_path.read_text(encoding="utf-8")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("snapshot_sha256") != _sha256_text(text):
        raise ValueError("REFERENCE_SCAN_SNAPSHOT_DIGEST_INVALID")
    expected_summary_digest = "sha256:" + hashlib.sha256(
        canonical_json({key: value for key, value in summary.items() if key != "summary_digest"}).encode("utf-8")
    ).hexdigest()
    if summary.get("summary_digest") != expected_summary_digest:
        raise ValueError("REFERENCE_SCAN_SUMMARY_DIGEST_INVALID")
    rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    if len(rows) != summary.get("reference_record_count"):
        raise ValueError("REFERENCE_SCAN_RECORD_COUNT")
    if summary.get("candidate_count") != len(candidates):
        raise ValueError("REFERENCE_SCAN_CANDIDATE_COUNT")
    candidate_ids = {row["consumer_id"] for row in candidates}
    if not {row["consumer_id"] for row in rows}.issubset(candidate_ids):
        raise ValueError("REFERENCE_SCAN_UNKNOWN_CONSUMER")
    return rows, {
        "files_scanned": summary["scan_universe_file_count"],
        "bytes_scanned": summary["scan_universe_bytes"],
        "decode_skipped_file_count": 0,
        "skipped_large_nonactive_artifact_count": 0,
        "reference_record_count": len(rows),
        "pattern_count": summary["pattern_count"],
        "matched_file_count": summary["matched_file_count"],
        "scan_scope": "ACTIVE_CODE_CONFIG_TEST_DOCS_AND_SELECTED_GENERATED_HANDOFF_PACKAGES",
        "scan_snapshot_sha256": summary["snapshot_sha256"],
        "scan_summary_digest": summary["summary_digest"],
    }
