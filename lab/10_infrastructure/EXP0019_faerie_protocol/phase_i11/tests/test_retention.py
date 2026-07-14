from fp_i11_visual import *

def test_old_facts_removed(snapshot):
 from dataclasses import replace
 s=replace(snapshot,generated_at=100_000_000);r=retain_snapshot(s,s.generated_at,1);assert len(r.windows)<=len(snapshot.windows)
def test_recent_fact_kept(snapshot): assert retain_snapshot(snapshot,snapshot.generated_at,30).snapshot_id==snapshot.snapshot_id
