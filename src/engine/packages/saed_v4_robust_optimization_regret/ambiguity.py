from __future__ import annotations
from .contracts import AmbiguitySetContract
from .errors import AmbiguityError
from .numerics import normalize,l1
from .canonical import content_hash

def compile_ambiguity_distributions(scenario_set,mapping,ledger=None):
    c=AmbiguitySetContract.from_mapping(mapping);n=len(scenario_set['scenarios'])
    if n<1:raise AmbiguityError('empty scenario set')
    nominal=[float(s['nominal_probability']) for s in scenario_set['scenarios']]
    ds=[{'distribution_id':'nominal','family':'nominal','probabilities':nominal,'distance':0.0}]
    radius=min(1.0,float(c.radius))
    for i in range(n):
        q=list(nominal);move=min(radius/2.0,sum(q[j]-c.probability_floor for j in range(n) if j!=i))
        if move<=0:continue
        q[i]+=move
        donors=[j for j in range(n) if j!=i and q[j]>c.probability_floor]
        remain=move
        for j in donors:
            d=min(remain,q[j]-c.probability_floor);q[j]-=d;remain-=d
            if remain<=1e-15:break
        q=normalize(q,c.probability_floor)
        dist=l1(q,nominal)
        if dist<=2*radius+1e-12:ds.append({'distribution_id':f'vertex::{i:03d}','family':c.family,'probabilities':q,'distance':dist})
    # deterministic adverse aggregate emphasizes lower nominal cross-treatment mean
    means=[]
    for s in scenario_set['scenarios']:
        means.append(sum(float(x) for x in s['utilities'].values())/len(s['utilities']))
    worst=sorted(range(n),key=lambda i:(means[i],scenario_set['scenarios'][i]['scenario_id']))[:max(1,n//3)]
    q=list(nominal);boost=radius/max(1,len(worst))
    for i in worst:q[i]+=boost
    q=normalize(q,c.probability_floor)
    ds.append({'distribution_id':'adverse_aggregate','family':'hybrid_adverse','probabilities':q,'distance':l1(q,nominal)})
    unique=[];seen=set()
    for d in ds:
        key=tuple(round(x,15) for x in d['probabilities'])
        if key not in seen:seen.add(key);unique.append(d)
    if ledger:ledger.consume('ambiguity_distributions',len(unique))
    out={'family':c.family,'radius':c.radius,'closed_support':c.closed_support,'nominal_probabilities':nominal,'distributions':unique,'distribution_count':len(unique),'synthetic_only':True}
    out['ambiguity_set_hash']=content_hash(out);return out
