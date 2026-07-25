from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import subprocess
import sys

ROOT = find_repository_root(__file__)
test_root = ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_06_treatment_dsl"
env = {**os.environ, "PYTHONPATH": str(ROOT / "src/engine/packages")}
raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q", str(test_root)], cwd=ROOT, env=env))
