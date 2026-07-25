#!/usr/bin/env python3
"""Audit active Alpha Lab repository topology across consolidation stages."""
from __future__ import annotations

import json
import sys
from pathlib import Path

LEGACY_EXPECTED = (
    "docs", "lab/01_observation", "lab/02_hypotheses", "lab/03_experiments",
    "lab/04_analysis", "lab/05_validation", "lab/06_production",
    "lab/07_monitoring", "lab/08_archive", "lab/09_execution",
    "lab/10_infrastructure", "registry", "data",
)
UC03_PART1_EXPECTED = (
    "src/engine", "contexts", "adapters", "contracts", "schemas", "policies",
    "registry", "configs", "mql5", "tests", "docs", "ops", "tools", "products",
    "examples", "releases/history",
)
UC03_PART2_EXPECTED = (
    "src/engine/packages", "src/engine/legacy", "src/engine/tooling/strategy_factory",
    "contexts/legacy", "tests/legacy", "mql5/legacy/strategy_factory_lab",
)
ROOT_ALLOWLIST = {
    ".editorconfig", ".gitattributes", ".gitignore", "AGENTS.md",
    "CODE_OF_CONDUCT.md", "COMMIT_MESSAGE.md", "COMMIT_MESSAGE.txt",
    "CONTRIBUTING.md", "FILE_INDEX.txt", "LICENSE", "PATCH_MANIFEST.json",
    "QA_REPORT.json", "README.md", "requirements.txt", "sitecustomize.py",
}


def _accepted(root: Path, relative: str, part_id: str) -> bool:
    receipt = root / relative
    if not receipt.is_file():
        return False
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
    except Exception:
        return False
    return data.get("status") == "ACCEPTED" and data.get("part_id") == part_id


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    part1 = _accepted(root, "registry/consolidation/uc03/part1/part1_exit_decision.json", "UC03-P1")
    part2 = _accepted(root, "registry/consolidation/uc03/part2/part2_exit_decision.json", "UC03-P2")

    if part2:
        expected = tuple(dict.fromkeys(UC03_PART1_EXPECTED + UC03_PART2_EXPECTED))
        mode = "UC03-P2"
    elif part1:
        expected = tuple(dict.fromkeys(LEGACY_EXPECTED + UC03_PART1_EXPECTED))
        mode = "UC03-P1"
    else:
        expected = LEGACY_EXPECTED
        mode = "PRE-UC03"

    missing = [relative for relative in expected if not (root / relative).is_dir()]
    errors = [f"missing expected directory: {relative}" for relative in missing]

    root_files = sorted(path.name for path in root.iterdir() if path.is_file())
    if part1 or part2:
        unexpected = sorted(set(root_files) - ROOT_ALLOWLIST)
        if unexpected:
            errors.append(f"root contains non-allowlisted files: {unexpected}")
        if len(root_files) > 20:
            errors.append(f"root file limit exceeded: {len(root_files)} > 20")

    if part2:
        lab = root / "lab"
        lab_files = [path for path in lab.rglob("*") if path.is_file()] if lab.exists() else []
        if lab_files:
            errors.append(f"lab still contains {len(lab_files)} files")
        strategy_factory = root / "tools/strategy_factory"
        unexpected_tool_files = []
        if strategy_factory.exists():
            unexpected_tool_files = [
                path.relative_to(strategy_factory).as_posix()
                for path in strategy_factory.rglob("*")
                if path.is_file() and "__pycache__" not in path.parts and path.name != "__init__.py"
            ]
        if unexpected_tool_files:
            errors.append(f"tools/strategy_factory contains production files: {unexpected_tool_files[:10]}")

    print(f"Root: {root}")
    print(f"Consolidation mode: {mode}")
    print(f"Missing expected directories: {len(missing)}")
    print(f"Root files: {len(root_files)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print("ERROR:", error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
