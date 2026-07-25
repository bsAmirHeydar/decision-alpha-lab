from tools.repository_paths import find_repository_root
from pathlib import Path
import json,subprocess,sys
ROOT=find_repository_root(__file__)
commands=[
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/validate_saed_v4_12_contracts.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/check_saed_v4_12_boundaries.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/validate_saed_v4_12_mql5_static.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/validate_saed_v4_12_obsidian.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/run_saed_v4_12_tests.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/reproduce_saed_v4_12_golden.py'],[sys.executable,'src/engine/tooling/strategy_factory/saed_v4_12/validate_saed_v4_12_status.py']]
results=[]
for command in commands:
 r=subprocess.run(command,cwd=ROOT,text=True,capture_output=True);results.append({'command':' '.join([Path(command[0]).name,*command[1:]]),'returncode':r.returncode,'passed':r.returncode==0,'stdout':r.stdout[-4000:],'stderr':r.stderr[-4000:]})
 if r.returncode:break
report={'phase':'SAED_V4_12','version':'1.0.0','passed':len(results)==len(commands) and all(x['passed'] for x in results),'results':results,'evidence_scope':'local_reference_synthetic','schema_pair_count':43,'obsidian_note_count':97,'mql5_static_file_count':10,'external_evidence':{'real_corpus_training':'not_claimed','gpu_reproduction':'not_claimed','distributed_training':'not_claimed','metaeditor_compile':'pending_local_windows','runtime_parity':'not_claimed','prospective_paper':'not_claimed','shadow':'not_claimed','live':'not_claimed'}}
(ROOT/'releases/history/saed/reports/SAED_V4_12_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
raise SystemExit(0 if report['passed'] else 1)
