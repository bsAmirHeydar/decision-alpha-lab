from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,subprocess,sys,time
from pathlib import Path
ROOT=find_repository_root(__file__);started=time.time();cmds=[
 [sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_38_immutable_runtime_mql5_parity'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_38/validate_contracts.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_38/validate_mql5_static.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_38/validate_authority.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_38/validate_runtime_bundle.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_38/validate_external_evidence_separation.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_38/validate_docs.py']]
results=[]
for cmd in cmds:
 p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);results.append({'command':' '.join(cmd),'returncode':p.returncode,'stdout':p.stdout[-6000:],'stderr':p.stderr[-6000:]})
 if p.returncode:print(p.stdout);print(p.stderr,file=sys.stderr);raise SystemExit(p.returncode)
report={'phase':'SAED_V4_38','passed':True,'duration_seconds':round(time.time()-started,3),'results':results,'claim_ceiling':'immutable runtime compilation and synthetic MQL5 semantic parity reference only; actual MetaEditor and terminal evidence pending','metaeditor_compile':'pending_external','terminal_parity':'pending_external','production_authorized':False}
(ROOT/'releases/history/saed/reports/SAED_V4_38_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');(ROOT/'releases/history/strategy_factory/program/status/SAED_V4_38.json').write_text(json.dumps({'phase':'SAED_V4_38','status':'accepted_reference_external_gates_open','qa_passed':True,'metaeditor_compile':'pending_external','terminal_parity':'pending_external','production_authorized':False},indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))
