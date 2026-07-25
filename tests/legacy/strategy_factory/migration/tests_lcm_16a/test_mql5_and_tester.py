def test_static_scan_is_not_overstated_as_metaeditor(load):
    matrix = load("mql5_compile_matrix.json")
    assert matrix["total_mql5_source_count"] == 2559
    assert matrix["mq5_file_count"] == 293
    assert matrix["mqh_file_count"] == 2266
    assert matrix["static_compatibility_status"] == "PASS"
    assert matrix["metaeditor_status"] == "UNKNOWN"


def test_strategy_tester_remains_unknown(load):
    matrix = load("strategy_tester_matrix.json")
    assert matrix["strategy_tester_status"] == "UNKNOWN"
    assert matrix["golden_replay_status"] == "UNKNOWN"
    assert all(item["strategy_tester_status"] == "UNKNOWN" for item in matrix["targets"])
