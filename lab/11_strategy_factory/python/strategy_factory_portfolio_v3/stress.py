from __future__ import annotations
from .contracts import StressResult

def run_stress(plan,scenarios,limits):
    results=[]
    selected=list(plan.selected)
    for s in scenarios:
        kept=[x for x in selected if x.context_id!=s.drop_context_id]
        risk=sum(x.allocated_risk for x in kept)*(1+s.correlation_multiplier*0.25)
        drawdown=sum(x.marginal_risk for x in kept)*(1+s.spread_multiplier*0.1)
        concentration=max((sum(x.allocated_risk for x in kept if x.context_id==cid) for cid in set(x.context_id for x in kept)),default=0.0)/max(risk,1e-12)
        safe=bool(kept) and risk<=limits.total_risk and drawdown<=limits.max_drawdown_budget and concentration<=1.0
        reasons=[]
        if not kept:reasons.append('all_contexts_removed')
        if risk>limits.total_risk:reasons.append('risk_limit_breach')
        if drawdown>limits.max_drawdown_budget:reasons.append('drawdown_budget_breach')
        results.append(StressResult(s.scenario_id,safe,len(set(x.context_id for x in kept)),risk,drawdown,concentration,tuple(reasons)))
    return tuple(results)
