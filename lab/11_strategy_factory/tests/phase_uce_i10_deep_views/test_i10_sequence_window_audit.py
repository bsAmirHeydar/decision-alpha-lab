import pytest

from strategy_factory_deep_views_v3.audit import deterministic_replay_audit, future_perturbation_audit
from strategy_factory_deep_views_v3.contracts import SequenceWindowSpec
from strategy_factory_deep_views_v3.errors import DeepViewError
from strategy_factory_deep_views_v3.sequence import SequenceWindowBuilder


def _rows():
    return (
        {"time_ms": 100, "a": 1.0, "b": 10.0},
        {"time_ms": 200, "a": 2.0, "b": None},
        {"time_ms": 300, "a": 3.0, "b": 30.0},
    )


def test_sequence_window_left_pads_and_masks_missing_values():
    spec = SequenceWindowSpec("seq", "1.0.0", 5, ("a", "b"))
    artifact = SequenceWindowBuilder(spec).build("ctx", 250, _rows())
    assert artifact.timestamps_ms[-2:] == (100, 200)
    assert len(artifact.values) == 10
    assert sum(artifact.mask) == 3
    assert artifact.values[-1] == 0.0


def test_sequence_window_ignores_future_suffix_even_when_suffix_is_reordered():
    spec = SequenceWindowSpec("seq", "1.0.0", 3, ("a", "b"))
    builder = SequenceWindowBuilder(spec)
    base = builder.build("ctx", 250, _rows())
    extended = builder.build(
        "ctx",
        250,
        _rows() + (
            {"time_ms": 999, "a": 999.0, "b": 999.0},
            {"time_ms": 700, "a": -999.0, "b": -999.0},
        ),
    )
    assert extended.evidence_hash == base.evidence_hash
    assert extended.values == base.values


def test_sequence_window_rejects_duplicate_known_time_rows():
    spec = SequenceWindowSpec("seq", "1.0.0", 3, ("a",))
    with pytest.raises(DeepViewError, match="strictly increasing"):
        SequenceWindowBuilder(spec).build(
            "ctx",
            250,
            (
                {"time_ms": 100, "a": 1.0},
                {"time_ms": 100, "a": 2.0},
            ),
        )


def test_generic_future_and_replay_audits_are_hash_stable():
    audit = future_perturbation_audit(lambda rows: tuple(row for row in rows if row <= 2), (1, 2), (3, 4))
    assert audit.passed
    replay = deterministic_replay_audit(lambda: {"b": 2, "a": 1}, runs=4)
    assert replay.passed
    assert len(set(replay.run_hashes)) == 1
