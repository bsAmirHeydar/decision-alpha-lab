from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
commands=[[sys.executable,'tools/strategy_factory/saed_v4_19/validate_saed_v4_19_contracts.py'],[sys.executable,'tools/strategy_factory/saed_v4_19/check_saed_v4_19_boundaries.py'],[sys.executable,'tools/strategy_factory/saed_v4_19/validate_saed_v4_19_mql5_static.py'],[sys.executable,'tools/strategy_factory/saed_v4_19/validate_saed_v4_19_obsidian.py'],[sys.executable,'tools/strategy_factory/saed_v4_19/run_saed_v4_19_tests.py'],[sys.executable,'tools/strategy_factory/saed_v4_19/reproduce_saed_v4_19_golden.py'],[sys.executable,'tools/strategy_factory/saed_v4_19/validate_saed_v4_19_status.py']]
results=[]
for command in commands:
 r=subprocess.run(command,cwd=ROOT,text=True,capture_output=True);results.append({'command':' '.join([Path(command[0]).name,*command[1:]]),'returncode':r.returncode,'passed':r.returncode==0,'stdout':r.stdout[-30000:],'stderr':r.stderr[-30000:]})
 if r.returncode:break
report={'phase':'SAED_V4_19','version':'1.0.0','passed':len(results)==len(commands) and all(x['passed'] for x in results),'results':results,'evidence_scope':'local_deterministic_synthetic_reference','external_evidence':{'real_data_setup_validity':'not_claimed','real_mechanism':'not_claimed','real_policy_value':'not_claimed','protected_final_evaluation':'not_claimed','independent_external_replication':'not_claimed','metaeditor_compile':'pending_local_windows','runtime_differential_parity':'not_claimed','prospective_paper':'not_claimed','shadow':'not_claimed','micro_live':'not_claimed','live':'not_claimed'}}
print(json.dumps(report,indent=2,sort_keys=True));raise SystemExit(0 if report['passed'] else 1)
