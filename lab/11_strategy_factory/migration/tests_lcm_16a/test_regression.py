def test_regression_receipt_is_zero_failure(load):
    report = load("python_regression_report.json")
    assert report["suite_count"] == 60
    assert report["passed_test_count"] == 3975
    assert report["failed_test_count"] == 0
    assert report["failed_suites"] == []
    assert report["validation_status"] == "PASS_WITH_RESIDUALS"


def test_lfs_boundary_is_not_mislabeled_as_product_failure(load):
    report = load("python_regression_report.json")
    lcm12a = next(item for item in report["suites"] if item["suite_id"] == "TESTS_LCM_12A")
    assert lcm12a["status"] == "PASS_WITH_BLOCKED_EVIDENCE"
    assert lcm12a["reason"] == "GIT_LFS_OBJECTS_NOT_MATERIALIZED"
    assert len(lcm12a["blocked_paths"]) == 2
    assert len(lcm12a["blocked_tests"]) == 3
