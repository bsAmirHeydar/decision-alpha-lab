from __future__ import annotations
from typing import Any
from .canonical import with_digest

def build_approval_bundle(decision_bundle:dict[str,Any], policy:dict[str,Any]) -> dict[str,Any]:
    eligible=decision_bundle['promotion_review_eligible_count']
    body={'schema_version':'1.0.0','eligible_subject_count':eligible,'approval_request_count':0,'approval_requests':[],'required_distinct_approvers':policy['required_distinct_approvers'],'self_approval_allowed':False,'approval_expiry_seconds':policy['approval_expiry_seconds'],'approval_not_requested_reason':'NO_PROMOTION_REVIEW_ELIGIBLE_SUBJECTS' if eligible==0 else 'REFERENCE_PHASE_DOES_NOT_ISSUE_APPROVAL_REQUESTS','promotion_execution_allowed':False}
    return with_digest(body,'approval_bundle_digest')

def build_dissent_bundle() -> dict[str,Any]:
    return with_digest({'schema_version':'1.0.0','dissent_record_count':0,'dissent_records':[],'dissent_not_required_reason':'NO_POSITIVE_PROMOTION_DECISION'},'dissent_bundle_digest')

def build_revocation_bundle() -> dict[str,Any]:
    return with_digest({'schema_version':'1.0.0','revocation_record_count':0,'revocation_records':[],'suspension_triggered':False,'retirement_triggered':False},'revocation_bundle_digest')
