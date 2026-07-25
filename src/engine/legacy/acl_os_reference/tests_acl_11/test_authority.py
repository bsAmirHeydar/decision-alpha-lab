import copy,pytest
from tools.strategy_factory.acl_os.acl_11.handoff_input import load_acl10_bundle
from tools.strategy_factory.acl_os.acl_11.authority import validate_permit
from tools.strategy_factory.acl_os.acl_11.errors import AuthorityError
def test_permit_passes(acl10,permit): assert validate_permit(permit,load_acl10_bundle(acl10)['binding'])['validated']
@pytest.mark.parametrize('field',['network_access_allowed','secret_access_allowed','runtime_generation_allowed','signing_key_access_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed'])
def test_capability_escalation_fails(acl10,permit,field):
    from tools.strategy_factory.acl_os.acl_11.canonical import with_digest
    p={k:v for k,v in permit.items() if k!='permit_digest'}; p[field]=True; p=with_digest(p,'permit_digest')
    with pytest.raises(AuthorityError): validate_permit(p,load_acl10_bundle(acl10)['binding'])
