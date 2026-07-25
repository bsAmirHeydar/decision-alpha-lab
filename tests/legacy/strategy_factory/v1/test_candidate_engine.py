from datetime import datetime, timezone
from pathlib import Path

from strategy_factory.candidate_engine import generate_candidates
from strategy_factory.contracts import AnatomyEvent, Direction
from strategy_factory.manifest import load_manifest


def test_candidate_matrix_is_deterministic_and_valid():
    manifest = load_manifest(Path(__file__).resolve().parents[1] / "examples" / "manifests" / "temporal_divergence.json")
    t = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    event = AnatomyEvent(
        event_id="E",
        strategy_id=manifest.strategy_id,
        strategy_version=manifest.version,
        symbol="NQ",
        direction=Direction.LONG,
        event_time_utc=t,
        known_time_utc=t,
        confirmation_time_utc=t,
        reference_price=100.0,
        invalidation_price=95.0,
    )
    context = {
        "confirmation_close": 101.0,
        "atr": 5.0,
        "impulse_start": 95.0,
        "impulse_end": 105.0,
        "reference_extreme": 95.0,
        "target_price": 115.0,
    }
    first = generate_candidates(event, context, manifest)
    second = generate_candidates(event, context, manifest)
    assert len(first) == 12
    assert [x.candidate_id for x in first] == [x.candidate_id for x in second]
    for candidate in first:
        candidate.validate()
