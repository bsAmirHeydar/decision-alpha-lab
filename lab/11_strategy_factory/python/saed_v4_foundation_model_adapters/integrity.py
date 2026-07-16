from .canonical import content_hash,stable_id

def receipt(core):
    component_hashes={k:content_hash(v) for k,v in sorted(core.items())};doc={'phase':'SAED_V4_14','component_hashes':component_hashes,'component_count':len(component_hashes),'closed_bundle':True,'upstream_mutated':False};doc['receipt_hash']=content_hash(doc);doc['receipt_id']=stable_id('fmreceipt',doc);return doc
