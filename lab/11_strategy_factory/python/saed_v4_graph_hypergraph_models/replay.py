from .canonical import content_hash,stable_id
def replay_receipt(first,second):
    passed=content_hash(first)==content_hash(second);doc={'phase':'SAED_V4_13','first_hash':content_hash(first),'second_hash':content_hash(second),'passed':passed,'scope':'deterministic_local_reference'};doc['replay_hash']=content_hash(doc);doc['replay_id']=stable_id('graphreplay',doc);return doc
