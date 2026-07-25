from __future__ import annotations
from collections import defaultdict
from .behavior import probability
from .numerics import mean,bootstrap_ci,weighted_mean,effective_sample_size
from .canonical import content_hash,stable_id

def policy_prob(policy,state,action): return float(policy['states'].get(state,{}).get(action,0.0))
def fit_fqe(dataset,policy,actions,discount,iterations=40):
    states=sorted({st['state'] for ep in dataset['episodes'] for st in ep['steps']}|{st['next_state'] for ep in dataset['episodes'] for st in ep['steps']});q={s:{a:0.0 for a in actions} for s in states};groups=defaultdict(list)
    for ep in dataset['episodes']:
        for st in ep['steps']:groups[(st['state'],st['action'])].append(st)
    for _ in range(iterations):
        nq={s:dict(q[s]) for s in states}
        for s in states:
            for a in actions:
                rows=groups.get((s,a),[])
                if rows:
                    vals=[]
                    for r in rows:
                        nv=sum(policy_prob(policy,r['next_state'],na)*q.get(r['next_state'],{}).get(na,0.0) for na in actions)
                        vals.append(float(r['reward'])+(0.0 if r['done'] else discount*nv))
                    nq[s][a]=mean(vals)
        q=nq
    return q

def evaluate(dataset,behavior,policy,contract,actions,ledger=None,seed=423):
    q=fit_fqe(dataset,policy,actions,contract.discount);episode_rows=[];wis_weights=[];wis_returns=[];pdis_returns=[];dr_returns=[];fqe_returns=[]
    for ep in dataset['episodes']:
        rho=1.0;g=0.0;pdis=0.0;dr=0.0;disc=1.0
        first=ep['steps'][0];fqe0=sum(policy_prob(policy,first['state'],a)*q[first['state']][a] for a in actions)
        for st in ep['steps']:
            pi=policy_prob(policy,st['state'],st['action']);mu=max(float(st['behavior_prob']),1e-12);ratio=min(contract.weight_clip,pi/mu);rho*=ratio;g+=disc*float(st['reward']);pdis+=disc*rho*float(st['reward'])
            v=sum(policy_prob(policy,st['state'],a)*q[st['state']][a] for a in actions);qsa=q[st['state']][st['action']];dr+=disc*(v+rho*(float(st['reward'])-qsa));disc*=contract.discount
        wis_weights.append(rho);wis_returns.append(g);pdis_returns.append(pdis);dr_returns.append(dr);fqe_returns.append(fqe0);episode_rows.append({'episode_id':ep['episode_id'],'cluster_id':ep['cluster_id'],'return':g,'terminal_weight':rho,'pdis':pdis,'doubly_robust':dr,'fqe':fqe0})
    wis=weighted_mean(wis_returns,wis_weights);estimates={'wis':wis,'pdis':mean(pdis_returns),'fqe':mean(fqe_returns),'doubly_robust':mean(dr_returns)}
    cis={name:bootstrap_ci(([wis_returns[i]*wis_weights[i] for i in range(len(wis_returns))] if name=='wis' else {'pdis':pdis_returns,'fqe':fqe_returns,'doubly_robust':dr_returns}[name]),seed+idx,contract.bootstrap_draws,1-contract.confidence_level) for idx,name in enumerate(['wis','pdis','fqe','doubly_robust'])}
    lower=min(ci['lower'] for ci in cis.values());upper=max(ci['upper'] for ci in cis.values())
    out={'ope_id':stable_id('ope',{'dataset':dataset['dataset_id'],'policy':policy['policy_id']}),'policy_id':policy['policy_id'],'dataset_id':dataset['dataset_id'],'estimators':estimates,'confidence_intervals':cis,'aggregate_lower_bound':lower,'aggregate_upper_bound':upper,'estimator_spread':max(estimates.values())-min(estimates.values()),'effective_sample_size':effective_sample_size(wis_weights),'maximum_terminal_weight':max(wis_weights or [0.0]),'episode_rows':episode_rows,'synthetic_positive_evidence':False,'promotion_authority':False}
    out['ope_hash']=content_hash(out)
    if ledger:ledger.consume('ope_evaluations',1,policy['policy_id']);ledger.consume('bootstrap_draws',contract.bootstrap_draws,policy['policy_id'])
    return out
