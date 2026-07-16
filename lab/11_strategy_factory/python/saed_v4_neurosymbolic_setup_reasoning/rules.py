from __future__ import annotations
from .contracts import RuleGrammar
from .errors import RuleError
from .canonical import content_hash

def compile_rule_library(grammar_mapping,rules,predicate_ids,temporal_clause_ids):
    g=RuleGrammar.from_mapping(grammar_mapping)
    if len(rules)>g.max_rules:raise RuleError('rule budget exceeded')
    out=[];ids=set()
    for r in rules:
        keys={'rule_id','priority','conditions','temporal_clauses','effect','conclusion_concept','conclusion_value','treatment_id','confidence','manual_doctrine','enabled'}
        if set(r)!=keys:raise RuleError('rule fields mismatch')
        if r['rule_id'] in ids:raise RuleError('duplicate rule id')
        if r['effect'] not in g.allowed_effects or len(r['conditions'])>g.max_conditions_per_rule or len(r['temporal_clauses'])>g.max_temporal_clauses:raise RuleError('rule outside grammar')
        if not set(r['conditions'])<=set(predicate_ids) or not set(r['temporal_clauses'])<=set(temporal_clause_ids):raise RuleError('rule references unknown predicate or temporal clause')
        if not 0<=float(r['confidence'])<=1:raise RuleError('invalid rule confidence')
        row=dict(r);row['rule_hash']=content_hash(r);out.append(row);ids.add(r['rule_id'])
    out.sort(key=lambda x:(not x['manual_doctrine'],-int(x['priority']),x['rule_id']))
    return {'grammar':g,'rules':out,'library_hash':content_hash(out)}
