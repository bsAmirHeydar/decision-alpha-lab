from .canonical import content_hash

def build(upstream_hash,dataset_hash,registry_hash):
    out={'phase':'SAED_V4_17','version':'1.0.0','generator':'saed_v4_causal_mechanism_discovery.service.build_reference_bundle','upstream_v4_16_handoff_hash':upstream_hash,'dataset_hash':dataset_hash,'registry_hash':registry_hash,'evidence_scope':'local_deterministic_synthetic_reference','network_access':False,'protected_evidence_access':False,'real_data_access':False};out['provenance_hash']=content_hash(out);return out
