from pathlib import Path

from tools.consolidation.uc03p3.apply import rewrite_active_files


def test_rewrite_updates_paths_and_imports(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    target = tmp_path / "src" / "probe.py"
    target.write_text(
        "from tools.strategy_factory import acl_os\n"
        "PATH = 'docs/alpha_lab_master_architecture/00_START_HERE/00_Home.md'\n",
        encoding="utf-8",
    )
    rows, count = rewrite_active_files(tmp_path)
    text = target.read_text(encoding="utf-8")
    assert "src.engine.tooling.strategy_factory" in text
    assert "docs/architecture/master" in text
    assert count == 2
    assert len(rows) == 1
