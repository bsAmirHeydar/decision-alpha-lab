from pathlib import Path

from tools.consolidation.ci.verify_migration_continuity import verify


def test_current_migration_continuity() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    result = verify(repo_root)
    assert result["status"] == "PASS", result
    assert result["relocation_count"] > 0
    assert result["rewrite_file_count"] > 0
    assert result["verified_amendment_path_count"] > 0
