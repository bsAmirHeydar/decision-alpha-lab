from __future__ import annotations
from collections import defaultdict
import math
from .trajectory import transitions
from .numerics import expectile,normalize
from .policies import make_policy

def train(dataset,behavior,contract,actions,masks,ledger=None):
    trs=transitions(dataset);states=sorted({t['state'] for t in trs}|{t['next_state'] for t in trs});q={s:{a:0.0 for a in actions} for s in states};v={s:0.0 for s in states};groups=defaultdict(list)
    for t in trs:groups[(t['state'],t['action'])].append(t)
    for _ in range(contract.iterations):
        for s in states:
            vals=[q[s][a] for a in actions];weights=[behavior['states'].get(s,{}).get(a,1/len(actions)) for a in actions];v[s]=expectile(vals,weights,contract.expectile,12)
        nq={s:dict(q[s]) for s in states}
        for s in states:
            for a in actions:
                rows=groups.get((s,a),[])
                if rows:nq[s][a]=sum(float(r['reward'])+(0.0 if r['done'] else contract.discount*v.get(r['next_state'],0.0)) for r in rows)/len(rows)
        q=nq
    dists={}
    for s in states:
        raw=[]
        for a in actions:
            if not masks['states'].get(s,{}).get(a,a=='skip'):raw.append(0.0);continue
            adv=q[s][a]-v[s];weight=min(contract.maximum_advantage_weight,math.exp(adv/contract.advantage_temperature));raw.append(behavior['states'].get(s,{}).get(a,0.0)*weight)
        probs=normalize(raw);dists[s]={a:probs[i] for i,a in enumerate(actions)}
    if ledger: ledger.consume('training_trials',1,'iql');ledger.consume('candidate_policies',1,'iql')
    return make_policy('iql_reference',dists,{'q_table':q,'value_table':v,'expectile':contract.expectile})
