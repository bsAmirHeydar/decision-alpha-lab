import pytest

from strategy_factory_deep_views_v3.errors import DeepViewError
from strategy_factory_deep_views_v3.golden import candles, raster_spec
from strategy_factory_deep_views_v3.raster import audit_prefix_invariance, render_chart_raster


def test_pixel_audit_reports_zero_changes_for_future_perturbations():
    source = candles()
    cutoff = source[15]["time_ms"]
    report = audit_prefix_invariance(
        raster_spec(),
        "ctx",
        cutoff,
        source,
        ({"time_ms": cutoff + 1, "open": 1e6, "high": 1e6 + 1, "low": 1e6 - 1, "close": 1e6},),
    )
    assert report.prefix_invariant
    assert report.changed_pixel_count == 0
    assert report.max_abs_difference == 0.0


def test_malformed_future_row_is_not_part_of_past_validation():
    source = candles(5)
    cutoff = source[-1]["time_ms"]
    artifact = render_chart_raster(
        raster_spec(),
        "ctx",
        cutoff,
        source + ({"time_ms": cutoff + 1, "open": 3, "high": 1, "low": 2, "close": 4},),
    )
    assert artifact.known_time_ms == cutoff


def test_duplicate_known_time_candle_is_rejected():
    source = candles(5)
    duplicate = dict(source[-1])
    with pytest.raises(DeepViewError, match="strictly increase"):
        render_chart_raster(raster_spec(), "ctx", source[-1]["time_ms"], source + (duplicate,))
