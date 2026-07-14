from fp_i13_release import *
def test_default_budget_passes_nominal():
 v={'full_replay_ms':100,'incremental_max_chunk_ms':5,'peak_memory_bytes':1_000_000,'object_count':100,'object_ops_per_frame':10,'checkpoint_bytes':1000,'minimum_events_per_second':50_000};assert evaluate_budget(default_budget(),v).status==BudgetStatus.PASS
def test_soft_overrun_degrades():
 v={'full_replay_ms':2000,'incremental_max_chunk_ms':5,'peak_memory_bytes':1_000_000,'object_count':100,'object_ops_per_frame':10,'checkpoint_bytes':1000,'minimum_events_per_second':50_000};assert evaluate_budget(default_budget(),v).status==BudgetStatus.DEGRADED
def test_hard_overrun_blocks():
 v={'full_replay_ms':6000,'incremental_max_chunk_ms':5,'peak_memory_bytes':1_000_000,'object_count':100,'object_ops_per_frame':10,'checkpoint_bytes':1000,'minimum_events_per_second':50_000};assert evaluate_budget(default_budget(),v).status==BudgetStatus.BLOCKED
def test_low_throughput_blocks():
 v={'full_replay_ms':100,'incremental_max_chunk_ms':5,'peak_memory_bytes':1_000_000,'object_count':100,'object_ops_per_frame':10,'checkpoint_bytes':1000,'minimum_events_per_second':100};assert evaluate_budget(default_budget(),v).status==BudgetStatus.BLOCKED
