from __future__ import annotations
from collections import defaultdict
from .trajectory import transitions
from .behavior import probability
from .numerics import effective_sample_size
from .canonical import content_hash,stable_id

def diagnose(dataset,behavior,candidate,contract,actions):
    counts=defaultdict(lambda:defaultdict(int));ratios=[];unsupported_mass=[];violations=[]
    for tr in transitions(dataset):
        counts[tr['state']][tr['action']]+=1
        pi=float(candidate['states'].get(tr['state'],{}).get(tr['action'],0.0));mu=max(probability(behavior,tr['state'],tr['action']),1e-12)
        ratios.append(min(contract.maximum_importance_weight,pi/mu))
    for state,dist in candidate['states'].items():
        mass=0.0
        for a,p in dist.items():
            c=counts[state][a];mu=probability(behavior,state,a)
            if c<contract.minimum_state_action_count or mu<contract.minimum_behavior_probability: mass+=float(p)
        unsupported_mass.append(mass)
        if mass>contract.maximum_unsupported_mass: violations.append({'state':state,'unsupported_mass':mass})
    ess=effective_sample_size(ratios);passed=(max(unsupported_mass or [0.0])<=contract.maximum_unsupported_mass and ess>=contract.minimum_effective_sample_size)
    out={'report_id':stable_id('support_report',{'candidate':candidate['policy_id'],'dataset':dataset['dataset_id']}),'candidate_policy_id':candidate['policy_id'],'minimum_count':min((counts[s][a] for s in counts for a in actions),default=0),'minimum_behavior_probability':min((probability(behavior,s,a) for s in behavior['states'] for a in actions),default=0.0),'maximum_unsupported_mass':max(unsupported_mass or [0.0]),'effective_sample_size':ess,'importance_weight_max':max(ratios or [0.0]),'violation_count':len(violations),'violations':violations,'passed':passed}
    out['support_hash']=content_hash(out);return out
