from __future__ import annotations
from .errors import SchedulingError
from .canonical import seal

def schedule(dag:dict,partition:dict,budget:dict)->dict:
    amap={a["task_id"]:a for a in partition["assignments"]}; pending={t["task_id"]:t for t in dag["tasks"]}; completed=set(); waves=[]; tick=0
    while pending:
        ready=sorted([t for t in pending.values() if set(t["dependencies"]).issubset(completed)],key=lambda x:x["task_id"])
        if not ready: raise SchedulingError("scheduler deadlock")
        wave=[]
        for t in ready:
            a=amap[t["task_id"]]; wave.append({"task_id":t["task_id"],"node_id":a["node_id"],"domain_id":a["domain_id"],"start_tick":tick,"end_tick":tick+1,"attempt":1,"dependencies":t["dependencies"]})
        waves.append({"wave":len(waves),"tick":tick,"tasks":wave}); completed.update(t["task_id"] for t in ready)
        for t in ready: pending.pop(t["task_id"])
        tick+=1
    if tick>budget["max_wall_clock_ticks"]: raise SchedulingError("wall-clock budget exceeded")
    return seal({"phase":"SAED_V4_34","dag_id":dag["dag_id"],"partition_plan_id":partition["plan_id"],"waves":waves,"wave_count":len(waves),"scheduled_task_count":len(completed),"final_tick":tick,"deterministic":True,"research_only":True},"v434_schedule","schedule_id","schedule_hash")
