from __future__ import annotations
from .canonical import with_digest

def build_runtime_candidate_manifest(decision_bundle:dict) -> dict:
    body={'schema_version':'1.0.0','runtime_candidate_count':0,'runtime_candidates':[],'source_promotion_review_eligible_count':decision_bundle['promotion_review_eligible_count'],'runtime_generation_allowed':False,'runtime_handoff_allowed':False,'reason_code':'NO_RUNTIME_ELIGIBLE_PROMOTION_DECISIONS' if decision_bundle['promotion_review_eligible_count']==0 else 'ACL10_REFERENCE_PHASE_DOES_NOT_GENERATE_RUNTIME'}
    return with_digest(body,'runtime_candidate_manifest_digest')
