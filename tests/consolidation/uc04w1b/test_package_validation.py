from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from tools.consolidation.uc04w1b.package_validation import (
    PackageValidationError,
    build_deterministic_zip,
    sha256_file,
    verify_tree,
    verify_zip,
)


def test_release_tree_contract_passes(repo_root: Path) -> None:
    result = verify_tree(repo_root)
    assert result["stage_id"] == "UC04-W1B-Q"
    assert result["lfs_pointer_count"] == 0
    assert result["secret_finding_count"] == 0
    assert result["line_endings"] == "PASS"
    assert result["schema_validation"] == "PASS"


def test_deterministic_zip_is_byte_reproducible(repo_root: Path, tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    first_result = build_deterministic_zip(repo_root, first)
    second_result = build_deterministic_zip(repo_root, second)
    assert first_result["zip_structure"] == "PASS"
    assert first_result["zip_sha256"] == second_result["zip_sha256"]
    assert sha256_file(first) == sha256_file(second)


def test_extracted_staging_has_exact_index_membership(repo_root: Path, tmp_path: Path) -> None:
    archive = tmp_path / "patch.zip"
    build_deterministic_zip(repo_root, archive)
    staging = tmp_path / "staging"
    with zipfile.ZipFile(archive) as handle:
        handle.extractall(staging)
    result = verify_tree(staging, payload_only=True)
    assert result["patch_file_count"] > 0


def test_bytecode_disabled_subprocess_does_not_mutate_staging(repo_root: Path, tmp_path: Path) -> None:
    archive = tmp_path / "patch.zip"
    build_deterministic_zip(repo_root, archive)
    staging = tmp_path / "staging"
    with zipfile.ZipFile(archive) as handle:
        handle.extractall(staging)

    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "tools.consolidation.uc04w1b.package_validation",
            "verify-tree",
            "--repo-root",
            str(staging),
            "--payload-only",
        ],
        cwd=staging,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert not list(staging.rglob("__pycache__"))
    assert not list(staging.rglob("*.pyc"))
    assert not list(staging.rglob("*.pyo"))


def test_zip_rejects_path_traversal(tmp_path: Path) -> None:
    archive = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(archive, "w") as handle:
        handle.writestr("../escape.txt", "x")
    with pytest.raises(PackageValidationError, match="unsafe relative path"):
        verify_zip(archive)


def test_zip_rejects_lfs_pointer_payload(repo_root: Path, tmp_path: Path) -> None:
    valid = tmp_path / "valid.zip"
    invalid = tmp_path / "lfs.zip"
    build_deterministic_zip(repo_root, valid)
    with zipfile.ZipFile(valid) as source, zipfile.ZipFile(invalid, "w") as target:
        for info in source.infolist():
            payload = source.read(info)
            if info.filename.endswith("/README.md"):
                payload = b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"0" * 64 + b"\nsize 1\n"
            target.writestr(info, payload)
    with pytest.raises(PackageValidationError, match="Git LFS pointer"):
        verify_zip(invalid)


def test_powershell_payload_is_crlf_and_installer_has_no_git_write(repo_root: Path) -> None:
    release = repo_root / "releases/unified_consolidation/uc04/w1b"
    for relative in (
        release / "APPLY.ps1",
        repo_root / "tools/consolidation/uc04w1b/Invoke-UC04W1BQualification.ps1",
    ):
        payload = relative.read_bytes()
        assert payload.endswith(b"\r\n")
        assert payload.count(b"\n") == payload.count(b"\r\n")
    installer = (release / "APPLY.ps1").read_text(encoding="utf-8-sig").lower()
    assert "git add ." not in installer
    assert "git add -a" not in installer
    assert "git commit" not in installer
    assert "git push" not in installer
    assert "$exitcode:" not in installer
    assert "exit code {0}: {1}" in installer
    assert 'prefix = @("-b")' in installer
    assert 'prefix = @("-3", "-b")' in installer
    assert "pythondontwritebytecode" in installer
    assert installer.count("no:cacheprovider") == 2
