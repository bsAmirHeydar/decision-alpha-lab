from strategy_factory_candidate import *

def test_parameter_hash_stable():
    p=PolicyParameters();assert p.hash==PolicyParameters().hash

def test_template_hash_changes_with_r():
    p=PolicyParameters();a=CandidateTemplate("t","1",True,1,"e","1",p,"s","1",p,"x","1",p)
    n=list(p.numeric);n[0]=2.0;p2=PolicyParameters(tuple(n),p.integers)
    b=CandidateTemplate("t","1",True,1,"e","1",p,"s","1",p,"x","1",p2)
    assert a.hash!=b.hash

def test_candidate_id_stable():
    from strategy_factory_candidate.fixtures import build_fixture_registry,build_reference_matrix
    from sf08_helpers import fixture
    r=build_fixture_registry();m=build_reference_matrix(r);e,s,f=fixture();eng=CandidateEngine(r,m);a=eng.build(e,s,f,8)[0];b=CandidateEngine(r,m).build(e,s,f,8)[0];assert a.candidate_id==b.candidate_id
