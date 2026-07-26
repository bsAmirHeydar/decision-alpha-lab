from src.engine.tooling.strategy_factory.acl_os.acl_15.authority import verify_permit
from src.engine.tooling.strategy_factory.acl_os.acl_15.contracts import build_contracts
from src.engine.tooling.strategy_factory.acl_os.acl_15.decision import build_decision
from src.engine.tooling.strategy_factory.acl_os.acl_15.handoff_input import load_acl14_bundle
from src.engine.tooling.strategy_factory.acl_os.acl_15.operations import build_operations
def _d(acl14_root,permit,policy):
 b=load_acl14_bundle(acl14_root)['binding']; a=verify_permit(permit,b,'2026-07-18T11:00:00Z'); c=build_contracts(b,policy,a,'2026-07-18T11:00:00Z'); o=build_operations(b,c,policy,'2026-07-18T11:00:00Z'); return build_decision(b,c,o,'2026-07-18T11:00:00Z')
def test_non_capital_closure(acl14_root,permit,policy): assert _d(acl14_root,permit,policy)['state']=='REFERENCE_LIFECYCLE_CLOSED_NON_CAPITAL'
def test_no_pilot_outcome_invention(acl14_root,permit,policy): assert _d(acl14_root,permit,policy)['pilot_outcomes_invented'] is False
def test_no_validation_bypass(acl14_root,permit,policy): assert _d(acl14_root,permit,policy)['validation_claim_allowed'] is False
def test_no_promotion(acl14_root,permit,policy): assert _d(acl14_root,permit,policy)['promotion_allowed'] is False
def test_no_runtime_order_capital(acl14_root,permit,policy):
 d=_d(acl14_root,permit,policy); assert not any(d[k] for k in ['runtime_generation_allowed','runtime_activation_allowed','live_order_submission_allowed','capital_activation_allowed'])
def test_automatic_reopen_denied(acl14_root,permit,policy): assert _d(acl14_root,permit,policy)['automatic_reopen_allowed'] is False
