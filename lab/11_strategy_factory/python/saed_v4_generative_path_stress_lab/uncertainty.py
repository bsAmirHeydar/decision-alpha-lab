from __future__ import annotations
from .numerics import mean,std
from .canonical import content_hash

def horizon_map(paths,minimum_trusted_horizon,threshold=0.025):
    grouped={}
    for p in paths:
        fam=p['generator_id'].split('::member::')[0];grouped.setdefault(fam,[]).append(p)
    rows=[];max_h=min(len(p['rows']) for p in paths) if paths else 0
    for h in range(max_h):
        rets=[]
        for p in paths:
            if h==0:rets.append(p['rows'][0]['close']/p['rows'][0]['open']-1)
            else:rets.append(p['rows'][h]['close']/p['rows'][h-1]['close']-1)
        rows.append({'horizon_step':h+1,'ensemble_return_mean':mean(rets),'ensemble_return_std':std(rets),'uncertainty_exceeds_threshold':std(rets)>threshold})
    trusted=0
    for r in rows:
        if r['uncertainty_exceeds_threshold']:break
        trusted=r['horizon_step']
    trusted=max(minimum_trusted_horizon if max_h>=minimum_trusted_horizon else max_h,trusted)
    out={'path_count':len(paths),'rows':rows,'trusted_horizon':trusted,'threshold':threshold,'research_only':True};out['uncertainty_map_hash']=content_hash(out);return out
