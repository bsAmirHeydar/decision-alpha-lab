from __future__ import annotations
from .canonical import content_hash
from .numerics import ridge_fit,predict,mean,std,l1

def audit(dataset,graph,environment_registry,config):
    rows=[];all_rows=dataset['rows']
    for target in graph['nodes']:
        parents=sorted(e['source'] for e in graph['edges'] if e['target']==target)
        if not parents:continue
        env_stats=[]
        for env in [e['environment_id'] for e in environment_registry.environments]:
            subset=[r for r in all_rows if r['environment_id']==env and r['split']!='selection_validation']
            x=[[r['values'][p] for p in parents] for r in subset];y=[r['values'][target] for r in subset];beta=ridge_fit(x,y);res=[v-predict(beta,row) for v,row in zip(y,x)]
            env_stats.append({'environment_id':env,'rows':len(subset),'coefficients':beta,'residual_mean':mean(res),'residual_std':std(res)})
        means=[x['residual_mean'] for x in env_stats];scales=[x['residual_std'] for x in env_stats];coef_ref=env_stats[0]['coefficients'];coef_drift=max([l1(coef_ref,x['coefficients']) for x in env_stats],default=0.0)
        mean_gap=max(means)-min(means);scale_gap=max(scales)-min(scales)
        rows.append({'target':target,'parents':parents,'environment_statistics':env_stats,'maximum_residual_mean_gap':mean_gap,'maximum_residual_scale_gap':scale_gap,'maximum_coefficient_l1_drift':coef_drift,'invariant':mean_gap<=config.invariance_mean_tolerance and scale_gap<=config.invariance_scale_tolerance})
    out={'phase':'SAED_V4_17','mechanism_count':len(rows),'invariant_count':sum(r['invariant'] for r in rows),'rows':rows};out['report_hash']=content_hash(out);return out
