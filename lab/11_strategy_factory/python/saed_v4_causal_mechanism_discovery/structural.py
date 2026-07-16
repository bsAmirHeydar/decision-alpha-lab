from __future__ import annotations
from .canonical import content_hash
from .numerics import ridge_fit,predict,mean,std,correlation

def fit_equations(dataset,graph):
    rows=[];train=[r for r in dataset['rows'] if r['split']=='train']
    for target in graph['nodes']:
        parents=sorted(e['source'] for e in graph['edges'] if e['target']==target)
        if not parents:continue
        x=[[r['values'][p] for p in parents] for r in train];y=[r['values'][target] for r in train];beta=ridge_fit(x,y);res=[v-predict(beta,row) for v,row in zip(y,x)]
        rows.append({'target':target,'parents':parents,'intercept':beta[0],'coefficients':dict(zip(parents,beta[1:])),'residual_mean':mean(res),'residual_std':std(res),'fit_rows':len(y),'synthetic_reference':True})
    out={'phase':'SAED_V4_17','equation_count':len(rows),'rows':rows,'causal_interpretation_allowed':False};out['report_hash']=content_hash(out);return out

def residual_independence(dataset,equations):
    train=[r for r in dataset['rows'] if r['split']=='train'];rows=[]
    for eq in equations['rows']:
        x=[[r['values'][p] for p in eq['parents']] for r in train];y=[r['values'][eq['target']] for r in train];beta=[eq['intercept']]+[eq['coefficients'][p] for p in eq['parents']];res=[v-predict(beta,row) for v,row in zip(y,x)]
        for p in eq['parents']:rows.append({'target':eq['target'],'parent':p,'residual_parent_correlation':correlation(res,[r['values'][p] for r in train])})
    out={'phase':'SAED_V4_17','row_count':len(rows),'rows':rows,'maximum_absolute_residual_parent_correlation':max([abs(r['residual_parent_correlation']) for r in rows],default=0.0)};out['report_hash']=content_hash(out);return out
