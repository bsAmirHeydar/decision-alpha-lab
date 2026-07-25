from strategy_factory_training import *

def test_feature_and_label_hashes_are_deterministic():
    a=FeatureColumn("f","1.0.0",0).with_hash();b=FeatureColumn("f","1.0.0",0).with_hash();assert a.column_hash==b.column_hash
    x=LabelContract("l","1.0.0",LabelKind.BINARY_NET_R).with_hash();assert x.label_hash==LabelContract("l","1.0.0",LabelKind.BINARY_NET_R).with_hash().label_hash

def test_training_plan_rejects_duplicate_families():
    plan=TrainingPlan("p","1",TaskKind.BINARY_CLASSIFICATION,"d","f","l",(ModelFamily.NEVER_TRADE,ModelFamily.NEVER_TRADE),"t",CalibrationMethod.NONE,"log_loss")
    try:plan.validate();assert False
    except ValueError:pass
