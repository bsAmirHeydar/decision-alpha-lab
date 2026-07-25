from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id
from .errors import ContractError

def verify(contract, docs:dict[str,Any])->dict[str,Any]:
    if set(docs)!={"certificate","handoff"}: raise ContractError("upstream docs must be exact")
    c,h=docs["certificate"],docs["handoff"]
    if c.get("phase")!="SAED_V4_26" or h.get("next_phase")!="SAED_V4_27": raise ContractError("wrong upstream phase")
    if c.get("certificate_hash")!=contract.certificate_hash or h.get("handoff_hash")!=contract.handoff_hash: raise ContractError("upstream hash mismatch")
    if not c.get("research_only") or not h.get("research_only") or any(h.get("authority",{}).values()): raise ContractError("upstream authority escape")
    payload={"phase":"SAED_V4_27","upstream_phase":"SAED_V4_26","certificate_hash":contract.certificate_hash,"handoff_hash":contract.handoff_hash,"hash_verified":True,"immutable":True,"research_only":True}
    payload["receipt_id"]=stable_id("v427_upstream",payload); payload["receipt_hash"]=content_hash(payload)
    return payload
