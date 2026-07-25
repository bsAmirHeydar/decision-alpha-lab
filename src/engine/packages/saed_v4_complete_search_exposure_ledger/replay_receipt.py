from .canonical import content_hash, stable_id

def build(config, manifests, trial_events, exposure_events, outputs):
    payload={"phase":"SAED_V4_27","input_hashes":{"config":content_hash(config),"manifests":content_hash(manifests),"trial_events":content_hash(trial_events),"exposure_events":content_hash(exposure_events)},"output_hashes":{k:content_hash(v) for k,v in outputs.items()},"deterministic":True,"network_access":False,"future_suffix_queries":0,"protected_evidence_queries":0,"hidden_evaluation_queries":0,"runtime_compilations":0,"order_submissions":0,"online_policy_mutations":0}
    payload["replay_receipt_id"]=stable_id("v427_replay",payload); payload["replay_receipt_hash"]=content_hash(payload)
    return payload
