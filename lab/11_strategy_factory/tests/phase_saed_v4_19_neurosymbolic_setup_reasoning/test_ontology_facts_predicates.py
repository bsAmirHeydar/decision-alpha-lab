import pytest
from saed_v4_neurosymbolic_setup_reasoning.ontology import compile_ontology,validate_fact
from saed_v4_neurosymbolic_setup_reasoning.facts import FactStore
from saed_v4_neurosymbolic_setup_reasoning.predicates import compile_predicates,evaluate_predicate
from saed_v4_neurosymbolic_setup_reasoning.errors import OntologyError,ContradictionError

def test_compile(load,ex):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));assert o['closed_world'] and len(o['concepts'])>=10
@pytest.mark.parametrize('pid,expected',[('p_context_active',True),('p_support_valid',True),('p_stage_triggered',True),('p_structure_high',True),('p_time_high',True),('p_manual_pass',False)])
def test_predicates(load,ex,pid,expected):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));p=compile_predicates(load(ex+'/PREDICATE_REGISTRY.JSON'),o);raw=load(ex+'/SYNTHETIC_FACTS.JSON');s=FactStore(o,raw['decision_time'])
 for f in raw['facts']:s.add(f)
 assert evaluate_predicate(p,s,'occurrence_synthetic_0001',pid) is expected
def test_future_fact_rejected(load,ex):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));f=dict(load(ex+'/SYNTHETIC_FACTS.JSON')['facts'][0]);f['known_time']=101
 with pytest.raises(OntologyError):validate_fact(o,f,100)
def test_unknown_concept_rejected(load,ex):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));f=dict(load(ex+'/SYNTHETIC_FACTS.JSON')['facts'][0]);f['concept_id']='unknown'
 with pytest.raises(OntologyError):validate_fact(o,f,100)
def test_contradiction(load,ex):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));f=dict(load(ex+'/SYNTHETIC_FACTS.JSON')['facts'][0]);s=FactStore(o,100);s.add(f);g=dict(f);g['fact_id']='opposite';g['polarity']=-1
 with pytest.raises(ContradictionError):s.add(g)
