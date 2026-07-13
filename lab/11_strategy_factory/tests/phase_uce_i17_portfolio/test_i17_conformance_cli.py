import json,subprocess,sys,os
from pathlib import Path
from strategy_factory_portfolio_v3.conformance import run_conformance

def test_conformance_passes():
 r=run_conformance();assert r['status']=='pass' and r['contexts']>=2
def test_cli_outputs_json():
 env=dict(os.environ);env['PYTHONPATH']=str(Path(__file__).resolve().parents[2]/'python')
 p=subprocess.run([sys.executable,'-m','strategy_factory_portfolio_v3.cli','conformance'],capture_output=True,text=True,env=env,check=True);assert json.loads(p.stdout)['status']=='pass'
