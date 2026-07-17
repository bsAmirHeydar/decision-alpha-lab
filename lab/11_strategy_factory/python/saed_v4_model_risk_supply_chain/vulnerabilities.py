from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_num,require_time_before
from .errors import VulnerabilityError
from .canonical import seal

def freeze_catalog(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"vulnerabilities",1); require_unique(items,"vulnerability_id","vulnerabilities"); out=[]
    for x in items:
        require_exact(x,["vulnerability_id","component_id","source","severity","cvss","known_time","exploitability","fix_available","status","synthetic_fixture"])
        require_num(x["cvss"],"cvss",0,10); require_time_before(x["known_time"],cutoff,"vulnerability.known_time")
        if x["severity"] not in ["LOW","MEDIUM","HIGH","CRITICAL"]: raise VulnerabilityError("severity invalid")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_35","records":sorted(out,key=lambda x:x["vulnerability_id"]),"record_count":len(out),"cutoff_time":cutoff,"synthetic_reference":True,"research_only":True},"v435_vulns","catalog_id","catalog_hash")

def review(catalog:dict,sbom:dict,thresholds:dict)->dict:
    require_exact(thresholds,["block_critical","block_high_exploitable","max_unfixed_high","staleness_days_max"])
    components={c["component_id"] for c in sbom["components"]}; rows=[]; unfixed_high=0; blocked=False
    for v in catalog["records"]:
        if v["component_id"] not in components: raise VulnerabilityError("vulnerability references unknown component")
        decision="ACCEPT_REFERENCE"
        if v["severity"]=="CRITICAL" and thresholds["block_critical"]: decision="QUARANTINE"; blocked=True
        if v["severity"]=="HIGH" and v["exploitability"]=="KNOWN_EXPLOITED" and thresholds["block_high_exploitable"]: decision="QUARANTINE"; blocked=True
        if v["severity"] in ["HIGH","CRITICAL"] and v["status"]!="remediated": unfixed_high+=1
        rows.append({"vulnerability_id":v["vulnerability_id"],"component_id":v["component_id"],"severity":v["severity"],"decision":decision,"fix_available":v["fix_available"],"status":v["status"]})
    if unfixed_high>thresholds["max_unfixed_high"]: blocked=True
    return seal({"phase":"SAED_V4_35","findings":rows,"unfixed_high_or_critical":unfixed_high,"blocked":blocked,"thresholds":deepcopy(thresholds),"scanner_fresh":True,"research_only":True},"v435_vuln_review","review_id","review_hash")
