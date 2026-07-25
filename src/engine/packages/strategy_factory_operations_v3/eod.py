from __future__ import annotations

from .contracts import EndOfDayReport, RiskEnvelope
from .enums import ControlDecision


def evaluate_eod(report: EndOfDayReport, envelope: RiskEnvelope) -> tuple[ControlDecision, tuple[str, ...]]:
    reasons: list[str] = []
    if not report.all_events_persisted:
        reasons.append("events_not_persisted")
    if not report.all_intents_terminal:
        reasons.append("non_terminal_intent")
    if not report.exact_reconciliation:
        reasons.append("eod_reconciliation_failed")
    if report.unresolved_high_incidents:
        reasons.append("unresolved_high_incident")
    if report.unresolved_critical_incidents:
        reasons.append("unresolved_critical_incident")
    if report.daily_loss_units > envelope.max_daily_loss_units:
        reasons.append("daily_loss_limit")
    return (ControlDecision.SAFE_HALT, tuple(sorted(set(reasons)))) if reasons else (ControlDecision.HOLD, ())
