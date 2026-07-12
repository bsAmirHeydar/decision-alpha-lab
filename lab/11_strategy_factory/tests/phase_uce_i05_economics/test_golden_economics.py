from decimal import Decimal
from strategy_factory_treatments_v3.enums import TradeSide
from strategy_factory_economics_v3 import *
def test_four_long_short_broker_golden_vectors():
    x=golden_envelopes(); assert len(x)==4; assert all(e.accepted for e in x); assert all(e.maximum_loss_cash<=e.risk_budget_cash for e in x)
def test_treatment_identity_is_not_mutated(): assert {e.treatment_id for e in golden_envelopes()}=={'ucet_fixture'}
def test_deterministic_envelope_identity(): assert [e.envelope_id for e in golden_envelopes()]==[e.envelope_id for e in golden_envelopes()]
def test_side_aware_entry_and_stop_prices():
    long=golden_envelopes()[0]; short=golden_envelopes()[2]
    assert long.entry_executable_price>=Decimal('1.10010'); assert long.stop_executable_price<=Decimal('1.09810')
    assert short.entry_executable_price<=Decimal('1.10000'); assert short.stop_executable_price>=Decimal('1.10200')
