from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
from .errors import ContractError

VALUE_TYPES={'boolean','number','string','timestamp','category'}
PREDICATE_OPS={'eq','neq','gt','ge','lt','le','between','in','exists','not_missing'}
TEMPORAL_OPS={'always','eventually_within','precedes','holds_for','until','count_within'}
RULE_EFFECTS={'derive','block','require','recommend','abstain','quarantine'}
FALLBACKS={'skip','manual','abstain','reject','quarantine'}

def exact(x:Mapping[str,Any],required:set[str],label:str):
    if set(x)!=required: raise ContractError(f'{label} fields mismatch: {sorted(set(x)^required)}')

@dataclass(frozen=True)
class OntologyContract:
    exact_version:str; concepts:tuple[dict,...]; relations:tuple[dict,...]; closed_world:bool; finite:bool; mutable_at_runtime:bool; synthetic_only:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','concepts','relations','closed_world','finite','mutable_at_runtime','synthetic_only'},'ontology')
        cs=tuple(dict(v) for v in x['concepts']); rs=tuple(dict(v) for v in x['relations']); ids=[]
        for c in cs:
            exact(c,{'concept_id','value_type','description','required','known_time_required','allowed_values'},'concept')
            if c['value_type'] not in VALUE_TYPES or not c['concept_id']:raise ContractError('invalid concept')
            ids.append(c['concept_id'])
        for r in rs:
            exact(r,{'relation_id','source_concept','target_concept','cardinality','temporal'},'relation')
            if r['source_concept'] not in ids or r['target_concept'] not in ids:raise ContractError('relation endpoint outside ontology')
        o=cls(str(x['exact_version']),cs,rs,bool(x['closed_world']),bool(x['finite']),bool(x['mutable_at_runtime']),bool(x['synthetic_only']))
        if len(ids)!=len(set(ids)) or not(o.closed_world and o.finite and o.synthetic_only) or o.mutable_at_runtime:raise ContractError('ontology safeguards absent')
        return o

@dataclass(frozen=True)
class PredicateRegistry:
    exact_version:str; predicates:tuple[dict,...]; unknown_predicate_policy:str; missing_value_policy:str; future_fact_policy:str
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','predicates','unknown_predicate_policy','missing_value_policy','future_fact_policy'},'predicate registry')
        ps=tuple(dict(v) for v in x['predicates']); ids=[]
        for p in ps:
            exact(p,{'predicate_id','concept_id','operator','threshold','values','negated','enabled'},'predicate')
            if p['operator'] not in PREDICATE_OPS:raise ContractError('invalid predicate operator')
            ids.append(p['predicate_id'])
        o=cls(str(x['exact_version']),ps,str(x['unknown_predicate_policy']),str(x['missing_value_policy']),str(x['future_fact_policy']))
        if len(ids)!=len(set(ids)) or o.unknown_predicate_policy!='reject' or o.missing_value_policy!='abstain' or o.future_fact_policy!='reject':raise ContractError('predicate fail-closed policy absent')
        return o

@dataclass(frozen=True)
class TemporalLogicContract:
    exact_version:str; operators:tuple[str,...]; event_time_field:str; known_time_field:str; max_window:int; max_history:int; future_suffix_forbidden:bool; deterministic_ties:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','operators','event_time_field','known_time_field','max_window','max_history','future_suffix_forbidden','deterministic_ties'},'temporal contract')
        o=cls(str(x['exact_version']),tuple(map(str,x['operators'])),str(x['event_time_field']),str(x['known_time_field']),int(x['max_window']),int(x['max_history']),bool(x['future_suffix_forbidden']),bool(x['deterministic_ties']))
        if not set(o.operators)<=TEMPORAL_OPS or o.max_window<1 or o.max_history<o.max_window or not(o.future_suffix_forbidden and o.deterministic_ties):raise ContractError('invalid temporal contract')
        return o

@dataclass(frozen=True)
class RuleGrammar:
    exact_version:str; allowed_effects:tuple[str,...]; max_rules:int; max_conditions_per_rule:int; max_temporal_clauses:int; max_derivation_depth:int; max_iterations:int; recursion_allowed:bool; dynamic_code_allowed:bool; manual_precedence:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','allowed_effects','max_rules','max_conditions_per_rule','max_temporal_clauses','max_derivation_depth','max_iterations','recursion_allowed','dynamic_code_allowed','manual_precedence'},'rule grammar')
        o=cls(str(x['exact_version']),tuple(map(str,x['allowed_effects'])),int(x['max_rules']),int(x['max_conditions_per_rule']),int(x['max_temporal_clauses']),int(x['max_derivation_depth']),int(x['max_iterations']),bool(x['recursion_allowed']),bool(x['dynamic_code_allowed']),bool(x['manual_precedence']))
        if not set(o.allowed_effects)<=RULE_EFFECTS or min(o.max_rules,o.max_conditions_per_rule,o.max_derivation_depth,o.max_iterations)<1 or o.recursion_allowed or o.dynamic_code_allowed or not o.manual_precedence:raise ContractError('unsafe grammar')
        return o

@dataclass(frozen=True)
class ReasoningBudget:
    max_facts:int; max_rules:int; max_inferences:int; max_counterexamples:int; max_synthesis_candidates:int; max_symbolic_terms:int; max_neural_queries:int; max_hidden_evaluation_queries:int; protected_evidence_exposure_limit:int; max_failures:int
    @classmethod
    def from_mapping(cls,x):
        keys={'max_facts','max_rules','max_inferences','max_counterexamples','max_synthesis_candidates','max_symbolic_terms','max_neural_queries','max_hidden_evaluation_queries','protected_evidence_exposure_limit','max_failures'};exact(x,keys,'reasoning budget')
        vals=[int(x[k]) for k in keys];o=cls(**{k:int(x[k]) for k in keys})
        if min(o.max_facts,o.max_rules,o.max_inferences,o.max_counterexamples,o.max_synthesis_candidates,o.max_symbolic_terms)<1 or o.max_hidden_evaluation_queries!=0 or o.protected_evidence_exposure_limit!=0 or o.max_failures<0:raise ContractError('unsafe exposure budget')
        return o

@dataclass(frozen=True)
class DecisionEnvelopeContract:
    exact_version:str; approved_treatments:tuple[str,...]; canonical_baseline:str; manual_fallback:str; default_fallback:str; minimum_symbolic_confidence:float; maximum_disagreement:float; proof_required:bool; runtime_executable:bool
    @classmethod
    def from_mapping(cls,x):
        exact(x,{'exact_version','approved_treatments','canonical_baseline','manual_fallback','default_fallback','minimum_symbolic_confidence','maximum_disagreement','proof_required','runtime_executable'},'decision envelope')
        o=cls(str(x['exact_version']),tuple(map(str,x['approved_treatments'])),str(x['canonical_baseline']),str(x['manual_fallback']),str(x['default_fallback']),float(x['minimum_symbolic_confidence']),float(x['maximum_disagreement']),bool(x['proof_required']),bool(x['runtime_executable']))
        if o.canonical_baseline not in o.approved_treatments or o.manual_fallback not in o.approved_treatments or o.default_fallback not in FALLBACKS or not 0<=o.minimum_symbolic_confidence<=1 or not 0<=o.maximum_disagreement<=1 or not o.proof_required or o.runtime_executable:raise ContractError('unsafe decision envelope')
        return o
