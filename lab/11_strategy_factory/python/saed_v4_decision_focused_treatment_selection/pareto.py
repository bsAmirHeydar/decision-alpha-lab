from __future__ import annotations

def _dominates(a,b,metrics):
    ge=all(a[m]>=b[m] for m in metrics);gt=any(a[m]>b[m] for m in metrics)
    return ge and gt

def pareto_frontier(rows,metrics=('robust_utility','lower_confidence_utility','negative_maximum_regret','negative_complexity')):
    ordered=sorted(rows,key=lambda r:r['treatment_id']);front=[]
    for row in ordered:
        if not any(_dominates(other,row,metrics) for other in ordered if other['treatment_id']!=row['treatment_id']):front.append(row['treatment_id'])
    return tuple(sorted(front))
