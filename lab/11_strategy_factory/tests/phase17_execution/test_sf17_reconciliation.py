from strategy_factory_execution import *

def test_reconciliation_detects_match_and_mismatch():
    p=PositionRecord("p","i","X",1,PositionState.OPEN,1,100,98,104,True,1); p.refresh_hash()
    r=reconcile_positions([p],[ObservedPosition("o","X",1,1,100,2)],3)
    assert r.matched==1 and r.mismatched==0
    r2=reconcile_positions([p],[ObservedPosition("o","X",1,2,100,2)],3)
    assert r2.mismatched==1
