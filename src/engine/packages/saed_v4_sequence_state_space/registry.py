from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import RegistryError

def build_registry(cards,tournament):
    ids=[c['checkpoint_id'] for c in cards]
    if len(ids)!=len(set(ids)):raise RegistryError('duplicate checkpoint id')
    entries=[]
    for c in sorted(cards,key=lambda x:x['checkpoint_id']):
        admitted=c['streaming_parity_passed'] and not c['state_collapsed']
        entries.append({'checkpoint_id':c['checkpoint_id'],'checkpoint_hash':c['checkpoint_hash'],'candidate_id':c['candidate_id'],'architecture':c['architecture'],'state':'admitted_reference' if admitted else 'quarantined','production_eligible':False,'runtime_authority':False})
    material={'phase':'SAED_V4_12','entries':entries,'reference_champion_id':tournament['reference_champion_id'],'immutable':True,'admission_scope':'synthetic_reference_challenger'}
    return {**material,'admitted_count':sum(e['state']=='admitted_reference' for e in entries),'registry_id':stable_id('seqregistry',material),'registry_hash':content_hash(material)}
