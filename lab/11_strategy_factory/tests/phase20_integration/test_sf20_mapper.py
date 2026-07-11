from strategy_factory_integration import map_candidate, reference_candidates, reference_config

def test_mapping_is_causal_and_uses_clean_symbol():
    c=reference_candidates()[0]; e,m=map_candidate(c,reference_config(),1783795000000)
    assert e.symbol==c.clean_symbol and e.reference_symbol==c.hunter_symbol
    assert e.event_time_ms==e.known_time_ms==e.confirmation_time_ms
    assert e.event_id==e.derived_event_id
    assert e.invalidation_price==c.clean_stop_reference_price
    assert "unconfirmed_trade" in e.anatomy_state
    assert m.canonical_event_id==e.event_id

def test_identity_is_stable_when_dynamic_extremes_change():
    from dataclasses import replace
    c=reference_candidates()[0]; cfg=reference_config(); now=1783795000000
    a,_=map_candidate(c,cfg,now); b,_=map_candidate(replace(c,hunter_current_extreme=c.hunter_current_extreme-10),cfg,now)
    assert a.event_id==b.event_id and a.source_hash==b.source_hash
