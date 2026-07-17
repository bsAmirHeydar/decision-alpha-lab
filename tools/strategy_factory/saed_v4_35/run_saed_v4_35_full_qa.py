from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];TOOLS=Path(__file__).resolve().parent
commands=[
 [sys.executable,'-m','pytest','-q',str(ROOT/'lab/11_strategy_factory/tests/phase_saed_v4_35_model_risk_supply_chain')],
 [sys.executable,str(TOOLS/'validate_contract_closure.py')],
 [sys.executable,str(TOOLS/'validate_authority_boundary.py')],
 [sys.executable,str(TOOLS/'validate_obsidian.py')],
 [sys.executable,str(TOOLS/'validate_mql5_static.py')]]
summary=[]
for cmd in commands:
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr);summary.append({'command':' '.join(cmd),'returncode':r.returncode});
 if r.returncode:raise SystemExit(r.returncode)
report={'phase':'SAED_V4_35','version':'1.0.0','passed':True,'checks':summary,'contract_pairs':46,'mql5_evidence':'static_only','external_signature_verification':False,'external_scanner_attestation':False,'external_build_reproduction':False,'metaeditor_compile':'pending_local_windows','runtime_parity':False,'production_authorization':False,'claim_ceiling':'synthetic_deterministic_reference_only'}
(ROOT/'SAED_V4_35_QA_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');status={'phase':'SAED_V4_35','title':'Model Risk and Supply Chain','version':'1.0.0','status':'accepted-reference','qa_passed':True,'implementation_complete':True,'research_only':True,'upstream_phase':'SAED_V4_34','next_phase':'SAED_V4_36','reference_certificate':'accepted','external_evidence_open':['real package signature verification','real vulnerability scanner attestation','real reproducible build','external independent validation','MetaEditor compilation','Python/MQL5 runtime parity','production release authorization'],'production_authorization':False,'live_trading_authority':False}
(ROOT/'lab/11_strategy_factory/phase_status/SAED_V4_35.json').write_text(json.dumps(status,indent=2,sort_keys=True)+'\n')
print('SAED V4-35 full QA passed')
