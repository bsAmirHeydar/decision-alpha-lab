from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id,hash_chain
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import ProvenanceError

SOURCE_KEYS=["source_id","source_type","uri_class","content_hash","known_time_epoch","evidence_role","protected","synthetic","license_class","lineage_ids"]
ROLES={"training","validation","challenge","protected_final","synthetic_stress","governance"}

def freeze_sources(items:list[dict])->dict:
    require_list(items,"sources",1); require_unique(items,"source_id","sources"); normalized=[]
    for s in items:
        require_exact(s,SOURCE_KEYS,name="source")
        require_enum(s["evidence_role"],ROLES,"evidence_role")
        if not isinstance(s["known_time_epoch"],int) or s["known_time_epoch"]<=0: raise ProvenanceError("known_time invalid")
        if s["protected"] and s["evidence_role"]!="protected_final": raise ProvenanceError("protected source role mismatch")
        if s["synthetic"] and s["evidence_role"]!="synthetic_stress": raise ProvenanceError("synthetic source role mismatch")
        normalized.append(deepcopy(s))
    body={"phase":"SAED_V4_32","sources":sorted(normalized,key=lambda x:x["source_id"]),"source_count":len(normalized),"known_time_explicit":True,"role_immutable":True,"research_only":True}
    body["registry_id"]=stable_id("v432_source_registry",body); body["registry_hash"]=content_hash(body); return body

def build_exposure_ledger(tasks:dict,sources:dict,agents:dict)->dict:
    by_source={s["source_id"]:s for s in sources["sources"]}; by_agent={a["agent_id"]:a for a in agents["agents"]}; records=[]
    for t in tasks["tasks"]:
        source_ids=[x.split(":",1)[1] for x in t["input_hashes"] if x.startswith("source:")]
        for sid in source_ids:
            if sid not in by_source: raise ProvenanceError("unknown source exposure")
            source=by_source[sid]; agent=by_agent[t["owner_agent_id"]]
            if source["known_time_epoch"]>t["known_time_epoch"]: raise ProvenanceError("future source exposure")
            allowed=True; reason="declared_nonprotected_source"
            if source["protected"]:
                allowed=t["protected_evidence_allowed"] and agent["role_id"] in {"evidence_curator","human_reviewer"}
                reason="protected_custodian_access" if allowed else "protected_access_denied"
            if not allowed: raise ProvenanceError("unauthorized protected exposure")
            records.append({"task_id":t["task_id"],"agent_id":agent["agent_id"],"role_id":agent["role_id"],"source_id":sid,"evidence_role":source["evidence_role"],"known_time_epoch":t["known_time_epoch"],"protected":source["protected"],"allowed":True,"reason":reason})
    chained=hash_chain(sorted(records,key=lambda x:(x["known_time_epoch"],x["task_id"],x["source_id"])),"v432_exposure")
    body={"phase":"SAED_V4_32","events":chained,"event_count":len(chained),"protected_exposure_count":sum(x["protected"] for x in chained),"future_suffix_exposures":0,"unauthorized_exposures":0,"complete":True,"research_only":True}
    body["ledger_id"]=stable_id("v432_exposure_ledger",body); body["ledger_hash"]=content_hash(body); return body

def prompt_task_output_ledger(tasks:dict,agents:dict)->dict:
    by_agent={a["agent_id"]:a for a in agents["agents"]}; records=[]
    for t in tasks["tasks"]:
        a=by_agent[t["owner_agent_id"]]
        record={"task_id":t["task_id"],"agent_id":a["agent_id"],"role_id":a["role_id"],"prompt_profile_hash":a["prompt_profile_hash"],"tool_profile_hash":a["tool_profile_hash"],"input_hashes":sorted(t["input_hashes"]),"output_contract":t["output_contract"],"output_hash":content_hash({"task_id":t["task_id"],"output_contract":t["output_contract"],"state":"synthetic_reference_complete"}),"known_time_epoch":t["known_time_epoch"],"network_access":False,"research_only":True}
        records.append(record)
    chained=hash_chain(sorted(records,key=lambda x:(x["known_time_epoch"],x["task_id"])),"v432_prompt_task_output")
    body={"phase":"SAED_V4_32","events":chained,"event_count":len(chained),"complete_trial_accounting":True,"complete_prompt_accounting":True,"complete_tool_accounting":True,"complete_output_accounting":True,"network_access":False,"research_only":True}
    body["ledger_id"]=stable_id("v432_prompt_task_output_ledger",body); body["ledger_hash"]=content_hash(body); return body
