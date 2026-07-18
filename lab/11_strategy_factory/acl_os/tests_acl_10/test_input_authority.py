import pytest
from tools.strategy_factory.acl_os.acl_10.authority import verify_authority_permit
from tools.strategy_factory.acl_os.acl_10.canonical import with_digest
from tools.strategy_factory.acl_os.acl_10.handoff_input import load_acl09_bundle
from tools.strategy_factory.acl_os.acl_10.errors import AuthorityError,IntegrityError

def test_acl09_bundle_loads(acl09_root):
    bundle=load_acl09_bundle(acl09_root); assert bundle['handoff']['reporting_eligible_candidate_count']==0; assert len(bundle['decisions'])==12

def test_permit_passes(acl09_root,permit):
    bundle=load_acl09_bundle(acl09_root); assert verify_authority_permit(permit,bundle['binding'])['passed']

def test_wrong_action_denied(acl09_root,permit):
    bundle=load_acl09_bundle(acl09_root); bad={**permit,'action':'PROMOTE_NOW'}; bad=with_digest({k:v for k,v in bad.items() if k!='permit_digest'},'permit_digest')
    with pytest.raises(AuthorityError): verify_authority_permit(bad,bundle['binding'])

def test_runtime_authority_denied(acl09_root,permit):
    bundle=load_acl09_bundle(acl09_root); bad={**permit,'runtime_generation_allowed':True}; bad=with_digest({k:v for k,v in bad.items() if k!='permit_digest'},'permit_digest')
    with pytest.raises(AuthorityError): verify_authority_permit(bad,bundle['binding'])

def test_manifest_tamper_denied(copied_acl09):
    p=copied_acl09/'planner/plan_portfolio.json'; p.write_text(p.read_text()+'\n',encoding='utf-8')
    with pytest.raises(IntegrityError): load_acl09_bundle(copied_acl09)

def test_memory_history_rewrite_denied(copied_acl09):
    import json
    p=copied_acl09/'memory/memory_index.json'; d=json.loads(p.read_text()); d['history_rewritten']=True; p.write_text(json.dumps(d),encoding='utf-8')
    with pytest.raises(IntegrityError): load_acl09_bundle(copied_acl09)
