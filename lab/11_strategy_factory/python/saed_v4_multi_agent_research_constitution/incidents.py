from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id,hash_chain
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import IncidentError

INC_KEYS=["incident_id","incident_type","detected_by_agent_id","affected_task_ids","trigger","severity","automatic_response","human_review_required","counterexamples_preserved","status","research_only"]
TYPES={"authority_violation","protected_exposure_attempt","budget_overrun","memory_boundary_attempt","self_approval_attempt","source_lineage_break","future_suffix_exposure","counterexample_suppression_attempt","constitution_amendment_attempt"}
SEV={"medium","high","critical"}
RESP={"reject","quarantine","stop_family","revoke_tokens","manual_review"}

def build_incident_ledger(items:list[dict],agents:dict,tasks:dict)->dict:
    require_list(items,"incidents",1); require_unique(items,"incident_id","incidents")
    agent_ids={a["agent_id"] for a in agents["agents"]}; task_ids={t["task_id"] for t in tasks["tasks"]}; rows=[]
    for x in items:
        require_exact(x,INC_KEYS,name="incident")
        require_enum(x["incident_type"],TYPES,"incident_type"); require_enum(x["severity"],SEV,"severity"); require_enum(x["automatic_response"],RESP,"automatic_response")
        if x["detected_by_agent_id"] not in agent_ids or set(x["affected_task_ids"])-task_ids: raise IncidentError("unknown incident reference")
        if x["human_review_required"] is not True or x["counterexamples_preserved"] is not True: raise IncidentError("incident safety controls missing")
        if x["status"] not in {"contained_synthetic","open_review"}: raise IncidentError("incident status invalid")
        if x["research_only"] is not True: raise IncidentError("research_only required")
        rows.append(deepcopy(x))
    chained=hash_chain(sorted(rows,key=lambda x:x["incident_id"]),"v432_incident")
    body={"phase":"SAED_V4_32","events":chained,"incident_count":len(chained),"critical_count":sum(x["severity"]=="critical" for x in chained),"automatic_containment":True,"counterexamples_preserved":True,"human_review_required":True,"research_only":True}
    body["ledger_id"]=stable_id("v432_incident_ledger",body); body["ledger_hash"]=content_hash(body); return body
