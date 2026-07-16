from .canonical import content_hash,stable_id

def build(checkpoints,tournament):
    entries=sorted([{'checkpoint_id':x['checkpoint_id'],'checkpoint_hash':x['checkpoint_hash'],'candidate_id':x['candidate_id'],'family':x['family'],'adapter_mode':x['adapter_mode'],'composite_score':x['composite_score'],'production_eligible':False} for x in checkpoints],key=lambda x:x['candidate_id'])
    doc={'phase':'SAED_V4_14','entries':entries,'reference_champion_id':tournament['reference_champion_id'],'tournament_hash':tournament['tournament_hash'],'immutable':True,'revocable':True,'runtime_authority':False}
    doc['registry_hash']=content_hash(doc);doc['registry_id']=stable_id('fmregistry',doc);return doc
