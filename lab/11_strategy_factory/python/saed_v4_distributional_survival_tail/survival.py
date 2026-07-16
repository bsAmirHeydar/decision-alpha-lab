from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import clamp,sigmoid,isotonic_probabilities,mean

def kaplan_meier(train,horizons):
    surv=[];s=1.0;prev=0
    for h in horizons:
        at=sum(r['event_duration_seconds']>=prev for r in train);d=sum(r['event_observed'] and prev<r['event_duration_seconds']<=h for r in train)
        if at:s*=max(0.0,1-d/at)
        surv.append(s);prev=h
    return surv

def cause_hazards(train,causes,horizons):
    out={c:[] for c in causes};prev=0
    for h in horizons:
        at=max(1,sum(r['event_duration_seconds']>=prev for r in train))
        for c in causes:out[c].append(sum(r['event_observed'] and r['event_cause']==c and prev<r['event_duration_seconds']<=h for r in train)/at)
        prev=h
    return out

def fit_candidate(candidate,dataset,registry,config):
    train=[r for r in dataset['rows'] if r['split']=='train'];km=kaplan_meier(train,config.horizons_seconds);haz=cause_hazards(train,registry.causes,config.horizons_seconds)
    state={'candidate_id':candidate.candidate_id,'algorithm':candidate.algorithm,'horizons_seconds':list(config.horizons_seconds),'km_survival':km,'cause_hazards':haz,'train_count':len(train),'feature_scale':candidate.feature_scale,'survival_family':candidate.survival_family};state['state_hash']=content_hash(state);return state

def predict(candidate,state,row,registry):
    score=sum((i+1)*v for i,v in enumerate(row['features']))/max(1,len(row['features']))
    adjustment=(sigmoid(candidate.feature_scale*score)-.5)*.16
    survival=[];cumulative={c:[] for c in registry.causes};cum_total=0.0
    for k,h in enumerate(state['horizons_seconds']):
        probs=[]
        for c in registry.causes:
            base=state['cause_hazards'][c][k];direction=1 if c in {'target','trail_exit','fill'} else -1
            probs.append(clamp(base*(1+direction*adjustment),0,.7))
        total=sum(probs)
        if total>0.92:probs=[p*.92/total for p in probs]
        step_mass=max(0.0,1-cum_total)*sum(probs);cum_total=min(1.0,cum_total+step_mass)
        survival.append(max(0.0,1-cum_total))
        for c,p in zip(registry.causes,probs):
            prev=cumulative[c][-1] if cumulative[c] else 0.0;cumulative[c].append(min(1.0,prev+max(0.0,1-cum_total+step_mass)*p))
    # normalize cumulative incidence so sum never exceeds one.
    for k in range(len(state['horizons_seconds'])):
        total=sum(cumulative[c][k] for c in registry.causes)
        if total>1:
            for c in registry.causes:cumulative[c][k]/=total
    survival=[max(0.0,1-sum(cumulative[c][k] for c in registry.causes)) for k in range(len(state['horizons_seconds']))]
    expected=sum((survival[k-1] if k else 1.0)*(h-(state['horizons_seconds'][k-1] if k else 0)) for k,h in enumerate(state['horizons_seconds']))
    out={'prediction_id':stable_id('v416surv',{'candidate':candidate.candidate_id,'row':row['row_id']}),'candidate_id':candidate.candidate_id,'row_id':row['row_id'],'horizons_seconds':list(state['horizons_seconds']),'survival_probability':survival,'cause_cumulative_incidence':cumulative,'expected_remaining_opportunity_seconds':expected,'known_as_of':row['known_as_of'],'synthetic_reference':True,'production_eligible':False};out['prediction_hash']=content_hash(out);return out

def build_predictions(candidates,dataset,registry,config):
    validation=[r for r in dataset['rows'] if r['split']=='selection_validation'];states=[];items=[]
    for c in candidates:
        if not c.enabled:continue
        state=fit_candidate(c,dataset,registry,config);states.append(state)
        items.extend(predict(c,state,r,registry) for r in validation)
    out={'phase':'SAED_V4_16','candidate_count':len(states),'prediction_count':len(items),'horizons_seconds':list(config.horizons_seconds),'states':states,'items':items};out['artifact_hash']=content_hash(out);return out
