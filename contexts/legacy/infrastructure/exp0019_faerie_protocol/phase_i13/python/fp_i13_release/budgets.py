from .contracts import *
from .canonical import sha256,stable_id

DEFAULT_LIMITS=(
 BudgetLimit('full_replay_ms',1500.0,5000.0,'ms'),
 BudgetLimit('incremental_max_chunk_ms',25.0,100.0,'ms'),
 BudgetLimit('peak_memory_bytes',32_000_000.0,128_000_000.0,'bytes'),
 BudgetLimit('object_count',2500.0,5000.0,'objects'),
 BudgetLimit('object_ops_per_frame',200.0,1000.0,'ops'),
 BudgetLimit('checkpoint_bytes',5_000_000.0,20_000_000.0,'bytes'),
 BudgetLimit('minimum_events_per_second',10_000.0,1_000.0,'events_per_second'),
)
def default_budget(profile_id=ReleaseProfileId.TRADING_30D): return PerformanceBudget(stable_id('FPBUDGET',{'profile':profile_id.value,'limits':DEFAULT_LIMITS}),DEFAULT_LIMITS,profile_id)
def evaluate_budget(budget:PerformanceBudget,values:dict[str,float])->PerformanceReport:
    obs=[];overall=BudgetStatus.PASS
    for limit in budget.limits:
        value=float(values.get(limit.metric,0.0));inverse=limit.metric.startswith('minimum_')
        if inverse:
            if value<limit.hard_limit: status=BudgetStatus.BLOCKED
            elif value<limit.soft_limit: status=BudgetStatus.DEGRADED
            else: status=BudgetStatus.PASS
        else:
            if value>limit.hard_limit: status=BudgetStatus.BLOCKED
            elif value>limit.soft_limit: status=BudgetStatus.DEGRADED
            else: status=BudgetStatus.PASS
        if status==BudgetStatus.BLOCKED: overall=BudgetStatus.BLOCKED
        elif status==BudgetStatus.DEGRADED and overall==BudgetStatus.PASS: overall=BudgetStatus.DEGRADED
        obs.append(BudgetObservation(limit.metric,value,limit.unit,status,limit.soft_limit,limit.hard_limit,'FP_REL_BUDGET_'+status.value))
    body={'budget':budget.budget_id,'observations':tuple((o.metric,o.value,o.status.value) for o in obs),'status':overall.value}
    return PerformanceReport(stable_id('FPPERF',body),budget.budget_id,tuple(obs),overall,sha256(body))
