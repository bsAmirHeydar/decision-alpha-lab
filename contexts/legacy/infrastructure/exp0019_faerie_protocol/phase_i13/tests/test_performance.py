from fp_i13_release import *
def test_benchmark_fixture_under_hard_limits(fixture,instance):
 f=run_full(fixture,instance);i=run_incremental(fixture,instance,chunk_size=32);values={'full_replay_ms':f.telemetry.elapsed_ns/1e6,'incremental_max_chunk_ms':i.telemetry.max_chunk_ns/1e6,'peak_memory_bytes':max(f.telemetry.peak_memory_bytes,i.telemetry.peak_memory_bytes),'object_count':i.telemetry.object_count,'object_ops_per_frame':i.telemetry.object_ops,'checkpoint_bytes':0,'minimum_events_per_second':i.telemetry.events_per_second};assert evaluate_budget(default_budget(),values).status!=BudgetStatus.BLOCKED
def test_incremental_does_not_full_scan(fixture,instance):assert run_incremental(fixture,instance).telemetry.full_scan_count==0
