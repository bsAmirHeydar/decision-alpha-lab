from pathlib import Path

import yaml

from tools.consolidation.uc02.guard import run_guard
from tools.consolidation.uc02.io_utils import write_jsonl_gz


def _minimal_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    baseline = repo / "registry/consolidation/uc01/baselines/UC01_BASELINE_V1"
    baseline.mkdir(parents=True)
    (repo / "policies/platform").mkdir(parents=True)
    (repo / "README.md").write_text("# test\n", encoding="utf-8")
    write_jsonl_gz(baseline / "artifact_inventory.jsonl.gz", [{"path": "README.md"}])
    policy = {
        "future_allowed_top_level_roots": ["src", "contexts", "adapters", "contracts", "schemas", "policies", "registry", "configs", "mql5", "tests", "docs", "ops", "tools", "products", "examples", "releases", ".github", ".obsidian"],
        "forbidden_new_root_patterns": ["README_*", "INSTALL_*", "ROLLBACK_*", "COMMIT_MESSAGE_*", "*_QA_REPORT.json"],
        "forbidden_new_parallel_engine_patterns": ["strategy_factory_*", "ucee_*", "acl_os_*", "saed_v*", "*_operating_system", "*_engine_v2", "*_engine_v3"],
        "allowed_new_tool_roots": ["tools/consolidation", "tools/engineering", "tools/maintenance"],
    }
    (repo / "policies/platform/root_and_package_guard.yaml").write_text(yaml.safe_dump(policy), encoding="utf-8")
    return repo


def test_guard_passes_for_allowed_target_root(tmp_path: Path) -> None:
    repo = _minimal_repo(tmp_path)
    (repo / "contracts/platform").mkdir(parents=True)
    (repo / "contracts/platform/test.yaml").write_text("x: 1\n", encoding="utf-8")
    result = run_guard(repo)
    assert result["status"] == "PASS", result


def test_guard_rejects_new_root_release_file(tmp_path: Path) -> None:
    repo = _minimal_repo(tmp_path)
    (repo / "README_NEW_ENGINE.md").write_text("bad\n", encoding="utf-8")
    result = run_guard(repo)
    assert result["status"] == "FAILED"
    assert any("root" in error for error in result["errors"])


def test_guard_rejects_new_parallel_engine(tmp_path: Path) -> None:
    repo = _minimal_repo(tmp_path)
    path = repo / "lab/11_strategy_factory/python/strategy_factory_new_engine"
    path.mkdir(parents=True)
    (path / "__init__.py").write_text("", encoding="utf-8")
    result = run_guard(repo)
    assert result["status"] == "FAILED"
    assert any("parallel engine" in error or "under lab" in error for error in result["errors"])


def test_guard_rejects_nested_product_root(tmp_path: Path) -> None:
    repo = _minimal_repo(tmp_path)
    path = repo / "src/alpha_lab"
    path.mkdir(parents=True)
    (path / "__init__.py").write_text("", encoding="utf-8")
    result = run_guard(repo)
    assert result["status"] == "FAILED"
    assert any("nested" in error for error in result["errors"])
