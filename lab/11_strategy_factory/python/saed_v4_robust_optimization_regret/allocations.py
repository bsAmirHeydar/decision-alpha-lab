from __future__ import annotations
from itertools import combinations
from .contracts import RobustOptimizationContract
from .canonical import content_hash
from .errors import OptimizationError

def enumerate_allocations(treatments,mapping,complexities,ledger=None):
    c=RobustOptimizationContract.from_mapping(mapping);tids=sorted(set(map(str,treatments)))
    if not tids:raise OptimizationError('empty treatment set')
    rows=[]
    def add(weights):
        active=sorted(k for k,v in weights.items() if v>1e-12)
        if len(active)>c.max_active_treatments:return
        weights={k:float(weights.get(k,0.0)) for k in tids}
        if abs(sum(weights.values())-1.0)>1e-9:return
        mix_complexity=sum(weights[k]*float(complexities.get(k,0)) for k in tids)
        div=max(0,len(active)-1)*c.diversification_penalty
        rid='allocation::'+'+'.join(f'{k}:{weights[k]:.6f}' for k in active)
        rows.append({'allocation_id':rid,'weights':weights,'active_treatments':active,'active_count':len(active),'weighted_complexity':mix_complexity,'diversification_penalty':div})
    for t in tids:add({t:1.0})
    if c.mixture_allowed and c.max_active_treatments>=2:
        steps=int(round(1.0/c.grid_step))
        for a,b in combinations(tids,2):
            for k in range(1,steps):
                p=k*c.grid_step
                if 0<p<1:add({a:p,b:1-p})
    rows=sorted({r['allocation_id']:r for r in rows}.values(),key=lambda r:r['allocation_id'])
    if ledger:ledger.consume('allocations',len(rows))
    out={'treatments':tids,'grid_step':c.grid_step,'max_active_treatments':c.max_active_treatments,'allocations':rows,'allocation_count':len(rows),'deterministic':True}
    out['allocation_universe_hash']=content_hash(out);return out
