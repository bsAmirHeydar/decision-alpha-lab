from dataclasses import replace
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.interactions import resolve_symbol_conflicts
from strategy_factory_portfolio_v3.enums import ConflictPolicy,Side
from strategy_factory_portfolio_v3.capacity import estimate_capacity
from strategy_factory_portfolio_v3.allocator import allocate
from strategy_factory_portfolio_v3.stress import run_stress

def test_net_policy_selects_one_direction():
    b=golden_batch();a=b.candidates[0];z=replace(b.candidates[1],symbol=a.symbol,side=Side.SHORT);d=resolve_symbol_conflicts((a,z),ConflictPolicy.NET);assert len(d.allowed_candidate_ids)==1
def test_hedge_policy_is_explicit():
    b=golden_batch();a=b.candidates[0];z=replace(b.candidates[1],symbol=a.symbol,side=Side.SHORT);d=resolve_symbol_conflicts((a,z),ConflictPolicy.HEDGE);assert d.net_side is Side.FLAT and len(d.allowed_candidate_ids)==2
def test_context_drop_does_not_corrupt_plan():
    b=golden_batch();q={c.candidate_id:estimate_capacity(c,b.as_of_ms) for c in b.candidates};p,_=allocate(b,golden_model(),golden_limits(),q);r=run_stress(p,golden_stress(),golden_limits());assert len(r)==2 and all(x.remaining_contexts>=1 for x in r)
def test_extreme_correlation_can_fail_safely():
    b=golden_batch();q={c.candidate_id:estimate_capacity(c,b.as_of_ms) for c in b.candidates};p,_=allocate(b,golden_model(),golden_limits(),q);s=(StressScenario('corr-extreme',20,0.9,10),);r=run_stress(p,s,golden_limits());assert r[0].safe is False
