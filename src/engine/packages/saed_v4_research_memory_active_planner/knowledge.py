from __future__ import annotations
from copy import deepcopy
from .canonical import seal
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import ContradictionError

CLAIM_STATES={"SUPPORTED","CONTESTED","REFUTED","UNRESOLVED","LIMITED"}

def freeze_claims(items:list[dict],memory:dict)->dict:
    ids={x["memory_id"] for x in memory["entries"]}; items=require_list(items,"claims",4); require_unique(items,"claim_id","claims"); out=[]
    for x in items:
        require_exact(x,["claim_id","statement","state","support_memory_ids","oppose_memory_ids","scope","confidence","actionability","synthetic_fixture"])
        require_enum(x["state"],CLAIM_STATES,"claim.state")
        refs=set(x["support_memory_ids"]+x["oppose_memory_ids"])
        if not refs<=ids: raise ContradictionError("claim references unknown memory")
        if x["actionability"]!="RESEARCH_ONLY": raise ContradictionError("claim actionability exceeds phase")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_36","claims":sorted(out,key=lambda x:x["claim_id"]),"claim_count":len(out),"research_only":True},"v436_claims","registry_id","registry_hash")

def contradiction_register(claims:dict,items:list[dict])->dict:
    claim_ids={x["claim_id"] for x in claims["claims"]}; items=require_list(items,"contradictions",2); require_unique(items,"contradiction_id","contradictions"); out=[]
    for x in items:
        require_exact(x,["contradiction_id","claim_id","support_side","oppose_side","severity","resolution_state","required_experiment_family","synthetic_fixture"])
        if x["claim_id"] not in claim_ids or not x["support_side"] or not x["oppose_side"]: raise ContradictionError("invalid contradiction")
        if x["severity"] not in ["LOW","MEDIUM","HIGH","BLOCKING"] or x["resolution_state"] not in ["OPEN","BOUNDED","RESOLVED"]: raise ContradictionError("contradiction state invalid")
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_36","records":sorted(out,key=lambda x:x["contradiction_id"]),"open_count":sum(x["resolution_state"]!="RESOLVED" for x in out),"blocking_count":sum(x["severity"]=="BLOCKING" and x["resolution_state"]!="RESOLVED" for x in out),"research_only":True},"v436_contradictions","register_id","register_hash")

def knowledge_state(claims:dict,coverage:dict,contradictions:dict,negative:dict)->dict:
    rows=[]; cov={x["memory_id"]:x for x in coverage["rows"]}
    for c in claims["claims"]:
        support_cov=all(cov.get(x,{"covered":False})["covered"] for x in c["support_memory_ids"]); blockers=[x for x in contradictions["records"] if x["claim_id"]==c["claim_id"] and x["severity"]=="BLOCKING" and x["resolution_state"]!="RESOLVED"]
        rows.append({"claim_id":c["claim_id"],"declared_state":c["state"],"support_covered":support_cov,"blocking_contradictions":len(blockers),"eligible_for_research_use":support_cov and not blockers and c["state"] in ["SUPPORTED","LIMITED"],"eligible_for_runtime_use":False})
    return seal({"phase":"SAED_V4_36","claims":rows,"negative_knowledge_count":negative["record_count"],"runtime_use_allowed":False,"research_only":True},"v436_knowledge","state_id","state_hash")
