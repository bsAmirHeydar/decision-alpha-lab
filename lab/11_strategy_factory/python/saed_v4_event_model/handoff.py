from .canonical import content_hash,stable_id

def build_v4_04_handoff(twin_manifest_hash,stream_manifests,projection,receipt,limitations):
    payload={'phase':'SAED_V4_03','next_phase':'SAED_V4_04','twin_manifest_hash':twin_manifest_hash,'stream_manifest_hashes':sorted(m.semantic_hash for m in stream_manifests),'projection_id':projection.projection_id,'projection_hash':projection.state_hash,'event_integrity_receipt_id':receipt.receipt_id,'known_as_of':projection.known_as_of,'event_as_of':projection.event_as_of,'limitations':sorted(limitations),'authority':{'mutate_ucee_truth':False,'mutate_twin_manifest':False,'select_treatment':False,'allocate_risk':False,'activate_runtime':False,'send_order':False,'network_access':False}}
    return {**payload,'handoff_id':stable_id('v403to04',payload),'handoff_hash':content_hash(payload)}
