from __future__ import annotations
from .numerics import entropy

def construct_selection_set(ranked,risk,pareto_ids):
    if not ranked:return []
    best=ranked[0]['objective_score'];selected=[]
    for row in ranked:
        if row['treatment_id'] in pareto_ids and best-row['objective_score']<=risk.minimum_margin and len(selected)<risk.maximum_set_size:selected.append(row['treatment_id'])
    if not selected:selected=[ranked[0]['treatment_id']]
    return selected

def selection_uncertainty(ranked):
    ps=[r['selection_probability'] for r in ranked]
    return {'entropy':entropy(ps),'top_probability':max(ps) if ps else 0.0,'margin_probability':(ps[0]-ps[1] if len(ps)>1 else (ps[0] if ps else 0.0))}
