from __future__ import annotations
from copy import deepcopy
from .canonical import seal
from .contracts import require_exact,require_num
from .errors import PlannerError

FIELDS=["information_gain","uncertainty_reduction","novelty","negative_knowledge_value","replication_value","coverage_gain","reusability","cost_efficiency","risk_penalty","exposure_penalty"]

def freeze_weights(v:dict)->dict:
    require_exact(v,["weight_id","weights","exploration_floor","replication_floor","negative_knowledge_floor","risk_hard_limit","minimum_utility","research_only"])
    if set(v["weights"])!=set(FIELDS): raise PlannerError("weight dimensions invalid")
    for k,x in v["weights"].items(): require_num(x,f"weight.{k}",0)
    for k in ["exploration_floor","replication_floor","negative_knowledge_floor"]: require_num(v[k],k,0,1)
    require_num(v["risk_hard_limit"],"risk_hard_limit",0,1); require_num(v["minimum_utility"],"minimum_utility",-10,10)
    if v["research_only"] is not True: raise PlannerError("weights must be research-only")
    return seal(deepcopy(v)|{"phase":"SAED_V4_36"},"v436_weights","weight_receipt_id","weight_hash")

def score_candidates(items:list[dict],weights:dict,risk_findings:list[dict])->dict:
    risk_by={x["candidate_id"]:x for x in risk_findings}; rows=[]
    for x in items:
        require_exact(x,["candidate_id","title","family","objective_id","gap_ids","prerequisite_ids","compute_units","exposure_units","review_hours","risk","information_gain","uncertainty_reduction","novelty","negative_knowledge_value","replication_value","coverage_gain","reusability","cost_efficiency","synthetic_fixture"])
        for k in ["risk","information_gain","uncertainty_reduction","novelty","negative_knowledge_value","replication_value","coverage_gain","reusability","cost_efficiency"]: require_num(x[k],k,0,1)
        rf=risk_by.get(x["candidate_id"],{"blocking":False,"residual_risk":x["risk"]}); blocked=bool(rf["blocking"] or x["risk"]>weights["risk_hard_limit"])
        dims={k:x[k] for k in FIELDS if k not in ["risk_penalty","exposure_penalty"]}; dims["risk_penalty"]=x["risk"]; dims["exposure_penalty"]=min(1.0,x["exposure_units"]/(1+x["exposure_units"]))
        utility=sum(weights["weights"][k]*(dims[k] if k not in ["risk_penalty","exposure_penalty"] else -dims[k]) for k in FIELDS)
        rows.append(deepcopy(x)|{"dimensions":dims,"utility":round(utility,8),"risk_blocked":blocked,"eligible":not blocked and utility>=weights["minimum_utility"]})
    rows=sorted(rows,key=lambda x:(-x["utility"],x["risk"],x["candidate_id"])); return seal({"phase":"SAED_V4_36","candidates":rows,"candidate_count":len(rows),"eligible_count":sum(x["eligible"] for x in rows),"research_only":True},"v436_scores","scorecard_id","scorecard_hash")
