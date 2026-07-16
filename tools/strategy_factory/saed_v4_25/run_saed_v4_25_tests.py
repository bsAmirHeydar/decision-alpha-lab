from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
environment = dict(os.environ)
python_root = str(ROOT / "lab/11_strategy_factory/python")
environment["PYTHONPATH"] = python_root + (os.pathsep + environment["PYTHONPATH"] if environment.get("PYTHONPATH") else "")
command = [
    sys.executable,
    "-m",
    "pytest",
    "-q",
    str(ROOT / "lab/11_strategy_factory/tests/phase_saed_v4_25_continual_meta_transfer"),
]
raise SystemExit(subprocess.run(command, cwd=ROOT, env=environment).returncode)
