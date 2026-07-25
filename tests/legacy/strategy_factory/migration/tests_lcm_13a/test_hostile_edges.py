def test_blocked_outputs_are_not_false_passes(results):
    blocked = [row for row in results if row["status"] == "BLOCKED"]
    assert blocked
    assert all(any(item["status"] == "BLOCKED_NOT_COMPARABLE" for item in row["dimension_results"]) for row in blocked)

def test_no_blocked_consumer_appears_as_pass(eligibility, results):
    blocked_ids = {row["consumer_id"] for row in eligibility if row["eligibility_state"] == "BLOCKED_REMAIN_LEGACY"}
    assert not [row for row in results if row["consumer_id"] in blocked_ids and row["status"] == "PASS"]
