import json,subprocess,sys
from saed_v4_causal_treatment_policy_value.validation import validate_upstream

def test_upstream_validation(load,art):
 x=load(f'{art}/GOLDEN_UPSTREAM_VALIDATION.JSON');assert x['hash_verified'] and x['immutable'] and x['upstream_phase']=='SAED_V4_17'

def test_service_outputs_are_reproducible(load,art):
 r=load(f'{art}/GOLDEN_REPLAY_RECEIPT.JSON');assert len(r['selected_hashes'])>25 and r['decision_equivalent']

def test_cli(root):
 r=subprocess.run([sys.executable,'-m','saed_v4_causal_treatment_policy_value.cli','--summary'],cwd=root,env={**__import__('os').environ,'PYTHONPATH':str(root/'src/engine/packages')},capture_output=True,text=True);assert r.returncode==0;rj=json.loads(r.stdout);assert rj['phase']=='SAED_V4_18' and rj['next_phase']=='SAED_V4_19' and not rj['production_authority']
