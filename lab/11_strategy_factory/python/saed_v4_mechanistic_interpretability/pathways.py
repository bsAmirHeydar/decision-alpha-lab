from __future__ import annotations
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import PathwayContract
from .model import forward

def run(records:list[dict[str,Any]], contract:PathwayContract, ledger:ResearchLedger)->dict[str,Any]:
    rows=[]
    for r in records:
        full=forward(r)["score"]
        deltas={
          "transfer":full-forward(r,transfer=False)["score"],
          "adaptation":full-forward(r,adaptation=False)["score"],
          "calibration":full-forward(r,calibration=False)["score"],
          "view_fusion":full-forward(r,views=[0.0]*len(r["view_values"]))["score"],
          "treatment_interaction":full-forward(r,interactions=False)["score"],
        }
        for name in contract.allowed_pathways: ledger.consume("pathway_ablations",1,{"record_id":r["record_id"],"pathway":name})
        total=sum(abs(v) for v in deltas.values()) or 1.0
        concentration=max(abs(v)/total for v in deltas.values())
        rows.append({"record_id":r["record_id"],"score":full,"pathways":[{"pathway":k,"score_delta":deltas[k],"absolute_share":abs(deltas[k])/total} for k in sorted(deltas)],"maximum_pathway_concentration":concentration,"concentration_breach":concentration>contract.maximum_pathway_concentration})
    payload={"phase":"SAED_V4_26","method":contract.ablation_method,"records":rows,"baseline_preserved":True,"deterministic":True}
    payload["pathway_bundle_id"]=stable_id("mechanistic_pathways",payload); payload["pathway_bundle_hash"]=content_hash(payload)
    return payload

def adaptation_attributions(records:list[dict[str,Any]])->dict[str,Any]:
    rows=[]
    for r in records:
        full=forward(r)["score"]; effects=[]
        for i,name in enumerate(r["feature_names"]):
            changed=dict(r); changed["adaptation_deltas"]=list(r["adaptation_deltas"]); changed["adaptation_deltas"][i]=0.0
            effects.append({"parameter":name,"parameter_delta":r["adaptation_deltas"][i],"score_delta":full-forward(changed)["score"]})
        rows.append({"record_id":r["record_id"],"effects":effects})
    payload={"phase":"SAED_V4_26","records":rows,"support_only_frozen_adaptation":True}
    payload["adaptation_mechanism_id"]=stable_id("adaptation_mechanism",payload); payload["adaptation_mechanism_hash"]=content_hash(payload)
    return payload

def calibration_attributions(records:list[dict[str,Any]])->dict[str,Any]:
    names=["support","ood","conformal_margin"]
    rows=[]
    for r in records:
        full=forward(r)["score"]; effects=[]
        for i,name in enumerate(names):
            changed=dict(r); changed["calibration_components"]=list(r["calibration_components"]); changed["calibration_components"][i]=0.0
            effects.append({"component":name,"component_value":r["calibration_components"][i],"score_delta":full-forward(changed)["score"]})
        rows.append({"record_id":r["record_id"],"effects":effects})
    payload={"phase":"SAED_V4_26","records":rows,"past_only_calibration":True,"runtime_mutation":False}
    payload["calibration_mechanism_id"]=stable_id("calibration_mechanism",payload); payload["calibration_mechanism_hash"]=content_hash(payload)
    return payload
