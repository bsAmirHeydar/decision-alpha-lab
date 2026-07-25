from strategy_factory_integration import EventDedupRegistry, LifecycleLedger, map_candidate, reference_candidates, reference_config
from strategy_factory_integration.enums import LifecycleState

def test_dedup_and_retirement():
    e,_=map_candidate(reference_candidates()[0],reference_config(),1783795000000)
    d=EventDedupRegistry(2); assert d.register(e,1); assert not d.register(e,2)
    l=LifecycleLedger(); r1=l.observe(e.event_id,1,1); assert r1.state==LifecycleState.FIRST_SEEN
    r2=l.observe(e.event_id,2,2); assert r2.state==LifecycleState.ACTIVE
    retired=l.retire_missing(set(),3,3); assert retired[0].state==LifecycleState.RETIRED
