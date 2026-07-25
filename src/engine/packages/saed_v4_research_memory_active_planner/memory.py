from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,semantic_fingerprint,hash_chain,seal,merkle_root
from .contracts import require_exact,require_list,require_unique,require_time_before,require_sha256,require_enum
from .errors import MemoryError

KINDS={"HYPOTHESIS","EXPERIMENT","RESULT","NEGATIVE_RESULT","CLAIM","LIMITATION","INCIDENT","RISK_FINDING","DECISION","ARTIFACT","DATASET","MODEL","RUNBOOK","QUESTION"}
STATUSES={"ACTIVE","REJECTED","SUPERSEDED","REPRODUCED","UNRESOLVED","CLOSED","QUARANTINED"}

def freeze_entries(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"memory_entries",12); require_unique(items,"memory_id","memory_entries"); out=[]; fps={}
    ids={x.get("memory_id") for x in items}
    for x in items:
        require_exact(x,["memory_id","kind","title","statement","status","known_time","source_phase","evidence_hashes","tags","supersedes","sensitivity","owner_id","synthetic_fixture"])
        require_enum(x["kind"],KINDS,"kind"); require_enum(x["status"],STATUSES,"status"); require_time_before(x["known_time"],cutoff,"memory.known_time")
        if sorted(set(x["tags"]))!=x["tags"]: raise MemoryError("tags must be sorted unique")
        for h in x["evidence_hashes"]: require_sha256(h,"evidence_hash")
        if x["supersedes"] and x["supersedes"] not in ids: raise MemoryError("supersedes references unknown memory")
        fp=semantic_fingerprint(x["kind"],x["title"],x["statement"],x["tags"])
        if fp in fps and not x["supersedes"]: raise MemoryError(f"semantic duplicate without supersession: {x['memory_id']}")
        fps[fp]=x["memory_id"]; y=deepcopy(x); y["semantic_fingerprint"]=fp; y["entry_hash"]=content_hash(y); out.append(y)
    out=sorted(out,key=lambda x:(x["known_time"],x["memory_id"])); chain=hash_chain(out,"v436_memory_event")
    return seal({"phase":"SAED_V4_36","cutoff_time":cutoff,"entries":out,"entry_count":len(out),"append_only":True,"semantic_duplicates":0,"chain":chain,"chain_head":chain[-1]["event_hash"],"merkle_root":merkle_root([x["entry_hash"] for x in out]),"research_only":True},"v436_memory","memory_store_id","memory_store_hash")

def negative_knowledge(store:dict)->dict:
    rows=[]
    for x in store["entries"]:
        if x["kind"] in {"NEGATIVE_RESULT","LIMITATION","INCIDENT","RISK_FINDING"} or x["status"] in {"REJECTED","QUARANTINED"}:
            rows.append({"memory_id":x["memory_id"],"kind":x["kind"],"statement":x["statement"],"evidence_hashes":x["evidence_hashes"],"mandatory_for_retrieval":True,"may_be_deleted":False})
    if not rows: raise MemoryError("negative knowledge is mandatory")
    return seal({"phase":"SAED_V4_36","records":rows,"record_count":len(rows),"deletion_allowed":False,"research_only":True},"v436_negative","registry_id","registry_hash")

def supersession_map(store:dict)->dict:
    links=[]
    for x in store["entries"]:
        if x["supersedes"]: links.append({"new_memory_id":x["memory_id"],"old_memory_id":x["supersedes"],"new_status":x["status"],"reason":"explicit_supersession"})
    return seal({"phase":"SAED_V4_36","links":links,"link_count":len(links),"destructive_update_allowed":False,"research_only":True},"v436_supersession","map_id","map_hash")
