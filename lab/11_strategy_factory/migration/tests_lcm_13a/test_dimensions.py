EXPECTED = {
    "INPUT_DIGEST","KNOWN_TIME","STATE","EVENT","DECISION","REQUEST",
    "VISUAL_ANCHOR","REASON_CODE","RESOLVED_LOCATOR","SIDE_EFFECT_AUTHORITY",
}

def test_all_hard_dimensions_compared(results):
    for row in results:
        assert {item["dimension"] for item in row["dimension_results"]} == EXPECTED

def test_no_tolerance_on_any_observation(results):
    assert all(not item["tolerance_applied"] for row in results for item in row["dimension_results"])
