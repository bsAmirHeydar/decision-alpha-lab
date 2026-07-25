from dataclasses import replace
from strategy_factory_integration import compare, map_candidate, reference_candidates, reference_config

def test_exact_parity_passes():
    cfg=reference_config(); now=1783795000000; legacy=reference_candidates(); events=tuple(map_candidate(c,cfg,now)[0] for c in legacy)
    r=compare("golden",legacy,events,cfg,now)
    assert r.passed and r.matched_count==2 and r.mismatch_count==0

def test_field_mismatch_fails():
    cfg=reference_config(); now=1783795000000; legacy=reference_candidates(); events=[map_candidate(c,cfg,now)[0] for c in legacy]
    events[0]=replace(events[0],reference_price=events[0].reference_price+1)
    r=compare("bad",legacy,tuple(events),cfg,now)
    assert not r.passed and r.mismatch_count==1
