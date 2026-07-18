import copy,json,pytest
from tools.strategy_factory.acl_os.acl_15.handoff_input import load_acl14_bundle
from tools.strategy_factory.acl_os.acl_15.authority import verify_permit
from tools.strategy_factory.acl_os.acl_15.errors import AuthorityError,IntegrityError
def test_acl14_input_verified(acl14_root): assert load_acl14_bundle(acl14_root)['binding']['reference_design_only'] is True
def test_acl14_execution_empty(acl14_root): assert load_acl14_bundle(acl14_root)['execution']['execution_count']==0
def test_acl14_no_prospective_rows(acl14_root): assert load_acl14_bundle(acl14_root)['execution']['prospective_observation_rows']==0
def test_permit_valid(acl14_root,permit): assert verify_permit(permit,load_acl14_bundle(acl14_root)['binding'],'2026-07-18T11:00:00Z')['permit_valid']
def test_permit_capability_escalation_denied(acl14_root,permit):
    from tools.strategy_factory.acl_os.acl_15.canonical import with_digest
    p=copy.deepcopy(permit); p.pop('permit_digest'); p['capabilities']['capital_activation_allowed']=True; p=with_digest(p,'permit_digest')
    with pytest.raises(AuthorityError): verify_permit(p,load_acl14_bundle(acl14_root)['binding'],'2026-07-18T11:00:00Z')
def test_expired_permit_denied(acl14_root,permit):
    with pytest.raises(AuthorityError): verify_permit(permit,load_acl14_bundle(acl14_root)['binding'],'2026-07-20T11:00:00Z')
