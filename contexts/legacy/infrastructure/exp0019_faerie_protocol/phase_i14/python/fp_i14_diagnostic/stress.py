from __future__ import annotations
from .contracts import *
from .trace import build_run
from .checkpoint import create_checkpoint
from .restart import resume_from_checkpoint
from .comparator import compare_runs
from .canonical import sha256,stable_id

def _duplicate(events,every):
    out=[]
    for i,e in enumerate(events,1):
        out.append(e)
        if every and i%every==0: out.append(e)
    return tuple(out)

def run_stress(baseline:TraceRun,scenario:StressScenario):
    reconnects=restarts=0
    if scenario.kind==ScenarioKind.DUPLICATE_DELIVERY:
        stressed=build_run(baseline.manifest,baseline.fixture_id,_duplicate(baseline.events,scenario.duplicate_every or 3))
    elif scenario.kind==ScenarioKind.RECONNECT:
        reconnects=1;cut=scenario.disconnect_after or max(1,len(baseline.events)//2);skip=scenario.reconnect_skip
        delivered=baseline.events[:cut]+baseline.events[max(0,cut-skip):]
        # canonical source reorders/dedups before ledger
        unique={e.computed_event_id:e for e in delivered};ordered=tuple(sorted(unique.values(),key=lambda e:e.sequence))
        stressed=build_run(baseline.manifest,baseline.fixture_id,ordered)
    elif scenario.kind==ScenarioKind.RESTART:
        restarts=1;cp=create_checkpoint(baseline,scenario.restart_after or max(1,len(baseline.events)//2));stressed,_=resume_from_checkpoint(baseline.manifest,baseline.fixture_id,baseline.events,cp)
    elif scenario.kind in (ScenarioKind.SYMBOL_STAGGER,ScenarioKind.LATE_REVISION,ScenarioKind.TIMEFRAME_SWITCH):
        # delivery order may differ, canonical trace order remains source sequence order
        stressed=build_run(baseline.manifest,baseline.fixture_id,tuple(sorted(baseline.events,key=lambda e:e.sequence)))
    elif scenario.kind==ScenarioKind.TRACE_TRUNCATION:
        stressed=build_run(baseline.manifest,baseline.fixture_id,baseline.events[:-1])
    else: stressed=build_run(baseline.manifest,baseline.fixture_id,baseline.events)
    diff=compare_runs(baseline,stressed)
    rid=stable_id("FPSTRESS",{"scenario":scenario.scenario_id,"product":baseline.product.value,"baseline":baseline.run_id,"stressed":stressed.run_id,"diff":diff.report_hash})
    return StressResult(rid,scenario.scenario_id,baseline.product,baseline.run_id,stressed.run_id,diff.status,len(diff.mismatches),stressed.duplicate_count,reconnects,restarts,sha256({"result_id":rid,"status":diff.status.value,"mismatches":len(diff.mismatches)}))
