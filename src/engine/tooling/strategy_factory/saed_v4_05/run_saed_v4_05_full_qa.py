from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import subprocess
import sys

ROOT = find_repository_root(__file__)
commands = (
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_05/run_saed_v4_05_tests.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_05/validate_saed_v4_05_contracts.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_05/check_saed_v4_05_boundaries.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_05/validate_saed_v4_05_obsidian.py"],
    [sys.executable, "src/engine/tooling/strategy_factory/saed_v4_05/validate_saed_v4_05_mql5_static.py"],
)
env = {**os.environ, "PYTHONPATH": str(ROOT / "src/engine/packages")}
for command in commands:
    result = subprocess.call(command, cwd=ROOT, env=env)
    if result:
        raise SystemExit(result)
print("SAED V4-05 full QA passed")
