from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parents[3]
scripts=['run_saed_v4_22_tests.py','validate_saed_v4_22_contracts.py','validate_saed_v4_22_status.py','validate_saed_v4_22_obsidian.py','validate_saed_v4_22_mql5_static.py','check_saed_v4_22_boundaries.py','reproduce_saed_v4_22_golden.py']
rows=[]
for s in scripts:
    p=subprocess.run([sys.executable,str(Path(__file__).parent/s)],cwd=ROOT,text=True,capture_output=True)
    rows.append({'script':s,'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()})
    if p.returncode:print(json.dumps({'passed':False,'rows':rows},indent=2));raise SystemExit(p.returncode)
print(json.dumps({'passed':True,'checks':len(rows),'rows':rows},indent=2,sort_keys=True))
