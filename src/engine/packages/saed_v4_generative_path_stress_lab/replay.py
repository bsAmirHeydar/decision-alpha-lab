from __future__ import annotations
from .canonical import content_hash

def build(inputs,outputs):
    out={'phase':'SAED_V4_22','input_hash':content_hash(inputs),'output_hash':content_hash(outputs),'deterministic':True,'replay_command':'python src/engine/tooling/strategy_factory/saed_v4_22/reproduce_saed_v4_22_golden.py','external_runtime_evidence':False,'metaeditor_evidence':False};out['replay_receipt_hash']=content_hash(out);return out
