from .canonical import content_hash,stable_id

def build(upstream,aligned,tournament,registry):
    doc={'phase':'SAED_V4_15','version':'1.0.0','upstream_v4_14_handoff_hash':upstream['v4_14_handoff_hash'],'upstream_v4_04_package_hash':upstream['v4_04_package_hash'],'aligned_set_hash':aligned['aligned_set_hash'],'tournament_hash':tournament['tournament_hash'],'registry_hash':registry['registry_hash'],'known_time_only':True,'outcome_labels_accessed':False,'external_models_invoked':False,'production_eligible':False};doc['provenance_hash']=content_hash(doc);doc['provenance_id']=stable_id('v415provenance',doc);return doc
