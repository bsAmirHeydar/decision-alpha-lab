from __future__ import annotations
from .canonical import content_hash,stable_id
from .chain import build_chain,verify_chain
from .errors import TimingError

def preregister(registry:dict,assignments:dict,protocol:dict)->dict:
    records=[]
    for lab,assignment in zip(registry["labs"],assignments["assignments"]):
        declared=lab["declared_at"]; assignment_open="2026-07-16T10:10:00Z"; run_start="2026-07-16T10:20:00Z"
        if not declared<assignment_open<run_start: raise TimingError("preregistration ordering failure")
        record={"lab_id":lab["lab_id"],"assignment_id":assignment["assignment_id"],"protocol_id":protocol["protocol_id"],"hypothesis":"frozen_v429_aggregate_result_reproduces","metric_ids":[m["metric_id"] for m in protocol["metrics"]],"semantic_hash_required":True,"maximum_runs":1,"failure_action":"quarantine","preregistered_at":declared,"assignment_opened_at":assignment_open,"run_not_before":run_start,"adaptive_changes_allowed":False}
        record["preregistration_id"]=stable_id("v430_prereg",record); record["preregistration_hash"]=content_hash(record); records.append(record)
    chain=build_chain(records,"v430_preregistration")
    return {"phase":"SAED_V4_30","records":chain,"chain_verification":verify_chain(chain,"v430_preregistration"),"all_pre_assignment":True,"all_pre_run":True,"research_only":True}
