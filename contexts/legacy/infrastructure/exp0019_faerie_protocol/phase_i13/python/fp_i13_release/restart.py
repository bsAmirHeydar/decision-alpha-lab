from __future__ import annotations
from time import perf_counter_ns
import tracemalloc
from .contracts import *
from .canonical import sha256,stable_id
from .replay import ReplayReducer,run_full
from .checkpoint import build_checkpoint,restore_reducer,validate_checkpoint
from .parity import compare_runs

def run_restart(fixture:ReplayFixture,instance:InstanceIdentity,split_sequence:int,chart_timeframe_minutes:int=1)->RestartReport:
    uninterrupted=run_full(fixture,instance,chart_timeframe_minutes)
    before=[e for e in fixture.events if e.sequence<=split_sequence];after=[e for e in fixture.events if e.sequence>split_sequence]
    r=ReplayReducer(fixture,instance)
    for e in before:r.apply(e)
    cp=build_checkpoint(r);validation=validate_checkpoint(cp,fixture,instance)
    rr=restore_reducer(cp,fixture,instance)
    tracemalloc.start();t0=perf_counter_ns()
    for e in after:rr.apply(e)
    elapsed=perf_counter_ns()-t0;_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    inv=rr.inventory();tel_body={'event_count':len(fixture.events),'chunk_count':2,'full_scan_count':0,'duplicate_count':rr.duplicates,'elapsed_ns':elapsed,'peak_memory_bytes':peak,'checkpoint_bytes':len(str(cp).encode()),'object_count':len(inv.visual_object_ids),'object_ops':rr.object_ops,'events_per_second':0.0,'max_chunk_ns':elapsed}
    tel=ReplayTelemetry(**tel_body,telemetry_hash=sha256(tel_body));rid=stable_id('FPRUN',{'fixture':fixture.fixture_id,'mode':'RESTART','inventory':inv.inventory_hash,'instance':instance.instance_id})
    restarted=ReplayRun(rid,fixture.fixture_id,ReplayMode.RESTART,instance.instance_id,chart_timeframe_minutes,fixture.resolved_host_timeframe_minutes,fixture.config_hash,inv,tel,sha256({'run_id':rid,'inventory':inv.inventory_hash}))
    parity=compare_runs(uninterrupted,restarted);body={'uninterrupted':uninterrupted.run_id,'restarted':restarted.run_id,'checkpoint':validation.disposition.value,'parity':parity.report_hash}
    return RestartReport(stable_id('FPRESTART',body),uninterrupted.run_id,restarted.run_id,validation.disposition,parity,sha256(body))
