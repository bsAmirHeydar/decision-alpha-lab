from __future__ import annotations
from .canonical import content_hash

def compare(neural_scores,symbolic_scores,maximum_disagreement=0.35):
    tids=sorted(set(neural_scores)|set(symbolic_scores));rows=[]
    for t in tids:
        n=float(neural_scores.get(t,0.0));s=float(symbolic_scores.get(t,0.0));rows.append({'treatment_id':t,'neural_score':n,'symbolic_score':s,'absolute_gap':abs(n-s)})
    max_gap=max([r['absolute_gap'] for r in rows] or [0.0]);directive='abstain' if max_gap>maximum_disagreement else 'continue_reference'
    return {'rows':rows,'maximum_gap':max_gap,'threshold':maximum_disagreement,'directive':directive,'report_hash':content_hash(rows)}
