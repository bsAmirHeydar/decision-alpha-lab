import pytest
from tools.strategy_factory.acl_os.acl_12.authority import validate_permit
from tools.strategy_factory.acl_os.acl_12.handoff_input import load_acl11_bundle
from tools.strategy_factory.acl_os.acl_12.canonical import with_digest
from tools.strategy_factory.acl_os.acl_12.errors import AuthorityError
def test_valid_permit(ACL11,permit): assert validate_permit(permit,load_acl11_bundle(ACL11)['binding'])['validated']
def test_bad_action_denied(ACL11,permit):
    p={k:v for k,v in permit.items() if k!='permit_digest'}; p['action']='BAD'; p=with_digest(p,'permit_digest')
    with pytest.raises(AuthorityError): validate_permit(p,load_acl11_bundle(ACL11)['binding'])
def test_key_access_denied(ACL11,permit):
    p={k:v for k,v in permit.items() if k!='permit_digest'}; p['production_key_access_allowed']=True; p=with_digest(p,'permit_digest')
    with pytest.raises(AuthorityError): validate_permit(p,load_acl11_bundle(ACL11)['binding'])
def test_digest_tamper_denied(ACL11,permit):
    permit['issuer']='tampered'
    with pytest.raises(AuthorityError): validate_permit(permit,load_acl11_bundle(ACL11)['binding'])
