from tools.repository_paths import find_repository_root
from pathlib import Path
import os,subprocess,sys
ROOT=find_repository_root(__file__)
env={**os.environ,'PYTHONPATH':str(ROOT/'src/engine/packages')}
cmd=[sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_07_constraint_solver_action_lattice']
r=subprocess.run(cmd,cwd=ROOT,env=env,check=False,timeout=180);raise SystemExit(r.returncode)
