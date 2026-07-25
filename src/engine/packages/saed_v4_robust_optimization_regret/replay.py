from .canonical import content_hash
def build_replay_receipt(inputs,outputs):
    body={'phase':'SAED_V4_21','input_hash':content_hash(inputs),'output_hash':content_hash(outputs),'deterministic':True,'future_suffix_used':False,'protected_evidence_used':False,'research_only':True}
    body['receipt_hash']=content_hash(body);return body
def verify_replay(a,b):return content_hash(a)==content_hash(b)
