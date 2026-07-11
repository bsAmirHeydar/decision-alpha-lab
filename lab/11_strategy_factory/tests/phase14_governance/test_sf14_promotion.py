from dataclasses import replace
import pytest
from strategy_factory_governance.examples import *
from strategy_factory_governance import *

def test_reference_evaluation_passes_all_gates():
    scope=reference_scope();e=reference_evidence();p=reference_policy()
    result=evaluate_promotion(e,scope,p,reference_measurements(),evaluated_at_utc_msc=10,evaluator_id="test")
    result.validate();assert result.verdict==PromotionVerdict.ELIGIBLE
    assert all(g.status==GateStatus.PASS for g in result.gates)

def test_weak_test_score_fails_closed():
    m=replace(reference_measurements(),test_score=0.10)
    result=evaluate_promotion(reference_evidence(),reference_scope(),reference_policy(),m,
        evaluated_at_utc_msc=10,evaluator_id="test")
    assert result.verdict==PromotionVerdict.INELIGIBLE
    assert any(g.reason_code=="TEST_SCORE_BELOW_FLOOR" for g in result.gates)

def test_scope_schema_mismatch_is_rejected_before_gates():
    scope=replace(reference_scope(),feature_schema_hash="different",scope_id="").with_id()
    with pytest.raises(ValueError,match="feature schema"):
        evaluate_promotion(reference_evidence(),scope,reference_policy(),reference_measurements(),
            evaluated_at_utc_msc=10,evaluator_id="test")
