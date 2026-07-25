from __future__ import annotations
from .numerics import mean
from .canonical import content_hash

def allocation_scenario_utilities(allocation,scenario_set,complexity_penalty=0.0):
    ws=allocation['weights'];pen=float(complexity_penalty)*float(allocation['weighted_complexity'])+float(allocation['diversification_penalty'])
    vals={}
    for s in scenario_set['scenarios']:
        vals[s['scenario_id']]=sum(float(ws.get(t,0))*float(u) for t,u in s['utilities'].items())-pen
    return vals

def regret_matrix(allocation_rows,scenario_set,complexity_penalty=0.0):
    utils={a['allocation_id']:allocation_scenario_utilities(a,scenario_set,complexity_penalty) for a in allocation_rows}
    scenario_ids=[s['scenario_id'] for s in scenario_set['scenarios']]
    oracle={sid:max(utils[aid][sid] for aid in utils) for sid in scenario_ids}
    rows=[]
    for a in allocation_rows:
        aid=a['allocation_id'];rs={sid:oracle[sid]-utils[aid][sid] for sid in scenario_ids}
        rows.append({'allocation_id':aid,'scenario_regret':rs,'maximum_regret':max(rs.values()),'mean_regret':mean(list(rs.values())),'total_regret':sum(rs.values())})
    out={'scenario_ids':scenario_ids,'oracle_utility':oracle,'rows':rows}
    out['regret_matrix_hash']=content_hash(out);return out

def dynamic_regret(sequence,oracle_sequence):
    per=[float(o)-float(x) for x,o in zip(sequence,oracle_sequence)]
    return {'per_step_regret':per,'cumulative_regret':sum(per),'maximum_step_regret':max(per) if per else 0.0,'step_count':len(per)}
