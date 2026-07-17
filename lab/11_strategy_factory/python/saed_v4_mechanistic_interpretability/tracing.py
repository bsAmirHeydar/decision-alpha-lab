from __future__ import annotations
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import CausalTraceContract
from .model import forward

def trace(records:list[dict[str,Any]], contract:CausalTraceContract, ledger:ResearchLedger)->dict[str,Any]:
    rows=[]
    for r in records:
        base=forward(r); interventions=[]
        for layer_id,values in zip(r["layer_ids"],[base["layer1"],base["layer2"]]):
            for idx in range(min(len(values),contract.maximum_neurons_per_layer)):
                changed=list(values); changed[idx]=0.0
                score=forward(r,layer1_override=changed)["score"] if layer_id=="representation_1" else forward(r,layer2_override=changed)["score"]
                interventions.append({"layer_id":layer_id,"neuron_index":idx,"baseline_activation":values[idx],"patched_activation":0.0,"score_delta":base["score"]-score})
                ledger.consume("trace_interventions",1,{"record_id":r["record_id"],"layer":layer_id,"neuron":idx})
        rows.append({"record_id":r["record_id"],"interventions":interventions})
    payload={"phase":"SAED_V4_26","intervention":"zero_activation","records":rows,"claim_class":"causal_trace_challenger_not_causal_proof","deterministic":True}
    payload["causal_trace_bundle_id"]=stable_id("causal_trace",payload); payload["causal_trace_bundle_hash"]=content_hash(payload)
    return payload

def patch(records:list[dict[str,Any]], contract:CausalTraceContract, ledger:ResearchLedger)->dict[str,Any]:
    rows=[]
    ordered=sorted(records,key=lambda r:(r["model_id"],r["context_id"],r["decision_time"],r["record_id"]))
    history={}
    for r in ordered:
        key=(r["model_id"],r["context_id"]); base=forward(r); source=history.get(key)
        if source is None:
            rows.append({"record_id":r["record_id"],"source_record_id":None,"eligible":False,"reason":"no_past_same_model_context_source","score_delta":0.0})
        else:
            source_state=forward(source)["layer2"]; patched=forward(r,layer2_override=source_state)["score"]
            rows.append({"record_id":r["record_id"],"source_record_id":source["record_id"],"eligible":True,"reason":"past_same_model_context_source","score_delta":patched-base["score"]})
            ledger.consume("patch_interventions",1,{"record_id":r["record_id"],"source_record_id":source["record_id"]})
        history[key]=r
    payload={"phase":"SAED_V4_26","records":rows,"past_only":True,"same_model_required":True,"claim_class":"activation_patching_challenger"}
    payload["activation_patch_bundle_id"]=stable_id("activation_patch",payload); payload["activation_patch_bundle_hash"]=content_hash(payload)
    return payload
