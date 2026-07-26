"""Verified post-phase baseline amendments for historical LCM evidence.

Historical phase packages remain immutable.  This module lets current-snapshot
verifiers accept a later, explicitly-scoped amendment only when the prior hash,
new hash, object digest and authority-negative fields all match.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def object_digest(value: Any, field: str | None = None) -> str:
    if field and isinstance(value, dict):
        value = {key: item for key, item in value.items() if key != field}
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_verified_amendments(repo_root: Path) -> dict[str, dict]:
    amendments: dict[str, dict] = {}
    audit_root = repo_root / "registry/history/lcm/full_system_audits"
    if not audit_root.is_dir():
        return amendments
    for document_path in sorted(audit_root.glob("*/baseline_amendment.json")):
        document = load_json(document_path)
        if document.get("validation_status") != "PASS":
            continue
        if document.get("amendment_digest") != object_digest(document, "amendment_digest"):
            raise ValueError(f"invalid baseline amendment digest: {document_path}")
        records_path = document_path.parent / "records/baseline_amendments.jsonl"
        if not records_path.is_file():
            raise ValueError(f"missing baseline amendment records: {records_path}")
        records = load_jsonl(records_path)
        if len(records) != document.get("amended_path_count"):
            raise ValueError(f"baseline amendment count mismatch: {document_path}")
        for record in records:
            relative = record["candidate_path"]
            if relative in amendments:
                raise ValueError(f"duplicate baseline amendment: {relative}")
            if record.get("deletion_approved") or record.get("deletion_performed"):
                raise ValueError(f"authority-bearing baseline amendment: {relative}")
            amendments[relative] = record
    return amendments


def digest_matches_current(
    repo_root: Path,
    relative: str,
    expected_sha256: str,
    current_sha256: str,
    amendments: dict[str, dict] | None = None,
) -> bool:
    if current_sha256 == expected_sha256:
        return True
    amendment_map = amendments if amendments is not None else load_verified_amendments(repo_root)
    amendment = amendment_map.get(relative)
    return bool(
        amendment
        and amendment.get("previous_sha256") == expected_sha256
        and amendment.get("amended_sha256") == current_sha256
    )
