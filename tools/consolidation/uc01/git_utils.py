"""Read-only Git and Git-LFS discovery helpers plus bounded preservation actions."""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .io_utils import redact_url


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    returncode: int
    stdout: str


def run_command(command: Iterable[str], cwd: Path, *, timeout: int = 120, check: bool = False) -> CommandResult:
    cmd = tuple(str(x) for x in command)
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        result = CommandResult(cmd, proc.returncode, proc.stdout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        result = CommandResult(cmd, 127, f"{type(exc).__name__}: {exc}")
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(cmd)}\n{result.stdout}")
    return result


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_available(repo_root: Path) -> bool:
    return run_command(("git", "rev-parse", "--is-inside-work-tree"), repo_root, timeout=15).returncode == 0


def list_repository_files(repo_root: Path) -> tuple[list[str], str]:
    """Return tracked plus non-ignored untracked paths, or filesystem fallback paths."""
    if git_available(repo_root):
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=repo_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode == 0:
            paths = sorted({p.decode("utf-8", errors="surrogateescape").replace("\\", "/") for p in result.stdout.split(b"\x00") if p})
            return paths, "git_index_plus_untracked"
    paths: list[str] = []
    for path in repo_root.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue
        rel = path.relative_to(repo_root)
        if any(part in {".git", ".pytest_cache", ".mypy_cache", ".ruff_cache", "__pycache__"} for part in rel.parts):
            continue
        paths.append(rel.as_posix())
    return sorted(set(paths)), "filesystem_fallback"


def git_metadata(repo_root: Path) -> dict:
    if not git_available(repo_root):
        return {"available": False}
    def out(*args: str) -> str:
        result = run_command(("git", *args), repo_root, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else ""
    remotes = []
    for line in out("remote", "-v").splitlines():
        parts = line.split()
        if len(parts) >= 3:
            remotes.append({"name": parts[0], "url": redact_url(parts[1]), "mode": parts[2].strip("()")})
    return {
        "available": True,
        "head": out("rev-parse", "HEAD"),
        "branch": out("branch", "--show-current") or "DETACHED",
        "describe": out("describe", "--always", "--dirty", "--tags"),
        "status_porcelain": out("status", "--short", "--untracked-files=all").splitlines(),
        "remotes": remotes,
        "object_format": out("rev-parse", "--show-object-format") or "sha1",
        "worktree": out("rev-parse", "--show-toplevel"),
    }


def git_status_map(repo_root: Path) -> dict[str, str]:
    if not git_available(repo_root):
        return {}
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return {}
    chunks = [x for x in proc.stdout.split(b"\x00") if x]
    result: dict[str, str] = {}
    index = 0
    while index < len(chunks):
        entry = chunks[index].decode("utf-8", errors="surrogateescape")
        status = entry[:2]
        path = entry[3:].replace("\\", "/")
        if status[0] in {"R", "C"} and index + 1 < len(chunks):
            old = chunks[index + 1].decode("utf-8", errors="surrogateescape").replace("\\", "/")
            result[path] = status
            result[old] = status + "_SOURCE"
            index += 2
        else:
            result[path] = status
            index += 1
    return result


def lfs_inventory(repo_root: Path) -> tuple[list[dict], dict]:
    version = run_command(("git", "lfs", "version"), repo_root, timeout=20)
    if version.returncode != 0:
        return [], {"available": False, "version_output": version.stdout.strip()}
    result = run_command(("git", "lfs", "ls-files", "--long"), repo_root, timeout=120)
    rows: list[dict] = []
    pattern = re.compile(r"^([0-9a-fA-F]{64})\s+([*-])\s+(.+)$")
    for line in result.stdout.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        oid, marker, path = match.groups()
        target = repo_root / path
        rows.append({
            "path": path.replace("\\", "/"),
            "oid_sha256": oid.lower(),
            "materialization_marker": marker,
            "exists": target.is_file(),
            "size": target.stat().st_size if target.is_file() else None,
        })
    return sorted(rows, key=lambda x: x["path"]), {
        "available": True,
        "version_output": version.stdout.strip(),
        "command_returncode": result.returncode,
    }


def create_git_preservation(
    repo_root: Path,
    output_dir: Path,
    *,
    tag_name: str,
    branch_name: str,
    overwrite_artifacts: bool = False,
) -> dict:
    """Create immutable Git references and a complete Git bundle from current HEAD.

    The repository worktree may contain UC-01 uncommitted files; refs intentionally point
    to HEAD, preserving the last committed pre-consolidation state.
    """
    if not git_available(repo_root):
        return {"status": "BLOCKED", "reason": "git_repository_unavailable"}
    output_dir.mkdir(parents=True, exist_ok=True)
    head = run_command(("git", "rev-parse", "HEAD"), repo_root, check=True).stdout.strip()
    existing_tag = run_command(("git", "rev-parse", "-q", "--verify", f"refs/tags/{tag_name}"), repo_root)
    if existing_tag.returncode == 0 and existing_tag.stdout.strip() != head:
        raise RuntimeError(f"tag {tag_name} exists at a different commit")
    if existing_tag.returncode != 0:
        run_command(("git", "tag", "-a", tag_name, head, "-m", "Alpha Lab pre-unified-consolidation preservation point"), repo_root, check=True)
    existing_branch = run_command(("git", "rev-parse", "-q", "--verify", f"refs/heads/{branch_name}"), repo_root)
    if existing_branch.returncode == 0 and existing_branch.stdout.strip() != head:
        raise RuntimeError(f"branch {branch_name} exists at a different commit")
    if existing_branch.returncode != 0:
        run_command(("git", "branch", branch_name, head), repo_root, check=True)
    bundle_path = output_dir / "decision-alpha-lab-pre-unified-consolidation.bundle"
    if bundle_path.exists() and not overwrite_artifacts:
        bundle_status = "reused_existing"
    else:
        if bundle_path.exists():
            bundle_path.unlink()
        run_command(("git", "bundle", "create", str(bundle_path), "--all"), repo_root, timeout=1800, check=True)
        bundle_status = "created"
    verify = run_command(("git", "bundle", "verify", str(bundle_path)), repo_root, timeout=300)
    return {
        "status": "PASS" if verify.returncode == 0 else "FAILED",
        "head": head,
        "tag": tag_name,
        "branch": branch_name,
        "bundle_path": str(bundle_path.resolve()),
        "bundle_size": bundle_path.stat().st_size if bundle_path.exists() else None,
        "bundle_sha256": _sha256_file(bundle_path) if bundle_path.exists() else None,
        "bundle_status": bundle_status,
        "bundle_verify_returncode": verify.returncode,
        "bundle_verify_output": verify.stdout.strip(),
    }
