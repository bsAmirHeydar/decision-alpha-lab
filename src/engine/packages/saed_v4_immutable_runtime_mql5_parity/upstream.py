from __future__ import annotations
from copy import deepcopy
from .contracts import exact,sha256
from .errors import UpstreamError
from .canonical import seal

def verify_upstream(docs:list[dict])->dict:
 if not isinstance(docs,list) or len(docs)!=2:raise UpstreamError("V4-38 requires V4-37 certificate and handoff")
 by={x.get("kind"):x for x in docs}
 if set(by)!={"v4_37_certificate","v4_37_handoff"}:raise UpstreamError("upstream kinds invalid")
 for kind,x in by.items():
  exact(x,["kind","phase","document_id","document_hash","next_phase","research_only","production_authorized"])
  if x["phase"]!="SAED_V4_37" or x["next_phase"]!="SAED_V4_38" or x["research_only"] is not True or x["production_authorized"] is not False:raise UpstreamError("upstream authority mismatch")
  sha256(x["document_hash"],kind+".document_hash")
 return seal({"phase":"SAED_V4_38","verified":True,"upstream_phase":"SAED_V4_37","documents":sorted(deepcopy(docs),key=lambda z:z["kind"]),"research_only":True},"v438_upstream","receipt_id","receipt_hash")
