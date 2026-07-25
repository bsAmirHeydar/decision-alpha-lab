from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique,require_enum,require_bool,require_positive_int
from .errors import ConstitutionError

CONSTITUTION_KEYS=["phase","title","version","effective_epoch","clauses","amendment_policy","safe_default","research_only"]
CLAUSE_KEYS=["clause_id","domain","statement","priority","immutable_in_phase","violation_response","evidence_required"]
AMENDMENT_KEYS=["proposal_roles","review_roles","minimum_independent_approvals","cooling_off_epochs","retroactive_change_allowed","self_approval_allowed"]
DOMAINS={"authority","evidence","identity","tasking","provenance","review","budget","memory","security","science","incident","amendment"}
RESPONSES={"reject","quarantine","abstain","manual_review","stop_family"}
MANDATORY={
 "C-AUTH-001","C-AUTH-002","C-EVID-001","C-ID-001","C-TASK-001","C-PROV-001","C-REVIEW-001","C-BUDGET-001","C-MEM-001","C-SEC-001","C-SCI-001","C-INC-001","C-AMEND-001"
}

def freeze_constitution(spec:dict)->dict:
    require_exact(spec,CONSTITUTION_KEYS,name="constitution")
    if spec["phase"]!="SAED_V4_32" or spec["research_only"] is not True: raise ConstitutionError("phase/research_only invalid")
    if spec["safe_default"]!="quarantine": raise ConstitutionError("safe default must be quarantine")
    clauses=require_list(spec["clauses"],"clauses",0)
    if len(clauses)<len(MANDATORY): raise ConstitutionError("mandatory clause count incomplete")
    require_unique(clauses,"clause_id","clauses")
    seen=set(); normalized=[]
    for item in clauses:
        require_exact(item,CLAUSE_KEYS,name="clause")
        require_enum(item["domain"],DOMAINS,"clause.domain")
        require_enum(item["violation_response"],RESPONSES,"clause.violation_response")
        if not isinstance(item["priority"],int) or not 1<=item["priority"]<=1000: raise ConstitutionError("clause priority invalid")
        require_bool(item["immutable_in_phase"],"immutable_in_phase",True)
        if not item["statement"].strip() or not item["evidence_required"]: raise ConstitutionError("clause content incomplete")
        seen.add(item["clause_id"]); normalized.append(deepcopy(item))
    if not MANDATORY.issubset(seen): raise ConstitutionError(f"mandatory clauses missing {sorted(MANDATORY-seen)}")
    ap=spec["amendment_policy"]; require_exact(ap,AMENDMENT_KEYS,name="amendment_policy")
    require_positive_int(ap["minimum_independent_approvals"],"minimum_independent_approvals")
    require_positive_int(ap["cooling_off_epochs"],"cooling_off_epochs")
    if ap["minimum_independent_approvals"]<2: raise ConstitutionError("two-person integrity required")
    if ap["retroactive_change_allowed"] is not False or ap["self_approval_allowed"] is not False: raise ConstitutionError("unsafe amendment policy")
    if set(ap["proposal_roles"]) & set(ap["review_roles"]): raise ConstitutionError("proposal and review roles must be separated")
    body=deepcopy(spec); body["clauses"]=sorted(normalized,key=lambda x:(x["priority"],x["clause_id"])); body["constitution_id"]=stable_id("v432_constitution",body); body["constitution_hash"]=content_hash(body); body["closed_contract"]=True; return body

def evaluate_clause_coverage(constitution:dict,policy_events:list[dict])->dict:
    triggered={e["clause_id"] for e in policy_events}
    rows=[]
    for clause in constitution["clauses"]:
        rows.append({"clause_id":clause["clause_id"],"domain":clause["domain"],"has_exercised_test":clause["clause_id"] in triggered,"immutable_in_phase":clause["immutable_in_phase"]})
    body={"phase":"SAED_V4_32","constitution_id":constitution["constitution_id"],"rows":rows,"total_clauses":len(rows),"exercised_clauses":sum(x["has_exercised_test"] for x in rows),"complete":all(x["has_exercised_test"] for x in rows),"research_only":True}
    body["coverage_id"]=stable_id("v432_constitution_coverage",body); body["coverage_hash"]=content_hash(body); return body
