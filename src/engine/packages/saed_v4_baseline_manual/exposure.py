from .canonical import content_hash, stable_id

def build_exposure(registry:dict,benchmark:dict)->dict:
    expected=sorted(x['baseline_key'] for x in registry['entries']); observed=sorted(x['baseline_key'] for x in benchmark['results'])
    payload={"phase":"SAED_V4_10","expected_baselines":expected,"observed_baselines":observed,"missing_baselines":sorted(set(expected)-set(observed)),"unexpected_baselines":sorted(set(observed)-set(expected)),"expected_count":len(expected),"observed_count":len(observed),"complete":expected==observed}
    payload['ledger_id']=stable_id('baselineexposure',payload);payload['ledger_hash']=content_hash(payload)
    return payload
