from strategy_factory_monitoring import *

def test_histogram_percentiles_and_slo():
    p=LatencySloPolicy("p","x",(100,500,1000,5000),500,1000,5000,5);h=FixedLatencyHistogram(p)
    for x in (10,50,100,300,900,6000):h.observe(x)
    s=h.snapshot(100);assert s.sample_count==6;assert s.p50_us<=s.p95_us<=s.p99_us;assert s.overflow_count==1

def test_latency_rejects_negative():
    import pytest
    h=FixedLatencyHistogram(reference_latency_policies()[0])
    with pytest.raises(ValueError):h.observe(-1)

def test_insufficient_samples_do_not_breach():
    p=LatencySloPolicy("p","x",(1,2),1,1,1,10);h=FixedLatencyHistogram(p);h.observe(100);assert not h.snapshot(1).slo_breached
