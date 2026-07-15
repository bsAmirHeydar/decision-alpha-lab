from pathlib import Path
import os
import runpy
import sys

ROOT = Path(__file__).resolve().parents[3]
PYTHON_ROOT = ROOT / "lab/11_strategy_factory/python"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))
os.environ["PYTHONPATH"] = str(PYTHON_ROOT)

# Run deterministic artifact reproduction and static validators in-process so
# the aggregate QA entry point is portable across constrained CI runners.
for relative in (
    "tools/strategy_factory/saed_v4_07/reproduce_saed_v4_07_golden.py",
    "tools/strategy_factory/saed_v4_07/validate_saed_v4_07_contracts.py",
    "tools/strategy_factory/saed_v4_07/check_saed_v4_07_boundaries.py",
    "tools/strategy_factory/saed_v4_07/validate_saed_v4_07_obsidian.py",
    "tools/strategy_factory/saed_v4_07/validate_saed_v4_07_mql5_static.py",
):
    try:
        runpy.run_path(str(ROOT / relative), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise

import pytest
exit_code = pytest.main([
    "-q",
    str(ROOT / "lab/11_strategy_factory/tests/phase_saed_v4_07_constraint_solver_action_lattice"),
])
if exit_code:
    raise SystemExit(exit_code)
print("SAED V4-07 full QA passed", flush=True)
