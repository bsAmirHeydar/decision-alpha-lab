def test_raw_mismatch_accounting(dual_root, mismatches):
    import json
    frequency = json.loads((dual_root / "mismatch_frequency_registry.json").read_text(encoding="utf-8"))
    assert frequency["raw_mismatch_count"] == len(mismatches)
    assert frequency["suppressed_mismatch_count"] == 0
    assert frequency["aggregation_rule_count"] == 0
    assert frequency["repeated_mismatches_retained"] is True

def test_every_mismatch_is_blocking_or_adjudicated(mismatches):
    assert mismatches
    assert all(row["status"] in {"OPEN_BLOCKING","RESOLVED","APPROVED_VARIANCE","REJECTED"} for row in mismatches)
    assert all(row["aggregation_rule_id"] is None for row in mismatches)
    assert all(row["repeated_mismatch_retained"] is True for row in mismatches)

def test_no_automatic_variance(dual_root):
    import json
    variance = json.loads((dual_root / "variance_approval_registry.json").read_text(encoding="utf-8"))
    assert variance["approval_count"] == 0
    assert variance["automatic_variance_approval_allowed"] is False
