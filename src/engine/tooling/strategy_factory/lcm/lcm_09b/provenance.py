from __future__ import annotations
from .canonical import digest_object,stable_id

def build_provenance(packages:list[dict],upstream_digest:str)->dict:
    nodes=[{"node_id":"LCM09A_HANDOFF","kind":"UPSTREAM_HANDOFF","digest":upstream_digest}]
    edges=[]
    for p in packages:
        nodes.extend([{"node_id":p["package_id"],"kind":"CANONICAL_SETUP_PACKAGE","digest":p["package_digest"]},{"node_id":p["setup_id"],"kind":"SETUP_IDENTITY","digest":p["source_binding"]["identity_digest"]}])
        edges.extend([{"from":p["setup_id"],"to":p["package_id"],"role":"MATERIALIZED_AS_REFERENCE_PACKAGE"},{"from":"LCM09A_HANDOFF","to":p["package_id"],"role":"AUTHORIZES_BOUNDED_MIGRATION_ATTEMPT"}])
    nodes=sorted(nodes,key=lambda x:x["node_id"]);edges=sorted(edges,key=lambda x:(x["from"],x["to"],x["role"]))
    body={"schema_version":"1.0.0","graph_id":stable_id("SETUPPROV","LCM-09B",upstream_digest),"nodes":nodes,"edges":edges}
    return {**body,"graph_digest":digest_object(body)}
