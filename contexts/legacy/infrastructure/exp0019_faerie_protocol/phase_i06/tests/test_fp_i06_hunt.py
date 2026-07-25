from fp_i02_kernel.enums import RelationCode,PriceSide
from fp_i06_relations.golden import golden_store_and_report
from fp_i06_relations.conformance import _row
from fp_i06_relations.hunt import observe_minute
from fp_i06_relations.enums import ContactState

def plan(side=PriceSide.HIGH):
    *_,report,_=golden_store_and_report(1)
    return next(p for p in report.side_plans if p.relation is RelationCode.AL and p.side is side)
def test_high_contact_uses_own_symbol_reference():
    p=plan();m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price+.01,p.left_reference_price-1,p.right_reference_price-.01,p.right_reference_price-1)
    obs,facts=observe_minute(p,row,'REV')
    assert obs.contact_state is ContactState.LEFT_ONLY and len(facts)==1 and facts[0].canonical_symbol==p.left_symbol
def test_low_contact_is_bullish_side_fact():
    p=plan(PriceSide.LOW);m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price+1,p.left_reference_price-.01,p.right_reference_price+1,p.right_reference_price+.01)
    obs,facts=observe_minute(p,row,'REV')
    assert obs.contact_state is ContactState.LEFT_ONLY and facts[0].side is PriceSide.LOW
def test_same_m1_two_contacts_are_symmetric():
    p=plan();m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price+.1,p.left_reference_price-1,p.right_reference_price+.1,p.right_reference_price-1)
    obs,facts=observe_minute(p,row,'REV')
    assert obs.contact_state is ContactState.BOTH_SAME_M1 and len(facts)==2
def test_missing_cell_blocks_minute():
    p=plan();m=p.check_start_utc_ms
    row=_row(p,m,1,0,1,0,blocked=True)
    obs,facts=observe_minute(p,row,'REV')
    assert obs.contact_state is ContactState.DATA_BLOCKED and facts==()
def test_no_contact_emits_no_fact():
    p=plan();m=p.check_start_utc_ms
    row=_row(p,m,p.left_reference_price-.1,p.left_reference_price-1,p.right_reference_price-.1,p.right_reference_price-1)
    obs,facts=observe_minute(p,row,'REV')
    assert obs.contact_state is ContactState.NONE and not facts
