from .canonical import content_hash,stable_id

def make(candidate,metric,tournament,upstream,dataset):
    out={'phase':'SAED_V4_16','checkpoint_id':stable_id('v416checkpoint',{'candidate':candidate.candidate_id,'metric':metric,'dataset':dataset['dataset_hash']}),'candidate_id':candidate.candidate_id,'algorithm':candidate.algorithm,'dataset_hash':dataset['dataset_hash'],'upstream_fusion_hash':upstream['v4_15_fusion_hash'],'reference_score':metric['reference_score'],'reference_champion':candidate.candidate_id==tournament['reference_champion_id'],'status':'research_checkpoint','immutable':True,'revoked':False,'runtime_eligible':False,'production_eligible':False};out['checkpoint_hash']=content_hash(out);return out
