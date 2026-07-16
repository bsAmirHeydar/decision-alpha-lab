from __future__ import annotations
from .contracts import OntologyContract,PredicateRegistry,TemporalLogicContract,RuleGrammar,ReasoningBudget,DecisionEnvelopeContract
from .errors import IntegrityError,ContractError

def validate_inputs(ontology,predicates,temporal,grammar,budget,envelope):
    return (OntologyContract.from_mapping(ontology),PredicateRegistry.from_mapping(predicates),TemporalLogicContract.from_mapping(temporal),RuleGrammar.from_mapping(grammar),ReasoningBudget.from_mapping(budget),DecisionEnvelopeContract.from_mapping(envelope))
def validate_upstream(handoff):
    if handoff.get('phase')!='SAED_V4_18' or handoff.get('next_phase')!='SAED_V4_19':raise IntegrityError('upstream phase mismatch')
    if not handoff.get('immutable') or not handoff.get('research_only'):raise IntegrityError('upstream immutability/research boundary absent')
    if not handoff.get('authority',{}).get('use_as_neurosymbolic_research_feature'):raise IntegrityError('upstream neurosymbolic use absent')
    forbidden=['select_live_treatment','sign_promotion','compile_runtime','activate_runtime','send_order']
    if any(handoff['authority'].get(k,True) for k in forbidden):raise IntegrityError('upstream authority contamination')
    if not all(handoff.get('entry_gates',{}).values()):raise IntegrityError('upstream entry gate open')
    return True
