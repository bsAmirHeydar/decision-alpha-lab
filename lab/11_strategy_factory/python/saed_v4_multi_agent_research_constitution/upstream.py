from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_sha256
from .errors import UpstreamError

DOC_KEYS=["document_type","phase","document_id","document_hash","payload"]

def _without_hash(payload:dict,field:str)->dict:
    value=deepcopy(payload); value.pop(field,None); return value

def verify_upstream(documents:list[dict])->dict:
    require_list(documents,"upstream_documents",2)
    seen=set(); rows=[]
    for item in documents:
        require_exact(item,DOC_KEYS,name="upstream_document")
        if item["phase"]!="SAED_V4_31": raise UpstreamError("upstream phase must be SAED_V4_31")
        require_sha256(item["document_hash"],"document_hash")
        if item["document_type"] in seen: raise UpstreamError("duplicate upstream document type")
        seen.add(item["document_type"])
        payload=item["payload"]
        if item["document_type"]=="formal_verification_safety_case_certificate":
            if payload.get("certificate_id")!=item["document_id"]: raise UpstreamError("certificate id mismatch")
            if payload.get("certificate_hash")!=item["document_hash"]: raise UpstreamError("certificate hash mismatch")
            if content_hash(_without_hash(payload,"certificate_hash"))!=item["document_hash"]: raise UpstreamError("certificate payload hash mismatch")
            if payload.get("production_authority") is not False or payload.get("live_trading_authority") is not False: raise UpstreamError("upstream authority violation")
        elif item["document_type"]=="v4_31_to_v4_32_handoff":
            if payload.get("handoff_id")!=item["document_id"] or payload.get("handoff_hash")!=item["document_hash"]: raise UpstreamError("handoff identity mismatch")
            if content_hash(_without_hash(payload,"handoff_hash"))!=item["document_hash"]: raise UpstreamError("handoff payload hash mismatch")
            if payload.get("next_phase")!="SAED_V4_32": raise UpstreamError("handoff next phase mismatch")
            if "multi_agent_role_constitution" not in payload.get("allowed_next_work",[]): raise UpstreamError("required next work absent")
        else: raise UpstreamError("unknown upstream document type")
        rows.append({"document_type":item["document_type"],"document_id":item["document_id"],"document_hash":item["document_hash"],"verified":True})
    required={"formal_verification_safety_case_certificate","v4_31_to_v4_32_handoff"}
    if seen!=required: raise UpstreamError("upstream set incomplete")
    body={"phase":"SAED_V4_32","source_phase":"SAED_V4_31","documents":sorted(rows,key=lambda x:x["document_type"]),"immutable":True,"hash_verified":True,"entry_gate_passed":True,"research_only":True}
    body["receipt_id"]=stable_id("v432_upstream_receipt",body); body["receipt_hash"]=content_hash(body); return body
