from __future__ import annotations
from .contracts import require_exact,require_sha256
from .errors import UpstreamError
from .canonical import content_hash,seal

def verify_upstream(docs:list[dict])->dict:
    if len(docs)!=2: raise UpstreamError("V4-33 requires V4-32 certificate and handoff")
    by_kind={d["kind"]:d for d in docs}
    if set(by_kind)!={"v4_32_certificate","v4_32_handoff"}: raise UpstreamError("upstream kinds invalid")
    for kind,d in by_kind.items():
        require_exact(d,["kind","phase","document_id","document_hash","next_phase","research_only"],name=kind)
        if d["phase"]!="SAED_V4_32" or d["next_phase"]!="SAED_V4_33" or d["research_only"] is not True: raise UpstreamError("upstream authority mismatch")
        require_sha256(d["document_hash"],f"{kind}.document_hash")
    return seal({"phase":"SAED_V4_33","verified":True,"upstream_phase":"SAED_V4_32","documents":sorted(docs,key=lambda x:x["kind"]),"research_only":True},"v433_upstream","receipt_id","receipt_hash")
