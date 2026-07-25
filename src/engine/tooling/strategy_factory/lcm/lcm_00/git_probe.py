from __future__ import annotations

import subprocess
from pathlib import Path

from .canonical import digest_object


def _run(root: Path, *args: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"{type(exc).__name__}:{exc}"
    if result.returncode != 0:
        return False, (result.stderr or result.stdout).strip()
    return True, result.stdout.strip()


def probe_git(root: Path) -> dict:
    ok, inside = _run(root, "rev-parse", "--is-inside-work-tree")
    if not ok or inside.lower() != "true":
        value = {
            "schema_version": "1.0.0",
            "repository_metadata_available": False,
            "state": "UNKNOWN_GIT_METADATA",
            "head_commit": "UNKNOWN",
            "branch": "UNKNOWN",
            "tags_pointing_at_head": [],
            "status_porcelain_v2": "UNKNOWN",
            "submodule_status": "UNKNOWN",
            "lfs_available": "UNKNOWN",
            "reason_codes": ["SOURCE_ARCHIVE_EXCLUDED_GIT_METADATA"],
            "git_state_digest": "",
        }
        value["git_state_digest"] = digest_object(value, "git_state_digest")
        return value

    _, head = _run(root, "rev-parse", "HEAD")
    branch_ok, branch = _run(root, "symbolic-ref", "--short", "HEAD")
    tags_ok, tags = _run(root, "tag", "--points-at", "HEAD")
    status_ok, status = _run(root, "status", "--porcelain=v2", "--untracked-files=all")
    sub_ok, sub = _run(root, "submodule", "status", "--recursive")
    lfs_ok, _ = _run(root, "lfs", "version")
    value = {
        "schema_version": "1.0.0",
        "repository_metadata_available": True,
        "state": "CAPTURED",
        "head_commit": head,
        "branch": branch if branch_ok else "DETACHED_OR_UNKNOWN",
        "tags_pointing_at_head": sorted(tags.splitlines()) if tags_ok and tags else [],
        "status_porcelain_v2": status if status_ok else "UNKNOWN",
        "working_tree_clean": bool(status_ok and not status),
        "submodule_status": sub if sub_ok else "UNKNOWN",
        "lfs_available": lfs_ok,
        "reason_codes": [],
        "git_state_digest": "",
    }
    value["git_state_digest"] = digest_object(value, "git_state_digest")
    return value
