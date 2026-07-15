from .canonical import content_hash,stable_id
from .errors import RegistryError
def build(checkpoints,tournament):
    ids=[x['checkpoint_id'] for x in checkpoints]
    if len(ids)!=len(set(ids)):raise RegistryError('duplicate checkpoint id')
    entries=[{'checkpoint_id':x['checkpoint_id'],'checkpoint_hash':x['checkpoint_hash'],'candidate_id':x['candidate_id'],'architecture':x['architecture'],'state':'admitted_reference','production_eligible':False,'runtime_authority':False} for x in sorted(checkpoints,key=lambda x:x['checkpoint_id'])]
    doc={'phase':'SAED_V4_13','immutable':True,'admission_scope':'synthetic_reference_challenger','admitted_count':len(entries),'reference_champion_id':tournament['reference_champion_id'],'entries':entries}
    doc['registry_hash']=content_hash(doc);doc['registry_id']=stable_id('graphregistry',doc);return doc
