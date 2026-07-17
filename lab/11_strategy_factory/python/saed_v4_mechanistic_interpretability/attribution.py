from __future__ import annotations
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import AttributionContract
from .model import forward
from .numerics import cosine

def integrated_gradients(record:dict[str,Any], contract:AttributionContract)->list[float]:
    x=record["feature_values"]; baseline=[contract.baseline_value]*len(x); steps=contract.integration_steps; eps=1e-5
    out=[]
    for j in range(len(x)):
        gradient=0.0
        for step in range(1,steps+1):
            alpha=step/steps; point=[baseline[i]+alpha*(x[i]-baseline[i]) for i in range(len(x))]
            plus=list(point); minus=list(point); plus[j]+=eps; minus[j]-=eps
            gradient+=(forward(record,features=plus)["score"]-forward(record,features=minus)["score"])/(2*eps)
        out.append((x[j]-baseline[j])*gradient/steps)
    return out

def run(records:list[dict[str,Any]], contract:AttributionContract, ledger:ResearchLedger)->dict[str,Any]:
    rows=[]
    for r in records:
        ig=integrated_gradients(r,contract); full=forward(r)["score"]
        occlusion=[]
        for i,name in enumerate(r["feature_names"]):
            x=list(r["feature_values"]); x[i]=contract.baseline_value
            delta=full-forward(r,features=x)["score"]; occlusion.append(delta)
            ledger.consume("feature_ablations",1,{"record_id":r["record_id"],"feature":name})
        views=[]
        for i,name in enumerate(r["view_names"]):
            v=list(r["view_values"]); v[i]=0.0
            views.append({"view":name,"score_delta":full-forward(r,views=v)["score"]})
        abs_sum=sum(abs(x) for x in ig) or 1.0
        normalized=[x/abs_sum for x in ig]
        concentration=max(abs(x) for x in normalized)
        rows.append({"record_id":r["record_id"],"model_id":r["model_id"],"context_id":r["context_id"],"decision_time":r["decision_time"],"score":full,"baseline_score":r["baseline_score"],"feature_attributions":[{"feature":n,"integrated_gradient":ig[i],"occlusion_delta":occlusion[i],"normalized_attribution":normalized[i]} for i,n in enumerate(r["feature_names"])],"view_attributions":views,"completeness_residual":(full-r["baseline_score"])-sum(ig),"maximum_feature_concentration":concentration,"concentration_breach":concentration>contract.maximum_feature_concentration})
    payload={"phase":"SAED_V4_26","method":contract.method,"integration_steps":contract.integration_steps,"records":rows,"record_count":len(rows),"deterministic":True,"future_suffix_queries":0}
    payload["attribution_bundle_id"]=stable_id("frozen_feature_attribution",payload); payload["attribution_bundle_hash"]=content_hash(payload)
    return payload
