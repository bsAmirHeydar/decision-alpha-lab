from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
TEST_DIR = ROOT / "lab/11_strategy_factory/tests/phase_saed_v4_05_semantic_temporal_hypergraph"
env = {**os.environ, "PYTHONPATH": str(ROOT / "lab/11_strategy_factory/python")}
raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q", str(TEST_DIR)], cwd=ROOT, env=env))
