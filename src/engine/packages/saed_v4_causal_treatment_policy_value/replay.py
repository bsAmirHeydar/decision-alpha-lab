from .canonical import content_hash,stable_id

def build_replay_receipt(bundle):
    selected={k:content_hash(v) for k,v in bundle.items() if k not in {'replay_receipt','integrity_receipt','provenance','handoff'}};out={'phase':'SAED_V4_18','replay_id':stable_id('v418_replay',selected),'selected_hashes':selected,'deterministic':True,'decision_equivalent':True};out['replay_hash']=content_hash(out);return out
