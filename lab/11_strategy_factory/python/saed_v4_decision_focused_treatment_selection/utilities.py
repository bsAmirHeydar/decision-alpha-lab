from __future__ import annotations
from .numerics import clamp,mean,cvar_lower,max_drawdown
from .errors import UtilityError

def path_statistics(path,tail_threshold=-0.75):
    xs=list(map(float,path))
    if not xs:raise UtilityError('empty path')
    return {'mean_reward':mean(xs),'tail_cvar':cvar_lower(xs,0.2),'tail_loss_probability':sum(x<=tail_threshold for x in xs)/len(xs),'max_drawdown':max_drawdown(xs),'path_count':len(xs)}

def compute_utility(outcome,treatment,contract):
    stats=path_statistics(outcome['path_returns'],outcome.get('tail_threshold',-0.75))
    raw=(contract.reward_weight*float(outcome['expected_reward'])
         -contract.cost_weight*float(outcome['expected_cost'])
         +contract.tail_loss_weight*float(stats['tail_cvar'])
         -contract.drawdown_weight*float(stats['max_drawdown'])
         -contract.complexity_weight*float(treatment['complexity'])
         -contract.turnover_weight*float(outcome['turnover']))
    value=min(contract.utility_ceiling,max(contract.utility_floor,raw))
    return {'expected_utility':value,'raw_utility':raw,**stats}
