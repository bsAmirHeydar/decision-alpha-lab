from __future__ import annotations

from strategy_factory_rthp_context_v1.governance_hashing import canonical_file_digest


def test_text_hash_is_stable_across_lf_and_crlf(tmp_path):
    lf = tmp_path / "lf.py"
    crlf = tmp_path / "crlf.py"
    lf.write_bytes(b"a=1\nb=2\n")
    crlf.write_bytes(b"a=1\r\nb=2\r\n")
    assert canonical_file_digest(lf) == canonical_file_digest(crlf)


def test_binary_hash_remains_raw(tmp_path):
    lf = tmp_path / "a.bin"
    crlf = tmp_path / "b.bin"
    lf.write_bytes(b"a\nb")
    crlf.write_bytes(b"a\r\nb")
    assert canonical_file_digest(lf) != canonical_file_digest(crlf)
