from .canonical import content_hash,stable_id

def receipt(core):
    hashes={k:content_hash(v) for k,v in sorted(core.items())};doc={'phase':'SAED_V4_15','artifact_hashes':hashes,'artifact_count':len(hashes),'all_hashes_present':all(hashes.values()),'immutable':True};doc['receipt_hash']=content_hash(doc);doc['receipt_id']=stable_id('v415integrity',doc);return doc
