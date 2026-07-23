from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import object_digest
from .constants import (
    AIEOS_MANIFEST_DIGEST,
    AIEOS_PATCH_ID,
    EXPECTED_AMENDMENT_COUNT,
    EXPECTED_BASELINE_COUNT,
    EXPECTED_UNCHANGED_COUNT,
    UPSTREAM_CLOSURE_ID,
)
from .io import file_digest, load_json, load_jsonl


def build_baseline_amendment(repo_root: Path, upstream_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    lock_path = upstream_root / "records/pre_delete_lock_records.jsonl"
    lock_rows = load_jsonl(lock_path)
    if len(lock_rows) != EXPECTED_BASELINE_COUNT:
        raise ValueError("unexpected LCM-15C lock-set size")

    reference = load_json(repo_root / "AIEOS_OBSIDIAN_ID_NORMALIZATION_REFERENCE_VALIDATION.json")
    manifest = load_json(repo_root / "AIEOS_OBSIDIAN_ID_NORMALIZATION_PATCH_MANIFEST.json")
    if manifest.get("patch_id") != AIEOS_PATCH_ID:
        raise ValueError("unexpected AIEOS patch id")
    if manifest.get("manifest_digest") != AIEOS_MANIFEST_DIGEST:
        raise ValueError("unexpected AIEOS manifest digest")
    if reference.get("simulated_applied_changes") != EXPECTED_AMENDMENT_COUNT:
        raise ValueError("AIEOS change-count evidence mismatch")

    amendments: list[dict[str, Any]] = []
    unchanged = 0
    missing = 0
    for row in lock_rows:
        relative = row["candidate_path"]
        path = repo_root / relative
        if not path.is_file():
            missing += 1
            continue
        current = file_digest(path)
        if current == row["locked_sha256"]:
            unchanged += 1
            continue
        if not relative.startswith("docs/ai_algorithm_engineering_os/"):
            raise ValueError(f"unapproved baseline drift outside AIEOS: {relative}")
        amendments.append(
            {
                "candidate_path": relative,
                "previous_sha256": row["locked_sha256"],
                "amended_sha256": current,
                "amendment_reason": "AIEOS_OBSIDIAN_NOTE_ID_NORMALIZATION",
                "cause_patch_id": AIEOS_PATCH_ID,
                "cause_manifest_digest": AIEOS_MANIFEST_DIGEST,
                "deletion_approved": False,
                "deletion_performed": False,
            }
        )

    if len(amendments) != EXPECTED_AMENDMENT_COUNT:
        raise ValueError("unexpected amended path count")
    if unchanged != EXPECTED_UNCHANGED_COUNT or missing != 0:
        raise ValueError("baseline amendment partition mismatch")

    amendments.sort(key=lambda item: item["candidate_path"])
    document: dict[str, Any] = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-16A",
        "claim_ceiling": "LCM_16A_REFERENCE_ONLY",
        "producer": "tools.strategy_factory.lcm.lcm_16a.baseline:build_baseline_amendment",
        "owner": "ALPHA_LAB_MIGRATION_OWNER",
        "reviewer": "INDEPENDENT_MIGRATION_REVIEWER",
        "generated_at": None,
        "generated_time_semantics": "DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY",
        "upstream_closure_id": UPSTREAM_CLOSURE_ID,
        "upstream_lock_record_count": len(lock_rows),
        "unchanged_path_count": unchanged,
        "amended_path_count": len(amendments),
        "missing_path_count": missing,
        "cause_patch_id": AIEOS_PATCH_ID,
        "cause_manifest_digest": AIEOS_MANIFEST_DIGEST,
        "all_amendments_within_approved_scope": True,
        "deletion_authority_created": False,
        "runtime_authority_created": False,
        "order_authority_created": False,
        "capital_authority_created": False,
        "validation_status": "PASS",
        "amendment_digest": None,
    }
    document["amendment_digest"] = object_digest(document, "amendment_digest")
    return document, amendments


def verify_baseline_amendment(repo_root: Path, upstream_root: Path, amendment_root: Path) -> tuple[int, int, int, int]:
    document = load_json(amendment_root / "baseline_amendment.json")
    if document.get("amendment_digest") != object_digest(document, "amendment_digest"):
        raise ValueError("baseline amendment digest mismatch")
    records = load_jsonl(amendment_root / "records/baseline_amendments.jsonl")
    expected_document, expected_records = build_baseline_amendment(repo_root, upstream_root)
    if document != expected_document:
        raise ValueError("baseline amendment document is not reproducible")
    if records != expected_records:
        raise ValueError("baseline amendment records are not reproducible")
    return (
        document["upstream_lock_record_count"],
        document["amended_path_count"],
        document["unchanged_path_count"],
        document["missing_path_count"],
    )
