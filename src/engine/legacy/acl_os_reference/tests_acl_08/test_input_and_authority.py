import copy,json,shutil,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_08.handoff_input import load_acl07_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_08.authority import validate_authority

def test_acl07_bundle_loads(acl07_root): assert load_acl07_bundle(acl07_root)['handoff']['handoff_type']=='ACL07_TO_ACL08'
def test_decision_coverage(acl07_root): b=load_acl07_bundle(acl07_root); assert len(b['candidate_decisions'])==12 and len(b['gates_by_setup'])==12
def test_wrong_action_rejected(acl07_root,permit): p=copy.deepcopy(permit); p['action']='AUTHORIZE_EXECUTION';
# digest remains invalid by design

def test_wrong_action_rejected_explicit(acl07_root,permit):
 p=copy.deepcopy(permit); p['action']='AUTHORIZE_EXECUTION'
 with pytest.raises(Exception): validate_authority(p,load_acl07_bundle(acl07_root)['handoff'])
def test_order_capability_rejected(acl07_root,permit):
 p=copy.deepcopy(permit); p['live_order_submission_allowed']=True
 with pytest.raises(Exception): validate_authority(p,load_acl07_bundle(acl07_root)['handoff'])
def test_tampered_decision_rejected(acl07_root,tmp_path):
 d=tmp_path/'acl07'; shutil.copytree(acl07_root,d); p=next((d/'decisions/candidates').glob('*.json')); x=json.loads(p.read_text()); x['decision_status']='VALIDATION_ELIGIBLE_FOR_REPORTING'; p.write_text(json.dumps(x))
 with pytest.raises(Exception): load_acl07_bundle(d)
def test_missing_marker_rejected(acl07_root,tmp_path):
 d=tmp_path/'acl07'; shutil.copytree(acl07_root,d); (d/'.acl07_generated_root').unlink()
 with pytest.raises(Exception): load_acl07_bundle(d)
