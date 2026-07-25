from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal,merkle_root
from .contracts import require_exact,require_list,require_unique,require_time_before,require_sha256,require_enum
from .errors import EvidenceError

ROLES={"PRIMARY","REPLICATION","NEGATIVE_CONTROL","STRESS","AUDIT","EXTERNAL_BOUNDARY"}

def freeze_evidence(items:list[dict],cutoff:str)->dict:
    items=require_list(items,"evidence_records",12); require_unique(items,"evidence_id","evidence_records"); out=[]
    for x in items:
        require_exact(x,["evidence_id","memory_id","role","artifact_hash","schema_hash","lineage_hash","known_time","operator_id","independent","synthetic_fixture","valid"])
        require_enum(x["role"],ROLES,"evidence.role"); require_time_before(x["known_time"],cutoff,"evidence.known_time")
        for k in ["artifact_hash","schema_hash","lineage_hash"]: require_sha256(x[k],k)
        y=deepcopy(x); y["evidence_hash"]=content_hash(y); out.append(y)
    return seal({"phase":"SAED_V4_36","records":sorted(out,key=lambda x:x["evidence_id"]),"record_count":len(out),"all_valid":all(x["valid"] for x in out),"independent_count":sum(x["independent"] for x in out),"merkle_root":merkle_root([x["evidence_hash"] for x in out]),"research_only":True},"v436_evidence","registry_id","registry_hash")

def lineage_graph(store:dict,evidence:dict,edges:list[dict])->dict:
    memory_ids={x["memory_id"] for x in store["entries"]}; evidence_ids={x["evidence_id"] for x in evidence["records"]}; nodes=memory_ids|evidence_ids; out=[]
    for e in require_list(edges,"lineage_edges",8):
        require_exact(e,["source_id","target_id","relation"])
        if e["source_id"] not in nodes or e["target_id"] not in nodes or e["source_id"]==e["target_id"]: raise EvidenceError("invalid lineage edge")
        out.append(deepcopy(e))
    out=sorted(out,key=lambda x:(x["source_id"],x["target_id"],x["relation"])); return seal({"phase":"SAED_V4_36","nodes":sorted(nodes),"edges":out,"node_count":len(nodes),"edge_count":len(out),"research_only":True},"v436_lineage","graph_id","graph_hash")

def evidence_coverage(store:dict,evidence:dict)->dict:
    by={}
    for e in evidence["records"]: by.setdefault(e["memory_id"],[]).append(e)
    rows=[]
    for x in store["entries"]:
        ev=by.get(x["memory_id"],[]); required=x["kind"] in {"CLAIM","RESULT","NEGATIVE_RESULT","RISK_FINDING"}; covered=(not required) or any(e["valid"] for e in ev)
        rows.append({"memory_id":x["memory_id"],"kind":x["kind"],"evidence_count":len(ev),"independent_count":sum(e["independent"] for e in ev),"required":required,"covered":covered})
    return seal({"phase":"SAED_V4_36","rows":rows,"covered":all(x["covered"] for x in rows),"uncovered_ids":[x["memory_id"] for x in rows if not x["covered"]],"research_only":True},"v436_coverage","coverage_id","coverage_hash")
