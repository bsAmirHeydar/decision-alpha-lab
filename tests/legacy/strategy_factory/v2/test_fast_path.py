import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

from strategy_factory.contracts import AnatomyEvent, Direction
from strategy_factory.decision import DecisionStatus
from strategy_factory.serving import build_reference_fast_engine

SPEC = Path(__file__).resolve().parents[1] / "examples" / "manifests_v2" / "temporal_divergence_fast.json"


def event(eid="e"):
    t = datetime(2026,1,1,12,tzinfo=timezone.utc)
    return AnatomyEvent(eid,"exp0017_temporal_divergence_fast","2.0.0","NQ",Direction.LONG,t,t,t,100,99)


def state(strength=2.0):
    return {"confirmation_close":100.2,"atr":1.0,"reference_extreme":99.0,"divergence_strength":strength,"volatility_regime":1.0,"spread_r":.01}


def test_fast_path_produces_decision_and_telemetry():
    engine = build_reference_fast_engine(json.loads(SPEC.read_text()))
    result = engine.decide(event(), state(), event().confirmation_time_utc, state_generation=1)
    assert result.status in {DecisionStatus.TRADE, DecisionStatus.ABSTAIN}
    assert result.plan_hash
    assert "total" in result.latency_ns
    assert len(engine.telemetry.snapshot()) == 1


def test_fast_path_abstains_on_missing_context():
    engine = build_reference_fast_engine(json.loads(SPEC.read_text()))
    result = engine.decide(event(), {"confirmation_close":100.2}, event().confirmation_time_utc, state_generation=1)
    assert result.status == DecisionStatus.ABSTAIN
    assert result.reason_codes


def test_fast_path_deduplicates_same_request():
    engine = build_reference_fast_engine(json.loads(SPEC.read_text()))
    e = event(); t=e.confirmation_time_utc
    engine.decide(e, state(), t, state_generation=1)
    duplicate = engine.decide(e, state(), t, state_generation=1)
    assert duplicate.status == DecisionStatus.ABSTAIN
    assert "duplicate_decision_request" in duplicate.reason_codes
