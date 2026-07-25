from __future__ import annotations
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique
from .errors import VerificationError

OBLIGATION_KEYS=["obligation_id","claim","kind","targets","criticality","discharge_rule","owner"]

def freeze_registry(items:list)->dict:
    require_list(items,"proof_obligations",1); require_unique(items,"obligation_id","proof_obligations")
    for item in items:
        require_exact(item,OBLIGATION_KEYS,name="proof_obligation")
        if item["kind"] not in {"invariants","temporal","mutation","hazard_coverage","assurance_case","authority","upstream","replay","independent_reproduction","contract_closure"}: raise VerificationError("unsupported obligation kind")
    body={"phase":"SAED_V4_31","obligations":items,"count":len(items),"frozen":True,"research_only":True}
    body["registry_id"]=stable_id("v431_proof_registry",body); body["registry_hash"]=content_hash(body); return body

def discharge(registry:dict,evidence:dict)->dict:
    statuses=[]
    for item in registry["obligations"]:
        kind=item["kind"]
        if kind=="invariants": passed=evidence["invariant_report"]["passed"] and all(next(x for x in evidence["invariant_report"]["results"] if x["invariant_id"]==target)["passed"] for target in item["targets"])
        elif kind=="temporal": passed=evidence["temporal_report"]["passed"] and all(next(x for x in evidence["temporal_report"]["results"] if x["property_id"]==target)["passed"] for target in item["targets"])
        elif kind=="mutation": passed=evidence["mutation_scorecard"]["score"]>=1.0 and evidence["mutation_scorecard"]["survivor_count"]==0
        elif kind=="hazard_coverage": passed=evidence["mitigation_coverage"]["all_hazards_controlled"] and evidence["residual_risk"]["all_within_threshold"]
        elif kind=="assurance_case": passed=evidence["assurance_case"]["valid"] and evidence["traceability"]["complete"]
        elif kind=="authority": passed=not any(evidence["authority"]["authority"].values())
        elif kind=="upstream": passed=evidence["upstream"]["verified"]
        elif kind=="replay": passed=evidence["replay"]["deterministic"] and evidence["replay"]["future_suffix_invariant"]
        elif kind=="independent_reproduction": passed=evidence["reproduction"]["exact_match"]
        elif kind=="contract_closure": passed=evidence["contract_closure"]["closed"] and evidence["contract_closure"]["unknown_fields_allowed"] is False
        else: passed=False
        statuses.append({"obligation_id":item["obligation_id"],"kind":kind,"passed":bool(passed),"criticality":item["criticality"],"targets":item["targets"],"evidence_hashes":{key:content_hash(value) for key,value in evidence.items() if key in {"invariant_report","temporal_report","mutation_scorecard","mitigation_coverage","residual_risk","assurance_case","traceability","authority","upstream","replay","reproduction","contract_closure"}}})
    body={"phase":"SAED_V4_31","registry_id":registry["registry_id"],"statuses":statuses,"discharged_count":sum(x["passed"] for x in statuses),"total_count":len(statuses),"all_discharged":all(x["passed"] for x in statuses),"fail_closed":True,"research_only":True}
    body["ledger_id"]=stable_id("v431_proof_ledger",body); body["ledger_hash"]=content_hash(body); return body
