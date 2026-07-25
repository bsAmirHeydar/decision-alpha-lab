from __future__ import annotations
from collections import defaultdict
from .trajectory import transitions
from .numerics import softmax
from .policies import make_policy

def train(dataset,contract,actions,masks,ledger=None):
    trs=transitions(dataset);states=sorted({t['state'] for t in trs}|{t['next_state'] for t in trs});q={s:{a:0.0 for a in actions} for s in states};groups=defaultdict(list);counts=defaultdict(int)
    for t in trs:groups[(t['state'],t['action'])].append(t);counts[(t['state'],t['action'])]+=1
    for _ in range(contract.iterations):
        new={s:dict(q[s]) for s in states}
        for s in states:
            for a in actions:
                rows=groups.get((s,a),[])
                if not rows:
                    new[s][a]=-contract.conservative_alpha*2.0;continue
                targets=[]
                for r in rows:
                    nxt=max(q.get(r['next_state'],{x:0.0 for x in actions}).values()) if not r['done'] else 0.0
                    targets.append(float(r['reward'])+contract.discount*nxt)
                penalty=contract.conservative_alpha/max(1.0,counts[(s,a)]**0.5)
                new[s][a]=sum(targets)/len(targets)-penalty
        q=new
    dists={}
    for s in states:
        allowed=[a for a in actions if masks['states'].get(s,{}).get(a,a=='skip')]
        probs=softmax([q[s][a] for a in allowed],contract.temperature);dists[s]={a:(probs[allowed.index(a)] if a in allowed else 0.0) for a in actions}
    if ledger: ledger.consume('training_trials',1,'cql');ledger.consume('candidate_policies',1,'cql')
    p=make_policy('cql_reference',dists,{'q_table':q,'iterations':contract.iterations,'conservative_alpha':contract.conservative_alpha})
    return p
