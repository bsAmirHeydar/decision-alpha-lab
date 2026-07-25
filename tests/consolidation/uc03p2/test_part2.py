from __future__ import annotations

import json
from pathlib import Path

from tools.consolidation.uc03p2.apply import apply
from tools.consolidation.uc03p2.verify import verify


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "registry/consolidation/uc03/part1").mkdir(parents=True)
    (repo / "registry/consolidation/uc03/part1/part1_exit_decision.json").write_text(
        json.dumps({"status": "ACCEPTED", "part_id": "UC03-P1", "uc03_part2_authorized": True}),
        encoding="utf-8",
    )
    (repo / "releases/unified_consolidation/uc03/part2").mkdir(parents=True)
    (repo / "releases/unified_consolidation/uc03/part2/STATIC_PATCH_FILE_INDEX.txt").write_text(
        "sitecustomize.py\n", encoding="utf-8"
    )
    (repo / "README.md").write_text("Alpha Lab\n", encoding="utf-8")
    (repo / "sitecustomize.py").write_text("# test\n", encoding="utf-8")
    (repo / "tools/consolidation/uc03p2").mkdir(parents=True)
    (repo / "tools/consolidation/uc03p2/__init__.py").write_text("", encoding="utf-8")
    (repo / "tools/repository_paths.py").write_text(
        "from pathlib import Path\ndef find_repository_root(x): return Path(x).resolve().parents[2]\n",
        encoding="utf-8",
    )
    return repo


def test_moves_code_and_creates_shim(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    source = repo / "tools/strategy_factory/lcm/module.py"
    source.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    package = repo / "lab/11_strategy_factory/python/example_package/__init__.py"
    package.parent.mkdir(parents=True)
    package.write_text("VALUE = 2\n", encoding="utf-8")

    result = apply(repo)

    assert result["status"] == "PASS"
    assert (repo / "src/engine/tooling/strategy_factory/lcm/module.py").is_file()
    assert (repo / "src/engine/packages/example_package/__init__.py").is_file()
    assert (repo / "tools/strategy_factory/__init__.py").is_file()


def test_apply_is_idempotent(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    source = repo / "lab/core/CP0000_sample/sample.py"
    source.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    first = apply(repo)
    second = apply(repo)
    assert first["status"] == "PASS"
    assert second["status"] == "PASS"
    assert (repo / "src/engine/legacy/core/CP0000_sample/sample.py").is_file()


def test_preserves_destination_conflict(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    source = repo / "lab/core/CP0000_sample/sample.py"
    destination = repo / "src/engine/legacy/core/CP0000_sample/sample.py"
    source.parent.mkdir(parents=True)
    destination.parent.mkdir(parents=True)
    source.write_text("SOURCE = 1\n", encoding="utf-8")
    destination.write_text("DESTINATION = 1\n", encoding="utf-8")

    result = apply(repo)

    assert result["conflict_count"] == 1
    assert destination.read_text(encoding="utf-8") == "SOURCE = 1\n"
    assert list((repo / "releases/history/conflicts/uc03_part2").rglob("sample__*.py"))


def test_rewrites_depth_coupled_root(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    source = repo / "lab/core/module.py"
    source.parent.mkdir(parents=True)
    # /repo/lab/core/module.py -> parents[2] is /repo
    source.write_text(
        "from pathlib import Path\nROOT = Path(__file__).resolve().parents[2]\n",
        encoding="utf-8",
    )

    apply(repo)

    text = (repo / "src/engine/legacy/core/module.py").read_text(encoding="utf-8")
    assert "find_repository_root(__file__)" in text
    assert "from tools.repository_paths import find_repository_root" in text


def test_exit_does_not_authorize_uc04(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    apply(repo)
    decision = json.loads(
        (repo / "registry/consolidation/uc03/part2/part2_exit_decision.json").read_text(encoding="utf-8")
    )
    assert decision["status"] == "ACCEPTED"
    assert decision["uc03_part3_authorized"] is True
    assert decision["uc04_authorized"] is False


def test_git_index_is_built_from_runtime_changes(tmp_path: Path) -> None:
    import subprocess

    repo = _repo(tmp_path)
    source = repo / "lab/core/sample.py"
    source.parent.mkdir(parents=True)
    source.write_text("VALUE = 1\n", encoding="utf-8")
    subprocess.run(["git", "init"], cwd=repo, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "baseline"], cwd=repo, check=True, stdout=subprocess.DEVNULL)

    apply(repo)

    index = (repo / "releases/unified_consolidation/uc03/part2/PATCH_FILE_INDEX.txt").read_text(encoding="utf-8").splitlines()
    assert "lab/core/sample.py" in index
    assert "src/engine/legacy/core/sample.py" in index
