import json,subprocess,sys,os
from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.evidence import build_evidence_bundle,verify_evidence_bundle
from strategy_factory_tournament_v3.conformance import conformance_report
from strategy_factory_tournament_v3.registry import capability_manifest

def test_evidence_tamper():
 b=build_evidence_bundle(decision=golden_run()[-1]);assert verify_evidence_bundle(b);b['artifacts']['x']=1;assert not verify_evidence_bundle(b)
def test_conformance():
 x=golden_run();b=build_evidence_bundle(decision=x[-1]);r=conformance_report(prefix=[x[2][0]],suffix=[x[2][1]],cut_ms=x[2][0].known_time_ms,evidence_bundle=b,decision=x[-1]);assert r['passed']
def test_capability_boundary():
 c=capability_manifest()['capabilities'];assert c['real_market_data_embedded'] is False;assert c['broker_execution_authority'] is False
def test_cli_golden():
 env=dict(os.environ);env['PYTHONPATH']='lab/11_strategy_factory/python';p=subprocess.run([sys.executable,'-m','strategy_factory_tournament_v3.cli','golden'],cwd='.',env=env,text=True,capture_output=True,check=True);data=json.loads(p.stdout);assert data['decision']['status']=='reject'
