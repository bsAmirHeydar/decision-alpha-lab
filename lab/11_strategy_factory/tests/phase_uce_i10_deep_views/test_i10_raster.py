import pytest
from strategy_factory_deep_views_v3.golden import candles,raster_spec
from strategy_factory_deep_views_v3.raster import render_chart_raster,prefix_invariance_passes
from strategy_factory_deep_views_v3.errors import DeepViewError
def test_raster_is_prefix_invariant_and_fixed_shape():
    cs=candles();spec=raster_spec();cut=cs[19]['time_ms'];a=render_chart_raster(spec,'ctx',cut,cs);future=({'time_ms':cut+60000,'open':999,'high':1000,'low':998,'close':999.5},)
    assert a.shape==(3,24,20);assert prefix_invariance_passes(spec,'ctx',cut,cs,future)
def test_raster_rejects_invalid_ohlc():
    spec=raster_spec();bad=({'time_ms':1,'open':2,'high':1,'low':0,'close':2},)
    with pytest.raises(DeepViewError,match='high'):render_chart_raster(spec,'ctx',1,bad)
