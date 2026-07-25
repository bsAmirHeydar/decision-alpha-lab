from __future__ import annotations
from typing import Any
from .budget import ResearchLedger
from .canonical import content_hash, stable_id
from .contracts import ConceptProbeContract
from .model import forward
from .numerics import cosine, mean

def run(records:list[dict[str,Any]], contract:ConceptProbeContract, ledger:ResearchLedger)->dict[str,Any]:
    rows=[]; margins=[]
    for r in records:
        hidden=forward(r)["layer2"]
        concepts=[]
        for name,vector in zip(contract.concept_names,contract.concept_vectors):
            signal=cosine(hidden,vector); control=cosine(hidden,tuple(reversed(vector))); margin=abs(signal)-abs(control); margins.append(margin)
            concepts.append({"concept":name,"activation":signal,"random_control_activation":control,"signal_over_random":margin})
            ledger.consume("concept_probes",2,{"record_id":r["record_id"],"concept":name})
        rows.append({"record_id":r["record_id"],"concepts":concepts})
    aggregate=mean(margins)
    payload={"phase":"SAED_V4_26","records":rows,"concept_count":len(contract.concept_names),"mean_signal_over_random":aggregate,"random_control_required":True,"reference_gate_passed":aggregate>=contract.minimum_signal_over_random,"claim_class":"associational_probe_only"}
    payload["concept_probe_bundle_id"]=stable_id("concept_probe",payload); payload["concept_probe_bundle_hash"]=content_hash(payload)
    return payload
