from .canonical import content_hash,stable_id

def build(checkpoints,tournament):
    entries=sorted(checkpoints,key=lambda x:x['candidate_id']);out={'phase':'SAED_V4_16','registry_id':stable_id('v416registry',[x['checkpoint_hash'] for x in entries]),'entry_count':len(entries),'entries':entries,'reference_champion_id':tournament['reference_champion_id'],'immutable':True,'runtime_authority':False,'production_authority':False};out['registry_hash']=content_hash(out);return out
