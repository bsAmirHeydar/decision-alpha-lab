from __future__ import annotations

import hashlib
from pathlib import Path

from tools.strategy_factory.lcm.portable_integrity import (
    digest_variants,
    matches_expected_digest,
    portable_file_digest,
)


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def test_lf_and_crlf_are_same_logical_utf8_text(tmp_path: Path) -> None:
    lf = b"alpha,beta\n1,2\n3,4\n"
    crlf = lf.replace(b"\n", b"\r\n")
    path = tmp_path / "sample.csv"
    path.write_bytes(crlf)
    assert matches_expected_digest(path, _digest(lf))
    assert portable_file_digest(path) == _digest(lf)
    assert _digest(crlf) in digest_variants(path)


def test_semantic_change_is_not_normalised_away(tmp_path: Path) -> None:
    expected = b"alpha,beta\n1,2\n"
    path = tmp_path / "sample.csv"
    path.write_bytes(b"alpha,beta\r\n1,999\r\n")
    assert not matches_expected_digest(path, _digest(expected))


def test_binary_payload_is_raw_byte_strict(tmp_path: Path) -> None:
    path = tmp_path / "sample.bin"
    path.write_bytes(b"\x00A\r\nB")
    assert matches_expected_digest(path, _digest(b"\x00A\r\nB"))
    assert not matches_expected_digest(path, _digest(b"\x00A\nB"))


def test_known_acl06_windows_worktree_representation() -> None:
    root = Path(__file__).resolve().parents[4]
    path = root / "releases/history/acl_os/inventories/ACL_OS_06_ARTIFACT_INVENTORY.csv"
    locked_lf = "sha256:9d31fc29d99420a931ac6763e8447341d05921f55ce3ec5a295f932bdca27a9d"
    assert matches_expected_digest(path, locked_lf)
