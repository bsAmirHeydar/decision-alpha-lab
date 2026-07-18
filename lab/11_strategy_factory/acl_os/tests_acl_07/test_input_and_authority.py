import copy,pytest
from tools.strategy_factory.acl_os.acl_07.handoff_input import load_acl06_bundle
from tools.strategy_factory.acl_os.acl_07.authority import validate_authority
from tools.strategy_factory.acl_os.acl_07.errors import AuthorityError

def test_acl06_bundle_loads(acl06_root):
 b=load_acl06_bundle(acl06_root); assert len(b['candidates'])==12 and len(b['segments_by_setup'])==12
def test_all_candidates_have_three_segments(acl06_root): assert all(len(x)==3 for x in load_acl06_bundle(acl06_root)['segments_by_setup'].values())
def test_handoff_is_bound(acl06_root):
 b=load_acl06_bundle(acl06_root); assert b['handoff']['result_bundle_digest']==b['bundle']['result_bundle_digest']
def test_authority_accepts(acl06_root,permit): assert validate_authority(permit,load_acl06_bundle(acl06_root)['handoff'])['passed']
def test_authority_rejects_order_flag(acl06_root,permit):
 bad=copy.deepcopy(permit); bad['live_order_submission_allowed']=True
 with pytest.raises(AuthorityError): validate_authority(bad,load_acl06_bundle(acl06_root)['handoff'])
def test_authority_rejects_wrong_run(acl06_root,permit):
 bad=copy.deepcopy(permit); bad['run_id']='OTHER'
 with pytest.raises(AuthorityError): validate_authority(bad,load_acl06_bundle(acl06_root)['handoff'])
