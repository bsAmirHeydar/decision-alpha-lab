from __future__ import annotations
from collections import Counter, defaultdict
from .canonical import content_id, digest_object


def build(records: list[dict], dependency_rows: list[dict]) -> dict:
    by_path={r["source_artifact_path"]:r["identity_id"] for r in records}
    nodes=[]
    for r in records:
        nodes.append({"identity_id":r["identity_id"],"family_candidate":r["family_candidate"],"risk_class":r["risk_class"],"wave_assignment":r["wave_assignment"],"source_artifact_path":r["source_artifact_path"]})
    edges=[]; seen=set()
    for row in dependency_rows:
        src=row.get("source_path",""); dst=row.get("resolved_path","")
        src_id=by_path.get(src); dst_id=by_path.get(dst)
        if not src_id and not dst_id: continue
        key=(src_id or src,row.get("edge_type"),dst_id or dst,row.get("line_number"))
        if key in seen:continue
        seen.add(key)
        edges.append({"edge_id":content_id("CTXEDGE",key),"source_identity_id":src_id,"source_path":src,"edge_type":row.get("edge_type"),"target_identity_id":dst_id,"target_path":dst or row.get("raw_target"),"resolution_status":row.get("resolution_status"),"semantic_reachability_claimed":False})
    graph={"schema_version":"1.0.0","graph_id":"LCM08A_CONTEXT_DEPENDENCY_GRAPH_V1","nodes":nodes,"edges":sorted(edges,key=lambda e:e["edge_id"]),"semantic_reachability_claimed":False,"graph_digest":None}
    graph["graph_digest"]=digest_object(graph,"graph_digest")
    return graph
