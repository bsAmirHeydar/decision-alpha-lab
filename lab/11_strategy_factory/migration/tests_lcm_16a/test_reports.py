def test_acceptance_distinguishes_package_from_program(load):
    report = load("reports/acceptance_report.json")
    assert report["package_validation"] == "PASS"
    assert report["deterministic_gate_status"] == "PASS"
    assert report["external_evidence_status"] == "UNKNOWN_BLOCKING"
    assert report["phase_decision"] == "BLOCKED"
    assert report["migration_program_closure"] == "NOT_AUTHORIZED"


def test_hostile_review_passes_all_cases(load):
    report = load("reports/hostile_review_report.json")
    assert report["hostile_case_count"] == 8
    assert report["failed_hostile_case_count"] == 0
    assert all(item["status"] == "PASS" for item in report["checks"])


def test_determinism_report_preserves_external_evidence_boundary(load):
    report = load("reports/determinism_report.json")
    assert report["baseline_amendment_rebuilt_from_bound_inputs"] is True
    assert report["wall_clock_excluded_from_identity"] is True
    assert report["external_evidence_can_change_status_only_with_bound_logs"] is True
