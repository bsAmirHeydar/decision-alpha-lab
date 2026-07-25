from datetime import datetime, timedelta, timezone
import pytest

from strategy_factory.contracts import AnatomyEvent, ContractError, Direction, FeatureSnapshot, FeatureValue


def event() -> AnatomyEvent:
    t = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    return AnatomyEvent(
        event_id="E1",
        strategy_id="S1",
        strategy_version="1.0.0",
        symbol="NQ",
        direction=Direction.LONG,
        event_time_utc=t,
        known_time_utc=t + timedelta(minutes=5),
        confirmation_time_utc=t + timedelta(minutes=5),
        reference_price=100.0,
        invalidation_price=95.0,
    )


def test_event_contract_accepts_causal_time():
    event().validate()


def test_event_contract_rejects_future_ordering():
    e = event()
    bad = AnatomyEvent(**{**e.__dict__, "known_time_utc": e.event_time_utc - timedelta(seconds=1)})
    with pytest.raises(ContractError):
        bad.validate()


def test_snapshot_rejects_future_feature():
    e = event()
    snapshot = FeatureSnapshot(
        snapshot_id="S",
        event_id=e.event_id,
        snapshot_time_utc=e.confirmation_time_utc,
        features=[FeatureValue("x", 1.0, e.confirmation_time_utc + timedelta(seconds=1), "test", "1")],
        schema_version="1",
        producer_version="1",
    )
    with pytest.raises(ContractError):
        snapshot.validate()
