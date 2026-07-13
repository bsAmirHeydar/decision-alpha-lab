from time import perf_counter
from .stack import resolve_active_stack
def benchmark_stack(config,contexts,data_state,at,iterations=1000):
    start=perf_counter()
    for _ in range(iterations): resolve_active_stack(config.pair_id,contexts,data_state,at,config)
    elapsed=perf_counter()-start
    return {"iterations":iterations,"elapsed_seconds":elapsed,"ops_per_second":iterations/elapsed if elapsed else 0.0}
