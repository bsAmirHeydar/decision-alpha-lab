from fp_i02_kernel.enums import PriceSide
from fp_i08_weekly.neutralization import apply_neutralization,expire_context
from fp_i08_weekly.enums import NeutralizationOutcome,WWLifecycleState
from helpers import context,observation

def test_second_symbol_touch_neutralizes():
 c=context();r,e=apply_neutralization(c,observation(c));assert r.outcome is NeutralizationOutcome.NEUTRALIZED and r.context.state is WWLifecycleState.NEUTRALIZED and e is not None
def test_hunter_retouch_does_not_neutralize():
 c=context();r,e=apply_neutralization(c,observation(c,symbol=c.hunter_symbol));assert r.outcome is NeutralizationOutcome.WRONG_SYMBOL and e is None
def test_wrong_side_does_not_neutralize():
 c=context();r,_=apply_neutralization(c,observation(c,side=PriceSide.HIGH));assert r.outcome is NeutralizationOutcome.WRONG_SIDE
def test_before_confirmation_does_not_neutralize():
 c=context();r,_=apply_neutralization(c,observation(c,minute=c.confirmed_utc_ms));assert r.outcome is NeutralizationOutcome.TOO_EARLY
def test_incomplete_data_blocks_neutralization():
 c=context();r,_=apply_neutralization(c,observation(c,complete=False));assert r.outcome is NeutralizationOutcome.DATA_BLOCKED
def test_no_price_contact_does_not_neutralize():
 c=context();r,_=apply_neutralization(c,observation(c,extreme=c.protected_reference_price+1));assert r.outcome is NeutralizationOutcome.NO_CONTACT
def test_expiry_at_week_end():
 c=context(week_end=1_000_080_000);u,e=expire_context(c,1_000_080_000);assert u.state is WWLifecycleState.EXPIRED and e is not None
