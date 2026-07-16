from __future__ import annotations
from .numerics import normalize,l1_distribution,kl_divergence
from .canonical import content_hash,stable_id
from .errors import ProjectionError

def project(candidate,behavior,masks,support_counts,contract,actions,ledger=None):
    states={};details=[]
    for s in sorted(behavior['states']):
        raw=[]
        for a in actions:
            allowed=masks['states'].get(s,{}).get(a,a=='skip');supported=support_counts.get(s,{}).get(a,0)>0 and behavior['states'][s].get(a,0.0)>=contract.minimum_supported_probability
            raw.append(candidate['states'].get(s,{}).get(a,0.0) if allowed and supported else 0.0)
        if sum(raw)<=0:raw=[1.0 if a=='skip' else 0.0 for a in actions]
        probs=normalize(raw)
        idx=actions.index('skip')
        if probs[idx]<contract.safe_action_floor:
            rem=1-contract.safe_action_floor;other=sum(probs)-probs[idx];probs=[(p*rem/other if i!=idx and other>0 else p) for i,p in enumerate(probs)];probs[idx]=contract.safe_action_floor
        dist={a:probs[i] for i,a in enumerate(actions)};base=behavior['states'][s]
        l1=l1_distribution(dist,base,actions);blend=1.0
        if l1>contract.maximum_l1_from_behavior:
            blend=contract.maximum_l1_from_behavior/max(l1,1e-12);dist={a:blend*dist[a]+(1-blend)*base[a] for a in actions}
        kl=kl_divergence(dist,base,actions)
        if kl>contract.maximum_kl_from_behavior:
            blend2=min(1.0,contract.maximum_kl_from_behavior/max(kl,1e-12));dist={a:blend2*dist[a]+(1-blend2)*base[a] for a in actions};blend*=blend2;kl=kl_divergence(dist,base,actions)
        if any(dist[a]>0 and not masks['states'].get(s,{}).get(a,a=='skip') for a in actions):raise ProjectionError('mask projection failure')
        states[s]=dist;details.append({'state':s,'l1':l1_distribution(dist,base,actions),'kl':kl,'blend':blend})
    out=dict(candidate);out['states']=states;out['family']=candidate['family']+'_projected';out['source_policy_id']=candidate['policy_id'];out['policy_id']=stable_id('projected_policy',{'source':candidate['policy_id'],'states':states});out['policy_hash']=content_hash({k:v for k,v in out.items() if k!='policy_hash'});out['projection']={'state_details':details,'passed':all(d['l1']<=contract.maximum_l1_from_behavior+1e-9 and d['kl']<=contract.maximum_kl_from_behavior+1e-9 for d in details),'mask_enforced':True,'support_enforced':True}
    if ledger:ledger.consume('projection_attempts',1,candidate['policy_id'])
    return out
