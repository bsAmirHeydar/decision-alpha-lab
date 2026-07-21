from __future__ import annotations
from .canonical import stable_id,digest_object
from .constants import ISOLATION_SCENARIOS,LIFECYCLE_SCENARIOS

def _name(template,instance,chart,symbol,timeframe,event):
    for k,v in {"{INSTANCE_ID}":instance,"{CHART_ID}":chart,"{SYMBOL}":symbol,"{TIMEFRAME}":timeframe,"{EVENT_ID}":event}.items():template=template.replace(k,v)
    return template

def isolation_results(contract,event,eligible):
    specs=[("SAME_CHART_DIFFERENT_INSTANCE","INSTANCE_B",event.chart_id,event.symbol,event.timeframe),("SAME_SYMBOL_DIFFERENT_TIMEFRAME",event.instance_id,event.chart_id,event.symbol,"H1"),("DIFFERENT_CHART_SAME_INSTANCE",event.instance_id,"CHART_2002",event.symbol,event.timeframe),("DIFFERENT_SYMBOL_EXPLICIT_CHART",event.instance_id,"CHART_3003","XAUUSD",event.timeframe)]
    base=_name(contract.namespace_template,event.instance_id,event.chart_id,event.symbol,event.timeframe,event.event_id);rows=[]
    for scenario,inst,chart,symbol,tf in specs:
        other=_name(contract.namespace_template,inst,chart,symbol,tf,event.event_id);r={"scenario_id":stable_id("VISISO",contract.visual_object_id,scenario),"visual_object_id":contract.visual_object_id,"scenario":scenario,"baseline_object_id":base,"comparison_object_id":other,"collision":base==other,"result":"PASS" if eligible and base!=other else ("BLOCKED" if not eligible else "FAIL")};r["scenario_digest"]=digest_object(r,"scenario_digest");rows.append(r)
    return rows

def lifecycle_results(contract,event,eligible,backfill_policy):
    rows=[];state=[]
    for seq,scenario in enumerate(LIFECYCLE_SCENARIOS,1):
        if scenario=="OWNED_CLEANUP":state=[]
        elif scenario in {"COLD_START_BACKFILL","PROCESS_RESTART_REHYDRATE","SECOND_RESTART_IDEMPOTENCY"}:state=[contract.visual_object_id]
        elif contract.visual_object_id not in state:state.append(contract.visual_object_id)
        r={"scenario_id":stable_id("VISLIFETEST",contract.visual_object_id,scenario),"visual_object_id":contract.visual_object_id,"scenario":scenario,"sequence":seq,"state_count":len(state),"owned_scope_only":True,"backfill_policy":backfill_policy,"domain_state_mutation_count":0,"result":"PASS" if eligible else "BLOCKED"};r["scenario_digest"]=digest_object(r,"scenario_digest");rows.append(r)
    return rows
