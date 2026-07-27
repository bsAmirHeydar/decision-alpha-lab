import pytest
from strategy_factory_candidate import *
from .sf08_helpers import fixture

def test_build_two_candidates():
    r=build_fixture_registry();m=build_reference_matrix(r);engine=CandidateEngine(r,m);e,s,f=fixture();out=engine.build(e,s,f,8);assert len(out)==2;assert len({x.candidate_id for x in out})==2;assert all(x.planned_r_multiple>0 for x in out)

def test_short_geometry():
    r=build_fixture_registry();m=build_reference_matrix(r);e,s,f=fixture(2);out=CandidateEngine(r,m).build(e,s,f,8);assert out;assert all(x.stop.stop_price>x.entry.requested_price for x in out);assert all((not x.exit_plan.has_price_target) or x.exit_plan.target_price<x.entry.requested_price for x in out)

def test_context_mismatch_fails():
    r=build_fixture_registry();m=build_reference_matrix(r);e,s,f=fixture();bad=ContextFrame(f.frame_id,"other",s.snapshot_id,8)
    with pytest.raises(ValueError):CandidateEngine(r,m).build(e,s,bad,8)

def test_generation_mismatch_fails():
    r=build_fixture_registry();m=build_reference_matrix(r);e,s,f=fixture();bad=ContextFrame(f.frame_id,e.event_id,s.snapshot_id,9)
    with pytest.raises(ValueError):CandidateEngine(r,m).build(e,s,bad,8)

def test_capacity_fails_closed():
    r=build_fixture_registry();m=build_reference_matrix(r);e,s,f=fixture()
    with pytest.raises(OverflowError):CandidateEngine(r,m,capacity=1).build(e,s,f,8)
