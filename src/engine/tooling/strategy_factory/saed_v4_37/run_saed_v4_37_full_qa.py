from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,subprocess,sys,time
from pathlib import Path
ROOT=find_repository_root(__file__); started=time.time(); commands=[
 [sys.executable,'-m','pytest','-q','tests/legacy/strategy_factory/v1/phase_saed_v4_37_portfolio_execution_economics'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_37/validate_contracts.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_37/validate_mql5_static.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_37/validate_docs.py'],
 [sys.executable,'src/engine/tooling/strategy_factory/saed_v4_37/validate_authority.py']]
results=[]
for cmd in commands:
 p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True); results.append({'command':' '.join(cmd),'returncode':p.returncode,'stdout':p.stdout[-4000:],'stderr':p.stderr[-4000:]})
 if p.returncode: print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(p.returncode)
report={'phase':'SAED_V4_37','passed':True,'duration_seconds':round(time.time()-started,3),'results':results,'claim_ceiling':'synthetic deterministic portfolio execution economics reference only','production_authorized':False}
(ROOT/'releases/history/saed/reports/SAED_V4_37_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); (ROOT/'releases/history/strategy_factory/program/status/SAED_V4_37.json').write_text(json.dumps({'phase':'SAED_V4_37','status':'accepted_reference','qa_passed':True,'production_authorized':False},indent=2,sort_keys=True)+'\n'); print(json.dumps(report,indent=2))
