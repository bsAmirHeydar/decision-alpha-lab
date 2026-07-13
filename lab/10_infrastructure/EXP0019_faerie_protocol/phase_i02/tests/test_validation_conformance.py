from dataclasses import replace

from fp_i02_kernel.conformance import run_conformance
from fp_i02_kernel.enums import HealthState
from fp_i02_kernel.golden import golden_bundle, golden_candidate, golden_manifest
from fp_i02_kernel.validation import derive_health, validate_bundle, validate_candidate_against_relation, validate_manifest


def test_bundle_candidate_manifest_validation_pass():
    assert validate_bundle(golden_bundle()).passed
    assert validate_candidate_against_relation(golden_candidate()).passed
    assert validate_manifest(golden_manifest()).passed


def test_health_is_ready_for_clean_reports():
    bundle = golden_bundle()
    health = derive_health(bundle.semantic.config_hash, bundle.semantic.adapter_snapshot_hash, [validate_bundle(bundle)], 1)
    assert health.state is HealthState.READY
    assert health.primary_reason_code == "FP_RC_READY"


def test_conformance_suite_has_all_expected_checks():
    report = run_conformance()
    assert report["passed"] is True
    assert report["check_count"] == 19
    assert all(item["passed"] for item in report["checks"])
