from __future__ import annotations
from .canonical import content_hash
from .numerics import mean,std

def support_report(dataset,registry):
    envs=sorted({r['environment_id'] for r in dataset['rows']});variables=[v['variable_id'] for v in registry.variables if v['role'] not in {'environment','negative_control_exposure','negative_control_outcome'}];rows=[]
    for var in variables:
        stats=[]
        for env in envs:
            vals=[r['values'][var] for r in dataset['rows'] if r['environment_id']==env];stats.append({'environment_id':env,'rows':len(vals),'mean':mean(vals),'std':std(vals),'minimum':min(vals),'maximum':max(vals)})
        overlap=max(s['minimum'] for s in stats)<=min(s['maximum'] for s in stats)
        rows.append({'variable_id':var,'environment_statistics':stats,'range_overlap':overlap,'transport_supported':False})
    out={'phase':'SAED_V4_17','variable_count':len(rows),'rows':rows,'all_ranges_overlap':all(r['range_overlap'] for r in rows),'transport_claim_allowed':False,'reason':'synthetic environment overlap is diagnostic only'};out['report_hash']=content_hash(out);return out
