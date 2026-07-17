from __future__ import annotations
from .canonical import content_hash,stable_id
from .chain import build_chain,verify_chain

def adjudicate(registry:dict,independence:dict,runs:dict,results:dict,semantic:dict,metrics:dict,protocol:dict)->tuple[dict,dict]:
    issues=[]
    if not independence["all_pairs_independent"]: issues.append({"class":"identity_independence","severity":"critical"})
    if runs["run_count"]!=registry["eligible_lab_count"] or not runs["one_run_per_lab"]: issues.append({"class":"run_accounting","severity":"critical"})
    if not semantic["all_match"]: issues.append({"class":"semantic_hash","severity":"critical"})
    if not metrics["all_within_tolerance"]: issues.append({"class":"metric_tolerance","severity":"critical"})
    accepted=not issues and registry["eligible_lab_count"]>=protocol["minimum_labs"]
    decision="accept_synthetic_reference" if accepted else "quarantine"
    record={"decision":decision,"issue_count":len(issues),"issues":issues,"failure_action":"quarantine","manual_override_allowed":False,"promotion_effect":False,"runtime_effect":False,"decided_at":"2026-07-16T10:30:00Z"}
    record["adjudication_id"]=stable_id("v430_adjudication",record); record["adjudication_hash"]=content_hash(record)
    chain=build_chain([record],"v430_adjudication")
    report={"phase":"SAED_V4_30","decision":decision,"accepted":accepted,"issues":issues,"unresolved_disagreements":len(issues),"safe_action":"quarantine" if not accepted else "retain_research_reference","research_only":True}
    report["report_id"]=stable_id("v430_disagreement",report); report["report_hash"]=content_hash(report)
    ledger={"phase":"SAED_V4_30","records":chain,"chain_verification":verify_chain(chain,"v430_adjudication"),"research_only":True}
    return report,ledger
