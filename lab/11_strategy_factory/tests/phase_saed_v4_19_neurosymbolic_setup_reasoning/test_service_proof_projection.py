from saed_v4_neurosymbolic_setup_reasoning.service import run_reference
from saed_v4_neurosymbolic_setup_reasoning.proofs import verify
from saed_v4_neurosymbolic_setup_reasoning.projection import project

def bundle(load,ex):
 return {'ontology':load(ex+'/ONTOLOGY_CONTRACT.JSON'),'predicates':load(ex+'/PREDICATE_REGISTRY.JSON'),'temporal':load(ex+'/TEMPORAL_LOGIC_CONTRACT.JSON'),'grammar':load(ex+'/RULE_GRAMMAR.JSON'),'budget':load(ex+'/REASONING_BUDGET.JSON'),'envelope':load(ex+'/DECISION_ENVELOPE_CONTRACT.JSON')}
def test_reference(load,ex,art):
 raw=load(ex+'/SYNTHETIC_FACTS.JSON');r=run_reference(bundle(load,ex),raw['facts'],load(ex+'/SYNTHETIC_EVENTS.JSON')['events'],load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses'],load(ex+'/RULE_LIBRARY.JSON')['rules'],load(ex+'/SOFT_INPUTS.JSON'),100,load(art+'/GOLDEN_UPSTREAM_VALIDATION.JSON')['upstream_handoff_hash']);assert r['projection']['treatment_id']=='treatment_alpha' and verify(r['proof'])
def test_proof_hash(load,art):assert verify(load(art+'/GOLDEN_PROOF_ENVELOPE.JSON'))
def test_hard_block(load,ex):
 e=load(ex+'/DECISION_ENVELOPE_CONTRACT.JSON');x=project([],{'scores':[]},e,['r_block'],False);assert x['directive']=='reject' and x['treatment_id']=='skip'
def test_contradiction_projection(load,ex):
 e=load(ex+'/DECISION_ENVELOPE_CONTRACT.JSON');x=project([],{'scores':[]},e,[],True);assert x['directive']=='quarantine'
def test_low_confidence_abstains(load,ex):
 e=load(ex+'/DECISION_ENVELOPE_CONTRACT.JSON');x=project([],{'scores':[{'rule_id':'x','score':0.1,'treatment_id':'treatment_alpha','effect':'recommend'}]},e,[],False);assert x['directive']=='abstain'
