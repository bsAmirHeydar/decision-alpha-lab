def test_baseline_preserved(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTROL_COMPARISON.JSON')['baseline_preserved']
def test_random_control_present(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTROL_COMPARISON.JSON')['random_control']['control_name']=='random_encoder'
def test_frozen_control_present(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTROL_COMPARISON.JSON')['frozen_control']['control_name']=='frozen_initial_encoder'
def test_no_auto_superiority_claim(load):assert not load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTROL_COMPARISON.JSON')['automatic_superiority_claim']
def test_from_scratch_deferred(load):assert 'deferred' in load('releases/history/strategy_factory/artifacts/saed_v4_11/GOLDEN_CONTROL_COMPARISON.JSON')['from_scratch_control']['status']
