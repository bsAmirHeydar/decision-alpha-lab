from __future__ import annotations
from .trajectory import transitions
from .numerics import mean,std,quantile
from .canonical import content_hash,stable_id

def audit(dataset,contract):
    trs=transitions(dataset);rewards=[float(t['reward']) for t in trs];component_totals={c:sum(float(t['reward_components'][c]) for t in trs) for c in contract.components}
    mismatch=max(abs(sum(float(t['reward_components'][c]) for c in contract.components)-float(t['reward'])) for t in trs)
    clipped=sum(1 for r in rewards if r<=contract.minimum_reward or r>=contract.maximum_reward)
    out={'audit_id':stable_id('reward_audit',{'dataset_id':dataset['dataset_id'],'reward_count':len(rewards)}),'reward_count':len(rewards),'mean':mean(rewards),'std':std(rewards),'minimum':min(rewards),'maximum':max(rewards),'q05':quantile(rewards,0.05),'q50':quantile(rewards,0.5),'q95':quantile(rewards,0.95),'component_totals':component_totals,'maximum_component_sum_error':mismatch,'boundary_clip_count':clipped,'passed':mismatch<=1e-9 and min(rewards)>=contract.minimum_reward and max(rewards)<=contract.maximum_reward,'synthetic_positive_evidence':False}
    out['audit_hash']=content_hash(out);return out
