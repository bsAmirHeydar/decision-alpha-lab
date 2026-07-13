from strategy_factory_deep_views_v3.contracts import ExportAssessment, SeedRunObservation
from strategy_factory_deep_views_v3.enums import ExportPath, QualificationDecision
from strategy_factory_deep_views_v3.gates import evaluate_deep_admission
from strategy_factory_deep_views_v3.golden import qualification_evidence
from strategy_factory_deep_views_v3.qualification import qualify_deep_model


def _admission(sample_size=2000, clusters=200, diversity=5):
    return evaluate_deep_admission("d", "m", sample_size, clusters, diversity, True, True, True, True, 0.6, "aug", "abl")


def test_duplicate_seed_is_a_hard_qualification_blocker():
    seeds, ablations, export = qualification_evidence()
    duplicate = seeds[:2] + (SeedRunObservation(17, "succeeded", 0.7, 0.5, 0.02, 10, 1, "duplicate"),)
    result = qualify_deep_model("a@1.0.0", "m", _admission(), duplicate, ablations, export, 0.5)
    assert result.decision is QualificationDecision.REJECTED
    assert "duplicate_seed_run" in result.blockers


def test_admission_warning_caps_model_at_challenger_only():
    seeds, ablations, export = qualification_evidence()
    admission = _admission(sample_size=700, clusters=70, diversity=3)
    result = qualify_deep_model("a@1.0.0", "m", admission, seeds, ablations, export, 0.5)
    assert result.decision is QualificationDecision.CHALLENGER_ONLY
    assert "admission_warning_prevents_promotion" in result.warnings


def test_export_latency_and_parity_are_hard_blockers():
    seeds, ablations, _ = qualification_evidence()
    export = ExportAssessment(ExportPath.ONNX, True, 1e-3, 100.0, "artifact", "slow", "evidence")
    result = qualify_deep_model("a@1.0.0", "m", _admission(), seeds, ablations, export, 0.5)
    assert "export_parity_failed" in result.blockers
    assert "latency_budget_exceeded" in result.blockers
