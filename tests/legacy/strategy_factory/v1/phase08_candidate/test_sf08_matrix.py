import pytest
from strategy_factory_candidate import *

def test_matrix_compiles_and_sorts():
    r=build_fixture_registry();m=build_reference_matrix(r);assert m.compiled;assert [x.priority for x in m.templates]==[10,20]

def test_matrix_hash_stable():
    r1=build_fixture_registry();r2=build_fixture_registry();assert build_reference_matrix(r1).plan_hash==build_reference_matrix(r2).plan_hash

def test_unresolved_policy_rejected():
    r=build_fixture_registry();m=CandidateMatrixPlan("x","1")
    p=PolicyParameters();m.add(CandidateTemplate("t","1",True,1,"missing","1",p,"sf08.stop.anatomy_invalidation","1.0.0",p,"sf08.exit.fixed_r","1.0.0",p))
    with pytest.raises(ValueError):m.compile(r)
