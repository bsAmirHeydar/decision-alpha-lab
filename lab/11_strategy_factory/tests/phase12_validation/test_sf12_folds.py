from strategy_factory_validation import *

def _plan(method):
 return ValidationPlan("p","1",method,"run","mh","ah","s","space",0,1500,300,100,100,200,20,30,1,1,1,10,12).with_hash()

def test_anchored_folds_are_ordered_and_gapped():
 folds=compile_walk_forward(_plan(SplitMethod.ANCHORED_WALK_FORWARD));assert len(folds)>=4
 for f in folds:
  assert f.train.start_utc_msc==0
  assert f.train.end_utc_msc<=f.validation.start_utc_msc<f.validation.end_utc_msc<=f.test.start_utc_msc
  assert role_for_timestamp(f,f.purge_before_validation.start_utc_msc)==FoldRole.PURGED

def test_rolling_train_moves():
 folds=compile_walk_forward(_plan(SplitMethod.ROLLING_WALK_FORWARD));assert folds[1].train.start_utc_msc>folds[0].train.start_utc_msc
