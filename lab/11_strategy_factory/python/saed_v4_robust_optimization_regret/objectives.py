from __future__ import annotations
from .numerics import weighted_mean,cvar_lower,mean,std
from .regret import allocation_scenario_utilities

def evaluate_allocation(allocation,scenario_set,ambiguity_set,regret_row,complexity_penalty,ledger=None):
    vals=allocation_scenario_utilities(allocation,scenario_set,complexity_penalty)
    ordered=[vals[s['scenario_id']] for s in scenario_set['scenarios']]
    robust=[]
    for d in ambiguity_set['distributions']:
        robust.append(weighted_mean(ordered,d['probabilities']))
        if ledger:ledger.consume('objective_evaluations',1)
    nominal=weighted_mean(ordered,ambiguity_set['nominal_probabilities'])
    worst=min(ordered);best=max(ordered);rcvar=cvar_lower(ordered,0.2)
    return {'allocation_id':allocation['allocation_id'],'nominal_utility':nominal,'worst_case_utility':worst,'best_case_utility':best,'distributionally_robust_utility':min(robust),'robust_cvar':rcvar,'utility_mean':mean(ordered),'utility_std':std(ordered),'maximum_regret':float(regret_row['maximum_regret']),'mean_regret':float(regret_row['mean_regret']),'active_count':allocation['active_count'],'weighted_complexity':allocation['weighted_complexity'],'scenario_utilities':vals}

def objective_key(row,objective):
    if objective=='maximin_utility':return (-row['worst_case_utility'],row['maximum_regret'],-row['robust_cvar'],row['weighted_complexity'],row['allocation_id'])
    if objective=='minimax_regret':return (row['maximum_regret'],row['mean_regret'],-row['worst_case_utility'],row['weighted_complexity'],row['allocation_id'])
    if objective=='distributionally_robust':return (-row['distributionally_robust_utility'],row['maximum_regret'],-row['worst_case_utility'],row['weighted_complexity'],row['allocation_id'])
    if objective=='robust_cvar':return (-row['robust_cvar'],row['maximum_regret'],-row['worst_case_utility'],row['weighted_complexity'],row['allocation_id'])
    return (row['maximum_regret'],-row['worst_case_utility'],-row['distributionally_robust_utility'],-row['robust_cvar'],row['weighted_complexity'],row['allocation_id'])
