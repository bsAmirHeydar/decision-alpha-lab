from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique
from .errors import SafetyCaseError

HAZARD_KEYS=["hazard_id","title","unsafe_control_action","severity","likelihood","detectability","control_ids","proof_obligation_ids","acceptance_threshold"]
CONTROL_KEYS=["control_id","title","constraint","verification_ids","effectiveness","owner","failure_action"]

def freeze_hazards(items:list)->dict:
    require_list(items,"hazards",1); require_unique(items,"hazard_id","hazards")
    for x in items:
        require_exact(x,HAZARD_KEYS,name="hazard")
        for field in ["severity","likelihood","detectability"]:
            if not isinstance(x[field],int) or not 1<=x[field]<=5: raise SafetyCaseError(f"invalid {field}")
        if not x["control_ids"] or not x["proof_obligation_ids"]: raise SafetyCaseError("hazard controls and obligations required")
    body={"phase":"SAED_V4_31","hazards":items,"count":len(items),"method":"closed_stpa_fmea_hybrid_reference","research_only":True}
    body["register_id"]=stable_id("v431_hazard_register",body); body["register_hash"]=content_hash(body); return body

def freeze_controls(items:list)->dict:
    require_list(items,"controls",1); require_unique(items,"control_id","controls")
    for x in items:
        require_exact(x,CONTROL_KEYS,name="control")
        if not 0<x["effectiveness"]<=1: raise SafetyCaseError("invalid effectiveness")
        if x["failure_action"] not in {"reject","quarantine","abstain"}: raise SafetyCaseError("unsafe failure action")
    body={"phase":"SAED_V4_31","controls":items,"count":len(items),"closed":True,"research_only":True}
    body["catalog_id"]=stable_id("v431_control_catalog",body); body["catalog_hash"]=content_hash(body); return body

def build_safety_constraints(controls:dict)->dict:
    constraints=[{"constraint_id":f"SC-{i:03d}","control_id":x["control_id"],"statement":x["constraint"],"failure_action":x["failure_action"],"verification_ids":x["verification_ids"],"mandatory":True} for i,x in enumerate(controls["controls"],1)]
    body={"phase":"SAED_V4_31","constraints":constraints,"count":len(constraints),"closed":True,"research_only":True}
    body["catalog_id"]=stable_id("v431_safety_constraints",body); body["catalog_hash"]=content_hash(body); return body

def assess(hazards:dict,controls:dict,proof_ids:set[str],passed_verification_ids:set[str])->tuple[dict,dict]:
    control_map={x["control_id"]:x for x in controls["controls"]}; coverage=[]; residual=[]
    for hazard in hazards["hazards"]:
        missing=[x for x in hazard["control_ids"] if x not in control_map]
        unverified=[]; combined=1.0
        for cid in hazard["control_ids"]:
            if cid in control_map:
                control=control_map[cid]; combined*=1-control["effectiveness"]
                if not set(control["verification_ids"]).issubset(passed_verification_ids): unverified.append(cid)
        obligation_missing=[x for x in hazard["proof_obligation_ids"] if x not in proof_ids]
        gross=hazard["severity"]*hazard["likelihood"]*hazard["detectability"]
        residual_score=round(gross*combined,6)
        controlled=not missing and not unverified and not obligation_missing and residual_score<=hazard["acceptance_threshold"]
        coverage.append({"hazard_id":hazard["hazard_id"],"control_ids":hazard["control_ids"],"missing_controls":missing,"unverified_controls":unverified,"missing_obligations":obligation_missing,"controlled":controlled})
        residual.append({"hazard_id":hazard["hazard_id"],"gross_risk_score":gross,"residual_risk_score":residual_score,"acceptance_threshold":hazard["acceptance_threshold"],"accepted":controlled,"acceptance_authority":"research_reference_only","production_acceptance":False})
    matrix={"phase":"SAED_V4_31","rows":coverage,"all_hazards_controlled":all(x["controlled"] for x in coverage),"hazard_count":len(coverage),"research_only":True}
    matrix["matrix_id"]=stable_id("v431_mitigation_coverage",matrix); matrix["matrix_hash"]=content_hash(matrix)
    ledger={"phase":"SAED_V4_31","entries":residual,"all_within_threshold":all(x["accepted"] for x in residual),"unaccepted_count":sum(not x["accepted"] for x in residual),"residual_risk_eliminated_claim":False,"research_only":True}
    ledger["ledger_id"]=stable_id("v431_residual_risk",ledger); ledger["ledger_hash"]=content_hash(ledger)
    return matrix,ledger
