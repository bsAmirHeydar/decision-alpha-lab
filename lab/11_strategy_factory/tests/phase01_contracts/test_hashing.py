from strategy_factory_contracts.hashing import fnv1a64_utf16le, stable_id

def test_fnv_is_deterministic():
    assert fnv1a64_utf16le("alpha") == fnv1a64_utf16le("alpha")
    assert fnv1a64_utf16le("alpha") != fnv1a64_utf16le("beta")

def test_expected_event_id_vector():
    canonical = 'exp0017_temporal_divergence|1.0.0|NQ|ES|LONG|1783771200000|1783771260000|1783771320000|60|none|cluster_20260711_001|sha256_deadbeef'
    assert stable_id("evt", canonical) == 'evt_cd79492563408d2b'
