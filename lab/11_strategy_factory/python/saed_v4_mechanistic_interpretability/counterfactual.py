from __future__ import annotations
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import CounterfactualContract
from .model import forward

def run(records:list[dict[str,Any]], contract:CounterfactualContract, ledger:ResearchLedger)->dict[str,Any]:
    rows=[]
    for r in records:
        base=forward(r)["score"]; target_above=base<contract.decision_threshold; candidates=[]
        for i,name in enumerate(r["feature_names"]):
            for delta in contract.perturbation_grid:
                if abs(delta)>contract.maximum_absolute_perturbation or delta==0: continue
                x=list(r["feature_values"]); x[i]+=delta; score=forward(r,features=x)["score"]
                crossed=score>=contract.decision_threshold if target_above else score<contract.decision_threshold
                candidates.append({"feature":name,"feature_index":i,"delta":delta,"score":score,"crossed":crossed})
                ledger.consume("counterfactual_trials",1,{"record_id":r["record_id"],"feature":name,"delta":delta})
        eligible=[c for c in candidates if c["crossed"]]
        best=sorted(eligible,key=lambda c:(abs(c["delta"]),c["feature"],c["delta"]))[0] if eligible else None
        rows.append({"record_id":r["record_id"],"original_score":base,"decision_threshold":contract.decision_threshold,"target_direction":"above" if target_above else "below","counterfactual_found":best is not None,"counterfactual":best,"safe_fallback":"abstain" if best is None else "research_explanation_only"})
    payload={"phase":"SAED_V4_26","records":rows,"single_feature_only":True,"immutable_model":True,"decision_authority":False}
    payload["counterfactual_bundle_id"]=stable_id("counterfactual_explanation",payload); payload["counterfactual_bundle_hash"]=content_hash(payload)
    return payload
