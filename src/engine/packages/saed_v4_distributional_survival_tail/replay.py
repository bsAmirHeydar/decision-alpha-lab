from .canonical import content_hash,stable_id

def receipt(first,second):
    a=content_hash(first);b=content_hash(second);out={'phase':'SAED_V4_16','replay_id':stable_id('v416replay',{'a':a,'b':b}),'first_bundle_hash':a,'second_bundle_hash':b,'deterministic':a==b,'decision_equivalent':a==b,'environment_scope':'standard_library_local_cpu'};out['receipt_hash']=content_hash(out);return out
