from .canonical import content_hash,stable_id

def build(checkpoints,tournament):
    entries=[]
    for c in checkpoints:entries.append({**c,'reference_champion':c['candidate_id']==tournament['reference_champion_id']})
    doc={'phase':'SAED_V4_15','entries':entries,'entry_count':len(entries),'reference_champion_id':tournament['reference_champion_id'],'runtime_authority':False,'production_authority':False,'immutable':True};doc['registry_hash']=content_hash(doc);doc['registry_id']=stable_id('v415registry',doc);return doc
