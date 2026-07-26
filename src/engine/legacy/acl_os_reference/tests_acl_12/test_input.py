import json,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_12.handoff_input import load_acl11_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_12.errors import IntegrityError
def test_valid_acl11_bundle(ACL11): assert load_acl11_bundle(ACL11)['binding']['runtime_candidate_count']==0
def test_missing_marker_fails(acl11_copy):
    (acl11_copy/'.acl11_generated_root').unlink()
    with pytest.raises(IntegrityError): load_acl11_bundle(acl11_copy)
def test_manifest_tamper_fails(acl11_copy):
    p=acl11_copy/'run/runtime_custody_run.json'; p.write_text(p.read_text()+' ')
    with pytest.raises(IntegrityError): load_acl11_bundle(acl11_copy)
def test_handoff_action_tamper_fails(acl11_copy):
    p=acl11_copy/'handoff/acl12_handoff.json'; d=json.loads(p.read_text()); d['required_acl12_actions']=[]; p.write_text(json.dumps(d))
    with pytest.raises(IntegrityError): load_acl11_bundle(acl11_copy)
def test_runtime_candidate_invention_fails(acl11_copy):
    p=acl11_copy/'handoff/acl12_handoff.json'; d=json.loads(p.read_text()); d['runtime_candidate_count']=1; p.write_text(json.dumps(d))
    with pytest.raises(IntegrityError): load_acl11_bundle(acl11_copy)
