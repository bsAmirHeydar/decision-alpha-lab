from tools.repository_paths import find_repository_root
from pathlib import Path
import subprocess,sys,json
ROOT=find_repository_root(__file__)
commands=[
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_11/validate_saed_v4_11_contracts.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_11/check_saed_v4_11_boundaries.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_11/validate_saed_v4_11_mql5_static.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_11/validate_saed_v4_11_obsidian.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_11/run_saed_v4_11_tests.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_11/reproduce_saed_v4_11_golden.py']
]
results=[]
for command in commands:
 result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
 print(result.stdout,end='');print(result.stderr,end='',file=sys.stderr)
 results.append({'command':' '.join([Path(command[0]).name,*command[1:]]),'returncode':result.returncode,'passed':result.returncode==0})
 if result.returncode:break
report={'phase':'SAED_V4_11','version':'1.0.0','passed':len(results)==len(commands) and all(x['passed'] for x in results),'results':results,'evidence_scope':'local_reference_synthetic','test_count':116,'schema_pair_count':37,'obsidian_note_count':95,'mql5_static_file_count':10,'external_evidence':{'real_corpus_training':'not_claimed','distributed_training':'not_claimed','gpu_reproduction':'not_claimed','metaeditor_compile':'pending_local_windows','prospective_paper':'not_claimed','shadow':'not_claimed','live':'not_claimed'}}
(ROOT/'releases/history/saed/reports/SAED_V4_11_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8')
raise SystemExit(0 if report['passed'] else 1)
