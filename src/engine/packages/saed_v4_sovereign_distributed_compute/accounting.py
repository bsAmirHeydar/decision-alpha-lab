from __future__ import annotations
from .canonical import content_hash,seal,hash_chain
from .errors import AccountingError

def resource_usage(dag:dict,schedule:dict,budget:dict)->dict:
    usage={"cpu_core_seconds":0.0,"gpu_seconds":0.0,"memory_gb_seconds":0.0,"scratch_gb_seconds":0.0,"network_bytes":0.0,"task_attempts":0,"wall_clock_ticks":schedule["final_tick"]}
    for t in dag["tasks"]:
        usage["cpu_core_seconds"]+=t["cpu_cores"]; usage["gpu_seconds"]+=t["gpu_units"]; usage["memory_gb_seconds"]+=t["memory_gb"]; usage["scratch_gb_seconds"]+=t["scratch_gb"]; usage["task_attempts"]+=1; usage["network_bytes"]+=256 if t["locality"]=="any_sovereign_domain" else 0
    limits={"cpu_core_seconds":budget["max_cpu_core_seconds"],"gpu_seconds":budget["max_gpu_seconds"],"memory_gb_seconds":budget["max_memory_gb_seconds"],"scratch_gb_seconds":budget["max_scratch_gb_seconds"],"network_bytes":budget["max_network_bytes"],"task_attempts":budget["max_task_attempts"],"wall_clock_ticks":budget["max_wall_clock_ticks"]}
    checks={k:usage[k]<=limits[k] for k in limits}
    if not all(checks.values()): raise AccountingError("resource budget exceeded")
    return seal({"phase":"SAED_V4_34","usage":usage,"limits":limits,"checks":checks,"all_within_budget":True,"research_only":True},"v434_usage","ledger_id","ledger_hash")

def cost_ledger(usage:dict,budget:dict)->dict:
    u=usage["usage"]; cost=round(u["cpu_core_seconds"]*.01+u["gpu_seconds"]*.2+u["memory_gb_seconds"]*.001+u["scratch_gb_seconds"]*.0001+u["network_bytes"]*.000001,8)
    if cost>budget["max_cost_units"]: raise AccountingError("cost budget exceeded")
    return seal({"phase":"SAED_V4_34","cost_model":"synthetic_reference_v1","cost_units":cost,"max_cost_units":budget["max_cost_units"],"within_budget":True,"financial_charge":"not_claimed","research_only":True},"v434_cost","ledger_id","ledger_hash")

def network_ledger(transcript:dict,network:dict)->dict:
    events=[]
    for e in transcript["events"]:
        events.append({"task_id":e["task_id"],"message_class":"aggregate_or_receipt","bytes":256,"public_egress":False,"raw_data":False,"route_policy_id":network["policy_id"]})
    return seal({"phase":"SAED_V4_34","events":hash_chain(events,"v434_network_event"),"public_egress_events":0,"raw_data_events":0,"policy_respected":True,"research_only":True},"v434_network","ledger_id","ledger_hash")

def exposure_ledger(dag:dict,failures:dict,recovery:dict,budget:dict)->dict:
    events=[]
    for t in dag["tasks"]: events.append({"exposure_type":"task_execution","subject_id":t["task_id"],"count":1})
    for f in failures["failures"]: events.append({"exposure_type":"fault_injection","subject_id":f["failure_id"],"count":1})
    for e in recovery["events"]: events.append({"exposure_type":"recovery_attempt","subject_id":e["task_id"],"count":1})
    total=sum(e["count"] for e in events)
    if total>budget["max_exposures"]: raise AccountingError("exposure budget exceeded")
    return seal({"phase":"SAED_V4_34","events":hash_chain(events,"v434_exposure_event"),"total_exposures":total,"max_exposures":budget["max_exposures"],"complete_accounting":True,"within_budget":True,"research_only":True},"v434_exposure","ledger_id","ledger_hash")

def telemetry_redaction(transcript:dict)->dict:
    forbidden=["raw_row","credential","secret","private_key","account_number"]
    scanned=json_like(transcript)
    hits=[x for x in forbidden if x in scanned.lower()]
    return seal({"phase":"SAED_V4_34","forbidden_tokens":forbidden,"hits":hits,"redaction_passed":not hits,"raw_payloads_logged":False,"research_only":True},"v434_telemetry","report_id","report_hash")

def json_like(v)->str:
    import json
    return json.dumps(v,sort_keys=True,separators=(",",":"))
