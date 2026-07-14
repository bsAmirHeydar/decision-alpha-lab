import json,subprocess,sys
from saed_v4_event_model.conformance import run_vectors

def test_vectors(root):
    v=json.loads((root/'lab/11_strategy_factory/test_vectors/saed_v4_03/SAED_V4_03_CONFORMANCE_VECTORS.json').read_text());r=run_vectors(v);assert len(r)>=10 and all(x['passed'] for x in r)

def test_cli(root,tmp_path):
    env={'PYTHONPATH':str(root/'lab/11_strategy_factory/python')};out=tmp_path/'out.json';cmd=[sys.executable,'-m','saed_v4_event_model.cli','conformance',str(root/'lab/11_strategy_factory/test_vectors/saed_v4_03/SAED_V4_03_CONFORMANCE_VECTORS.json'),'--output',str(out)];assert subprocess.run(cmd,env=env).returncode==0;assert json.loads(out.read_text())['passed']>=10
