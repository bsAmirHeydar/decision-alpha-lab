from pathlib import Path

from tools.consolidation.uc02.verify import verify_static_patch


def test_static_release_verifies(repo_root: Path) -> None:
    result = verify_static_patch(repo_root)
    assert result["status"] == "PASS", result
    assert result["path_count"] >= 40
