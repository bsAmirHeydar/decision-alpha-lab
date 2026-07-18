from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.strategy_factory.lcm.lcm_01.cross_platform_integrity import (
    canonicalize_text_eol,
    verify_repository_bytes_cross_platform,
)
from tools.strategy_factory.lcm.lcm_01.errors import IntegrityError


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _package(tmp_path: Path, records: list[dict[str, str]]) -> Path:
    package = tmp_path / "baseline"
    package.mkdir()
    (package / "baseline_manifest.json").write_text(
        json.dumps({"records": records}, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )
    return package


def test_crlf_working_tree_matches_lf_baseline(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    expected = b"alpha\nbeta\n"
    (repo / "sample.csv").write_bytes(b"alpha\r\nbeta\r\n")
    package = _package(tmp_path, [{"path": "sample.csv", "sha256": _sha256(expected)}])

    result = verify_repository_bytes_cross_platform(repo, package)

    assert result["passed"] is True
    assert result["raw_match_count"] == 0
    assert result["canonical_text_match_count"] == 1


def test_real_text_change_still_fails_closed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    expected = b"alpha\nbeta\n"
    (repo / "sample.md").write_bytes(b"alpha\r\nCHANGED\r\n")
    package = _package(tmp_path, [{"path": "sample.md", "sha256": _sha256(expected)}])

    with pytest.raises(IntegrityError, match="HASH_MISMATCH"):
        verify_repository_bytes_cross_platform(repo, package)


def test_binary_payload_never_receives_eol_normalization(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    expected = b"PK\x00alpha\nbeta\n"
    (repo / "sample.bin").write_bytes(b"PK\x00alpha\r\nbeta\r\n")
    package = _package(tmp_path, [{"path": "sample.bin", "sha256": _sha256(expected)}])

    with pytest.raises(IntegrityError, match="HASH_MISMATCH"):
        verify_repository_bytes_cross_platform(repo, package)


def test_path_escape_is_denied(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    package = _package(tmp_path, [{"path": "../escape.txt", "sha256": "0" * 64}])

    with pytest.raises(IntegrityError, match="PATH_ESCAPE"):
        verify_repository_bytes_cross_platform(repo, package)


def test_canonicalizer_changes_only_line_endings() -> None:
    assert canonicalize_text_eol(b" a \r\n\r\nb\r") == b" a \n\nb\n"
