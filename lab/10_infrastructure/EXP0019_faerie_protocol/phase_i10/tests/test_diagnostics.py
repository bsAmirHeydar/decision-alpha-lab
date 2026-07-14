from fp_i10_indicator import *

def test_diagnostic(engine):
 d=build_diagnostic(engine,engine.snapshot.generated_utc_ms); assert d.runtime_authority=='NONE' and d.snapshot_hash==engine.snapshot.snapshot_hash
def test_counters_sorted(engine): assert tuple(k for k,_ in build_diagnostic(engine,engine.snapshot.generated_utc_ms).counters)==tuple(sorted(engine.counters))
def test_chain_head_matches(engine): assert build_diagnostic(engine,engine.snapshot.generated_utc_ms).chain_head_hash==engine.event_chain.head
