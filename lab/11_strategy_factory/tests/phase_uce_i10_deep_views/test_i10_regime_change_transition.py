import pytest

from strategy_factory_deep_views_v3.errors import DeepViewError
from strategy_factory_deep_views_v3.regime import CusumChangeDetector, RegimeModel


def test_regime_transition_probabilities_are_normalized():
    rows = [(float(i % 2), float(i // 2)) for i in range(20)]
    model = RegimeModel.fit(rows, k=2)
    for index in range(2):
        probabilities = model.transition_probabilities(index)
        assert abs(sum(probabilities) - 1.0) < 1e-12
        assert all(value > 0 for value in probabilities)


def test_cusum_detects_persistent_shift_but_not_reference_noise():
    detector = CusumChangeDetector.fit([0.0, 0.1, -0.1, 0.05, -0.05] * 10, threshold_sigma=3.0)
    assert detector.first_alarm_index([0.0, 0.02, -0.01, 0.01]) is None
    shifted = [0.0] * 5 + [2.0] * 20
    alarm = detector.first_alarm_index(shifted)
    assert alarm is not None and alarm >= 5
    assert detector.score(shifted) >= 1.0


def test_regime_transition_rejects_invalid_index_and_smoothing():
    model = RegimeModel.fit([(0.0,), (0.1,), (10.0,), (10.1,)], k=2)
    with pytest.raises(DeepViewError, match="out of range"):
        model.transition_probabilities(9)
    with pytest.raises(DeepViewError, match="smoothing"):
        model.transition_probabilities(0, -1.0)
