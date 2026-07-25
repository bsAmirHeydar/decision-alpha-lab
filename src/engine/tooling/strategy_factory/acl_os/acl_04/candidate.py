from __future__ import annotations
from typing import Any
from .canonical import digest_object, stable_id
from .schema_validation import validate_instance


def behavior_payload(ir: dict[str, Any]) -> dict[str, Any]:
    return {k:v for k,v in ir.items() if k not in {"lane","policy_ir_digest"}}


def build_candidate(ir: dict[str, Any], *, source_id: str, source_digest: str, authority_digest: str, envelope_digest: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
    behavior_digest=digest_object(behavior_payload(ir))
    blocked=any(f["severity"] in {"ERROR","BLOCKER"} for f in findings)
    if ir.get("diagnostic_only"):
        status="DIAGNOSTIC_ONLY"
    else:
        status="INVALID" if blocked else "ELIGIBLE_FOR_BATCH_DEFINITION"
    body={
        "schema_version":"1.0.0",
        "candidate_id":stable_id("CAND", source_id, ir["policy_ir_digest"]),
        "setup_id":stable_id("SETUP", behavior_digest),
        "context_id":ir["context_id"],
        "context_version":ir["context_version"],
        "origin":ir["lane"],
        "treatment_family":ir["treatment_family"],
        "policy_ir":ir,
        "behavior_digest":behavior_digest,
        "status":status,
        "findings":findings,
        "provenance":[
            {"artifact_id":source_id,"digest":source_digest,"role":"SOURCE_DEFINITION"},
            {"artifact_id":"ACL04_SEARCH_AUTHORITY","digest":authority_digest,"role":"SEARCH_AUTHORITY"},
            {"artifact_id":"ACL04_TREATMENT_ENVELOPE","digest":envelope_digest,"role":"TREATMENT_ENVELOPE"},
        ],
        "live_order_submission_allowed":False,
        "capital_activation_allowed":False,
    }
    candidate={**body,"candidate_digest":digest_object(body)}
    validate_instance("setup_candidate", candidate)
    return candidate
