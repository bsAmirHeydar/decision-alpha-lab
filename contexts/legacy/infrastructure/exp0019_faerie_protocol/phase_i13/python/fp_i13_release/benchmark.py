from .replay import run_full,run_incremental
from .budgets import default_budget,evaluate_budget

def benchmark_fixture(fixture,instance,profile_id):
    full=run_full(fixture,instance,1);inc=run_incremental(fixture,instance,1,chunk_size=256)
    values={'full_replay_ms':full.telemetry.elapsed_ns/1e6,'incremental_max_chunk_ms':inc.telemetry.max_chunk_ns/1e6,'peak_memory_bytes':max(full.telemetry.peak_memory_bytes,inc.telemetry.peak_memory_bytes),'object_count':inc.telemetry.object_count,'object_ops_per_frame':inc.telemetry.object_ops,'checkpoint_bytes':inc.telemetry.checkpoint_bytes,'minimum_events_per_second':inc.telemetry.events_per_second}
    return full,inc,evaluate_budget(default_budget(profile_id),values)
