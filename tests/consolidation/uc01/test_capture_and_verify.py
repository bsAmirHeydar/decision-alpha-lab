from pathlib import Path

from tools.consolidation.uc01.capture import capture_baseline
from tools.consolidation.uc01.verify import verify_baseline


def _minimal_static_index(repo: Path) -> None:
    release = repo / "releases" / "unified_consolidation" / "uc01"
    release.mkdir(parents=True)
    (release / "UC01_PATCH_FILE_INDEX.txt").write_text("releases/unified_consolidation/uc01/UC01_PATCH_FILE_INDEX.txt\n", encoding="utf-8")


def test_capture_is_complete_and_non_destructive(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _minimal_static_index(repo)
    source = repo / "tools" / "context_engine.py"
    test = repo / "tests" / "test_context_engine.py"
    source.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    source.write_text("def context_identity(value):\n    return value\n", encoding="utf-8")
    test.write_text("def test_context_identity():\n    assert True\n", encoding="utf-8")
    baseline = repo / "registry" / "consolidation" / "uc01" / "baselines" / "UC01_BASELINE_V1"
    result = capture_baseline(repo, baseline)
    assert result["status"] == "CAPTURED"
    assert source.read_text(encoding="utf-8").startswith("def context_identity")
    verified = verify_baseline(repo, baseline)
    assert verified["status"] == "PASS"


def test_capture_refuses_to_overwrite_immutable_baseline(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _minimal_static_index(repo)
    (repo / "x.txt").write_text("x", encoding="utf-8")
    baseline = repo / "registry" / "consolidation" / "uc01" / "baselines" / "UC01_BASELINE_V1"
    capture_baseline(repo, baseline)
    try:
        capture_baseline(repo, baseline)
    except FileExistsError:
        pass
    else:  # pragma: no cover
        raise AssertionError("immutable baseline overwrite was accepted")
