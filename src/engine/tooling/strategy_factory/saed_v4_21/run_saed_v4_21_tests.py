from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys,json,re
ROOT=find_repository_root(__file__)
r=subprocess.run([sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_21_robust_optimization_regret'],cwd=ROOT,text=True,capture_output=True)
print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr)
if r.returncode:raise SystemExit(r.returncode)
m=re.search(r'(\d+) passed',r.stdout);print(json.dumps({'passed':True,'python_tests':int(m.group(1)) if m else 0},sort_keys=True))
