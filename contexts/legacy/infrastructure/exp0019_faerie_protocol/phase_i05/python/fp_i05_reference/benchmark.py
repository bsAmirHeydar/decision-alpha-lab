from time import perf_counter
from .selector import select_prior_n_calendar_days
def run_calendar_depth_benchmark(depth=366,iterations=100):
    start=perf_counter()
    for _ in range(iterations): select_prior_n_calendar_days('2026-12-31',depth,(), 'a'*64)
    elapsed=perf_counter()-start
    return {'depth':depth,'iterations':iterations,'selection_count':depth*iterations,'elapsed_seconds':elapsed,'per_selection_microseconds':elapsed*1_000_000/(depth*iterations)}
