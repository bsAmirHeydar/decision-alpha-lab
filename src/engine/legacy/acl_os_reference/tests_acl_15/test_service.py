import json
from src.engine.tooling.strategy_factory.acl_os.acl_15.service import ACL15FleetOperationsClosureService
from src.engine.tooling.strategy_factory.acl_os.acl_15.verify import verify_output
def test_build_and_verify(tmp_path,acl14_root,permit,policy):
 out=tmp_path/'out'; r=ACL15FleetOperationsClosureService().build(acl14_root,permit,policy,out); assert r['passed']; assert verify_output(out)['passed']
def test_deterministic_replay(tmp_path,acl14_root,permit,policy):
 s=ACL15FleetOperationsClosureService(); a=tmp_path/'a'; b=tmp_path/'b'; s.build(acl14_root,permit,policy,a); s.build(acl14_root,permit,policy,b)
 ma=json.loads((a/'output_manifest.json').read_text()); mb=json.loads((b/'output_manifest.json').read_text()); assert ma['manifest_digest']==mb['manifest_digest']
def test_reference_fixture(root): assert verify_output(root/'src/engine/legacy/acl_os_reference/fixtures/acl_15/reference_fleet_closure')['passed']
def test_output_has_zero_execution(root):
 d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_15/reference_fleet_closure/execution/runtime_and_order_manifest.json').read_text()); assert sum(d[k] for k in ['pilot_execution_count','runtime_generation_count','live_order_count','capital_activation_count'])==0
def test_output_handoff_closed(root):
 d=json.loads((root/'src/engine/legacy/acl_os_reference/fixtures/acl_15/reference_fleet_closure/handoff/lifecycle_closure_handoff.json').read_text()); assert d['program_reference_lifecycle_closed'] is True
