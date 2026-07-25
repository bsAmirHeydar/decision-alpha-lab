def test_reference_parity_does_not_claim_terminal_parity(load):
    report = load("cross_language_parity_report.json")
    assert report["python_reference_vector_parity_status"] == "PASS"
    assert report["terminal_compiled_mql5_parity_status"] == "UNKNOWN"
    assert report["proof_ceiling"] == "PYTHON_AND_STATIC_REFERENCE_PARITY_NOT_TERMINAL_COMPILED_PARITY"


def test_security_and_authority_are_fail_closed(load):
    report = load("security_authority_audit.json")
    assert report["validation_status"] == "PASS"
    assert report["phase_forbidden_capability_hit_count"] == 0
    assert report["unreviewed_private_key_marker_count"] == 0
    assert report["heuristic_secret_assignment_hit_count"] == 0
    for key in (
        "runtime_authority_created", "live_order_authority_created",
        "capital_authority_created", "deletion_authority_created",
        "network_authority_created", "credential_authority_created",
    ):
        assert report[key] is False
