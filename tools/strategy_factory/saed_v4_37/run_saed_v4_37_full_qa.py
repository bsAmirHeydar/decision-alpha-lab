from __future__ import annotations
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; started=time.time(); commands=[
 [sys.executable,'-m','pytest','-q','lab/11_strategy_factory/tests/phase_saed_v4_37_portfolio_execution_economics'],
 [sys.executable,'tools/strategy_factory/saed_v4_37/validate_contracts.py'],
 [sys.executable,'tools/strategy_factory/saed_v4_37/validate_mql5_static.py'],
 [sys.executable,'tools/strategy_factory/saed_v4_37/validate_docs.py'],
 [sys.executable,'tools/strategy_factory/saed_v4_37/validate_authority.py']]
results=[]
for cmd in commands:
 p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True); results.append({'command':' '.join(cmd),'returncode':p.returncode,'stdout':p.stdout[-4000:],'stderr':p.stderr[-4000:]})
 if p.returncode: print(p.stdout); print(p.stderr,file=sys.stderr); raise SystemExit(p.returncode)
report={'phase':'SAED_V4_37','passed':True,'duration_seconds':round(time.time()-started,3),'results':results,'claim_ceiling':'synthetic deterministic portfolio execution economics reference only','production_authorized':False}
(ROOT/'SAED_V4_37_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n'); (ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_37.json').write_text(json.dumps({'phase':'SAED_V4_37','status':'accepted_reference','qa_passed':True,'production_authorized':False},indent=2,sort_keys=True)+'\n'); print(json.dumps(report,indent=2))
