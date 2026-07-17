from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique,require_nonnegative_int
from .errors import BudgetError

BUDGET_KEYS=["budget_id","task_family","compute_units","tool_calls","source_reads","protected_exposures","human_review_minutes","max_agent_steps","hard_stop","research_only"]

def freeze_budgets(items:list[dict])->dict:
    require_list(items,"budgets",1); require_unique(items,"budget_id","budgets"); normalized=[]
    for b in items:
        require_exact(b,BUDGET_KEYS,name="budget")
        for k in ["compute_units","tool_calls","source_reads","protected_exposures","human_review_minutes","max_agent_steps"]: require_nonnegative_int(b[k],k)
        if b["hard_stop"] is not True or b["research_only"] is not True: raise BudgetError("hard stop and research only required")
        normalized.append(deepcopy(b))
    body={"phase":"SAED_V4_32","budgets":sorted(normalized,key=lambda x:x["budget_id"]),"hard_stop":True,"research_only":True}
    body["policy_id"]=stable_id("v432_budget_policy",body); body["policy_hash"]=content_hash(body); return body

def account(budgets:dict,tasks:dict)->dict:
    by={b["budget_id"]:b for b in budgets["budgets"]}; counts={k:0 for k in by}; rows=[]
    for t in tasks["tasks"]:
        bid=t["budget_id"]
        if bid not in by: raise BudgetError("task references unknown budget")
        counts[bid]+=1
    for bid,b in sorted(by.items()):
        used={"compute_units":counts[bid]*3,"tool_calls":counts[bid]*2,"source_reads":counts[bid]*4,"protected_exposures":sum(1 for t in tasks["tasks"] if t["budget_id"]==bid and t["protected_evidence_allowed"]),"human_review_minutes":counts[bid]*5,"agent_steps":counts[bid]*6}
        limits={"compute_units":b["compute_units"],"tool_calls":b["tool_calls"],"source_reads":b["source_reads"],"protected_exposures":b["protected_exposures"],"human_review_minutes":b["human_review_minutes"],"agent_steps":b["max_agent_steps"]}
        over=[k for k in limits if used[k]>limits[k]]
        rows.append({"budget_id":bid,"task_family":b["task_family"],"used":used,"limits":limits,"within_budget":not over,"overrun_dimensions":over,"hard_stop_triggered":bool(over)})
    if any(not r["within_budget"] for r in rows): raise BudgetError("reference workload exceeds hard budget")
    body={"phase":"SAED_V4_32","rows":rows,"all_within_budget":True,"hard_stop_events":0,"protected_exposure_total":sum(r["used"]["protected_exposures"] for r in rows),"research_only":True}
    body["ledger_id"]=stable_id("v432_budget_ledger",body); body["ledger_hash"]=content_hash(body); return body
