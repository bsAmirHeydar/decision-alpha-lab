from strategy_factory_execution import compare_shadow_execution

def test_shadow_tolerance():
    x=compare_shadow_execution(intent_id="i",paper_order_id="p",observed_external_order_id="o",paper_fill_price=100,
      observed_fill_price=100.01,paper_fill_time_utc_msc=1000,observed_fill_time_utc_msc=1020,paper_volume=1,
      observed_volume=1,price_tolerance=.02,latency_tolerance_milliseconds=50,volume_tolerance=1e-9)
    assert x.matched
