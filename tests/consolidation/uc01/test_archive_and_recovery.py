from pathlib import Path

from tools.consolidation.uc01.archive import create_source_archive, recovery_drill
from tools.consolidation.uc01.io_utils import sha256_file, write_jsonl_gz


def test_archive_round_trip_is_exact(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "a.txt").write_text("alpha\n", encoding="utf-8")
    (repo / "nested").mkdir()
    (repo / "nested" / "b.bin").write_bytes(b"\x00\x01")
    rows = [
        {"path": "a.txt", "sha256": sha256_file(repo / "a.txt"), "size": (repo / "a.txt").stat().st_size},
        {"path": "nested/b.bin", "sha256": sha256_file(repo / "nested/b.bin"), "size": 2},
    ]
    inventory = tmp_path / "inventory.jsonl.gz"
    write_jsonl_gz(inventory, rows)
    archive = tmp_path / "source.zip"
    receipt = create_source_archive(repo, inventory, archive)
    assert receipt["status"] == "PASS"
    drill = recovery_drill(inventory, archive)
    assert drill["status"] == "PASS"
    assert drill["restored_file_count"] == 2
