from pathlib import Path
import os,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
env={**os.environ,'PYTHONPATH':str(ROOT/'lab/11_strategy_factory/python')}
cmd=[sys.executable,'-m','pytest','-q','lab/11_strategy_factory/tests/phase_saed_v4_07_constraint_solver_action_lattice']
r=subprocess.run(cmd,cwd=ROOT,env=env,check=False,timeout=180);raise SystemExit(r.returncode)
