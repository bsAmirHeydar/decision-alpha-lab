"""Capture deterministic qualification command receipts without hiding failures."""
from __future__ import annotations

import sys
import time
from pathlib import Path

from .git_utils import run_command


def run_qualification(repo_root: Path, *, include_full_regression: bool = True) -> dict:
    commands: list[tuple[str, tuple[str, ...], int]] = [
        ("uc01_direct_tests", (sys.executable, "-m", "pytest", "-q", "tests/consolidation/uc01"), 600),
        ("engineering_policy", (sys.executable, "tools/engineering/run_engineering_policy.py"), 1200),
    ]
    if include_full_regression and (repo_root / "tools/strategy_factory/lcm/lcm_16a/regression.py").is_file():
        commands.append((
            "lcm16a_full_regression",
            (
                sys.executable, "-m", "tools.strategy_factory.lcm.lcm_16a.regression",
                "--repo-root", ".",
                "--output", str((repo_root / "registry/consolidation/uc01/baselines/UC01_BASELINE_V1/lcm16a_regression_receipt.json").resolve()),
            ),
            3600,
        ))
    rows = []
    for name, command, timeout in commands:
        started = time.time()
        result = run_command(command, repo_root, timeout=timeout)
        rows.append({
            "name": name,
            "command": list(command),
            "returncode": result.returncode,
            "duration_seconds": round(time.time() - started, 3),
            "output": result.stdout[-100000:],
            "status": "PASS" if result.returncode == 0 else "FAILED",
        })
    return {
        "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAILED",
        "commands": rows,
        "full_regression_requested": include_full_regression,
    }
