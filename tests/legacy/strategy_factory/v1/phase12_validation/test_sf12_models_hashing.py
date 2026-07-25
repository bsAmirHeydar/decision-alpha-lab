from strategy_factory_validation import ValidationPlan, SplitMethod

def plan():
    return ValidationPlan("p","1",SplitMethod.ANCHORED_WALK_FORWARD,"run","mh","ah","s","space",0,1000,200,100,100,100,10,10,1,1,1,8,12).with_hash()

def test_plan_hash_and_validation():
    p=plan();p.validate();assert p.plan_hash.startswith("vplan_")

def test_plan_rejects_bad_lineage():
    p=ValidationPlan("","1",SplitMethod.ANCHORED_WALK_FORWARD,"run","mh","ah","s","space",0,1000,200,100,100,100,10,10,1,1,1)
    try:p.validate()
    except ValueError:pass
    else:raise AssertionError("missing lineage accepted")
