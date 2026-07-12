import json,subprocess,sys
from strategy_factory_trainers_v3.conformance import run_conformance
def test_conformance():
 r=run_conformance();assert r['passed'] and r['registry_size']==3 and len(r['cases'])==3
def test_cli():
 p=subprocess.run([sys.executable,'-m','strategy_factory_trainers_v3.cli','conformance'],capture_output=True,text=True,check=True);assert json.loads(p.stdout)['passed']
