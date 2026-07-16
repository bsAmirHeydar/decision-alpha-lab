from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import quantile,monotone,mean,clamp

def _training_outcomes(dataset):return [r['net_r'] for r in dataset['rows'] if r['split']=='train' and r['outcome_observed']]
def _zero_mass(dataset):
    tr=[r for r in dataset['rows'] if r['split']=='train'];return sum(not r['outcome_observed'] or r['net_r']==0 for r in tr)/max(1,len(tr))
def predict(candidate,row,train_values,zero_mass,config):
    base=[quantile(train_values,q) for q in config.quantiles];signal=sum((i+1)*v for i,v in enumerate(row['features']))/max(1,len(row['features']))
    shift=candidate.feature_scale*.08*signal
    if candidate.algorithm=='empirical_km_baseline':vals=base
    elif candidate.algorithm=='monotone_quantile_hazard':vals=[x+shift*(.5+abs(q-.5)) for x,q in zip(base,config.quantiles)]
    elif candidate.algorithm=='zero_inflated_mixture':vals=[(1-zero_mass)*(x+shift) for x in base]
    elif candidate.algorithm=='competing_risk_ensemble':vals=[x+shift*(1.2 if q>.5 else .8) for x,q in zip(base,config.quantiles)]
    else:vals=[x*(1-candidate.tail_shrinkage*(1 if q<.2 else .25))+shift for x,q in zip(base,config.quantiles)]
    raw=list(vals);vals=monotone(vals) if config.monotone_quantiles else vals
    expected=mean(vals);out={'prediction_id':stable_id('v416dist',{'candidate':candidate.candidate_id,'row':row['row_id']}),'candidate_id':candidate.candidate_id,'row_id':row['row_id'],'quantile_levels':list(config.quantiles),'raw_quantiles':raw,'monotone_quantiles':vals,'quantile_crossing_before_projection':any(a>b for a,b in zip(raw,raw[1:])),'quantile_crossing_after_projection':any(a>b for a,b in zip(vals,vals[1:])),'zero_mass_probability':clamp(zero_mass+(0.03 if candidate.algorithm=='zero_inflated_mixture' else 0),0,1),'expected_net_r':expected,'known_as_of':row['known_as_of'],'synthetic_reference':True,'production_eligible':False};out['prediction_hash']=content_hash(out);return out

def build_predictions(candidates,dataset,config):
    train=_training_outcomes(dataset);zm=_zero_mass(dataset);validation=[r for r in dataset['rows'] if r['split']=='selection_validation'];items=[]
    for c in candidates:
        if c.enabled:items.extend(predict(c,r,train,zm,config) for r in validation)
    out={'phase':'SAED_V4_16','candidate_count':sum(c.enabled for c in candidates),'prediction_count':len(items),'quantile_levels':list(config.quantiles),'train_observed_outcome_count':len(train),'empirical_zero_mass_probability':zm,'items':items};out['artifact_hash']=content_hash(out);return out
