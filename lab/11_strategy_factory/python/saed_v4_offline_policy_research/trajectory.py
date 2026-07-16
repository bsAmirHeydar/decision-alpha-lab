from __future__ import annotations
from .errors import DatasetError
from .canonical import content_hash,stable_id
STEP_FIELDS={'t','state','action','reward','next_state','done','behavior_prob','allowed_actions','known_at','reward_components'}
EPISODE_FIELDS={'episode_id','cluster_id','start_time','steps'}
DOC_FIELDS={'dataset_id','context_id','role','known_time_cutoff','action_space_hash','reward_contract_hash','episodes'}

def validate_dataset(doc,contract,action_contract,reward_contract,ledger=None):
    if set(doc)!=DOC_FIELDS: raise DatasetError('dataset document fields mismatch')
    if doc['role'] not in contract.allowed_roles: raise DatasetError('dataset role forbidden')
    if len(doc['episodes'])<contract.minimum_episodes: raise DatasetError('insufficient episodes')
    seen=set();total=0;states=set();actions=set();clusters=set()
    for ep in doc['episodes']:
        if set(ep)!=EPISODE_FIELDS or ep['episode_id'] in seen: raise DatasetError('episode contract failure')
        seen.add(ep['episode_id']);clusters.add(ep['cluster_id'])
        if len(ep['steps'])<contract.minimum_steps_per_episode: raise DatasetError('short episode')
        prior=-1
        for i,step in enumerate(ep['steps']):
            if set(step)!=STEP_FIELDS: raise DatasetError('step fields mismatch')
            if int(step['t'])<=prior: raise DatasetError('non-monotonic time')
            prior=int(step['t'])
            if step['known_at']>doc['known_time_cutoff']: raise DatasetError('future suffix detected')
            if step['action'] not in action_contract.actions or step['next_state']=='' or step['state']=='': raise DatasetError('invalid state/action')
            if set(step['allowed_actions'])-set(action_contract.actions) or action_contract.safe_action not in step['allowed_actions'] or step['action'] not in step['allowed_actions']: raise DatasetError('action mask violation')
            if not 0<float(step['behavior_prob'])<=1: raise DatasetError('invalid behavior probability')
            comps=step['reward_components']
            if set(comps)!=set(reward_contract.components): raise DatasetError('reward components mismatch')
            gross=float(comps['gross_return']);cost=float(comps['execution_cost']);risk=float(comps['risk_penalty'])
            if cost>1e-12 or risk>1e-12: raise DatasetError('cost and penalty must be non-positive')
            if abs((gross+cost+risk)-float(step['reward']))>1e-9: raise DatasetError('reward component sum mismatch')
            if not reward_contract.minimum_reward<=float(step['reward'])<=reward_contract.maximum_reward: raise DatasetError('reward out of bounds')
            total+=1;states|={step['state'],step['next_state']};actions.add(step['action'])
        if ep['steps'][-1]['done'] is not True: raise DatasetError('episode must terminate')
        if ledger: ledger.consume('dataset_episodes',1,ep['episode_id'])
    out={'dataset_id':doc['dataset_id'],'context_id':doc['context_id'],'role':doc['role'],'episode_count':len(doc['episodes']),'step_count':total,'cluster_count':len(clusters),'states':sorted(states),'actions':sorted(actions),'known_time_cutoff':doc['known_time_cutoff'],'dataset_hash':content_hash(doc)}
    out['summary_id']=stable_id('dataset_summary',out);out['summary_hash']=content_hash(out);return out

def transitions(doc):
    return [dict(step,episode_id=ep['episode_id'],cluster_id=ep['cluster_id']) for ep in doc['episodes'] for step in ep['steps']]
