from collections import Counter

def test_exact_consumer_accounting(consumers):
    assert len(consumers) == 1419
    assert Counter(row["domain"] for row in consumers) == {
        "CONTEXT": 321,
        "SETUP": 60,
        "TREATMENT": 422,
        "VISUAL": 128,
        "DOCUMENTATION": 488,
    }

def test_three_scenarios_per_consumer(consumers, scenarios):
    assert len(scenarios) == len(consumers) * 3
    counts = Counter(row["consumer_id"] for row in scenarios)
    assert set(counts.values()) == {3}

def test_scenario_kinds_complete(scenarios):
    assert set(row["scenario_kind"] for row in scenarios) == {
        "HISTORICAL_REPLAY",
        "CONTROLLED_LIVE_LIKE",
        "RESTART_REPLAY",
    }
