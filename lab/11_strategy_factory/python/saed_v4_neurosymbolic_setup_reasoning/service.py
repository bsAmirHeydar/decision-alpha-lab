from __future__ import annotations
from .ontology import compile_ontology
from .predicates import compile_predicates
from .temporal import compile_temporal
from .rules import compile_rule_library
from .facts import FactStore
from .contracts import ReasoningBudget
from .reasoner import forward_chain
from .differentiable import evaluate_soft_rules
from .projection import project
from .contradictions import audit_facts,audit_decisions
from .proofs import build as build_proof
from .canonical import content_hash

def run_reference(contracts,facts,events,temporal_clauses,rules,soft_inputs,decision_time,upstream_hash):
    ontology=compile_ontology(contracts['ontology']);preds=compile_predicates(contracts['predicates'],ontology);tc=compile_temporal(contracts['temporal']);budget=ReasoningBudget.from_mapping(contracts['budget'])
    library=compile_rule_library(contracts['grammar'],rules,preds['predicates'].keys(),[x['clause_id'] for x in temporal_clauses])
    store=FactStore(ontology,decision_time,budget.max_facts)
    for f in facts:store.add(f)
    fact_audit=audit_facts(facts)
    subjects=sorted({f['subject_id'] for f in facts})
    result=forward_chain(library,preds,store,subjects,events,decision_time,tc,temporal_clauses,budget)
    decision_audit=audit_decisions(result['decisions'])
    soft=evaluate_soft_rules(library['rules'],soft_inputs)
    hard_blocks=[d['rule_id'] for d in result['decisions'] if d['effect'] in {'block','require'}]
    projection=project(result['decisions'],soft,contracts['envelope'],hard_blocks,fact_audit['count']>0 or decision_audit['count']>0)
    proof=build_proof(subjects[0],decision_time,projection,result['trace'],store.facts(),upstream_hash,content_hash(contracts['ontology']),library['library_hash'])
    return {'compiled_ontology':ontology,'compiled_predicates':preds,'rule_library_hash':library['library_hash'],'reasoning':result,'soft_logic':soft,'projection':projection,'proof':proof,'fact_audit':fact_audit,'decision_audit':decision_audit,'facts':store.facts()}
