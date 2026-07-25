from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys,time
ROOT=find_repository_root(__file__)
cmds=[['run_saed_v4_23_tests.py'],['validate_saed_v4_23_contracts.py'],['validate_saed_v4_23_status.py'],['validate_saed_v4_23_obsidian.py'],['validate_saed_v4_23_mql5_static.py'],['check_saed_v4_23_boundaries.py'],['reproduce_saed_v4_23_golden.py']]
started=time.time()
for parts in cmds:
    p=ROOT/'src/engine/tooling/strategy_factory/saed_v4_23'/parts[0];r=subprocess.run([sys.executable,str(p)],cwd=ROOT)
    if r.returncode:raise SystemExit(r.returncode)
print(f'V4-23 full QA passed in {time.time()-started:.2f}s')
