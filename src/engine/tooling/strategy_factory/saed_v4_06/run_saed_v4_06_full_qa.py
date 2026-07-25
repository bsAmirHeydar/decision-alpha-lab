from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import subprocess
import sys

ROOT = find_repository_root(__file__)
commands = (
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_06/run_saed_v4_06_tests.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_06/validate_saed_v4_06_contracts.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_06/check_saed_v4_06_boundaries.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_06/validate_saed_v4_06_obsidian.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_06/validate_saed_v4_06_mql5_static.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_06/reproduce_saed_v4_06_golden.py"],
)
env = {**os.environ, "PYTHONPATH": str(ROOT / "src/engine/packages")}
for command in commands:
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False, timeout=120)
    if completed.returncode:
        raise SystemExit(completed.returncode)
print("SAED V4-06 full QA passed", flush=True)
