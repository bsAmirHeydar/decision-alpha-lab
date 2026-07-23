def test_documentation_integrity_is_explicit_about_residuals(load):
    report = load("documentation_integrity_report.json")
    assert report["engineering_policy_status"] == "PASS"
    assert report["obsidian_vault_status"] == "PASS"
    assert report["obsidian_error_count"] == 0
    assert report["obsidian_warning_count"] == 0
    assert len(report["known_status_freshness_residuals"]) == 3


def test_closure_matrix_is_non_compensatory(load):
    matrix = load("closure_test_matrix.json")
    statuses = {item["gate_id"]: item["status"] for item in matrix["gates"]}
    assert matrix["non_compensatory"] is True
    assert matrix["phase_decision"] == "BLOCKED"
    assert matrix["deterministic_failure_count"] == 0
    assert statuses["MQL5_METAEDITOR_COMPILE"] == "UNKNOWN"
    assert statuses["STRATEGY_TESTER_GOLDEN_REPLAY"] == "UNKNOWN"
    assert statuses["OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS"] == "UNKNOWN"
    assert statuses["GIT_LFS_MATERIALIZATION"] == "BLOCKED"
