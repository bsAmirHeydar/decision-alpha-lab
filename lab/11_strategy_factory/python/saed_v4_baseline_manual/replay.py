from .canonical import content_hash, stable_id

def replay_receipt(original:dict,reproduced:dict)->dict:
    keys=['benchmark_hash','registry_hash','manifest_hash','compiled_program_hash']
    original_hash=next((original[k] for k in keys if k in original),content_hash(original)); reproduced_hash=next((reproduced[k] for k in keys if k in reproduced),content_hash(reproduced))
    payload={"phase":"SAED_V4_10","original_hash":original_hash,"reproduced_hash":reproduced_hash,"exact_match":original_hash==reproduced_hash,"deterministic":original_hash==reproduced_hash}
    payload['replay_id']=stable_id('v410replay',payload);payload['replay_hash']=content_hash(payload);return payload
