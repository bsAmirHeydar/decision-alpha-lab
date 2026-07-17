from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_sha256
from .errors import UpstreamError
from .canonical import seal

def verify_upstream(docs:list[dict])->dict:
    if not isinstance(docs,list) or len(docs)!=2: raise UpstreamError("V4-37 requires V4-36 certificate and handoff")
    by={d.get("kind"):d for d in docs}
    if set(by)!={"v4_36_certificate","v4_36_handoff"}: raise UpstreamError("upstream kinds invalid")
    for kind,d in by.items():
        require_exact(d,["kind","phase","document_id","document_hash","next_phase","research_only","production_authorized"])
        if d["phase"]!="SAED_V4_36" or d["next_phase"]!="SAED_V4_37" or d["research_only"] is not True or d["production_authorized"] is not False: raise UpstreamError("upstream authority mismatch")
        require_sha256(d["document_hash"],f"{kind}.document_hash")
    return seal({"phase":"SAED_V4_37","verified":True,"upstream_phase":"SAED_V4_36","documents":sorted(deepcopy(docs),key=lambda x:x["kind"]),"research_only":True},"v437_upstream","receipt_id","receipt_hash")
