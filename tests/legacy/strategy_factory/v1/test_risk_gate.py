from datetime import date, datetime, timedelta, timezone

from strategy_factory.contracts import Direction, ExecutionIntent
from strategy_factory.execution.risk import RiskPolicy, RiskState, evaluate_intent


def intent(risk=100.0):
    now = datetime.now(timezone.utc)
    return ExecutionIntent(
        intent_id="I",
        event_id="E",
        candidate_id="C",
        symbol="NQ",
        direction=Direction.LONG,
        created_time_utc=now,
        entry_type="market",
        entry_price=100,
        stop_price=95,
        target_price=110,
        volume=1,
        risk_dollars=risk,
        expires_at_utc=now + timedelta(hours=1),
        strategy_id="S",
        strategy_version="1",
    )


def policy():
    return RiskPolicy("P", 100, 200, 150, 200, 150, 150, 2, allowed_strategies=("S",), allowed_symbols=("NQ",))


def test_risk_gate_approves_valid_intent():
    decision = evaluate_intent(intent(), policy(), RiskState(date.today()))
    assert decision.approved


def test_risk_gate_rejects_kill_switch():
    state = RiskState(date.today(), kill_switch=True)
    decision = evaluate_intent(intent(), policy(), state)
    assert not decision.approved
    assert "kill_switch_active" in decision.reasons
