def test_acceptance_and_hostile_review_pass(dual_root):
    import json
    acceptance = json.loads((dual_root / "reports/acceptance_report.json").read_text(encoding="utf-8"))
    hostile = json.loads((dual_root / "reports/hostile_review_report.json").read_text(encoding="utf-8"))
    assert acceptance["passed"] is True
    assert acceptance["input_equality_failure_count"] == 0
    assert acceptance["eligible_high_critical_mismatch_count"] == 0
    assert acceptance["suppressed_mismatch_count"] == 0
    assert hostile["result"] == "PASS"
    assert hostile["failed_check_count"] == 0
