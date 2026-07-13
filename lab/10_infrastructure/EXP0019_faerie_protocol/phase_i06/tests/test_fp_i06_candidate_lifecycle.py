from fp_i02_kernel.enums import RelationCode,PriceSide
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.conformance import _row
from fp_i06_relations.engine import scan_side_plan
from fp_i06_relations.enums import CandidateState,CandidateTransition

def p():
    *_,report,_=golden_store_and_report(1)
    return next(x for x in report.side_plans if x.relation is RelationCode.AL and x.side is PriceSide.HIGH)
def test_second_symbol_touch_cancels_raw_candidate():
    plan=p();m=plan.check_start_utc_ms
    first=_row(plan,m,plan.left_reference_price+.1,0,plan.right_reference_price-.1,0)
    second=_row(plan,m+60_000,plan.left_reference_price+.2,0,plan.right_reference_price+.1,0)
    r=scan_side_plan(plan,(first,second),'REV')
    assert r.candidate.state is CandidateState.CANCELLED_SECOND_TOUCH
    assert [e.transition for e in r.candidate_events]==[CandidateTransition.CREATED,CandidateTransition.SECOND_TOUCH_CANCELLED]
def test_repeated_hunter_touch_does_not_cancel():
    plan=p();m=plan.check_start_utc_ms
    rows=(_row(plan,m,plan.left_reference_price+.1,0,plan.right_reference_price-.1,0),_row(plan,m+60_000,plan.left_reference_price+.2,0,plan.right_reference_price-.1,0))
    r=scan_side_plan(plan,rows,'REV')
    assert r.candidate.state is CandidateState.RAW_ACTIVE and len(r.candidate_events)==1
def test_data_gap_after_candidate_invalidates_candidate():
    plan=p();m=plan.check_start_utc_ms
    rows=(_row(plan,m,plan.left_reference_price+.1,0,plan.right_reference_price-.1,0),_row(plan,m+60_000,1,0,1,0,blocked=True))
    r=scan_side_plan(plan,rows,'REV')
    assert r.candidate.state is CandidateState.INVALID_DATA
def test_window_close_can_terminalize_unconfirmed_raw_candidate():
    plan=p();m=plan.check_start_utc_ms
    r=scan_side_plan(plan,(_row(plan,m,plan.left_reference_price+.1,0,plan.right_reference_price-.1,0),),'REV',close_at_window_end=True)
    assert r.candidate.state is CandidateState.CHECK_WINDOW_ENDED
