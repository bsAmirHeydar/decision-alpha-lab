import json,pytest
from tools.strategy_factory.acl_os.acl_09.service import ACL09MemoryPlannerService
from tools.strategy_factory.acl_os.acl_09.replay_validator import verify_generated_root

def test_service_builds(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'out'; r=ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z'); assert d.exists() and r['memory_run_id'] and r['artifact_count']>0
def test_replay_validator_passes(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'out'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z'); assert verify_generated_root(d)['passed']
def test_deterministic_replay(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 a=tmp_path/'a'; b=tmp_path/'b'; s=ACL09MemoryPlannerService(); ra=s.build(acl08_root,permit,memory_policy,planner_policy,a,'2026-07-18T02:00:00Z'); rb=s.build(acl08_root,permit,memory_policy,planner_policy,b,'2026-07-18T02:00:00Z'); assert ra['memory_run_id']==rb['memory_run_id']; assert (a/'memory/memory_index.json').read_bytes()==(b/'memory/memory_index.json').read_bytes()
def test_atomic_destination_rejects_nonempty(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'out'; d.mkdir(); (d/'x').write_text('x')
 with pytest.raises(Exception): ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z')
def test_event_chain_has_nine_events(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'out'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z'); assert json.loads((d/'events/memory_event_ledger.json').read_text())['event_count']==9
def test_handoff_has_no_authority(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=tmp_path/'out'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,'2026-07-18T02:00:00Z'); h=json.loads((d/'handoff/acl10_handoff.json').read_text()); assert not h['research_execution_allowed'] and not h['promotion_allowed'] and not h['live_order_submission_allowed'] and not h['capital_activation_allowed']
