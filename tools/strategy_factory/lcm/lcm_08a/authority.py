from __future__ import annotations
from .canonical import digest_object
from .constants import CLAIM_CEILING, PHASE_ID


def permit(source_handoff_digest: str, issued_at: str):
    obj={"schema_version":"1.0.0","phase_id":PHASE_ID,"claim_ceiling":CLAIM_CEILING,"source_handoff_digest":source_handoff_digest,"issued_at":issued_at,"allowed_actions":["RECONSTRUCT_CONTEXT_PORTFOLIO","ASSESS_CONTEXT_RISK","ASSIGN_MIGRATION_WAVES","SELECT_ONE_REFERENCE_PILOT","ISSUE_LCM08A_TO_LCM08B_HANDOFF"],"forbidden_actions":["MOVE_SOURCE","DELETE_SOURCE","REWRITE_CONTEXT","PUBLISH_COMPATIBILITY_ADAPTER","SWITCH_CONSUMER","MATERIALIZE_SHARED_ENGINE","ENABLE_EXECUTION","AUTHORIZE_RUNTIME","AUTHORIZE_LIVE_ORDER","ACTIVATE_CAPITAL"],"source_move_allowed":False,"source_delete_allowed":False,"semantic_refactor_allowed":False,"consumer_cutover_allowed":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"permit_digest":None};obj["permit_digest"]=digest_object(obj,"permit_digest");return obj
