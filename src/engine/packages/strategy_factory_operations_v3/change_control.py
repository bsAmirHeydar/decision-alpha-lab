from __future__ import annotations

from .contracts import ChangeDecision, ChangeRequest, OperationsPolicy
from .enums import ChangeClass

_INVALIDATING = {
    "source_commit",
    "qualification_report_hash",
    "release_manifest_hash",
    "environment_hash",
    "generation_hash",
    "rollback_generation_hash",
    "broker_server_hash",
    "account_hashes",
    "symbol_spec_hash",
    "context_spec_hash",
    "feature_manifest_hash",
    "model_hash",
    "calibrator_hash",
    "policy_graph_hash",
    "treatment_hash",
    "economics_policy_hash",
    "risk_envelope_hash",
}
_FORBIDDEN_HOT = {"active_generation_bytes", "live_feature_order", "open_position_identity", "reservation_ledger"}
_DOC_ONLY = {"documentation", "runbook", "contact_roster", "dashboard_label"}
_NON_AUTH = {"alert_route", "log_retention_days", "dashboard_layout", "ticket_queue"}
_RISK_REDUCTION = {"max_risk_units", "max_positions", "max_orders_per_minute", "allowed_symbols"}


def classify_change(request: ChangeRequest, policy: OperationsPolicy, evaluated_at_ms: int) -> ChangeDecision:
    fields = set(request.field_changes)
    reasons: list[str] = []
    if fields & _FORBIDDEN_HOT:
        classification, approved, requal, flat = ChangeClass.FORBIDDEN_HOT_CHANGE, False, True, True
        reasons.append("forbidden_hot_mutation")
    elif fields & _INVALIDATING:
        classification, approved, requal, flat = ChangeClass.QUALIFICATION_INVALIDATING, False, True, policy.required_flat_before_environment_change
        reasons.append("qualification_invalidated")
    elif fields <= _DOC_ONLY:
        classification, approved, requal, flat = ChangeClass.DOCUMENTATION_ONLY, True, False, False
    elif fields <= _NON_AUTH:
        classification, approved, requal, flat = ChangeClass.NON_AUTHORITY_OPERATIONS, True, False, False
    elif fields <= _RISK_REDUCTION and request.emergency:
        risk_reducing = all(_is_reduction(field, old, new) for field, (old, new) in request.field_changes.items())
        classification = ChangeClass.RISK_REDUCTION if risk_reducing else ChangeClass.FORBIDDEN_HOT_CHANGE
        approved, requal, flat = risk_reducing, False, False
        if not risk_reducing:
            reasons.append("emergency_change_not_risk_reducing")
    else:
        classification, approved, requal, flat = ChangeClass.QUALIFICATION_INVALIDATING, False, True, True
        reasons.append("unclassified_authority_change")
    return ChangeDecision(
        decision_id=f"change-decision:{request.change_id}:{evaluated_at_ms}",
        classification=classification,
        approved=approved,
        requalification_required=requal,
        flat_required=flat,
        evaluated_at_ms=evaluated_at_ms,
        request_hash=request.request_hash,
        reason_codes=tuple(reasons),
    )


def _is_reduction(field: str, old: str, new: str) -> bool:
    if field == "allowed_symbols":
        return set(filter(None, new.split(","))) <= set(filter(None, old.split(",")))
    try:
        return float(new) <= float(old)
    except ValueError:
        return False
