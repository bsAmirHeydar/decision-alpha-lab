from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any


def _run(command: list[str], cwd: Path, timeout: int = 120) -> dict[str, Any]:
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            env={**os.environ, "PYTHONHASHSEED": "0"},
            check=False,
        )
        output = (process.stdout + "\n" + process.stderr).strip()
        return {
            "command": command,
            "return_code": process.returncode,
            "passed": process.returncode == 0,
            "output": output[-12000:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "command": command,
            "return_code": None,
            "passed": False,
            "output": f"{type(exc).__name__}: {exc}",
        }


def collect_test_baseline(repo_root: Path, run_pytest: bool = True) -> dict[str, Any]:
    baseline: dict[str, Any] = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "compileall": _run([sys.executable, "-m", "compileall", "-q", "lab"], repo_root),
    }
    baseline["pytest"] = (
        _run([sys.executable, "-m", "pytest", "-q"], repo_root)
        if run_pytest
        else {"skipped": True, "reason": "run_pytest disabled"}
    )
    return baseline
