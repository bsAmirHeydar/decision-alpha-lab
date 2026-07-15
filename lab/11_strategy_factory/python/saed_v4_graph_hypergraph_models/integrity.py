from .canonical import content_hash,merkle_root,stable_id
def receipt(documents):
    entries=[{'name':k,'hash':content_hash(v)} for k,v in sorted(documents.items())];root=merkle_root([x['hash'] for x in entries]);doc={'phase':'SAED_V4_13','entries':entries,'entry_count':len(entries),'merkle_root':root,'immutable':True};doc['receipt_hash']=content_hash(doc);doc['receipt_id']=stable_id('graphintegrity',doc);return doc
