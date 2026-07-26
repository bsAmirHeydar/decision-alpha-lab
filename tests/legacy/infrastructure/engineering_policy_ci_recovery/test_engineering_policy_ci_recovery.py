from __future__ import annotations
from tools.repository_paths import find_repository_root

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = find_repository_root(__file__)
RUNNER_PATH = REPO_ROOT / "tools/engineering/run_engineering_policy.py"
POLICY_PATH = REPO_ROOT / "tools/engineering/validate_alpha_lab_policy.py"
CANONICAL_VAULT = "docs/architecture/master/ai_algorithm_engineering_os"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_preflight_runs_the_canonical_vault_validator() -> None:
    runner = load_module("engineering_policy_runner", RUNNER_PATH)
    obsidian = next(
        check
        for check in runner._checks(sys.executable)
        if check.name == "Obsidian operating system"
    )
    assert obsidian.command == (
        sys.executable,
        f"{CANONICAL_VAULT}/tools/validate_vault.py",
        CANONICAL_VAULT,
    )

    code, output = runner._run(obsidian, REPO_ROOT)
    assert code == 0, output
    assert "Errors: 0" in output
    assert "Warnings: 0" in output


def test_repository_policy_requires_canonical_entry_points() -> None:
    policy = load_module("alpha_lab_policy_validator", POLICY_PATH)
    canonical_prefix = f"{CANONICAL_VAULT}/"
    legacy_prefix = "docs/history/aieos_legacy/"
    required_vault_paths = [
        path for path in policy.REQUIRED if "ai_algorithm_engineering_os" in path
    ]
    assert len(required_vault_paths) == 4
    assert all(path.startswith(canonical_prefix) for path in required_vault_paths)
    assert not any(path.startswith(legacy_prefix) for path in policy.REQUIRED)


def test_workflow_uses_node24_action_majors() -> None:
    workflow = (
        REPO_ROOT / ".github/workflows/engineering-policy.yml"
    ).read_text(encoding="utf-8")
    assert "uses: actions/checkout@v5" in workflow
    assert "uses: actions/setup-python@v6" in workflow
    assert "uses: actions/checkout@v4" not in workflow
    assert "uses: actions/setup-python@v5" not in workflow
