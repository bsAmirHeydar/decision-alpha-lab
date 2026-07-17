from __future__ import annotations
import os
import subprocess
import sys
from _common import ROOT, PY_ROOT
env = dict(os.environ)
env["PYTHONPATH"] = str(PY_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
raise SystemExit(subprocess.call([
    sys.executable, "-m", "pytest", "-q",
    str(ROOT / "lab/11_strategy_factory/tests/phase_saed_v4_32_multi_agent_research_constitution")
], cwd=ROOT, env=env))
