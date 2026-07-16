from __future__ import annotations
from .numerics import fuzzy_and,fuzzy_or,fuzzy_not,clamp
from .canonical import content_hash

def soft_predicate(value,threshold,direction='ge',temperature=8.0):
    import math
    z=(float(value)-float(threshold))*float(temperature)
    if direction in {'lt','le'}:z=-z
    z=max(-40,min(40,z));return 1/(1+math.exp(-z))
def score_rule(predicate_scores,temporal_scores,confidence=1.0,t_norm='product'):
    all_scores=list(predicate_scores)+list(temporal_scores);return clamp(fuzzy_and(all_scores,t_norm)*float(confidence))
def evaluate_soft_rules(rules,soft_inputs):
    rows=[]
    for r in rules:
        ps=[soft_inputs.get(p,0.0) for p in r['conditions']];ts=[soft_inputs.get(c,0.0) for c in r['temporal_clauses']]
        score=score_rule(ps,ts,r['confidence'])
        rows.append({'rule_id':r['rule_id'],'score':score,'treatment_id':r['treatment_id'],'effect':r['effect']})
    return {'scores':rows,'score_hash':content_hash(rows)}
