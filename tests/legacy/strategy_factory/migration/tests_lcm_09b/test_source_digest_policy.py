from pathlib import Path

from src.engine.tooling.strategy_factory.lcm.lcm_09b.source_digest import source_binding_digest


def test_text_digest_is_identical_for_lf_and_crlf(tmp_path: Path):
    lf = tmp_path / "source.mq5"
    crlf = tmp_path / "source_copy.mq5"
    lf.write_bytes(b"line_1\nline_2\n")
    crlf.write_bytes(b"line_1\r\nline_2\r\n")
    assert source_binding_digest(lf) == source_binding_digest(crlf)


def test_binary_digest_remains_byte_exact(tmp_path: Path):
    first = tmp_path / "first.bin"
    second = tmp_path / "second.bin"
    first.write_bytes(b"A\r\nB")
    second.write_bytes(b"A\nB")
    assert source_binding_digest(first) != source_binding_digest(second)
