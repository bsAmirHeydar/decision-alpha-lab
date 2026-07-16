from __future__ import annotations
from .numerics import ridge_fit,predict,rmse,mean
from .canonical import content_hash

def fit_t_learner(train_rows,treatment_ids,ridge=0.01,outcome_field='observed_outcome'):
    models={}
    for t in treatment_ids:
        rows=[r for r in train_rows if r['assigned_treatment']==t and r['outcome_observed']]
        models[t]=ridge_fit([r['features'] for r in rows],[r[outcome_field] for r in rows],ridge)
    return models

def fit_s_learner(train_rows,treatment_ids,ridge=0.01,outcome_field='observed_outcome'):
    x=[];y=[]
    for r in train_rows:
        one=[1.0 if r['assigned_treatment']==t else 0.0 for t in treatment_ids[1:]];x.append(r['features']+one);y.append(r[outcome_field])
    return ridge_fit(x,y,ridge)

def predict_s_learner(model,features,treatment_ids,treatment):
    one=[1.0 if treatment==t else 0.0 for t in treatment_ids[1:]];return predict(model,features+one)

def nuisance_diagnostics(predictions):
    predictions=predictions['predictions'] if isinstance(predictions,dict) else predictions
    observed=[x['observed_outcome'] for x in predictions];fitted=[x['mu_hat'][x['assigned_treatment']] for x in predictions]
    per_fold=[]
    for fid in sorted(set(x['fold_id'] for x in predictions)):
        rows=[x for x in predictions if x['fold_id']==fid];per_fold.append({'fold_id':fid,'row_count':len(rows),'rmse':rmse([r['observed_outcome'] for r in rows],[r['mu_hat'][r['assigned_treatment']] for r in rows]),'mean_residual':mean([r['observed_outcome']-r['mu_hat'][r['assigned_treatment']] for r in rows])})
    out={'phase':'SAED_V4_18','row_count':len(predictions),'overall_rmse':rmse(observed,fitted),'folds':per_fold,'passed':all(x['rmse']<0.6 for x in per_fold)};out['report_hash']=content_hash(out);return out
