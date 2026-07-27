from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from tools.consolidation.uc04w0.verify import (
    parse_lfs_pointer,
    verify_historical_lfs_artifact,
)


def _pointer(payload: bytes) -> bytes:
    return (
        "version https://git-lfs.github.com/spec/v1\n"
        f"oid sha256:{hashlib.sha256(payload).hexdigest()}\n"
        f"size {len(payload)}\n"
    ).encode("ascii")


def _git(repo: Path, *arguments: str) -> None:
    subprocess.run(["git", "-C", str(repo), *arguments], check=True, capture_output=True)


def _committed_pointer_repo(tmp_path: Path, payload: bytes) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "ci@example.invalid")
    _git(repo, "config", "user.name", "CI Test")
    relative = "registry/history/example.bin"
    target = repo / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(_pointer(payload))
    _git(repo, "add", "--", relative)
    _git(repo, "commit", "-m", "test pointer")
    return repo, relative


def test_pointer_parser_requires_version_oid_and_size() -> None:
    payload = b"alpha-lab-lfs-fixture"
    assert parse_lfs_pointer(_pointer(payload)) == (hashlib.sha256(payload).hexdigest(), len(payload))
    assert parse_lfs_pointer(b"not a pointer\n") is None


def test_source_archive_pointer_representation_passes(tmp_path: Path) -> None:
    payload = b"archive-payload"
    relative = "registry/history/example.bin"
    target = tmp_path / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(_pointer(payload))
    errors: list[str] = []
    verify_historical_lfs_artifact(tmp_path, relative, errors)
    assert errors == []


def test_hydrated_checkout_matching_head_pointer_passes(tmp_path: Path) -> None:
    payload = b"hydrated-payload" * 128
    repo, relative = _committed_pointer_repo(tmp_path, payload)
    (repo / relative).write_bytes(payload)
    errors: list[str] = []
    verify_historical_lfs_artifact(repo, relative, errors)
    assert errors == []


def test_hydrated_checkout_digest_mismatch_fails(tmp_path: Path) -> None:
    payload = b"expected-payload" * 128
    repo, relative = _committed_pointer_repo(tmp_path, payload)
    corrupted = bytearray(payload)
    corrupted[-1] ^= 1
    (repo / relative).write_bytes(bytes(corrupted))
    errors: list[str] = []
    verify_historical_lfs_artifact(repo, relative, errors)
    assert errors == [f"hydrated Git LFS object digest mismatch: {relative}"]
