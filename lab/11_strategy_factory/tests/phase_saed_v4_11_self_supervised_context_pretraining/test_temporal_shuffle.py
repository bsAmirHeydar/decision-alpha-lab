def test_shuffle_audit_is_diagnostic(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TEMPORAL_SHUFFLE_AUDIT.JSON')['admission_effect']=='diagnostic_only'
def test_no_future_suffix(load):assert not load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TEMPORAL_SHUFFLE_AUDIT.JSON')['future_suffix_used']
def test_shuffle_method_deterministic(load):assert load('lab/11_strategy_factory/artifacts/saed_v4_11/GOLDEN_TEMPORAL_SHUFFLE_AUDIT.JSON')['method']=='deterministic_reverse_order'
