from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.state import build_snapshot
from saed_v4_context_twin.replay import replay_snapshot
from saed_v4_context_twin.diff import diff_snapshots
from saed_v4_context_twin.integrity import build_receipt,verify_receipt

def test_snapshot_deterministic(context_spec,seed):
 m=compile_twin(context_spec,seed);a=build_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1);b=build_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1);assert a.snapshot_hash==b.snapshot_hash
def test_replay_exact(context_spec,seed):
 m=compile_twin(context_spec,seed);a=build_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1);assert replay_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1,a.snapshot_hash)==a
def test_diff(context_spec,seed):
 m=compile_twin(context_spec,seed);a=build_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1);b=build_snapshot(m,'2026-07-13T10:01:00Z','initialized',(),(),None,(),(),(),2);d=diff_snapshots(a,b);assert 'known_as_of' in d.changed_fields and 'sequence' in d.changed_fields
def test_receipt(context_spec,seed):
 m=compile_twin(context_spec,seed);s=build_snapshot(m,'2026-07-13T10:00:00Z','initialized',(),(),None,(),(),(),1);r=build_receipt(m,s);assert verify_receipt(r,m,s)
