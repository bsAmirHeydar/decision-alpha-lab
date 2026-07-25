from .canonical import content_hash,stable_id

def receipt(core):
    hashes={k:content_hash(v) for k,v in sorted(core.items())};out={'phase':'SAED_V4_16','receipt_id':stable_id('v416integrity',hashes),'artifact_count':len(hashes),'artifact_hashes':hashes,'all_hashes_present':all(len(v)==64 for v in hashes.values()),'immutable':True};out['receipt_hash']=content_hash(out);return out
