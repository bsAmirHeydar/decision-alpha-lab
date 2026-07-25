from fp_i13_release import *
def test_timeframe_invariance(fixture,instance): assert verify_timeframe_invariance(fixture,instance,(1,5,15,60,240)).status==ParityStatus.PASS
def test_host_timeframe_fixed(fixture,instance): assert verify_timeframe_invariance(fixture,instance,(1,15,60)).resolved_host_timeframe_minutes==5
def test_all_semantic_hashes_equal(fixture,instance): assert len(set(verify_timeframe_invariance(fixture,instance,(1,2,3,5,10,30,60)).semantic_inventory_hashes))==1
