from __future__ import annotations
from collections import defaultdict,deque
from copy import deepcopy
from .canonical import content_hash,stable_id,hash_chain
from .contracts import require_exact,require_list,require_unique,require_enum,require_nonnegative_int,require_positive_int
from .errors import TaskError
from .authority import authorize

TASK_KEYS=["task_id","task_type","owner_agent_id","reviewer_agent_ids","depends_on","required_capabilities","input_hashes","output_contract","budget_id","known_time_epoch","priority","protected_evidence_allowed","self_review_allowed","delegation_depth","research_only"]
TASK_TYPES={"hypothesis","data_audit","leakage_audit","model_build","causal_audit","execution_audit","statistical_challenge","evidence_curation","human_review","incident_review"}

def freeze_tasks(items:list[dict],agents:dict)->dict:
    require_list(items,"tasks",1); require_unique(items,"task_id","tasks")
    by_agent={a["agent_id"]:a for a in agents["agents"]}; ids={x["task_id"] for x in items}; normalized=[]
    for t in items:
        require_exact(t,TASK_KEYS,name="task")
        require_enum(t["task_type"],TASK_TYPES,"task_type")
        if t["owner_agent_id"] not in by_agent: raise TaskError("unknown owner")
        if set(t["reviewer_agent_ids"])-set(by_agent): raise TaskError("unknown reviewer")
        if set(t["depends_on"])-ids: raise TaskError("unknown dependency")
        if t["task_id"] in t["depends_on"]: raise TaskError("self dependency")
        require_positive_int(t["known_time_epoch"],"known_time_epoch")
        require_positive_int(t["priority"],"priority")
        require_nonnegative_int(t["delegation_depth"],"delegation_depth")
        if t["self_review_allowed"] is not False: raise TaskError("self review forbidden")
        if t["owner_agent_id"] in t["reviewer_agent_ids"]: raise TaskError("owner cannot review own task")
        if t["research_only"] is not True: raise TaskError("research_only required")
        normalized.append(deepcopy(t))
    _topological_order(normalized)
    body={"phase":"SAED_V4_32","tasks":sorted(normalized,key=lambda x:x["task_id"]),"task_count":len(normalized),"acyclic":True,"self_review_denied":True,"research_only":True}
    body["registry_id"]=stable_id("v432_task_registry",body); body["registry_hash"]=content_hash(body); return body

def _topological_order(tasks:list[dict])->list[str]:
    indeg={t["task_id"]:0 for t in tasks}; children=defaultdict(list)
    for t in tasks:
        for dep in t["depends_on"]: indeg[t["task_id"]]+=1; children[dep].append(t["task_id"])
    q=deque(sorted([k for k,v in indeg.items() if v==0])); out=[]
    while q:
        node=q.popleft(); out.append(node)
        for child in sorted(children[node]):
            indeg[child]-=1
            if indeg[child]==0: q.append(child)
    if len(out)!=len(tasks): raise TaskError("task graph contains cycle")
    return out

def build_delegation_graph(tasks:dict,agents:dict,capabilities:dict)->dict:
    by_agent={a["agent_id"]:a for a in agents["agents"]}; cap={x["capability_id"]:x for x in capabilities["capabilities"]}
    edges=[]
    for t in tasks["tasks"]:
        owner=by_agent[t["owner_agent_id"]]
        for capability_id in t["required_capabilities"]:
            if capability_id not in cap: raise TaskError("unknown required capability")
            if t["delegation_depth"]>cap[capability_id]["maximum_delegation_depth"]: raise TaskError("delegation depth exceeded")
            decision=authorize(owner,capability_id,capabilities,checkpoint_ids=["task-bound-checkpoint"] if t["protected_evidence_allowed"] else [],independent_roles=["human_reviewer","evidence_curator"] if t["protected_evidence_allowed"] else [])
            if not decision["allowed"]: raise TaskError(f"task owner unauthorized for {capability_id}")
        for reviewer_id in t["reviewer_agent_ids"]:
            edges.append({"task_id":t["task_id"],"owner_agent_id":t["owner_agent_id"],"reviewer_agent_id":reviewer_id,"owner_role":owner["role_id"],"reviewer_role":by_agent[reviewer_id]["role_id"],"self_review":False})
    body={"phase":"SAED_V4_32","edges":sorted(edges,key=lambda x:(x["task_id"],x["reviewer_agent_id"])),"acyclic":True,"self_review_edges":0,"maximum_delegation_depth":max(t["delegation_depth"] for t in tasks["tasks"]),"research_only":True}
    body["graph_id"]=stable_id("v432_delegation_graph",body); body["graph_hash"]=content_hash(body); return body

