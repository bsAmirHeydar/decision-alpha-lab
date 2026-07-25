import pytest
from fp_i14_diagnostic import *
def test_trace_builds(runs): assert all(r.inventory.event_count==18 for r in runs.values())
def test_trace_chain_nonzero(runs): assert all(r.inventory.chain_hash!='0'*64 for r in runs.values())
def test_duplicate_ignored(manifests,facts):
    p=ProductKind.INDICATOR;events=adapt_facts(p,manifests[p],facts);r=build_run(manifests[p],'F',events+(events[-1],));assert r.duplicate_count==1
def test_collision_fails(manifests,facts):
    p=ProductKind.INDICATOR;e=list(adapt_facts(p,manifests[p],facts));bad=TraceEvent(e[-1].sequence+1,e[-1].event_time_utc_ms+1,p,e[-1].event_type,e[-1].semantic_id,sha256('bad'),e[-1].config_hash,e[-1].source_revision_id,event_id=e[-1].computed_event_id)
    with pytest.raises(FPI14Error): build_run(manifests[p],'F',tuple(e)+(bad,))
def test_sequence_regression_fails(manifests,facts):
    p=ProductKind.INDICATOR;e=list(adapt_facts(p,manifests[p],facts));bad=TraceEvent(1,e[-1].event_time_utc_ms+1,p,TraceEventType.HEALTH,'NEW',sha256('new'),e[-1].config_hash,e[-1].source_revision_id)
    with pytest.raises(FPI14Error): build_run(manifests[p],'F',tuple(e)+(bad,))
