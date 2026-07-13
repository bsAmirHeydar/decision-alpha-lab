from strategy_factory_classical_v3 import *
def test_optional_dependency_clean_unavailable():
 p=DependencyProbe(disabled=('xgboost',));a=p.evaluate(BY_ID['xgboost_classifier']);assert not a.available;assert a.reason=='algorithm dependency unavailable';assert a.dependencies[0].state.value=='disabled'
def test_builtin_baseline_available():assert DependencyProbe().evaluate(BY_ID['prevalence']).available
def test_sklearn_availability_is_explicit():
 a=DependencyProbe().evaluate(BY_ID['logistic_regression']);assert a.available in (True,False);assert a.evidence_hash
