from time import perf_counter
from .enums import DataReadiness,ActiveWWDirection

def benchmark_incremental(engine,start_m1,iterations=500):
    state={'data_readiness':DataReadiness.READY,'history_ready':True,'source_revision_id':'REV-BENCH','source_revision_sequence':1,'active_ww_direction':ActiveWWDirection.NONE,'confirmed_signal_count':0,'allowed_signal_count':0,'suppressed_by_ww_count':0,'suppressed_by_quota_count':0,'quota_winner_signal_id':'','ledger_event_count':0}
    t=perf_counter()
    for i in range(iterations): engine.calculate(target_closed_m1=start_m1+i*60000,upstream_state=state)
    elapsed=perf_counter()-t
    return {'iterations':iterations,'elapsed_seconds':elapsed,'avg_microseconds':elapsed*1_000_000/iterations,'processed_minutes':engine.counters['processed_minutes']}
