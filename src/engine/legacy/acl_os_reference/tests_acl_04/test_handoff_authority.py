from copy import deepcopy
import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_04.handoff_input import load_acl03_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_04.authority import validate_authority
from src.engine.tooling.strategy_factory.acl_os.acl_04.search_authority import validate_search_authority
from src.engine.tooling.strategy_factory.acl_os.acl_04.atom_registry import validate_registry
from src.engine.tooling.strategy_factory.acl_os.acl_04.errors import AuthorityError, ContractError


def test_acl03_bundle_is_bound(fixtures):
    bundle=load_acl03_bundle(fixtures['acl03'])
    assert bundle['handoff']['handoff_type']=='ACL03_TO_ACL04'
    assert bundle['handoff']['live_order_submission_allowed'] is False
    assert bundle['handoff']['capital_activation_allowed'] is False
    assert bundle['bundle_digest'].startswith('sha256:')


def test_authority_accepts_exact_binding(fixtures):
    handoff=load_acl03_bundle(fixtures['acl03'])['handoff']
    result=validate_authority(fixtures['permit'],handoff)
    assert result['passed']

@pytest.mark.parametrize('field,value',[
    ('decision','DENY'),('action','ACL03_COMPILE_CONTEXT'),('subject_context_id','CTX_OTHER'),
    ('upstream_handoff_digest','sha256:'+'0'*64),('live_order_submission_allowed',True),('capital_activation_allowed',True)
])
def test_authority_fails_closed(fixtures,field,value):
    permit=deepcopy(fixtures['permit']);permit[field]=value
    handoff=load_acl03_bundle(fixtures['acl03'])['handoff']
    with pytest.raises((AuthorityError,ContractError)): validate_authority(permit,handoff)


def test_search_authority_accepts_registered_atoms(fixtures):
    handoff=load_acl03_bundle(fixtures['acl03'])['handoff']
    assert validate_search_authority(fixtures['search'],handoff,validate_registry(fixtures['registry']))['decision']=='ALLOW'

@pytest.mark.parametrize('mutation',[
    lambda x:x.update({'decision':'DENY'}),
    lambda x:x.update({'context_id':'CTX_OTHER'}),
    lambda x:x.update({'allowed_atoms':['UNKNOWN_ATOM']}),
    lambda x:x.update({'max_candidates':0}),
    lambda x:x.update({'live_order_submission_allowed':True}),
])
def test_search_authority_rejects_mutations(fixtures,mutation):
    x=deepcopy(fixtures['search']);mutation(x)
    handoff=load_acl03_bundle(fixtures['acl03'])['handoff']
    with pytest.raises((AuthorityError,ContractError)): validate_search_authority(x,handoff,fixtures['registry'])
