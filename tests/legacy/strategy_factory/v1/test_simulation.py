from datetime import datetime, timedelta, timezone

import pandas as pd

from strategy_factory.contracts import CandidateState, Direction, TradeCandidate
from strategy_factory.costs import CostModel
from strategy_factory.simulation import SimulationPolicy, simulate_candidate


def candidate() -> TradeCandidate:
    t = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    return TradeCandidate(
        candidate_id="C",
        event_id="E",
        symbol="NQ",
        direction=Direction.LONG,
        entry_policy_id="market",
        stop_policy_id="structural",
        exit_policy_id="fixed",
        created_time_utc=t,
        eligible_from_utc=t,
        expires_at_utc=t + timedelta(hours=1),
        entry_type="market",
        entry_price=100.0,
        stop_price=95.0,
        target_price=110.0,
        risk_distance=5.0,
        max_holding_seconds=3600,
        cost_model_id="cost",
        state=CandidateState.ELIGIBLE,
    )


def test_target_fill_and_cost_are_recorded():
    bars = pd.DataFrame(
        [
            {"timestamp_utc": "2026-01-01T12:05:00Z", "open": 100, "high": 104, "low": 99, "close": 103},
            {"timestamp_utc": "2026-01-01T12:10:00Z", "open": 103, "high": 111, "low": 102, "close": 109},
        ]
    )
    outcome = simulate_candidate(
        candidate(),
        bars,
        CostModel("cost", spread_price=0.5),
        SimulationPolicy(allow_fill_on_creation_bar=True),
    )
    assert outcome.filled
    assert outcome.exit_reason == "target"
    assert outcome.gross_r == 2.0
    assert outcome.net_r == 1.9
