from __future__ import annotations
import os
import subprocess
import sys
from _common import ROOT, PY_ROOT
env = dict(os.environ)
env["PYTHONPATH"] = str(PY_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
raise SystemExit(subprocess.call([
    sys.executable, "-m", "pytest", "-q",
    str(ROOT / "tests/legacy/strategy_factory/v1/phase_saed_v4_32_multi_agent_research_constitution")
], cwd=ROOT, env=env))
