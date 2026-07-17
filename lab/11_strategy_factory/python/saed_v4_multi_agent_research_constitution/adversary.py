from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import ReviewError

CHALLENGE_KEYS=["challenge_id","claim_id","challenger_agent_id","challenge_type","severity","finding","required_resolution","blocking","evidence_source_ids","research_only"]
TYPES={"multiplicity","dependence","leakage","support","calibration","causal_identification","execution_realism","selection_bias","transport","baseline"}
SEVERITY={"low","medium","high","critical"}

def run_challenges(items:list[dict],agents:dict,claim_graph:dict)->tuple[dict,dict]:
    require_list(items,"challenges",1); require_unique(items,"challenge_id","challenges")
    by_agent={a["agent_id"]:a for a in agents["agents"]}; claim_ids={x["claim_id"] for x in claim_graph["nodes"]}; rows=[]
    for c in items:
        require_exact(c,CHALLENGE_KEYS,name="challenge")
        require_enum(c["challenge_type"],TYPES,"challenge_type"); require_enum(c["severity"],SEVERITY,"severity")
        if c["claim_id"] not in claim_ids: raise ReviewError("unknown challenged claim")
        agent=by_agent.get(c["challenger_agent_id"])
        if not agent or agent["role_id"] not in {"statistical_adversary","leakage_sentinel","causal_auditor","execution_auditor","data_audit"}: raise ReviewError("invalid challenger role")
        if c["research_only"] is not True: raise ReviewError("research_only required")
        row=deepcopy(c); row["challenge_hash"]=content_hash(c); rows.append(row)
    report={"phase":"SAED_V4_32","challenges":sorted(rows,key=lambda x:x["challenge_id"]),"challenge_count":len(rows),"blocking_count":sum(x["blocking"] for x in rows),"independent_challenger_groups":sorted({by_agent[x["challenger_agent_id"]]["role_id"] for x in rows}),"counter_report_required":True,"research_only":True}
    report["report_id"]=stable_id("v432_adversarial_report",report); report["report_hash"]=content_hash(report)
    issues=[]
    for x in rows:
        if x["blocking"]:
            issue={"issue_id":stable_id("v432_blocking_issue",x),"challenge_id":x["challenge_id"],"claim_id":x["claim_id"],"severity":x["severity"],"required_resolution":x["required_resolution"],"status":"open_synthetic_reference","waivable_by_agent":False,"suppression_allowed":False}
            issue["issue_hash"]=content_hash(issue); issues.append(issue)
    ledger={"phase":"SAED_V4_32","issues":issues,"open_count":len(issues),"suppressed_count":0,"agent_waiver_count":0,"research_only":True}
    ledger["ledger_id"]=stable_id("v432_blocking_ledger",ledger); ledger["ledger_hash"]=content_hash(ledger)
    return report,ledger
