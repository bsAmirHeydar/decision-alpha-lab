from pathlib import Path
import os
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
TOOL_ROOT = ROOT / "tools/strategy_factory/saed_v4_26"
PYTHON_ROOT = ROOT / "lab/11_strategy_factory/python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

started = time.time()
import pytest
code = pytest.main([
    "-q",
    str(ROOT / "lab/11_strategy_factory/tests/phase_saed_v4_26_mechanistic_interpretability"),
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