def issue_tokens(tasks:dict,agents:dict,capabilities:dict)->dict:
    by_agent={a["agent_id"]:a for a in agents["agents"]}; tokens=[]
    for t in tasks["tasks"]:
        owner=by_agent[t["owner_agent_id"]]
        for cid in sorted(t["required_capabilities"]):
            decision=authorize(owner,cid,capabilities,checkpoint_ids=["task-bound-checkpoint"] if t["protected_evidence_allowed"] else [],independent_roles=["human_reviewer","evidence_curator"] if t["protected_evidence_allowed"] else [])
            if not decision["allowed"]: raise TaskError("cannot issue denied token")
            token={"task_id":t["task_id"],"agent_id":owner["agent_id"],"role_id":owner["role_id"],"capability_id":cid,"known_time_epoch":t["known_time_epoch"],"expires_after_task":True,"delegable":t["delegation_depth"]>0,"delegation_depth":t["delegation_depth"],"live_authority":False,"research_only":True}
            token["token_id"]=stable_id("v432_capability_token",token); token["token_hash"]=content_hash(token); tokens.append(token)
    body={"phase":"SAED_V4_32","tokens":sorted(tokens,key=lambda x:(x["task_id"],x["capability_id"])),"ephemeral":True,"scope_bound":True,"live_authority_tokens":0,"research_only":True}
    body["ledger_id"]=stable_id("v432_token_ledger",body); body["ledger_hash"]=content_hash(body); return body

def deterministic_plan(tasks:dict)->dict:
    order=_topological_order(tasks["tasks"]); lookup={t["task_id"]:t for t in tasks["tasks"]}
    order=sorted(order,key=lambda tid:(lookup[tid]["known_time_epoch"],lookup[tid]["priority"],tid))
    # restore dependency correctness with deterministic Kahn scheduling
    pending={t["task_id"]:set(t["depends_on"]) for t in tasks["tasks"]}; done=[]; trace=[]
    while pending:
        ready=[tid for tid,deps in pending.items() if not deps]
        if not ready: raise TaskError("scheduler deadlock")
        tid=min(ready,key=lambda x:(lookup[x]["known_time_epoch"],lookup[x]["priority"],x)); t=lookup[tid]
        trace.append({"step":len(trace),"task_id":tid,"owner_agent_id":t["owner_agent_id"],"task_type":t["task_type"],"known_time_epoch":t["known_time_epoch"],"priority":t["priority"],"dependency_count":len(t["depends_on"]),"state":"scheduled"})
        done.append(tid); pending.pop(tid)
        for deps in pending.values(): deps.discard(tid)
    body={"phase":"SAED_V4_32","ordered_task_ids":done,"task_count":len(done),"dependency_preserving":True,"known_time_ordered":True,"deterministic":True,"research_only":True}
    body["plan_id"]=stable_id("v432_execution_plan",body); body["plan_hash"]=content_hash(body)
    chained=hash_chain(trace,"v432_scheduler_event")
    scheduler={"phase":"SAED_V4_32","plan_id":body["plan_id"],"events":chained,"event_count":len(chained),"final_event_hash":chained[-1]["event_hash"] if chained else "0"*64,"network_access":False,"deterministic":True,"research_only":True}
    scheduler["trace_id"]=stable_id("v432_scheduler_trace",scheduler); scheduler["trace_hash"]=content_hash(scheduler)
    return {"plan":body,"trace":scheduler}
