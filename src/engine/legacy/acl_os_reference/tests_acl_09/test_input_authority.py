import copy,json,shutil,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_09.handoff_input import load_acl08_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_09.authority import validate_authority

def test_acl08_bundle_loads(acl08_root): assert load_acl08_bundle(acl08_root)['handoff']['handoff_type']=='ACL08_TO_ACL09'
def test_twelve_records_verified(acl08_root): assert len(load_acl08_bundle(acl08_root)['records'])==12
def test_wrong_action_rejected(acl08_root,permit):
 p=copy.deepcopy(permit); p['action']='AUTHORIZE_EXECUTION'
 with pytest.raises(Exception): validate_authority(p,load_acl08_bundle(acl08_root)['handoff'])
def test_research_execution_capability_rejected(acl08_root,permit):
 p=copy.deepcopy(permit); p['research_execution_allowed']=True
 with pytest.raises(Exception): validate_authority(p,load_acl08_bundle(acl08_root)['handoff'])
def test_tampered_record_rejected(acl08_root,tmp_path):
 d=tmp_path/'acl08'; shutil.copytree(acl08_root,d); p=next((d/'experience/records').glob('*.json')); x=json.loads(p.read_text()); x['promotion_allowed']=True; p.write_text(json.dumps(x))
 with pytest.raises(Exception): load_acl08_bundle(d)
def test_missing_marker_rejected(acl08_root,tmp_path):
 d=tmp_path/'acl08'; shutil.copytree(acl08_root,d); (d/'.acl08_generated_root').unlink()
 with pytest.raises(Exception): load_acl08_bundle(d)
