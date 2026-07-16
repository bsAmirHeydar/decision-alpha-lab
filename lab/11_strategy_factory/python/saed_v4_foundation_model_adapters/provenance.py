from .canonical import content_hash,stable_id

def build(upstream,seq,tournament,registry,intake_decisions):
    doc={'phase':'SAED_V4_14','upstream_v4_13_handoff_hash':upstream['v4_13_handoff_hash'],'upstream_v4_13_registry_hash':upstream['v4_13_registry_hash'],'source_token_sequence_hash':seq['token_sequence_hash'],'tournament_hash':tournament['tournament_hash'],'foundation_checkpoint_registry_hash':registry['registry_hash'],'intake_decision_hashes':[x['decision_hash'] for x in sorted(intake_decisions,key=lambda x:x['intake_id'])],'code_identity':'saed_v4_foundation_model_adapters@1.0.0','evidence_scope':'deterministic_synthetic_reference','external_weights_loaded':False}
    doc['provenance_hash']=content_hash(doc);doc['provenance_id']=stable_id('fmprov',doc);return doc
