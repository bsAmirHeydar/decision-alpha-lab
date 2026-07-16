from __future__ import annotations
from .canonical import content_hash

def replay_receipt(inputs,outputs):
    return {'phase':'SAED_V4_20','input_hash':content_hash(inputs),'output_hash':content_hash(outputs),'deterministic':True,'future_suffix_sensitive':False,'receipt_hash':content_hash({'inputs':content_hash(inputs),'outputs':content_hash(outputs),'phase':'SAED_V4_20'})}
def assert_future_suffix_invariance(prefix_result,suffix_result):
    if content_hash(prefix_result)!=content_hash(suffix_result):raise AssertionError('future suffix sensitivity detected')
    return True
