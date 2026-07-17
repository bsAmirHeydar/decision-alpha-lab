from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .schema_validation import validate_instance


def build_acl05_handoff(*, context_id: str, context_version: str, upstream_handoff_digest: str, candidates: list[dict[str, Any]], dedup_report: dict[str, Any], exposure_ledger: dict[str, Any], provenance: dict[str, Any]) -> dict[str, Any]:
    eligible=[c for c in candidates if c["status"] in {"ELIGIBLE_FOR_BATCH_DEFINITION","DIAGNOSTIC_ONLY"}]
    body={
        "schema_version":"1.0.0",
        "handoff_type":"ACL04_TO_ACL05",
        "context_id":context_id,
        "context_version":context_version,
        "upstream_acl03_handoff_digest":upstream_handoff_digest,
        "candidate_references":[{"setup_id":c["setup_id"],"candidate_id":c["candidate_id"],"candidate_digest":c["candidate_digest"],"behavior_digest":c["behavior_digest"],"status":c["status"]} for c in eligible],
        "deduplication_report_digest":dedup_report["report_digest"],
        "search_exposure_ledger_digest":exposure_ledger["ledger_digest"],
        "provenance_graph_digest":provenance["graph_digest"],
        "required_acl05_actions":["FREEZE_SETUP_UNIVERSE","FREEZE_SEARCH_EXPOSURE","CREATE_IMMUTABLE_RESEARCH_BATCH"],
        "forbidden_acl05_inferences":["INFER_ALPHA","AUTHORIZE_EXECUTION","ACTIVATE_CAPITAL","MUTATE_SETUP_BEHAVIOR"],
        "live_order_submission_allowed":False,
        "capital_activation_allowed":False,
        "claim_ceiling":"SETUP_DEFINITION_REFERENCE_ONLY",
    }
    handoff={**body,"handoff_digest":digest_object(body)}
    validate_instance("acl05_handoff", handoff)
    return handoff
