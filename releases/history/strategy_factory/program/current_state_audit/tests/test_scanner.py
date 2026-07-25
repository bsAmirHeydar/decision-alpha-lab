from __future__ import annotations

from pathlib import Path

from sf_phase00.scanner import scan_files


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "lab").mkdir()
    (tmp_path / "docs").mkdir()
    return tmp_path


def test_happy_path_inventory_is_sorted_and_hashed(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    (root / "lab" / "a.py").write_text("print('x')\n", encoding="utf-8")
    (root / "docs" / "b.md").write_text("# B\n", encoding="utf-8")
    records = scan_files(root)
    assert [record.path for record in records] == ["docs/b.md", "lab/a.py"]
    assert all(len(record.sha256) == 64 for record in records)


def test_empty_file_is_recorded(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    (root / "docs" / "empty.md").write_text("", encoding="utf-8")
    [record] = scan_files(root)
    assert record.is_empty is True
    assert record.line_count == 0


def test_scanner_is_deterministic(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    (root / "lab" / "z.py").write_text("VALUE = 1\n", encoding="utf-8")
    assert scan_files(root) == scan_files(root)


def test_phase00_implementation_excludes_itself_from_baseline(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    legacy = root / "lab" / "legacy.py"
    legacy.write_text("VALUE = 1\n", encoding="utf-8")
    self_file = root / "lab" / "11_strategy_factory" / "phase00_current_state_audit" / "python" / "audit.py"
    self_file.parent.mkdir(parents=True)
    self_file.write_text("VALUE = 2\n", encoding="utf-8")
    assert [record.path for record in scan_files(root)] == ["lab/legacy.py"]
