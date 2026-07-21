def test_scenario_input_equality(scenarios):
    assert all(row["input_equality"] for row in scenarios)
    assert all(row["legacy_input_digest"] == row["canonical_input_digest"] == row["causal_input_digest"] for row in scenarios)

def test_result_input_equality(results):
    assert all(row["input_equality"] for row in results)
    assert all(row["legacy_input_digest"] == row["canonical_input_digest"] == row["causal_input_digest"] for row in results)
