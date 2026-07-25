from strategy_factory_training.examples import build_reference_training_bundle
from strategy_factory_training import *

def test_plan_lineage_mismatch_fails_closed():
    bundle,label,plan,_=build_reference_training_bundle();bad=TrainingPlan(plan.plan_id,plan.plan_version,plan.task,"wrong",plan.feature_schema_hash,plan.label_contract_hash,plan.model_families,plan.transform_spec_hash,plan.calibration_method,plan.selection_metric).with_hash()
    try:train_binary(bundle,label,bad,TransformSpec());assert False
    except ValueError as error:assert "lineage" in str(error)

def test_published_prediction_role_must_be_oos():
    p=PredictionRecord("m","c","d","r","f",PredictionRole.VALIDATION_SELECTION,0,0.5,0,0).with_hashes()
    try:p.validate();assert False
    except ValueError:pass
