from tools.strategy_factory.acl_os.acl_14.authority import validate_permit
from tools.strategy_factory.acl_os.acl_14.canonical import with_digest
from tools.strategy_factory.acl_os.acl_14.handoff_input import load_acl13_bundle
from tools.strategy_factory.acl_os.acl_14.request import validate_request
import pytest

def test_acl13_bundle(acl13_root):
    assert load_acl13_bundle(acl13_root)['binding']['pilot_design_allowed'] is True

def test_permit_valid(acl13_root,permit):
    assert validate_permit(permit,load_acl13_bundle(acl13_root)['binding'])['valid']

def test_permit_digest_rejected(acl13_root,permit):
    permit['issuer']='tampered'
    with pytest.raises(Exception):
        validate_permit(permit,load_acl13_bundle(acl13_root)['binding'])

def test_permit_authority_escalation(acl13_root,permit):
    permit['pilot_execution_allowed']=True
    permit=with_digest({k:v for k,v in permit.items() if k!='permit_digest'},'permit_digest')
    with pytest.raises(Exception):
        validate_permit(permit,load_acl13_bundle(acl13_root)['binding'])

def test_request_valid(acl13_root,pilot_request):
    assert validate_request(pilot_request,load_acl13_bundle(acl13_root)['binding'])['request_valid']

def test_synthetic_reuse_denied(acl13_root,pilot_request):
    pilot_request['synthetic_or_reference_reuse_as_real']=True
    pilot_request=with_digest({k:v for k,v in pilot_request.items() if k!='pilot_request_digest'},'pilot_request_digest')
    with pytest.raises(Exception):
        validate_request(pilot_request,load_acl13_bundle(acl13_root)['binding'])

def test_dynamic_search_denied(acl13_root,pilot_request):
    pilot_request['setup_search_space']['dynamic_generation_allowed']=True
    pilot_request=with_digest({k:v for k,v in pilot_request.items() if k!='pilot_request_digest'},'pilot_request_digest')
    with pytest.raises(Exception):
        validate_request(pilot_request,load_acl13_bundle(acl13_root)['binding'])

def test_non_capital_boundary_enforced(acl13_root,pilot_request):
    pilot_request['non_capital_boundary']['order_submission_allowed']=True
    pilot_request=with_digest({k:v for k,v in pilot_request.items() if k!='pilot_request_digest'},'pilot_request_digest')
    with pytest.raises(Exception):
        validate_request(pilot_request,load_acl13_bundle(acl13_root)['binding'])
