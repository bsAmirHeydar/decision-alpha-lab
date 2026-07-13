import pytest
from dataclasses import replace
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.capacity import estimate_capacity
from strategy_factory_portfolio_v3.reservations import ReservationLedger
from strategy_factory_portfolio_v3.enums import ReservationStatus
from strategy_factory_portfolio_v3.errors import PortfolioError

def test_capacity_is_deterministic():
    c=golden_batch().candidates[0];assert estimate_capacity(c,2000)==estimate_capacity(c,2000)
def test_closed_market_has_zero_capacity():
    q=estimate_capacity(golden_batch().candidates[0],2000,market_open=False);assert q.max_risk_units==0 and q.expected_fill_ratio==0
def test_volume_rounding_respects_step():
    q=estimate_capacity(golden_batch().candidates[0],2000,broker_volume_step=.25);assert abs((q.max_risk_units/.25)-round(q.max_risk_units/.25))<1e-9
def test_reservation_requires_available_risk():
    l=ReservationLedger(golden_limits(),2000);c=golden_batch().candidates[0];r=l.reserve(c,1,3000);assert r.status is ReservationStatus.RESERVED and l.total()==1
def test_reservation_breach_fails():
    l=ReservationLedger(golden_limits(),2000);c=golden_batch().candidates[0]
    with pytest.raises(PortfolioError):l.reserve(c,9,3000)
def test_release_updates_active_total():
    l=ReservationLedger(golden_limits(),2000);r=l.reserve(golden_batch().candidates[0],1,3000);l.release(r.reservation_id);assert l.total()==0
def test_hash_chain_changes_on_each_entry():
    l=ReservationLedger(golden_limits(),2000);r=l.reserve(golden_batch().candidates[0],1,3000);h1=l.head_hash;l.release(r.reservation_id);assert l.head_hash!=h1
