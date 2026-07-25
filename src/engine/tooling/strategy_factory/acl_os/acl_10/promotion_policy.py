from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest
from .errors import PolicyError
REQUIRED_KEYS = {'policy_id','evaluation_mode','unknown_blocks_promotion','diagnostic_promotion_allowed','baseline_promotion_allowed','requires_reporting_eligibility','requires_validated_evidence','requires_prospective_evidence','requires_independent_replication','requires_execution_economics','requires_ood_evidence','requires_human_approval','required_distinct_approvers','self_approval_allowed','approval_expiry_seconds','runtime_generation_allowed','promotion_execution_allowed','live_order_submission_allowed','capital_activation_allowed','policy_digest'}
def validate_promotion_policy(policy: dict[str,Any]) -> dict[str,Any]:
    if not REQUIRED_KEYS.issubset(policy): raise PolicyError('ACL10_PROMOTION_POLICY_INCOMPLETE')
    if not verify_embedded_digest(policy,'policy_digest'): raise PolicyError('ACL10_PROMOTION_POLICY_DIGEST_INVALID')
    checks = {
        'evaluation_only': policy['evaluation_mode'] == 'EVALUATE_ONLY',
        'unknown_blocks': policy['unknown_blocks_promotion'] is True,
        'diagnostic_denied': policy['diagnostic_promotion_allowed'] is False,
        'baseline_denied': policy['baseline_promotion_allowed'] is False,
        'validated_required': policy['requires_validated_evidence'] is True,
        'human_approval_required': policy['requires_human_approval'] is True,
        'distinct_approvers': int(policy['required_distinct_approvers']) >= 2,
        'self_approval_denied': policy['self_approval_allowed'] is False,
        'runtime_denied': policy['runtime_generation_allowed'] is False,
        'promotion_execution_denied': policy['promotion_execution_allowed'] is False,
        'order_denied': policy['live_order_submission_allowed'] is False,
        'capital_denied': policy['capital_activation_allowed'] is False,
    }
    if not all(checks.values()): raise PolicyError('ACL10_PROMOTION_POLICY_UNSAFE')
    return policy
