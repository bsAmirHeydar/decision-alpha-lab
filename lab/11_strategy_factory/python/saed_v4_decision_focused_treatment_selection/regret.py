from __future__ import annotations
from .numerics import mean

def scenario_regret_matrix(candidate_rows):
    tids=[r['treatment_id'] for r in candidate_rows]
    scenarios=sorted(set().union(*(r['scenario_utilities'].keys() for r in candidate_rows)))
    matrix=[]
    for sid in scenarios:
        vals={r['treatment_id']:float(r['scenario_utilities'].get(sid,float('-inf'))) for r in candidate_rows}
        best=max(vals.values())
        matrix.append({'scenario_id':sid,'best_utility':best,'regret_by_treatment':{k:(best-v if v!=float('-inf') else 1e9) for k,v in sorted(vals.items())}})
    summary=[]
    for tid in tids:
        rs=[row['regret_by_treatment'][tid] for row in matrix]
        summary.append({'treatment_id':tid,'mean_regret':mean(rs),'maximum_regret':max(rs) if rs else 0.0})
    return {'scenarios':matrix,'summary':summary}
