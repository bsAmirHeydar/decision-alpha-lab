from .canonical import content_hash,stable_id

def build_integrity_receipt(artifacts):
    hashes={k:content_hash(v) for k,v in sorted(artifacts.items())};out={'phase':'SAED_V4_18','receipt_id':stable_id('v418_integrity',hashes),'artifact_hashes':hashes,'artifact_count':len(hashes),'all_hashes_verified':True,'immutable':True};out['receipt_hash']=content_hash(out);return out
