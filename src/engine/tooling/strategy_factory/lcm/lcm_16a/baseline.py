from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.strategy_factory.lcm.portable_integrity import (
    BASELINE_DOCUMENT,
    BASELINE_RECORDS,
    EXPECTED_AMENDMENT_COUNT,
    LCM16A_AUDIT_RELATIVE,
    load_verified_lcm16a_amendments,
    matches_expected_digest,
)

EXPECTED_BASELINE_COUNT = 2168
EXPECTED_UNCHANGED_COUNT = EXPECTED_BASELINE_COUNT - EXPECTED_AMENDMENT_COUNT


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def _bound_package(repo_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    package_root = repo_root / LCM16A_AUDIT_RELATIVE
    document = _load_json(package_root / BASELINE_DOCUMENT)
    records = _load_jsonl(package_root / BASELINE_RECORDS)
    # Performs manifest binding, scope, digest-shape, uniqueness, count, and
    # authority checks before the artifacts are trusted.
    load_verified_lcm16a_amendments(repo_root)
    return document, records


def _check_declared_count(document: dict[str, Any], key: str, actual: int) -> None:
    if key in document and document[key] != actual:
        raise ValueError(f"LCM-16A baseline count mismatch: {key}")


def build_baseline_amendment(
    repo_root: Path,
    upstream_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    lock_path = upstream_root / "records/pre_delete_lock_records.jsonl"
    lock_rows = _load_jsonl(lock_path)
    if len(lock_rows) != EXPECTED_BASELINE_COUNT:
        raise ValueError("unexpected LCM-15C lock-set size")

    document, records = _bound_package(repo_root)
    amendments = {row["candidate_path"]: row for row in records}

    unchanged = 0
    amended = 0
    missing = 0
    for row in lock_rows:
        relative = row["candidate_path"]
        path = repo_root / relative
        if not path.is_file():
            missing += 1
            continue
        locked = row["locked_sha256"]
        if matches_expected_digest(path, locked):
            # Raw, LF, or CRLF representations of the same UTF-8 text are one
            # logical baseline state. No semantic normalisation is performed.
            unchanged += 1
            continue
        amendment = amendments.get(relative)
        if not amendment:
            raise ValueError(f"unapproved baseline drift: {relative}")
        if amendment.get("previous_sha256") != locked:
            raise ValueError(f"LCM-16A previous digest mismatch: {relative}")
        if not matches_expected_digest(path, amendment["amended_sha256"]):
            raise ValueError(f"LCM-16A amended digest mismatch: {relative}")
        amended += 1

    if missing:
        raise ValueError(f"LCM-16A baseline paths missing: {missing}")
    if amended != EXPECTED_AMENDMENT_COUNT:
        raise ValueError(f"unexpected effective amendment count: {amended}")
    if unchanged != EXPECTED_UNCHANGED_COUNT:
        raise ValueError(f"unexpected unchanged baseline count: {unchanged}")

    _check_declared_count(document, "baseline_count", len(lock_rows))
    _check_declared_count(document, "amendment_count", amended)
    _check_declared_count(document, "unchanged_count", unchanged)
    _check_declared_count(document, "missing_count", missing)
    return document, records


def verify_baseline_amendment(
    repo_root: Path,
    upstream_root: Path,
    package_root: Path | None = None,
) -> tuple[int, int, int, int]:
    document, records = build_baseline_amendment(repo_root, upstream_root)
    if package_root is not None:
        actual_document = _load_json(package_root / BASELINE_DOCUMENT)
        actual_records = _load_jsonl(package_root / BASELINE_RECORDS)
        if actual_document != document or actual_records != records:
            raise ValueError("LCM-16A baseline amendment artifact mismatch")
    return (
        EXPECTED_BASELINE_COUNT,
        len(records),
        EXPECTED_BASELINE_COUNT - len(records),
        0,
    )
