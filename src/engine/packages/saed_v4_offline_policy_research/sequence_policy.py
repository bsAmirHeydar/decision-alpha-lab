from __future__ import annotations
from collections import defaultdict
from .numerics import normalize
from .policies import make_policy

def train(dataset,behavior,contract,actions,masks,ledger=None):
    counts=defaultdict(lambda:defaultdict(float));sequence_counts=defaultdict(int)
    for ep in dataset['episodes']:
        history=[]
        for step in ep['steps']:
            history=(history+[step['state']])[-contract.maximum_context_length:]
            key='|'.join(history);w=contract.recency_decay**(len(ep['steps'])-1-int(step['t']))
            counts[(step['state'],key)][step['action']]+=w;sequence_counts[(step['state'],key)]+=1
    state_raw=defaultdict(lambda:defaultdict(float));used=0
    for (state,key),dist in counts.items():
        if sequence_counts[(state,key)]>=contract.minimum_sequence_count:
            used+=1
            for a,v in dist.items():state_raw[state][a]+=v
    dists={}
    for s in behavior['states']:
        raw=[]
        for a in actions:
            if not masks['states'].get(s,{}).get(a,a=='skip'):raw.append(0.0)
            else:raw.append(state_raw[s][a]+contract.smoothing*behavior['states'][s].get(a,0.0))
        probs=normalize(raw);dists[s]={a:probs[i] for i,a in enumerate(actions)}
    if ledger: ledger.consume('training_trials',1,'sequence');ledger.consume('candidate_policies',1,'sequence')
    return make_policy('sequence_reference',dists,{'sequence_contexts_used':used,'maximum_context_length':contract.maximum_context_length,'fallback_to_behavior':True})
