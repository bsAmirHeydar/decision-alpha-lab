from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess
import sys
import time

ROOT = find_repository_root(__file__)
commands = [
    "run_saed_v4_25_tests.py",
    "validate_saed_v4_25_contracts.py",
    "validate_saed_v4_25_status.py",
    "validate_saed_v4_25_obsidian.py",
    "validate_saed_v4_25_mql5_static.py",
    "check_saed_v4_25_boundaries.py",
    "reproduce_saed_v4_25_golden.py",
]
started = time.time()
for name in commands:
    result = subprocess.run([sys.executable, str(ROOT / "src/engine/tooling/strategy_factory/saed_v4_25" / name)], cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)
print(f"V4-25 full QA passed in {time.time() - started:.2f}s")
