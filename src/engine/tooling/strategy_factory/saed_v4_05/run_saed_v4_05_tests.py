from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import subprocess
import sys

ROOT = find_repository_root(__file__)
TEST_DIR = ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_05_semantic_temporal_hypergraph"
env = {**os.environ, "PYTHONPATH": str(ROOT / "src/engine/packages")}
raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q", str(TEST_DIR)], cwd=ROOT, env=env))
