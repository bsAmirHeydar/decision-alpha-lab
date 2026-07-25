from .canonical import content_hash,stable_id

def receipt(a,b):
    same=content_hash(a)==content_hash(b);doc={'phase':'SAED_V4_15','deterministic':same,'first_hash':content_hash(a),'second_hash':content_hash(b),'production_eligible':False};doc['receipt_hash']=content_hash(doc);doc['receipt_id']=stable_id('v415replay',doc);return doc
