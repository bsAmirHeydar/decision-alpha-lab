from copy import deepcopy
import pytest
from tools.strategy_factory.acl_os.acl_04.ai_generator import generate_ai_setups
from tools.strategy_factory.acl_os.acl_04.errors import ContractError


def test_ai_generation_is_deterministic(fixtures):
    a,ea=generate_ai_setups(fixtures['ai'],fixtures['search'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    b,eb=generate_ai_setups(fixtures['ai'],fixtures['search'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
    assert a==b and ea==eb
    assert len(a)==6
    assert ea['complete_enumeration'] is True
    assert {x['parameters']['ENTRY_THRESHOLD'] for x in a}=={0.25,0.5,0.75}


def test_ai_budget_rejected(fixtures):
    request=deepcopy(fixtures['ai']);request['requested_candidates']=33
    with pytest.raises(ContractError): generate_ai_setups(request,fixtures['search'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')


def test_ai_unknown_domain_rejected(fixtures):
    request=deepcopy(fixtures['ai']);request['vary_parameters']=['UNDECLARED']
    with pytest.raises(ContractError): generate_ai_setups(request,fixtures['search'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')


def test_ai_generator_allowlist_is_closed(fixtures):
    request=deepcopy(fixtures['ai']);request['generator']='LLM_FREEFORM'
    with pytest.raises(ContractError): generate_ai_setups(request,fixtures['search'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')


def test_ai_context_mismatch_rejected(fixtures):
    request=deepcopy(fixtures['ai']);request['context_version']='9.9.9'
    with pytest.raises(ContractError): generate_ai_setups(request,fixtures['search'],context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')


def test_registered_generator_must_also_be_permitted_by_search_authority(fixtures):
    authority=deepcopy(fixtures['search']);authority['generator_allowlist']=[]
    with pytest.raises(ContractError, match='ACL04_AI_GENERATOR_OUTSIDE_SEARCH_AUTHORITY'):
        generate_ai_setups(fixtures['ai'],authority,context_id='CTX_REFERENCE_ALPHA',context_version='0.1.0')
