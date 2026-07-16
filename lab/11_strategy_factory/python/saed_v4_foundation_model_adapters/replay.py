from .canonical import content_hash,stable_id

def receipt(first,second):
    a=content_hash(first);b=content_hash(second);doc={'phase':'SAED_V4_14','first_hash':a,'second_hash':b,'deterministic':a==b,'external_state_accessed':False,'network_accessed':False};doc['replay_hash']=content_hash(doc);doc['replay_id']=stable_id('fmreplay',doc);return doc
