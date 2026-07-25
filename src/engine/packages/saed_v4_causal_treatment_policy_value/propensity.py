from __future__ import annotations
from .numerics import ridge_fit,predict,softmax,clamp,mean,effective_sample_size
from .canonical import content_hash

def fit_multitreatment_propensity(train_rows,treatment_ids,ridge=0.01):
    x=[r['features'] for r in train_rows];models={}
    for t in treatment_ids:models[t]=ridge_fit(x,[1.0 if r['assigned_treatment']==t else 0.0 for r in train_rows],ridge)
    return models

def predict_propensity(models,features,treatment_ids,clip=0.03):
    raw=softmax([predict(models[t],features) for t in treatment_ids]);p=[max(clip,min(1-clip,v)) for v in raw];s=sum(p);return {t:p[i]/s for i,t in enumerate(treatment_ids)}

def propensity_diagnostics(predictions,treatment_ids,overlap_floor):
    rows=[]
    for t in treatment_ids:
        ps=[x['propensities'][t] for x in predictions];w=[1.0/max(1e-12,x['propensities'][t]) for x in predictions if x['assigned_treatment']==t]
        rows.append({'treatment_id':t,'minimum_propensity':min(ps),'mean_propensity':mean(ps),'maximum_propensity':max(ps),'below_overlap_floor':sum(v<overlap_floor for v in ps),'observed_count':sum(x['assigned_treatment']==t for x in predictions),'effective_sample_size':effective_sample_size(w)})
    out={'phase':'SAED_V4_18','row_count':len(predictions),'treatments':rows,'global_minimum_propensity':min(x['minimum_propensity'] for x in rows),'overlap_floor':overlap_floor,'passed':all(x['observed_count']>10 and x['effective_sample_size']>10 for x in rows)};out['report_hash']=content_hash(out);return out
