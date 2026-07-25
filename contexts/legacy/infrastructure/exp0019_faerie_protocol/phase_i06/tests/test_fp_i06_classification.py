from fp_i02_kernel.enums import RelationCode,PriceSide,Direction
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.conformance import _row
from fp_i06_relations.engine import scan_side_plan
from fp_i06_relations.enums import SweepOutcome,CandidateState

def get_plan(side):
    *_,report,_=golden_store_and_report(1)
    return next(p for p in report.side_plans if p.relation is RelationCode.AL and p.side is side)
def test_left_first_high_creates_bearish_candidate():
    p=get_plan(PriceSide.HIGH);m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price+.1,p.left_reference_price-1,p.right_reference_price-.1,p.right_reference_price-1)
    r=scan_side_plan(p,(row,),'REV')
    assert r.classification.outcome is SweepOutcome.LEFT_FIRST and r.candidate.direction is Direction.BEARISH and r.candidate.hunter_symbol==p.left_symbol
def test_right_first_low_creates_bullish_candidate():
    p=get_plan(PriceSide.LOW);m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price+1,p.left_reference_price+.1,p.right_reference_price+1,p.right_reference_price-.1)
    r=scan_side_plan(p,(row,),'REV')
    assert r.classification.outcome is SweepOutcome.RIGHT_FIRST and r.candidate.direction is Direction.BULLISH and r.candidate.protected_symbol==p.left_symbol
def test_same_m1_creates_no_candidate_and_no_invented_order():
    p=get_plan(PriceSide.HIGH);m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price+.1,p.left_reference_price-1,p.right_reference_price+.1,p.right_reference_price-1)
    r=scan_side_plan(p,(row,),'REV')
    assert r.classification.outcome is SweepOutcome.SYMMETRIC_SAME_M1 and r.candidate is None and not r.classification.hunter_symbol
def test_missing_data_creates_no_candidate():
    p=get_plan(PriceSide.HIGH);m=p.check_start_utc_ms
    r=scan_side_plan(p,(_row(p,m,1,0,1,0,blocked=True),),'REV')
    assert r.classification.outcome is SweepOutcome.DATA_BLOCKED and r.candidate is None
def test_no_contact_creates_no_candidate():
    p=get_plan(PriceSide.HIGH);m=p.check_start_utc_ms
    r=scan_side_plan(p,(_row(p,m,p.left_reference_price-1,p.left_reference_price-2,p.right_reference_price-1,p.right_reference_price-2),),'REV')
    assert r.classification.outcome is SweepOutcome.NO_CONTACT and r.candidate is None
