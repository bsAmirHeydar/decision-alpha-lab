from src.engine.tooling.strategy_factory.acl_os.acl_14.authority import validate_permit
from src.engine.tooling.strategy_factory.acl_os.acl_14.contracts import build_contracts
from src.engine.tooling.strategy_factory.acl_os.acl_14.handoff_input import load_acl13_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_14.readiness import assess

def build(acl13_root,permit,pilot_request,policy):
    binding=load_acl13_bundle(acl13_root)['binding']
    authority=validate_permit(permit,binding)
    contracts=build_contracts(pilot_request,policy,authority)
    return binding,contracts,assess(binding,pilot_request,contracts)

def test_contract_authored(acl13_root,permit,pilot_request,policy):
    assert build(acl13_root,permit,pilot_request,policy)[1]['contract']['pilot_execution_allowed'] is False

def test_reference_not_ready(acl13_root,permit,pilot_request,policy):
    assert build(acl13_root,permit,pilot_request,policy)[2]['pilot_ready_non_capital'] is False

def test_real_identity_unsatisfied(acl13_root,permit,pilot_request,policy):
    result=build(acl13_root,permit,pilot_request,policy)[2]
    assert next(x for x in result['gates'] if x['gate_id']=='REAL_CONTEXT_IDENTITY')['status']=='UNSATISFIED'

def test_owner_approval_unknown(acl13_root,permit,pilot_request,policy):
    result=build(acl13_root,permit,pilot_request,policy)[2]
    assert next(x for x in result['gates'] if x['gate_id']=='INDEPENDENT_OWNER_APPROVAL')['status']=='UNKNOWN'

def test_known_time_satisfied(acl13_root,permit,pilot_request,policy):
    result=build(acl13_root,permit,pilot_request,policy)[2]
    assert next(x for x in result['gates'] if x['gate_id']=='KNOWN_TIME_GUARD')['status']=='SATISFIED'

def test_search_freeze_satisfied(acl13_root,permit,pilot_request,policy):
    result=build(acl13_root,permit,pilot_request,policy)[2]
    assert next(x for x in result['gates'] if x['gate_id']=='SETUP_SEARCH_SPACE_FROZEN')['status']=='SATISFIED'

def test_all_gates_present(acl13_root,permit,pilot_request,policy):
    assert build(acl13_root,permit,pilot_request,policy)[2]['gate_count']==24

def test_unknown_blocks_readiness(acl13_root,permit,pilot_request,policy):
    result=build(acl13_root,permit,pilot_request,policy)[2]
    assert result['unknown_blocks_readiness'] and result['status_counts']['UNKNOWN']>0
