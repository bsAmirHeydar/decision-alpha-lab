import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_13.handoff_input import load_acl12_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_13.authority import validate_permit
from src.engine.tooling.strategy_factory.acl_os.acl_13.input_contract import validate_request
from src.engine.tooling.strategy_factory.acl_os.acl_13.errors import AuthorityError,ContractError
def test_acl12_bundle_valid(acl12): assert load_acl12_bundle(acl12)['binding']['runtime_candidate_count']==0
def test_permit_valid(acl12,permit): assert validate_permit(permit,load_acl12_bundle(acl12)['binding'])['validated']
def test_permit_escalation_denied(acl12,permit):
    p=copy.deepcopy(permit); p['capital_activation_allowed']=True
    with pytest.raises(AuthorityError): validate_permit(p,load_acl12_bundle(acl12)['binding'])
def test_request_valid(assessment_request): assert validate_request(assessment_request)['known_time_safe']
def test_request_digest_tamper_denied(assessment_request):
    r=copy.deepcopy(assessment_request); r['context_id']='TAMPERED'
    with pytest.raises(ContractError): validate_request(r)
def test_known_time_violation_denied(assessment_request):
    r=copy.deepcopy(assessment_request); r['observations'][0]['label_available_at']='2027-01-01T00:00:00Z'
    from src.engine.tooling.strategy_factory.acl_os.acl_13.canonical import with_digest
    r=with_digest({k:v for k,v in r.items() if k!='assessment_request_digest'},'assessment_request_digest')
    with pytest.raises(ContractError): validate_request(r)
