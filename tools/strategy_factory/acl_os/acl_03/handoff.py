from __future__ import annotations
from typing import Any
from .canonical import digest_object

def build_acl04_handoff(package:dict[str,Any],source_snapshot:dict[str,Any],detector_ir:dict[str,Any],occurrence_ir:dict[str,Any],feature_ir:dict[str,Any],onboarding:dict[str,Any])->dict[str,Any]:
    body={"schema_version":"1.0.0","handoff_type":"ACL03_TO_ACL04","context_id":package["manifest"]["context_id"],"context_version":package["manifest"]["context_version"],"source_snapshot_digest":source_snapshot["snapshot_digest"],"detector_ir_digest":detector_ir["detector_ir_digest"],"occurrence_ir_digest":occurrence_ir["occurrence_ir_digest"],"feature_binding_ir_digest":feature_ir["feature_binding_ir_digest"],"onboarding_report_digest":onboarding["report_digest"],"allowed_scope":["DEFINE_HUMAN_SETUP_DSL","GENERATE_BOUNDED_AI_SETUP_CANDIDATES","CANONICALIZE_SETUP_BEHAVIOR","VALIDATE_TREATMENT_ENVELOPE"],"forbidden_scope":["ALTER_CONTEXT_SEMANTICS","ALTER_CONTEXT_STATE_MACHINE","BYPASS_KNOWN_TIME_GUARDS","ACTIVATE_CAPITAL","SUBMIT_ORDERS","MODIFY_GENERATED_IR"],"search_authority_required":True,"live_order_submission_allowed":False,"capital_activation_allowed":False}
    return {**body,"handoff_digest":digest_object(body)}
