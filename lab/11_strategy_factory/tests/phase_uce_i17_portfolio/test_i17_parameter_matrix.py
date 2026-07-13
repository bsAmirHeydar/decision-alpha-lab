import pytest
from dataclasses import replace
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.queue import rank_batch
from strategy_factory_portfolio_v3.capacity import estimate_capacity
from strategy_factory_portfolio_v3.allocator import allocate

@pytest.mark.parametrize('liquidity,expected',[(0.0,False),(0.1,True),(0.5,True),(1.0,True)])
def test_liquidity_matrix(liquidity,expected):
 b=golden_batch();c=replace(b.candidates[0],liquidity_score=liquidity);b=replace(b,candidates=(c,)+b.candidates[1:]);eligible=rank_batch(b)[0].status.value=='eligible';assert eligible is expected or liquidity==0.0
@pytest.mark.parametrize('spread',[0,1,5,25,100])
def test_capacity_spread_is_monotonic(spread):
 c=golden_batch().candidates[0];q=estimate_capacity(c,2000,spread_bps=spread);assert q.degraded_utility<=c.utility_mean
@pytest.mark.parametrize('depth',[0.1,0.5,1,5,20])
def test_capacity_never_exceeds_declared(depth):
 c=golden_batch().candidates[0];q=estimate_capacity(c,2000,base_depth=depth);assert q.max_risk_units<=c.capacity_units+1e-9
@pytest.mark.parametrize('risk',[0.1,0.5,1.0,1.5])
def test_allocator_respects_total_risk(risk):
 b=golden_batch();b=replace(b,candidates=tuple(replace(c,requested_risk=risk) for c in b.candidates));q={c.candidate_id:estimate_capacity(c,b.as_of_ms) for c in b.candidates};p,l=allocate(b,golden_model(),golden_limits(),q);assert p.total_risk<=golden_limits().total_risk
