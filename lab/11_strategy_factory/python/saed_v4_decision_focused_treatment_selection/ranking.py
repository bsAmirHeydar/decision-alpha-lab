from __future__ import annotations
from .objectives import objective_score

def rank_candidates(rows,policy,risk,baseline_id):
    ranked=[]
    for row in rows:
        x=dict(row);x['objective_score']=objective_score(x,policy.objective,risk);ranked.append(x)
    def key(x):
        baseline_bias=0 if policy.tie_policy=='baseline_first' and x['treatment_id']==baseline_id else 1
        return (-x['objective_score'],baseline_bias,x['treatment_id'])
    ranked.sort(key=key)
    for i,row in enumerate(ranked,1):row['rank']=i
    return ranked
