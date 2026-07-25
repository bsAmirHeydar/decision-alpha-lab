from tools.repository_paths import find_repository_root
from pathlib import Path
import os
import subprocess
import sys

ROOT = find_repository_root(__file__)
environment = dict(os.environ)
python_root = str(ROOT / "src/engine/packages")
environment["PYTHONPATH"] = python_root + (os.pathsep + environment["PYTHONPATH"] if environment.get("PYTHONPATH") else "")
command = [
    sys.executable,
    "-m",
    "pytest",
    "-q",
    str(ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_25_continual_meta_transfer"),
]
raise SystemExit(subprocess.run(command, cwd=ROOT, env=environment).returncode)
