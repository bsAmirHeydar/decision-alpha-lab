from strategy_factory_candidate import AnatomyEvent,FeatureSnapshot,ContextFrame

def fixture(direction=1):
    e=AnatomyEvent("evt_fixture","sf08_fixture","1.0.0","EURUSD",direction,1.1000,1.0980 if direction==1 else 1.1020,1000,1000,"src")
    s=FeatureSnapshot("snap_fixture",e.event_id,8,1000,{"confirmation_price":1.1010 if direction==1 else 1.0990})
    f=ContextFrame("ctx_fixture",e.event_id,s.snapshot_id,8)
    return e,s,f
