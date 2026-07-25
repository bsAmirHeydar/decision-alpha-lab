from fp_i02_kernel.enums import RelationCode,PriceSide
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.conformance import _row
from fp_i06_relations.engine import scan_side_plan

def test_duplicate_scan_reproduces_same_candidate_id():
    *_,report,_=golden_store_and_report(1);p=next(x for x in report.side_plans if x.relation is RelationCode.AL and x.side is PriceSide.HIGH);m=p.check_start_utc_ms;rows=(_row(p,m,p.left_reference_price+.1,0,p.right_reference_price-.1,0),)
    a=scan_side_plan(p,rows,'REV');b=scan_side_plan(p,rows,'REV')
    assert a==b and a.candidate.candidate_id==b.candidate.candidate_id
def test_relation_and_calendar_offset_are_identity_bearing():
    *_,report,_=golden_store_and_report(2)
    high=[p for p in report.side_plans if p.side is PriceSide.HIGH]
    assert len({p.side_plan_id for p in high})==len(high)
def test_hunt_fact_id_is_stable_for_same_bar_and_reference():
    *_,report,_=golden_store_and_report(1);p=next(x for x in report.side_plans if x.relation is RelationCode.AL and x.side is PriceSide.HIGH);m=p.check_start_utc_ms;row=_row(p,m,p.left_reference_price+.1,0,p.right_reference_price-.1,0)
    a=scan_side_plan(p,(row,),'REV');b=scan_side_plan(p,(row,),'REV')
    assert a.hunt_facts[0].hunt_fact_id==b.hunt_facts[0].hunt_fact_id
