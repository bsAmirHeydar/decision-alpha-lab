from __future__ import annotations
from .canonical import content_hash,stable_id

def build(metrics,tournament,dataset_hash,upstream_hash):
    items=[]
    for row in metrics['rows']:
        item={'phase':'SAED_V4_17','checkpoint_id':stable_id('v417checkpoint',{'candidate':row['candidate_id'],'dataset':dataset_hash}),'candidate_id':row['candidate_id'],'algorithm':row['algorithm'],'dataset_hash':dataset_hash,'upstream_v4_16_handoff_hash':upstream_hash,'graph_hash':row['graph_hash'],'reference_score':row['reference_score'],'status':'research_checkpoint','immutable':True,'revoked':False,'reference_champion':row['candidate_id']==tournament['reference_champion_id'],'causal_claim_eligible':False,'runtime_eligible':False,'production_eligible':False};item['checkpoint_hash']=content_hash(item);items.append(item)
    return items

def registry(checkpoints,tournament):
    out={'phase':'SAED_V4_17','registry_id':stable_id('v417registry',[x['checkpoint_hash'] for x in checkpoints]),'entry_count':len(checkpoints),'entries':sorted(checkpoints,key=lambda x:x['candidate_id']),'reference_champion_id':tournament['reference_champion_id'],'immutable':True,'causal_claim_authority':False,'runtime_authority':False,'production_authority':False};out['registry_hash']=content_hash(out);return out
