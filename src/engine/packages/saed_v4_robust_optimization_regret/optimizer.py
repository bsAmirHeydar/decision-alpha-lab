from __future__ import annotations
from .contracts import RobustOptimizationContract,RegretContract
from .objectives import evaluate_allocation,objective_key
from .regret import regret_matrix
from .baselines import baseline_gate
from .canonical import content_hash
from .errors import OptimizationError

def solve(allocation_universe,scenario_set,ambiguity_set,opt_mapping,regret_mapping,baseline_mapping,ledger=None):
    oc=RobustOptimizationContract.from_mapping(opt_mapping);rc=RegretContract.from_mapping(regret_mapping)
    allocations=allocation_universe['allocations']
    rm=regret_matrix(allocations,scenario_set,oc.complexity_penalty);rmap={r['allocation_id']:r for r in rm['rows']}
    rows=[evaluate_allocation(a,scenario_set,ambiguity_set,rmap[a['allocation_id']],oc.complexity_penalty,ledger) for a in allocations]
    bg=baseline_gate(rows,baseline_mapping);bmap={r['allocation_id']:r for r in bg['rows']}
    enriched=[]
    for r in rows:
        failures=[]
        if r['maximum_regret']>rc.maximum_regret_limit:failures.append('maximum_regret_limit')
        if r['mean_regret']>rc.mean_regret_limit:failures.append('mean_regret_limit')
        failures+=bmap[r['allocation_id']]['baseline_failures']
        x=dict(r);x['baseline_gate']=bmap[r['allocation_id']];x['constraint_failures']=failures;x['feasible']=not failures;enriched.append(x)
    feasible=[r for r in enriched if r['feasible']]
    ranked=sorted(feasible,key=lambda r:objective_key(r,oc.objective))
    fallback='allocation::'+baseline_mapping['skip_treatment']+':1.000000'
    abstain=False;reasons=[]
    if not ranked:abstain=True;reasons=['no_robust_feasible_allocation']
    else:
        best=ranked[0]
        if len(ranked)>1:
            margin=ranked[1]['worst_case_utility']-best['worst_case_utility'] if oc.objective=='minimax_regret' else best['worst_case_utility']-ranked[1]['worst_case_utility']
            margin=abs(margin)
        else:margin=float('inf')
        if margin<rc.robust_margin:abstain=True;reasons.append('insufficient_robust_margin')
        if best['maximum_regret']>rc.maximum_regret_limit:abstain=True;reasons.append('maximum_regret_violation')
    selected=fallback if abstain else ranked[0]['allocation_id']
    decision={'decision':'abstain' if abstain else 'research_recommendation','selected_allocation_id':selected,'fallback_allocation_id':fallback,'abstain':abstain,'reasons':reasons,'runtime_executable':False,'decision_authority':False,'risk_allocation_authority':False}
    out={'objective':oc.objective,'rows':sorted(enriched,key=lambda r:objective_key(r,oc.objective)),'regret_matrix':rm,'baseline_report':bg,'decision':decision,'feasible_count':len(feasible),'allocation_count':len(enriched)}
    out['optimization_report_hash']=content_hash(out);return out
