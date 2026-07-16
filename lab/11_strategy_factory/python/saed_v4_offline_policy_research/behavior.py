from __future__ import annotations
from collections import defaultdict
from .numerics import normalize
from .canonical import content_hash,stable_id
from .trajectory import transitions

def estimate(dataset,contract,actions):
    counts=defaultdict(lambda:defaultdict(float));clusters=defaultdict(set)
    for tr in transitions(dataset): counts[tr['state']][tr['action']]+=1.0;clusters[tr['state']].add(tr['cluster_id'])
    policies={}
    for state in sorted(counts):
        raw=[counts[state][a]+contract.smoothing for a in actions];probs=normalize(raw)
        probs=[max(contract.minimum_probability,p) for p in probs];probs=normalize(probs)
        policies[state]={a:probs[i] for i,a in enumerate(actions)}
    out={'policy_id':stable_id('behavior_policy',{'dataset_id':dataset['dataset_id'],'contract':contract.exact_version}),'states':policies,'counts':{s:{a:int(counts[s][a]) for a in actions} for s in sorted(counts)},'cluster_counts':{s:len(clusters[s]) for s in sorted(clusters)},'actions':list(actions),'deterministic':True}
    out['policy_hash']=content_hash(out);return out

def probability(policy,state,action): return float(policy['states'].get(state,{}).get(action,0.0))
