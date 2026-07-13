import pytest

from strategy_factory_deep_views_v3.adapters import AdapterPlan, probe_dependency, validate_adapter_plan
from strategy_factory_deep_views_v3.enums import DependencyStatus, MissingViewPolicy, TransferDecision
from strategy_factory_deep_views_v3.errors import DeepViewError
from strategy_factory_deep_views_v3.fusion import GatedFusion, StackedFusion
from strategy_factory_deep_views_v3.transfer import evaluate_transfer_boundary


def test_gated_fusion_abstains_when_total_confidence_is_too_low():
    targets = [0.0, 1.0, 2.0, 3.0]
    predictions = {"sequence": targets, "graph": [0.1, 0.9, 2.1, 2.9]}
    model = GatedFusion.fit(predictions, targets, MissingViewPolicy.GLOBAL_FALLBACK, 0.5)
    result = model.predict("row", {"sequence": 1.0, "graph": 1.2}, {"sequence": 0.1, "graph": 0.1})
    assert result.abstained
    assert result.reason == "insufficient_gate_confidence"


def test_stacking_rejects_non_oof_training_predictions():
    with pytest.raises(DeepViewError, match="out-of-fold"):
        StackedFusion.fit({"a": [0.0, 1.0]}, [0.0, 1.0], oof_predictions=False)


def test_transfer_boundary_rejects_final_test_overlap():
    boundary = evaluate_transfer_boundary("source", "target", ("a", "test"), ("train",), ("test",), True)
    assert boundary.decision is TransferDecision.REJECT
    assert "source_contains_target_final_test_rows" in boundary.blockers


def test_optional_dependency_probe_and_plan_fail_closed():
    module = "uce_i10_dependency_that_does_not_exist"
    probe = probe_dependency("test", module, "1.0.0")
    assert probe.status is DependencyStatus.MISSING
    plan = AdapterPlan("uce.deep.test@1.0.0", "test", {module: "1.0.0"}, True, 7)
    with pytest.raises(DeepViewError, match="unavailable"):
        validate_adapter_plan(plan)
