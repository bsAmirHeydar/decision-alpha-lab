from strategy_factory.serving import benchmark


def test_benchmark_returns_percentiles():
    result = benchmark(lambda: 1+1, warmup=1, iterations=5)
    assert result["iterations"] == 5
    assert result["p99_ns"] >= result["p50_ns"]
