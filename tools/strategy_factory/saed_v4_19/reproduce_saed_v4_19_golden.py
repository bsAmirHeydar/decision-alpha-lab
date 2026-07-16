from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'lab/11_strategy_factory/python'))
from saed_v4_neurosymbolic_setup_reasoning.service import run_reference
from saed_v4_neurosymbolic_setup_reasoning.proofs import verify
load=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
ex='lab/11_strategy_factory/examples/saed_v4_19';art='lab/11_strategy_factory/artifacts/saed_v4_19'
contracts={'ontology':load(ex+'/ONTOLOGY_CONTRACT.JSON'),'predicates':load(ex+'/PREDICATE_REGISTRY.JSON'),'temporal':load(ex+'/TEMPORAL_LOGIC_CONTRACT.JSON'),'grammar':load(ex+'/RULE_GRAMMAR.JSON'),'budget':load(ex+'/REASONING_BUDGET.JSON'),'envelope':load(ex+'/DECISION_ENVELOPE_CONTRACT.JSON')};facts=load(ex+'/SYNTHETIC_FACTS.JSON');up=load(art+'/GOLDEN_UPSTREAM_VALIDATION.JSON')
r=run_reference(contracts,facts['facts'],load(ex+'/SYNTHETIC_EVENTS.JSON')['events'],load(ex+'/TEMPORAL_CLAUSES.JSON')['clauses'],load(ex+'/RULE_LIBRARY.JSON')['rules'],load(ex+'/SOFT_INPUTS.JSON'),facts['decision_time'],up['upstream_handoff_hash'])
gp=load(art+'/GOLDEN_PROOF_ENVELOPE.JSON');proj=load(art+'/GOLDEN_CONSTRAINT_PROJECTION.JSON')
assert verify(r['proof']) and r['proof']['proof_hash']==gp['proof_hash'] and r['projection']['projection_hash']==proj['projection_hash']
print('SAED V4-19 golden deterministic replay passed')
