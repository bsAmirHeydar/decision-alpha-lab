from dataclasses import replace
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.queue import rank_batch
from strategy_factory_portfolio_v3.capacity import estimate_capacity
from strategy_factory_portfolio_v3.allocator import allocate
from strategy_factory_portfolio_v3.enums import AllocationStatus,ConflictPolicy,Side

def setup(batch=None,limits=None):
    b=batch or golden_batch();l=limits or golden_limits();q={c.candidate_id:estimate_capacity(c,b.as_of_ms) for c in b.candidates};return allocate(b,golden_model(),l,q)
def test_allocator_reserves_every_selected_item():
    p,l=setup();assert p.status is AllocationStatus.ALLOCATED and abs(sum(x.allocated_risk for x in p.selected)-l.total())<1e-9
def test_allocator_is_deterministic(): assert setup()[0].plan_hash==setup()[0].plan_hash
def test_no_context_consumes_unreserved_risk():
    p,l=setup();assert p.checks['reserved_risk']
def test_context_count_gate_is_hard():
    l=replace(golden_limits(),min_context_count=4);p,_=setup(limits=l);assert p.status is not AllocationStatus.ALLOCATED
def test_capacity_missing_rejects_candidate():
    b=golden_batch();q={b.candidates[0].candidate_id:estimate_capacity(b.candidates[0],b.as_of_ms)};p,_=allocate(b,golden_model(),golden_limits(),q);assert len(p.rejected_candidate_ids)>=2
def test_opposite_direction_deny_blocks_both():
    b=golden_batch();c=replace(b.candidates[1],symbol='EURUSD',side=Side.SHORT);b=replace(b,candidates=(b.candidates[0],c,b.candidates[2]));q={x.candidate_id:estimate_capacity(x,b.as_of_ms) for x in b.candidates};p,_=allocate(b,golden_model(),golden_limits(),q,ConflictPolicy.DENY);assert 'cand-1' in p.rejected_candidate_ids and 'cand-2' in p.rejected_candidate_ids
