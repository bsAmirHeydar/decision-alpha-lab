from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import *

def test_training_publishes_only_test_oos_predictions():
    bundle,label,plan,trained=build_reference_training_bundle()
    assert len(trained.predictions)==bundle.manifest.test_count
    assert all(p.role==PredictionRole.TEST_OOS for p in trained.predictions)
    assert trained.model.selected_on_role==DatasetRole.VALIDATION and trained.model.no_execution_authority
    assert "test evidence was unavailable" in " ".join(trained.card.limitations)

def test_training_is_bit_reproducible():
    a=build_reference_training_bundle()[3];b=build_reference_training_bundle()[3]
    assert a.model.artifact_hash==b.model.artifact_hash and a.report.report_hash==b.report.report_hash
    assert [p.prediction_hash for p in a.predictions]==[p.prediction_hash for p in b.predictions]
