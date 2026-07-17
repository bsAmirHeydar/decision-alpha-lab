from __future__ import annotations
from copy import deepcopy
from .canonical import seal,hash_chain
from .errors import PlannerError

def select(scorecard:dict,available:dict,weights:dict)->dict:
    remaining={"compute_units":available["compute_units"],"exposure_units":available["exposure_units"],"review_hours":available["review_hours"],"risk_capacity":available["risk_capacity"]}; selected=[]; rejected=[]; selected_ids=set()
    eligible=[x for x in scorecard["candidates"] if x["eligible"]]
    def fits(x): return all(x[k]<=remaining[k] for k in ["compute_units","exposure_units","review_hours"]) and x["risk"]<=remaining["risk_capacity"] and set(x["prerequisite_ids"])<=selected_ids
    # deterministic protected floors: negative knowledge, replication, exploration families
    protected=[]
    if eligible:
        protected += sorted([x for x in eligible if x["negative_knowledge_value"]>=weights["negative_knowledge_floor"]],key=lambda x:(-x["utility"],x["candidate_id"]))[:1]
        protected += sorted([x for x in eligible if x["replication_value"]>=weights["replication_floor"]],key=lambda x:(-x["utility"],x["candidate_id"]))[:1]
        protected += sorted([x for x in eligible if x["novelty"]>=weights["exploration_floor"]],key=lambda x:(-x["utility"],x["candidate_id"]))[:1]
    order=[]
    for x in protected+eligible:
        if x["candidate_id"] not in {q["candidate_id"] for q in order}: order.append(x)
    pending=order[:]
    progress=True
    while pending and progress and len(selected)<available["max_selected"]:
        progress=False
        for x in pending[:]:
            if fits(x):
                selected.append(x); selected_ids.add(x["candidate_id"])
                for k in ["compute_units","exposure_units","review_hours"]: remaining[k]=round(remaining[k]-x[k],8)
                remaining["risk_capacity"]=round(remaining["risk_capacity"]-x["risk"],8); pending.remove(x); progress=True
                if len(selected)>=available["max_selected"]: break
        if not progress: break
    for x in scorecard["candidates"]:
        if x["candidate_id"] not in selected_ids:
            reason="INELIGIBLE" if not x["eligible"] else "BUDGET_OR_PREREQUISITE_OR_CAPACITY"
            rejected.append({"candidate_id":x["candidate_id"],"reason":reason,"utility":x["utility"]})
    if not selected: raise PlannerError("planner must fail closed when no proposal fits")
    events=[]
    for rank,x in enumerate(selected,1): events.append({"event_type":"PROPOSAL_SELECTED","candidate_id":x["candidate_id"],"rank":rank,"utility":x["utility"]})
    return seal({"phase":"SAED_V4_36","selected":[{"candidate_id":x["candidate_id"],"title":x["title"],"family":x["family"],"objective_id":x["objective_id"],"utility":x["utility"],"compute_units":x["compute_units"],"exposure_units":x["exposure_units"],"review_hours":x["review_hours"],"risk":x["risk"],"prerequisite_ids":x["prerequisite_ids"]} for x in selected],"rejected":rejected,"selected_count":len(selected),"remaining_budget":remaining,"planner_events":hash_chain(events,"v436_planner_event"),"status":"PROPOSED_FOR_HUMAN_REVIEW","automatic_execution_allowed":False,"research_only":True},"v436_plan","plan_id","plan_hash")

def schedule(plan:dict,max_parallel:int)->dict:
    selected={x["candidate_id"]:x for x in plan["selected"]}; done=set(); waves=[]
    while len(done)<len(selected):
        ready=sorted([x for x in selected.values() if x["candidate_id"] not in done and set(x["prerequisite_ids"])<=done],key=lambda x:(-x["utility"],x["candidate_id"]))[:max_parallel]
        if not ready: raise PlannerError("candidate dependency cycle")
        wave=len(waves)+1; waves.append({"wave":wave,"candidate_ids":[x["candidate_id"] for x in ready],"parallel_count":len(ready),"execution_status":"NOT_EXECUTED"}); done.update(x["candidate_id"] for x in ready)
    return seal({"phase":"SAED_V4_36","waves":waves,"wave_count":len(waves),"all_candidates_scheduled":True,"execution_started":False,"research_only":True},"v436_schedule","schedule_id","schedule_hash")
