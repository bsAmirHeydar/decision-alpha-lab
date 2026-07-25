from __future__ import annotations
from itertools import combinations
from .numerics import mean
from .canonical import stable_id,content_hash

def fit_reference(rows,feature_ids,target_field,max_terms=3):
    y=[float(r[target_field]) for r in rows];my=mean(y);terms=[]
    for k in range(1,min(max_terms,len(feature_ids))+1):
        for combo in combinations(sorted(feature_ids),k):
            x=[sum(float(r['features'].get(f,0.0)) for f in combo) for r in rows];mx=mean(x)
            den=sum((v-mx)**2 for v in x);beta=sum((a-mx)*(b-my) for a,b in zip(x,y))/den if den>1e-12 else 0.0;alpha=my-beta*mx
            p=[alpha+beta*v for v in x];mse=mean([(a-b)**2 for a,b in zip(y,p)]);score=mse+0.001*k
            terms.append({'model_id':stable_id('symreg',combo),'features':list(combo),'intercept':alpha,'coefficient':beta,'mse':mse,'complexity':k,'mdl_cost':score})
    terms.sort(key=lambda x:(x['mdl_cost'],x['complexity'],x['model_id']))
    return {'models':terms,'champion':terms[0] if terms else None,'model_count':len(terms),'registry_hash':content_hash(terms)}
