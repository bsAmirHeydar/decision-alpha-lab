import copy,json
from saed_v4_portfolio_execution_economics import run_reference

def test_pipeline_exact_replay(fixture,output):assert run_reference(fixture)==output
def test_certificate_accepts_reference(output):assert output["certificate"]["decision"]=="ACCEPT_REFERENCE"
def test_handoff_targets_v438(output):assert output["handoff"]["next_phase"]=="SAED_V4_38"
def test_research_only_every_major_artifact(output):
    for k,v in output.items():
        if isinstance(v,dict) and "research_only" in v: assert v["research_only"] is True,k
def test_authority_denied(output):
    a=output["authority_boundary"]
    for k in ["may_send_order","may_activate_capital","may_mutate_ucee","may_promote_model","may_compile_live_runtime","production_authorization","live_trading_authority"]: assert a[k] is False
def test_schedule_non_executable(output):
    assert output["non_executable_schedule"]["order_submission_allowed"] is False
    assert all(not s["executable"] for o in output["non_executable_schedule"]["orders"] for s in o["slices"])
def test_baseline_preserved(output):assert output["baseline_receipt"]["baseline_preserved"] is True
def test_external_capital_untouched(output):assert output["baseline_receipt"]["external_capital_mutated"] is False
def test_no_broker_evidence(output):assert output["synthetic_reconciliation"]["broker_evidence_present"] is False
def test_stress_passes(output):assert output["stress_suite"]["all_passed"] is True
def test_reservation_not_negative(output):assert output["reservation_ledger"]["available_balance"]>=0
def test_all_economics_bounded(output):
    assert all(x["candidate_notional"]<=1800000 for x in output["opportunity_economics"]["rows"])
def test_ineligible_low_edge_rejected(output):
    e=next(x for x in output["opportunity_economics"]["rows"] if x["opportunity_id"]=="OPP_08")
    assert e["eligible"] is False
def test_allocation_deterministic_order(output):
    scores=[x["score"] for x in output["allocation_plan"]["allocations"]]; assert scores==sorted(scores,reverse=True)
def test_review_quorum(output):assert output["review_bundle"]["approved_reference"] is True
def test_certificate_denies_activation(output):
    c=output["certificate"]; assert c["capital_activation_allowed"] is False and c["order_submission_allowed"] is False and c["production_authorized"] is False
