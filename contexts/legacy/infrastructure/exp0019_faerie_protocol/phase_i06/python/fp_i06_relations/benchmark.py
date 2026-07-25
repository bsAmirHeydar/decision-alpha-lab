from __future__ import annotations
from time import perf_counter
from .engine import scan_side_plan

def benchmark_scan(plan,rows,revision_id,repeats=3):
    durations=[];result=None
    for _ in range(repeats):
        start=perf_counter();result=scan_side_plan(plan,rows,revision_id);durations.append((perf_counter()-start)*1000)
    return {'row_count':len(rows),'repeat_count':repeats,'minimum_ms':min(durations),'maximum_ms':max(durations),'average_ms':sum(durations)/len(durations),'candidate_count':int(result.candidate is not None)}
