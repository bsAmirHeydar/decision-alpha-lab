from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_num,require_list,require_unique
from .errors import RiskError
from .canonical import seal

DIMENSIONS=["conceptual_soundness","data_risk","validation_risk","operational_risk","cyber_supply_chain_risk","explainability_risk","change_risk","concentration_risk","third_party_risk","governance_risk"]
def tier_models(models:dict,inputs:list[dict])->dict:
    inputs=require_list(inputs,"tier_inputs",len(models["records"])); require_unique(inputs,"model_id","tier_inputs"); mids={m["model_id"] for m in models["records"]}; rows=[]
    for x in inputs:
        require_exact(x,["model_id","decision_materiality","maximum_capital_at_risk","automation_level","external_dependency","irreversibility","customer_or_market_impact"])
        if x["model_id"] not in mids: raise RiskError("tier unknown model")
        scores=[x["decision_materiality"],x["automation_level"],x["irreversibility"],x["customer_or_market_impact"]]
        for i,s in enumerate(scores): require_num(s,f"tier score {i}",0,5)
        require_num(x["maximum_capital_at_risk"],"capital",0)
        raw=sum(scores)+(2 if x["external_dependency"] else 0)+(2 if x["maximum_capital_at_risk"]>0 else 0)
        tier="TIER_1" if raw>=16 else "TIER_2" if raw>=11 else "TIER_3" if raw>=6 else "TIER_4"
        rows.append(deepcopy(x)|{"raw_score":raw,"risk_tier":tier,"production_capital_authority":False})
    return seal({"phase":"SAED_V4_35","assignments":sorted(rows,key=lambda x:x["model_id"]),"tier_method":"deterministic-materiality-v1","research_only":True},"v435_tiers","registry_id","registry_hash")

def scorecards(models:dict,tiering:dict,assessments:list[dict])->dict:
    assessments=require_list(assessments,"assessments",len(models["records"])); require_unique(assessments,"model_id","assessments"); tier={x["model_id"]:x["risk_tier"] for x in tiering["assignments"]}; rows=[]
    for a in assessments:
        require_exact(a,["model_id","dimension_scores","open_findings","validation_coverage","monitoring_readiness","owner_attestation"])
        if set(a["dimension_scores"])!=set(DIMENSIONS): raise RiskError("risk dimensions incomplete")
        scores={k:require_num(v,k,0,5) for k,v in a["dimension_scores"].items()}; require_num(a["validation_coverage"],"coverage",0,1); require_num(a["monitoring_readiness"],"monitoring",0,1)
        weighted=round(sum(scores.values())/len(scores),6); blocking=a["open_findings"]>0 or a["validation_coverage"]<0.95 or a["monitoring_readiness"]<0.9 or not a["owner_attestation"]
        rows.append({"model_id":a["model_id"],"risk_tier":tier[a["model_id"]],"dimension_scores":scores,"aggregate_risk_score":weighted,"open_findings":a["open_findings"],"validation_coverage":a["validation_coverage"],"monitoring_readiness":a["monitoring_readiness"],"blocking":blocking,"production_authorized":False})
    return seal({"phase":"SAED_V4_35","scorecards":sorted(rows,key=lambda x:x["model_id"]),"all_dimensions_present":True,"research_only":True},"v435_scorecards","registry_id","registry_hash")
