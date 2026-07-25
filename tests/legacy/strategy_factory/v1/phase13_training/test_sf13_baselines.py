from strategy_factory_training.baselines import *
from strategy_factory_training.enums import *

def test_constant_baselines():
    x=[(0.0,),(1.0,)];y=[0.0,1.0]
    assert fit_never(1,TaskKind.BINARY_CLASSIFICATION).probability(x[0])<1e-6
    assert fit_always(1,TaskKind.BINARY_CLASSIFICATION).probability(x[0])>1-1e-6
    assert fit_prevalence(x,y,TaskKind.BINARY_CLASSIFICATION).probability(x[0])==0.5

def test_logistic_ridge_learns_separable_signal_deterministically():
    x=[(-2.0,),(-1.0,),(-0.5,),(0.5,),(1.0,),(2.0,)];y=[0,0,0,1,1,1]
    a=fit_logistic_ridge(x,y,400,0.1,0.01);b=fit_logistic_ridge(x,y,400,0.1,0.01)
    assert a.parameter_values==b.parameter_values and a.probability((1.0,))>a.probability((-1.0,))

def test_threshold_and_stump_are_bounded():
    x=[(-2.0,),(-1.0,),(1.0,),(2.0,)];y=[0,0,1,1]
    for family in (ModelFamily.SINGLE_FEATURE_THRESHOLD,ModelFamily.DECISION_STUMP):
        model=fit_threshold(x,y,TaskKind.BINARY_CLASSIFICATION,8,family);assert model.probability((2.0,))>model.probability((-2.0,))
