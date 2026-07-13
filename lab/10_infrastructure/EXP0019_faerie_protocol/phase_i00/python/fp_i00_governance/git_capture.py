"""Source-control snapshot capture with archive-safe behavior."""
from __future__ import annotations

from pathlib import Path
import subprocess

from .models import SourceControlSnapshot


def _run(repo: Path, *args: str) -> tuple[int, str]:
    process = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return process.returncode, process.stdout.rstrip("\r\n")


def capture_source_control(repo: Path, ignored_prefixes: tuple[str, ...] = ()) -> SourceControlSnapshot:
    code, inside = _run(repo, "rev-parse", "--is-inside-work-tree")
    if code != 0 or inside != "true":
        return SourceControlSnapshot(
            mode="ARCHIVE_OR_NON_GIT",
            git_available=False,
            branch="UNAVAILABLE",
            head_commit="UNAVAILABLE",
            clean=None,
            phase_clean=None,
            changed_paths=(),
            ignored_phase_changed_paths=(),
            unrelated_changed_paths=(),
            remote_urls=(),
        )
    _, branch = _run(repo, "rev-parse", "--abbrev-ref", "HEAD")
    _, head = _run(repo, "rev-parse", "HEAD")
    _, status = _run(repo, "status", "--porcelain=v1", "--untracked-files=all")
    _, remotes = _run(repo, "remote", "-v")
    changed = tuple(line[3:] if len(line) > 3 else line for line in status.splitlines() if line)
    def ignored(path: str) -> bool:
        normalized = path.replace("\\", "/")
        return any(normalized == prefix.rstrip("/") or normalized.startswith(prefix.rstrip("/") + "/") for prefix in ignored_prefixes)
    ignored_changes = tuple(path for path in changed if ignored(path))
    unrelated_changes = tuple(path for path in changed if not ignored(path))
    remote_urls = tuple(sorted({line.split()[1] for line in remotes.splitlines() if len(line.split()) >= 2}))
    return SourceControlSnapshot(
        mode="GIT",
        git_available=True,
        branch=branch,
        head_commit=head,
        clean=not bool(changed),
        phase_clean=not bool(unrelated_changes),
        changed_paths=changed,
        ignored_phase_changed_paths=ignored_changes,
        unrelated_changed_paths=unrelated_changes,
        remote_urls=remote_urls,
    )
