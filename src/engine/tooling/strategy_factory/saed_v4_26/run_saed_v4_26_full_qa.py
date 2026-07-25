from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import runpy
import sys
import time

ROOT = find_repository_root(__file__)
TOOL_ROOT = ROOT / "src/engine/tooling/strategy_factory/saed_v4_26"
PYTHON_ROOT = ROOT / "src/engine/packages"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

started = time.time()
import pytest
code = pytest.main([
    "-q",
    str(ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_26_mechanistic_interpretability"),
])
if code:
    raise SystemExit(code)

for name in [
    "validate_saed_v4_26_contracts.py",
    "validate_saed_v4_26_status.py",
    "validate_saed_v4_26_obsidian.py",
    "validate_saed_v4_26_mql5_static.py",
    "check_saed_v4_26_boundaries.py",
    "reproduce_saed_v4_26_golden.py",
]:
    runpy.run_path(str(TOOL_ROOT / name), run_name="__main__")

print(f"V4-26 full QA passed in {time.time() - started:.2f}s")
