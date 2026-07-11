from strategy_factory_training import *

def test_exact_registry_resolution_and_hash():
    a=reference_registry();b=reference_registry();assert a.registry_hash==b.registry_hash
    assert a.resolve(ModelFamily.LOGISTIC_RIDGE,"1.0.0",TaskKind.BINARY_CLASSIFICATION).family==ModelFamily.LOGISTIC_RIDGE
    try:a.resolve(ModelFamily.LOGISTIC_RIDGE,"2.0.0",TaskKind.BINARY_CLASSIFICATION);assert False
    except KeyError:pass
