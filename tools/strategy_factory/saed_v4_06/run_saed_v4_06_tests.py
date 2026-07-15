from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
test_root = ROOT / "lab/11_strategy_factory/tests/phase_saed_v4_06_treatment_dsl"
env = {**os.environ, "PYTHONPATH": str(ROOT / "lab/11_strategy_factory/python")}
raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q", str(test_root)], cwd=ROOT, env=env))
