from strategy_factory_monitoring import *

def event(seq):
    e=reference_schema().entries[0]
    return TelemetryEvent(e.metric_name,e.schema_id,"r","g","s","m",f"c{seq}","x",seq,seq,seq,float(seq))

def test_ring_drops_oldest_boundedly():
    r=TelemetryRing(2);assert r.append(event(1));assert r.append(event(2));assert r.append(event(3));assert len(r)==2;assert r.dropped_count==1;assert [x.sequence for x in r.snapshot()]==[2,3]

def test_duplicate_rejected():
    r=TelemetryRing(3);e=event(1);assert r.append(e);assert not r.append(e);assert r.duplicate_count==1

def test_non_monotonic_sequence_rejected():
    r=TelemetryRing(3);assert r.append(event(2));assert not r.append(event(1));assert r.rejected_sequence_count==1

def test_reject_new_policy():
    r=TelemetryRing(1,OverflowPolicy.REJECT_NEW);assert r.append(event(1));assert not r.append(event(2));assert r.snapshot()[0].sequence==1
