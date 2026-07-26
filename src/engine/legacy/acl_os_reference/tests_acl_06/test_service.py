from pathlib import Path
from src.engine.tooling.strategy_factory.acl_os.acl_06.replay import verify_research_run
def test_reference_run_passes(build):
    r=build(); assert r['passed'] and r['task_count']==54 and r['candidate_count']==12
def test_lanes_are_segregated(build):
    r=build(); assert r['research_candidate_count']==11 and r['diagnostic_candidate_count']==1 and not r['result_bundle']['diagnostic_candidates_selectable']
def test_run_is_non_promotional(build):
    r=build(); assert r['research_run']['alpha_claim_allowed'] is False and r['result_bundle']['validation_status']=='NOT_RUN'
def test_replay_passes(build):
    r=build(); assert verify_research_run(Path(r['output_root']))['passed']
def test_same_inputs_same_identities(build):
    a=build('a'); b=build('b'); assert a['run_id']==b['run_id'] and a['dag']['dag_digest']==b['dag']['dag_digest'] and a['result_bundle']['result_bundle_digest']==b['result_bundle']['result_bundle_digest']
def test_acl07_handoff_is_non_executing(build):
    h=build()['handoff']; assert h['handoff_type']=='ACL06_TO_ACL07' and not h['live_order_submission_allowed'] and not h['capital_activation_allowed']
def test_all_tasks_have_receipts(build):
    r=build(); assert r['receipts']['receipt_count']==r['task_count'] and r['receipts']['all_success']
def test_budget_is_respected(build): assert build()['accounting']['within_budget']
def test_docs_are_generated(build):
    root=Path(build()['output_root']); assert (root/'docs/ACL06_RESEARCH_RUN_SUMMARY.md').is_file() and (root/'docs/RESEARCH_DAG_INDEX.md').is_file()
