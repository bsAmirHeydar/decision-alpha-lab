from __future__ import annotations
from .canonical import content_hash,stable_id
from .chain import build_chain,verify_chain
from .errors import RunBudgetError,IntegrityError

def deterministic_metrics(payload:dict)->dict:
    rows=payload["aggregate_reference_rows"]
    n=len(rows); accuracy=sum(int(r["prediction"]==r["label"]) for r in rows)/n
    brier=sum((float(r["probability"])-int(r["label"]))**2 for r in rows)/n
    mean_probability=sum(float(r["probability"]) for r in rows)/n
    return {"accuracy":round(accuracy,12),"brier":round(brier,12),"mean_probability":round(mean_probability,12),"sample_count":n}

def execute(registry:dict,assignments:dict,prereg:dict,environments:dict,package:dict,protocol:dict,payload:dict)->tuple[dict,dict]:
    if payload.get("payload_commitment_hash")!=package["payload_commitment_hash"]: raise IntegrityError("payload commitment mismatch")
    metric_values=deterministic_metrics(payload)
    semantic={"metric_values":metric_values,"protocol_hash":protocol["protocol_hash"],"package_hash":package["package_hash"],"implementation_contract":"v430_reference_v1"}
    semantic_hash=content_hash(semantic)
    run_records=[]; result_records=[]
    for lab,assignment,pre,env in zip(registry["labs"],assignments["assignments"],prereg["records"],environments["attestations"]):
        if assignment["maximum_runs"]!=1 or pre["maximum_runs"]!=1: raise RunBudgetError("run budget not one")
        run={"lab_id":lab["lab_id"],"assignment_id":assignment["assignment_id"],"preregistration_id":pre["preregistration_id"],"environment_id":env["environment_id"],"package_id":package["package_id"],"run_ordinal":1,"started_at":"2026-07-16T10:20:00Z","completed_at":"2026-07-16T10:20:01Z","retry_count":0,"network_access":False,"package_installation":False,"interactive_adaptation":False,"future_suffix_records_seen":0,"status":"completed"}
        run["run_id"]=stable_id("v430_run",run); run["run_hash"]=content_hash(run); run_records.append(run)
        result={"lab_id":lab["lab_id"],"run_id":run["run_id"],"package_id":package["package_id"],"protocol_id":protocol["protocol_id"],"environment_id":env["environment_id"],"semantic_output_hash":semantic_hash,"aggregate_metrics":dict(metric_values),"raw_rows_exported":False,"hidden_labels_exported":False,"candidate_identity_revealed":False,"result_status":"completed","research_only":True}
        result["result_id"]=stable_id("v430_result",result); result["result_hash"]=content_hash(result); result_records.append(result)
    runs=build_chain(run_records,"v430_run")
    results=build_chain(result_records,"v430_result")
    return ({"phase":"SAED_V4_30","records":runs,"chain_verification":verify_chain(runs,"v430_run"),"run_count":len(runs),"retry_count":0,"one_run_per_lab":True,"research_only":True},
            {"phase":"SAED_V4_30","records":results,"chain_verification":verify_chain(results,"v430_result"),"result_count":len(results),"aggregate_only":True,"research_only":True})
