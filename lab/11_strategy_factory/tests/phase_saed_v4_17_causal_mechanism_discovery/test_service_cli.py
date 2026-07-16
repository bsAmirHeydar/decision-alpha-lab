import json,subprocess,sys
def test_cli_status(root):
 r=subprocess.run([sys.executable,'-m','saed_v4_causal_mechanism_discovery.cli','status'],cwd=root,env={**__import__('os').environ,'PYTHONPATH':str(root/'lab/11_strategy_factory/python')},capture_output=True,text=True);assert r.returncode==0 and json.loads(r.stdout)['phase']=='SAED_V4_17'
def test_cli_authority(root):
 r=subprocess.run([sys.executable,'-m','saed_v4_causal_mechanism_discovery.cli','authority'],cwd=root,env={**__import__('os').environ,'PYTHONPATH':str(root/'lab/11_strategy_factory/python')},capture_output=True,text=True);assert r.returncode==0 and not json.loads(r.stdout)['production_authority']
def test_cli_handoff(root):
 r=subprocess.run([sys.executable,'-m','saed_v4_causal_mechanism_discovery.cli','handoff'],cwd=root,env={**__import__('os').environ,'PYTHONPATH':str(root/'lab/11_strategy_factory/python')},capture_output=True,text=True);assert r.returncode==0 and json.loads(r.stdout)['next_phase']=='SAED_V4_18'
