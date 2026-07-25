from tools.repository_paths import find_repository_root
from pathlib import Path
import json,subprocess,sys
ROOT=find_repository_root(__file__)
commands=[[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/validate_saed_v4_17_contracts.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/check_saed_v4_17_boundaries.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/validate_saed_v4_17_mql5_static.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/validate_saed_v4_17_obsidian.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/run_saed_v4_17_tests.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/reproduce_saed_v4_17_golden.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_17/validate_saed_v4_17_status.py']]
results=[]
for command in commands:
 r=subprocess.run(command,cwd=ROOT,text=True,capture_output=True);results.append({'command':' '.join([Path(command[0]).name,*command[1:]]),'returncode':r.returncode,'passed':r.returncode==0,'stdout':r.stdout[-20000:],'stderr':r.stderr[-20000:]})
 if r.returncode:break
report={'phase':'SAED_V4_17','version':'1.0.0','passed':len(results)==len(commands) and all(x['passed'] for x in results),'results':results,'evidence_scope':'local_deterministic_synthetic_reference','external_evidence':{'real_causal_discovery':'not_claimed','real_treatment_effect':'not_claimed','protected_final_evaluation':'not_claimed','independent_external_replication':'not_claimed','metaeditor_compile':'pending_local_windows','runtime_differential_parity':'not_claimed','prospective_paper':'not_claimed','shadow':'not_claimed','micro_live':'not_claimed','live':'not_claimed'}}
print(json.dumps(report,indent=2,sort_keys=True));raise SystemExit(0 if report['passed'] else 1)
