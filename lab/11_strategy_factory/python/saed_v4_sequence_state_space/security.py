from .canonical import content_hash,stable_id

def sbom():
    material={'phase':'SAED_V4_12','runtime':'python-standard-library','external_runtime_dependencies':[],'optional_accelerators':[],'network_access_required':False,'dynamic_code_loading':False,'pickle_allowed':False,'checkpoint_format':'canonical_json','supply_chain_state':'reference_local'}
    return {**material,'sbom_id':stable_id('seqsbom',material),'sbom_hash':content_hash(material)}
def incident_template():
    material={'phase':'SAED_V4_12','incident_classes':['causal_mask_breach','state_leakage','reset_mismatch','streaming_parity_failure','snapshot_corruption','numerical_instability','upstream_hash_mismatch'],'immediate_actions':['quarantine_checkpoint','disable_reference_handoff','preserve_logs','replay_from_frozen_inputs'],'execution_kill_switch_required':False}
    return {**material,'template_id':stable_id('seqincident',material),'template_hash':content_hash(material)}
