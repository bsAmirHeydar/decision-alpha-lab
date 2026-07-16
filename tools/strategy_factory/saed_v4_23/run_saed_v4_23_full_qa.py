from pathlib import Path
import subprocess,sys,time
ROOT=Path(__file__).resolve().parents[3]
cmds=[['run_saed_v4_23_tests.py'],['validate_saed_v4_23_contracts.py'],['validate_saed_v4_23_status.py'],['validate_saed_v4_23_obsidian.py'],['validate_saed_v4_23_mql5_static.py'],['check_saed_v4_23_boundaries.py'],['reproduce_saed_v4_23_golden.py']]
started=time.time()
for parts in cmds:
    p=ROOT/'tools/strategy_factory/saed_v4_23'/parts[0];r=subprocess.run([sys.executable,str(p)],cwd=ROOT)
    if r.returncode:raise SystemExit(r.returncode)
print(f'V4-23 full QA passed in {time.time()-started:.2f}s')
