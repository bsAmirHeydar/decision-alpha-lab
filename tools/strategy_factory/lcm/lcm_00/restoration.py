from __future__ import annotations

import shutil
from pathlib import Path

from .canonical import digest_object, sha256_file
from .errors import IntegrityError


def rehearse_restore(source_root: Path, records: list[dict], rehearsal_root: Path) -> dict:
    if rehearsal_root.exists():
        shutil.rmtree(rehearsal_root)
    rehearsal_root.mkdir(parents=True)
    copied = 0
    for item in records:
        src = source_root / item["path"]
        dst = rehearsal_root / item["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if item["kind"] == "SYMLINK":
            dst.symlink_to(item["symlink_target"])
        else:
            shutil.copy2(src, dst)
        copied += 1
    mismatches: list[dict] = []
    restored_paths: set[str] = set()
    for item in records:
        dst = rehearsal_root / item["path"]
        restored_paths.add(item["path"])
        if not dst.exists() and not dst.is_symlink():
            mismatches.append({"path": item["path"], "reason": "MISSING"})
            continue
        if item["kind"] == "FILE":
            actual = sha256_file(dst)
            if actual != item["sha256"]:
                mismatches.append({"path": item["path"], "reason": "HASH_MISMATCH", "actual": actual})
    value = {
        "schema_version": "1.0.0",
        "method": "CLEAN_DIRECTORY_COPY_AND_FULL_PATH_HASH_COMPARISON",
        "copied_record_count": copied,
        "verified_record_count": len(records) - len(mismatches),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "passed": not mismatches,
        "external_artifacts_restored": False,
        "git_metadata_restored": False,
        "claim_ceiling": "CONTENT_RESTORE_REHEARSAL_REFERENCE_ONLY",
        "restore_rehearsal_digest": "",
    }
    value["restore_rehearsal_digest"] = digest_object(value, "restore_rehearsal_digest")
    return value
