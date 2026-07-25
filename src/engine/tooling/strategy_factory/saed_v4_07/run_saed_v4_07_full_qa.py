from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import runpy
import sys

ROOT = find_repository_root(__file__)
PYTHON_ROOT = ROOT / "src/engine/packages"
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))
os.environ["PYTHONPATH"] = str(PYTHON_ROOT)

# Run deterministic artifact reproduction and static validators in-process so
# the aggregate QA entry point is portable across constrained CI runners.
for relative in (
    "src/engine/tooling/strategy_factory/saed_v4_07/reproduce_saed_v4_07_golden.py",
    "src/engine/tooling/strategy_factory/saed_v4_07/validate_saed_v4_07_contracts.py",
    "src/engine/tooling/strategy_factory/saed_v4_07/check_saed_v4_07_boundaries.py",
    "src/engine/tooling/strategy_factory/saed_v4_07/validate_saed_v4_07_obsidian.py",
    "src/engine/tooling/strategy_factory/saed_v4_07/validate_saed_v4_07_mql5_static.py",
):
    try:
        runpy.run_path(str(ROOT / relative), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise

import pytest
exit_code = pytest.main([
    "-q",
    str(ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_07_constraint_solver_action_lattice"),
])
if exit_code:
    raise SystemExit(exit_code)
print("SAED V4-07 full QA passed", flush=True)
