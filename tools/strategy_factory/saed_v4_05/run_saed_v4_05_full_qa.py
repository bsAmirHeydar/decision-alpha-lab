from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
commands = (
    [sys.executable, "tools/strategy_factory/saed_v4_05/run_saed_v4_05_tests.py"],
    [sys.executable, "tools/strategy_factory/saed_v4_05/validate_saed_v4_05_contracts.py"],
    [sys.executable, "tools/strategy_factory/saed_v4_05/check_saed_v4_05_boundaries.py"],
    [sys.executable, "tools/strategy_factory/saed_v4_05/validate_saed_v4_05_obsidian.py"],
    [sys.executable, "tools/strategy_factory/saed_v4_05/validate_saed_v4_05_mql5_static.py"],
)
env = {**os.environ, "PYTHONPATH": str(ROOT / "lab/11_strategy_factory/python")}
for command in commands:
    result = subprocess.call(command, cwd=ROOT, env=env)
    if result:
        raise SystemExit(result)
print("SAED V4-05 full QA passed")
