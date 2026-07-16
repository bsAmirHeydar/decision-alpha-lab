from __future__ import annotations
from .canonical import hash_signed,hash_unit,content_hash,stable_id
from .numerics import softmax

def _covariates(i,env):
    return {
      'context_strength':0.75*hash_signed(f'ctx:{i}')+0.12*env,
      'liquidity_state':0.70*hash_signed(f'liq:{i}')-0.08*env,
      'volatility_state':0.65*hash_signed(f'vol:{i}')+0.10*(env-2),
      'execution_friction':0.55+0.28*hash_unit(f'fric:{i}')+0.05*(env%2),
      'structure_state':0.72*hash_signed(f'struct:{i}')+0.08*(2-env),
      'tail_risk':0.25+0.55*hash_unit(f'tail:{i}')+0.06*(env==4),
      'instrument_z':hash_signed(f'z:{i}'),
      'negative_control_exposure':hash_signed(f'ncx:{i}')}

def _logits(x):
    return [
      0.05-0.10*x['context_strength']+0.08*x['execution_friction'],
      0.30*x['context_strength']-0.18*x['volatility_state']-0.15*x['execution_friction']+0.10*x['instrument_z'],
      0.22*x['liquidity_state']-0.18*x['tail_risk']-0.08*x['instrument_z'],
      0.20*x['structure_state']+0.15*x['volatility_state']-0.20*x['execution_friction']]

def _choose(probs,u):
    s=0.0
    for k,p in enumerate(probs):
        s+=p
        if u<=s:return k
    return len(probs)-1

def build_synthetic_dataset(treatment_ids,n=480,environment_count=6):
    rows=[];ground=[]
    for i in range(n):
        env=min(environment_count-1,i//(n//environment_count));x=_covariates(i,env);probs=softmax(_logits(x));idx=_choose(probs,hash_unit(f'assign:{i}'));t=treatment_ids[idx]
        base=-0.10*x['execution_friction']-0.05*x['tail_risk']+0.08*x['liquidity_state']+0.04*x['structure_state']
        taus={
          treatment_ids[0]:0.0,
          treatment_ids[1]:0.20+0.34*x['context_strength']-0.18*x['volatility_state']-0.14*x['execution_friction'],
          treatment_ids[2]:0.11-0.17*x['context_strength']+0.30*x['liquidity_state']-0.12*x['tail_risk'],
          treatment_ids[3]:0.07+0.24*x['structure_state']+0.16*x['volatility_state']-0.21*x['execution_friction']}
        costs={treatment_ids[0]:0.0,treatment_ids[1]:0.018,treatment_ids[2]:0.014,treatment_ids[3]:0.022}
        common_noise=0.055*hash_signed(f'noise:{i}')
        potential={k:base+v-costs[k]+common_noise for k,v in taus.items()}
        outcome=potential[t]
        nc_outcome=0.12*hash_signed(f'ncy:{i}')+0.02*x['instrument_z']
        features=[x[k] for k in ['context_strength','liquidity_state','volatility_state','execution_friction','structure_state','tail_risk','instrument_z','negative_control_exposure']]
        row={'row_id':stable_id('row',{'phase':'v418','i':i}),'ordinal':i,'cluster_id':f'cluster_{i//2:04d}','environment_id':f'env_{env}','features':features,'feature_map':x,'assigned_treatment':t,'observed_outcome':outcome,'outcome_observed':True,'negative_control_outcome':nc_outcome,'known_time_valid':True,'protected_evidence':False}
        rows.append(row);ground.append({'row_id':row['row_id'],'true_propensities':{tid:probs[k] for k,tid in enumerate(treatment_ids)},'potential_outcomes':potential,'true_effects_vs_baseline':{tid:potential[tid]-potential[treatment_ids[0]] for tid in treatment_ids}})
    dataset={'phase':'SAED_V4_18','dataset_id':stable_id('v418_dataset',{'n':n,'treatments':treatment_ids}),'row_count':len(rows),'treatment_ids':list(treatment_ids),'feature_names':['context_strength','liquidity_state','volatility_state','execution_friction','structure_state','tail_risk','instrument_z','negative_control_exposure'],'environment_count':environment_count,'cluster_count':len(set(r['cluster_id'] for r in rows)),'known_time_only':True,'synthetic_only':True,'protected_evidence_exposures':0,'rows':rows}
    dataset['dataset_hash']=content_hash(dataset)
    truth={'phase':'SAED_V4_18','benchmark_only':True,'selectable':False,'visible_to_estimators':False,'rows':ground};truth['ground_truth_hash']=content_hash(truth)
    return dataset,truth
