from __future__ import annotations
from .predicates import evaluate_predicate
from .temporal import evaluate_clause
from .canonical import stable_id,content_hash
from .errors import BudgetError,ContradictionError

def evaluate_rule(rule,subject_id,predicates,store,temporal_results):
    vals=[evaluate_predicate(predicates,store,subject_id,p) for p in rule['conditions']]
    if any(v is None for v in vals):return {'matched':False,'reason':'missing_predicate'}
    if not all(vals):return {'matched':False,'reason':'predicate_false'}
    if not all(temporal_results.get(c,False) for c in rule['temporal_clauses']):return {'matched':False,'reason':'temporal_false'}
    return {'matched':True,'reason':'matched'}

def forward_chain(compiled_rules,predicates,store,subjects,events,decision_time,temporal_contract,temporal_clauses,budget):
    trace=[];decisions=[];inferences=0
    temporal_results={c['clause_id']:evaluate_clause(c,events,decision_time,temporal_contract) for c in temporal_clauses}
    for iteration in range(compiled_rules['grammar'].max_iterations):
        changed=False
        for subject in sorted(subjects):
            for rule in compiled_rules['rules']:
                if not rule['enabled']:continue
                ev=evaluate_rule(rule,subject,predicates,store,temporal_results)
                row={'iteration':iteration,'subject_id':subject,'rule_id':rule['rule_id'],'matched':ev['matched'],'reason':ev['reason'],'rule_hash':rule['rule_hash']}
                trace.append(row)
                if not ev['matched']:continue
                inferences+=1
                if inferences>budget.max_inferences:raise BudgetError('inference budget exhausted')
                if rule['effect']=='derive':
                    fact={'fact_id':stable_id('fact',{'s':subject,'r':rule['rule_id']}),'subject_id':subject,'concept_id':rule['conclusion_concept'],'value':rule['conclusion_value'],'polarity':1,'event_time':decision_time,'known_time':decision_time,'source_hash':rule['rule_hash'],'synthetic_only':True}
                    if store.add(fact,derived_by=rule['rule_id'],depth=iteration+1):changed=True
                else:
                    decisions.append({'subject_id':subject,'rule_id':rule['rule_id'],'effect':rule['effect'],'treatment_id':rule['treatment_id'],'confidence':rule['confidence'],'manual_doctrine':rule['manual_doctrine'],'priority':rule['priority']})
        if not changed:break
    return {'trace':trace,'decisions':decisions,'temporal_results':temporal_results,'inferences':inferences,'trace_hash':content_hash(trace)}
