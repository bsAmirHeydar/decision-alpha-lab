from pathlib import Path
import pytest

from src.engine.tooling.strategy_factory.lcm.lcm_09b.errors import IntegrityError
from src.engine.tooling.strategy_factory.lcm.lcm_09b.patch_verify import verify_hash_ledger


def test_hash_ledger_accepts_sorted_exact_files(tmp_path: Path):
    payload = tmp_path / "a.txt"
    payload.write_text("alpha\n", encoding="utf-8")
    from src.engine.tooling.strategy_factory.lcm.lcm_09b.canonical import file_digest
    ledger = tmp_path / "hashes.sha256"
    ledger.write_text(f"{file_digest(payload)}  a.txt\n", encoding="utf-8")
    out = verify_hash_ledger(tmp_path, ledger)
    assert out["passed"] and out["verified_file_count"] == 1


def test_hash_ledger_rejects_traversal(tmp_path: Path):
    ledger = tmp_path / "hashes.sha256"
    ledger.write_text("sha256:" + "0" * 64 + "  ../escape\n", encoding="utf-8")
    with pytest.raises(IntegrityError):
        verify_hash_ledger(tmp_path, ledger)
