from tools.strategy_factory.acl_os.acl_14.authority import validate_permit
from tools.strategy_factory.acl_os.acl_14.contracts import build_contracts
from tools.strategy_factory.acl_os.acl_14.decision import issue
from tools.strategy_factory.acl_os.acl_14.execution import build_manifest
from tools.strategy_factory.acl_os.acl_14.handoff_input import load_acl13_bundle
from tools.strategy_factory.acl_os.acl_14.readiness import assess

def items(acl13_root,permit,pilot_request,policy):
    binding=load_acl13_bundle(acl13_root)['binding']
    contracts=build_contracts(pilot_request,policy,validate_permit(permit,binding))
    readiness=assess(binding,pilot_request,contracts)
    return contracts,readiness,issue(pilot_request,readiness,'2026-07-18T10:00:00Z')

def test_reference_decision(acl13_root,permit,pilot_request,policy):
    assert items(acl13_root,permit,pilot_request,policy)[2]['state']=='PILOT_CONTRACT_AUTHORED_REAL_EVIDENCE_REQUIRED'

def test_no_execution_authority(acl13_root,permit,pilot_request,policy):
    assert items(acl13_root,permit,pilot_request,policy)[2]['pilot_execution_allowed'] is False

def test_no_alpha_claim(acl13_root,permit,pilot_request,policy):
    assert items(acl13_root,permit,pilot_request,policy)[2]['alpha_claim_allowed'] is False

def test_no_validation_claim(acl13_root,permit,pilot_request,policy):
    assert items(acl13_root,permit,pilot_request,policy)[2]['validation_claim_allowed'] is False

def test_empty_execution_manifest(acl13_root,permit,pilot_request,policy):
    contracts,readiness,_=items(acl13_root,permit,pilot_request,policy)
    manifest=build_manifest(pilot_request,contracts['contract'],readiness)
    assert manifest['execution_count']==0 and manifest['pilot_execution_materialized'] is False

def test_no_live_order(acl13_root,permit,pilot_request,policy):
    assert items(acl13_root,permit,pilot_request,policy)[2]['live_order_submission_allowed'] is False

def test_no_capital(acl13_root,permit,pilot_request,policy):
    assert items(acl13_root,permit,pilot_request,policy)[2]['capital_activation_allowed'] is False
