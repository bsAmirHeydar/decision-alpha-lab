import pytest
from saed_v4_neurosymbolic_setup_reasoning.temporal import compile_temporal,evaluate_clause
from saed_v4_neurosymbolic_setup_reasoning.ontology import compile_ontology
from saed_v4_neurosymbolic_setup_reasoning.predicates import compile_predicates
from saed_v4_neurosymbolic_setup_reasoning.rules import compile_rule_library
from saed_v4_neurosymbolic_setup_reasoning.errors import TemporalLogicError,RuleError

@pytest.mark.parametrize('cid,expected',[('tc_context_seen',True),('tc_armed_precedes_trigger',True),('tc_support_persistent',True)])
def test_temporal(load,ex,cid,expected):
 tc=compile_temporal(load(ex+'/TEMPORAL_LOGIC_CONTRACT.JSON'));clauses=load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses'];events=load(ex+'/SYNTHETIC_EVENTS.JSON')['events'];c=next(x for x in clauses if x['clause_id']==cid);assert evaluate_clause(c,events,100,tc) is expected
def test_future_suffix_ignored(load,ex):
 tc=compile_temporal(load(ex+'/TEMPORAL_LOGIC_CONTRACT.JSON'));events=load(ex+'/SYNTHETIC_EVENTS.JSON')['events']+[{'event_id':'future','event_time':105,'known_time':105,'predicate_ids':['p_stage_armed']}];c=load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses'][1];assert evaluate_clause(c,events,100,tc)
def test_invalid_window(load,ex):
 tc=compile_temporal(load(ex+'/TEMPORAL_LOGIC_CONTRACT.JSON'));c=dict(load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses'][0]);c['window']=999
 with pytest.raises(TemporalLogicError):evaluate_clause(c,[],100,tc)
def test_compile_rules(load,ex):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));p=compile_predicates(load(ex+'/PREDICATE_REGISTRY.JSON'),o);r=load(ex+'/RULE_LIBRARY.JSON')['rules'];lib=compile_rule_library(load(ex+'/RULE_GRAMMAR.JSON'),r,p['predicates'].keys(),[x['clause_id'] for x in load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses']]);assert len(lib['rules'])==len(r)
def test_dynamic_rule_field_rejected(load,ex):
 o=compile_ontology(load(ex+'/ONTOLOGY_CONTRACT.JSON'));p=compile_predicates(load(ex+'/PREDICATE_REGISTRY.JSON'),o);r=load(ex+'/RULE_LIBRARY.JSON')['rules'];r[0]['python']='eval(1)'
 with pytest.raises(RuleError):compile_rule_library(load(ex+'/RULE_GRAMMAR.JSON'),r,p['predicates'].keys(),[x['clause_id'] for x in load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses']])
