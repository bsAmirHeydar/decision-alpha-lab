from strategy_factory_qualification_v3.conformance import run_conformance


def test_repository_reference_is_blocked_without_external_evidence():
    result = run_conformance(False)
    assert result["report"]["activation_allowed"] is False
    assert result["bundle"]["external_evidence_present"] is False


def test_synthetic_full_matrix_can_exercise_qualified_path():
    result = run_conformance(True)
    assert result["report"]["activation_allowed"] is True
    assert result["bundle"]["external_evidence_present"] is True
