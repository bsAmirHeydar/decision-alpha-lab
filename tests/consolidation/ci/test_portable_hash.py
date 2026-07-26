from __future__ import annotations

import hashlib
from pathlib import Path

from tools.consolidation.ci.portable_hash import hash_matches, sha256_variants


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def test_lf_and_crlf_are_portable_equivalents(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_bytes(b"alpha\nbeta\n")
    assert hash_matches(path, _sha(b"alpha\r\nbeta\r\n"))
    assert _sha(b"alpha\nbeta\n") in sha256_variants(path)


def test_semantic_text_change_is_not_accepted(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_bytes(b"alpha\nbeta\n")
    assert not hash_matches(path, _sha(b"alpha\ngamma\n"))


def test_binary_hash_remains_byte_exact(tmp_path: Path) -> None:
    path = tmp_path / "sample.bin"
    path.write_bytes(b"\x00alpha\r\nbeta")
    assert hash_matches(path, _sha(path.read_bytes()))
    assert not hash_matches(path, _sha(b"\x00alpha\nbeta"))
