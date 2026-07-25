from collections import Counter

def test_exact_eligibility_accounting(eligibility):
    states = Counter(row["eligibility_state"] for row in eligibility)
    assert states == {
        "ELIGIBLE_FOR_LCM13B_WAVE_PLANNING": 613,
        "BLOCKED_REMAIN_LEGACY": 806,
    }

def test_no_high_or_critical_mismatch_on_eligible(eligibility, mismatches):
    eligible_ids = {row["consumer_id"] for row in eligibility if row["eligibility_state"].startswith("ELIGIBLE")}
    assert not [row for row in mismatches if row["consumer_id"] in eligible_ids and row["severity"] in {"HIGH","CRITICAL"}]

def test_blocked_consumers_never_cutover_authorized(eligibility):
    assert all(not row["cutover_authorized"] for row in eligibility)
    assert all(row["owner_approval_required"] for row in eligibility)
