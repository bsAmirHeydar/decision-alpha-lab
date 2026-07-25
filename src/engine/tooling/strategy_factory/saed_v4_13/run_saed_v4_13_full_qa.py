from tools.repository_paths import find_repository_root
from pathlib import Path
import json,subprocess,sys
ROOT=find_repository_root(__file__)
commands=[[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/validate_saed_v4_13_contracts.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/check_saed_v4_13_boundaries.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/validate_saed_v4_13_mql5_static.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/validate_saed_v4_13_obsidian.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/run_saed_v4_13_tests.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/reproduce_saed_v4_13_golden.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_13/validate_saed_v4_13_status.py']]
results=[]
for command in commands:
 r=subprocess.run(command,cwd=ROOT,text=True,capture_output=True);results.append({'command':' '.join([Path(command[0]).name,*command[1:]]),'returncode':r.returncode,'passed':r.returncode==0,'stdout':r.stdout[-6000:],'stderr':r.stderr[-6000:]})
 if r.returncode:break
report={'phase':'SAED_V4_13','version':'1.0.0','passed':len(results)==len(commands) and all(x['passed'] for x in results),'results':results,'evidence_scope':'local_reference_synthetic','external_evidence':{'metaeditor_compile':'pending_local_windows','runtime_parity':'not_claimed','prospective_paper':'not_claimed','shadow':'not_claimed','live':'not_claimed'}}
print(json.dumps(report,indent=2,sort_keys=True));raise SystemExit(0 if report['passed'] else 1)
