from pathlib import Path

from tools.consolidation.uc01.capture import capture_artifacts, resume_capture
from tools.consolidation.uc01.io_utils import read_json


def _index(repo: Path) -> None:
    release = repo / "releases/unified_consolidation/uc01"
    release.mkdir(parents=True)
    (release / "UC01_PATCH_FILE_INDEX.txt").write_text(
        "releases/unified_consolidation/uc01/UC01_PATCH_FILE_INDEX.txt\n",
        encoding="utf-8",
    )


def test_resume_reuses_completed_artifact_step(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _index(repo)
    (repo / "module.py").write_text("def identity(x):\n    return x\n", encoding="utf-8")
    baseline = repo / "registry/consolidation/uc01/baselines/UC01_BASELINE_V1"
    baseline.mkdir(parents=True)
    first = capture_artifacts(repo, baseline)
    result = resume_capture(repo, baseline)
    assert first["file_count"] == 2
    assert result["steps"]["artifacts"]["status"] == "REUSED"
    state = read_json(baseline / "capture_state.json")
    assert state["steps"]["assemble"]["status"] == "PASS"


def test_capture_state_contains_all_resumable_steps(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _index(repo)
    (repo / "module.py").write_text("def market_clock():\n    return 1\n", encoding="utf-8")
    baseline = repo / "registry/consolidation/uc01/baselines/UC01_BASELINE_V1"
    baseline.mkdir(parents=True)
    resume_capture(repo, baseline)
    state = read_json(baseline / "capture_state.json")
    assert set(state["steps"]) == {"artifacts", "python", "mql5", "documents", "references", "assemble"}
