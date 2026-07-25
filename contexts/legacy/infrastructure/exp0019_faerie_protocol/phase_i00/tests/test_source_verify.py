from pathlib import Path

from fp_i00_governance.canonical import file_sha256
from fp_i00_governance.source_verify import parse_hash_contract, verify_source_directory


def test_source_contract_parser_and_verifier(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_text("alpha", encoding="utf-8")
    digest = file_sha256(source / "a.txt")
    contract = tmp_path / "hashes.sha256"
    contract.write_text(f"{digest}  a.txt\n", encoding="utf-8")
    assert parse_hash_contract(contract) == {"a.txt": digest}
    report = verify_source_directory(source, contract)
    assert report["passed"]
    assert report["verified_count"] == 1


def test_source_mismatch_is_reported(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_text("changed", encoding="utf-8")
    contract = tmp_path / "hashes.sha256"
    contract.write_text(f"{'0' * 64}  a.txt\n", encoding="utf-8")
    report = verify_source_directory(source, contract)
    assert not report["passed"]
    assert report["mismatched"][0]["name"] == "a.txt"
