from __future__ import annotations
from .canonical import digest_object, stable_id

def build_provenance(inventory_id: str, binding: dict, sources: list[dict], artifacts: dict[str,str]) -> dict:
    nodes=[{"node_id":binding['binding_digest'],"node_type":"UPSTREAM_BINDING","digest":binding['binding_digest']}]
    nodes.extend({"node_id":s['source_id'],"node_type":"SOURCE_FILE","path":s['path'],"digest":s['sha256']} for s in sources)
    nodes.extend({"node_id":stable_id('ARTNODE',name,digest),"node_type":"GENERATED_ARTIFACT","name":name,"digest":digest} for name,digest in sorted(artifacts.items()))
    body={"schema_version":"1.0.0","inventory_id":inventory_id,"nodes":nodes,"edges":[{"from":binding['binding_digest'],"to":stable_id('ARTNODE',name,digest),"relation":"BOUNDS"} for name,digest in sorted(artifacts.items())],"source_behavior_changed":False,"source_move_performed":False,"source_delete_performed":False}
    return {**body,"graph_digest":digest_object(body)}
