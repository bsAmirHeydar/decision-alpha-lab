import json,subprocess,sys
from pathlib import Path
from strategy_factory_onboarding_v3.golden import golden_run
from strategy_factory_onboarding_v3.conformance import assert_conformant

def test_conformance_accepts_golden():
 r=golden_run(Path('.'));assert_conformant(r[0],r[2],r[4],r[5])
def test_cli_is_deterministic(tmp_path):
 env=dict(__import__('os').environ);env['PYTHONPATH']='lab/11_strategy_factory/python'
 cmd=[sys.executable,'-m','strategy_factory_onboarding_v3.cli','--repo-root','.']
 a=subprocess.check_output(cmd,env=env,text=True);b=subprocess.check_output(cmd,env=env,text=True);assert a==b;assert json.loads(a)['invariance']=='pass'
