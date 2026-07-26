import json
from src.engine.tooling.strategy_factory.acl_os.acl_09.service import ACL09MemoryPlannerService

def build(acl08_root,permit,memory_policy,planner_policy,tmp_path,prior=None,at='2026-07-18T02:00:00Z'):
 d=tmp_path/'out'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,d,at,prior); return d

def test_planner_evaluates_eight_questions(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); x=json.loads((d/'planner/plan_portfolio.json').read_text()); assert x['proposal_count']==8
def test_planner_bounded_to_six(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); x=json.loads((d/'planner/plan_portfolio.json').read_text()); assert x['selected_count']<=6 and x['selected_cost_units']<=100
def test_selected_proposals_not_authorized(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); rows=[json.loads(p.read_text()) for p in (d/'planner/proposals').glob('*.json')]; assert all(not r['research_execution_allowed'] and not r['promotion_allowed'] for r in rows)
def test_baseline_and_diagnostic_do_not_source_plans(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 d=build(acl08_root,permit,memory_policy,planner_policy,tmp_path); entries={json.loads(p.read_text())['memory_entry_id']:json.loads(p.read_text()) for p in (d/'memory/entries').glob('*.json')}; rows=[json.loads(p.read_text()) for p in (d/'planner/proposals').glob('*.json')]; assert all(all(entries[e]['experience_class'] in {'INSUFFICIENT_EVIDENCE','NEGATIVE_VALIDATION','REPORTABLE_EVIDENCE'} for e in r['source_memory_entry_ids']) for r in rows)
def test_second_run_suppresses_prior_proposals(acl08_root,permit,memory_policy,planner_policy,tmp_path):
 first=tmp_path/'first'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,first,'2026-07-18T02:00:00Z'); second=tmp_path/'second'; ACL09MemoryPlannerService().build(acl08_root,permit,memory_policy,planner_policy,second,'2026-07-18T03:00:00Z',first); x=json.loads((second/'planner/plan_portfolio.json').read_text()); assert x['selected_count']==0 and x['proposal_count']==0
