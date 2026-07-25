"""Shared decision-to-intent execution runner."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Mapping

from ..contracts import DecisionAction, ExecutionIntent, ModelDecision, TradeCandidate, stable_hash
from .broker import BrokerAdapter
from .risk import RiskGateDecision, RiskPolicy, RiskState, evaluate_intent, reserve_intent


def build_intent(
    *,
    candidate: TradeCandidate,
    decision: ModelDecision,
    strategy_id: str,
    strategy_version: str,
    volume: float,
    risk_dollars: float,
) -> ExecutionIntent:
    candidate.validate()
    decision.validate()
    if decision.action != DecisionAction.TRADE:
        raise ValueError("only trade decisions can create execution intents")
    if decision.candidate_id != candidate.candidate_id:
        raise ValueError("decision candidate does not match candidate")
    payload = {
        "candidate_id": candidate.candidate_id,
        "decision_id": decision.decision_id,
        "strategy_id": strategy_id,
        "strategy_version": strategy_version,
        "volume": volume,
        "risk_dollars": risk_dollars,
    }
    intent = ExecutionIntent(
        intent_id=stable_hash(payload, prefix="intent_")[:40],
        event_id=candidate.event_id,
        candidate_id=candidate.candidate_id,
        symbol=candidate.symbol,
        direction=candidate.direction,
        created_time_utc=datetime.now(timezone.utc),
        entry_type=candidate.entry_type,
        entry_price=candidate.entry_price,
        stop_price=candidate.stop_price,
        target_price=candidate.target_price,
        volume=volume,
        risk_dollars=risk_dollars,
        expires_at_utc=candidate.expires_at_utc,
        strategy_id=strategy_id,
        strategy_version=strategy_version,
        model_decision_id=decision.decision_id,
    )
    intent.validate()
    return intent


def submit_with_risk_gate(
    intent: ExecutionIntent,
    *,
    broker: BrokerAdapter,
    risk_policy: RiskPolicy,
    risk_state: RiskState,
):
    gate = evaluate_intent(intent, risk_policy, risk_state)
    if not gate.approved:
        return gate, None
    trace = broker.submit(intent)
    if trace.state in {"accepted", "filled", "partially_filled"}:
        reserve_intent(intent, risk_state)
    return gate, trace
