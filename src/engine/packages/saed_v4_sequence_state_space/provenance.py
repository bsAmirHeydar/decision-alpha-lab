from .canonical import content_hash,stable_id

def provenance(upstream_binding,config_hash,code_version='1.0.0'):
    material={'phase':'SAED_V4_12','code_version':code_version,'upstream_binding_hash':upstream_binding['binding_hash'],'configuration_hash':config_hash,'environment':'python_standard_library_reference','source_revision':'patch_payload','evidence_scope':'synthetic_reference'}
    return {**material,'provenance_id':stable_id('seqprov',material),'provenance_hash':content_hash(material)}
