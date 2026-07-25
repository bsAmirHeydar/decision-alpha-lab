from __future__ import annotations
from typing import Any
from .canonical import digest_object


def build_provenance(candidates: list[dict[str, Any]], handoff: dict[str, Any]) -> dict[str, Any]:
    nodes=[{"id":handoff["handoff_digest"],"kind":"ACL03_HANDOFF"}]
    edges=[]
    for c in candidates:
        nodes.append({"id":c["candidate_digest"],"kind":"SETUP_CANDIDATE","candidate_id":c["candidate_id"]})
        edges.append({"from":handoff["handoff_digest"],"to":c["candidate_digest"],"relation":"BOUNDS_CONTEXT_FOR"})
        for p in c["provenance"]:
            nodes.append({"id":p["digest"],"kind":p["role"],"artifact_id":p["artifact_id"]})
            edges.append({"from":p["digest"],"to":c["candidate_digest"],"relation":"CONTRIBUTES_TO"})
    unique={n["id"]:n for n in nodes}
    body={"schema_version":"1.0.0","nodes":[unique[k] for k in sorted(unique)],"edges":sorted(edges,key=lambda e:(e["from"],e["to"],e["relation"]))}
    return {**body,"graph_digest":digest_object(body)}
