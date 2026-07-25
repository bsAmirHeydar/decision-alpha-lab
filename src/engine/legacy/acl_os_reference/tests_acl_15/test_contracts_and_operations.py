from tools.strategy_factory.acl_os.acl_15.contracts import build_contracts
from tools.strategy_factory.acl_os.acl_15.operations import build_operations
from tools.strategy_factory.acl_os.acl_15.registry import build_registries
from tools.strategy_factory.acl_os.acl_15.handoff_input import load_acl14_bundle
from tools.strategy_factory.acl_os.acl_15.authority import verify_permit
def _all(acl14_root,permit,policy):
 b=load_acl14_bundle(acl14_root)['binding']; a=verify_permit(permit,b,'2026-07-18T11:00:00Z'); c=build_contracts(b,policy,a,'2026-07-18T11:00:00Z'); return b,c,build_operations(b,c,policy,'2026-07-18T11:00:00Z')
def test_closed_registries():
 r=build_registries(); assert all(x['dynamic_registration_allowed'] is False for x in [r['fleet'],r['closure']])
def test_fleet_reference_only(acl14_root,permit,policy):
 _,c,_=_all(acl14_root,permit,policy); assert c['fleet']['evidence_classification']=='REFERENCE_DESIGN_NOT_PROSPECTIVE_EVIDENCE'
def test_ownership_separation(acl14_root,permit,policy):
 _,c,_=_all(acl14_root,permit,policy); assert c['ownership']['self_approval_allowed'] is False and len(c['ownership']['roles'])>=3
def test_retention_no_delete(acl14_root,permit,policy):
 _,c,_=_all(acl14_root,permit,policy); assert c['retention']['deletion_allowed'] is False
def test_surveillance_non_operational(acl14_root,permit,policy):
 _,c,_=_all(acl14_root,permit,policy); assert c['surveillance']['production_monitoring_claimed'] is False
def test_evidence_inventory_empty(acl14_root,permit,policy):
 _,_,o=_all(acl14_root,permit,policy); assert o['evidence']['prospective_observation_rows']==0 and o['evidence']['pilot_outcomes_present'] is False
def test_execution_manifest_zero(acl14_root,permit,policy):
 _,_,o=_all(acl14_root,permit,policy); assert o['execution']['runtime_generation_count']==o['execution']['live_order_count']==o['execution']['capital_activation_count']==0
