from __future__ import annotations
from .canonical import content_hash
PREFIX='SAED_V4_22_SYNTHETIC_STRESS_ONLY'
def make(generator_id,seed,source_hash):
    payload={'prefix':PREFIX,'generator_id':str(generator_id),'seed':int(seed),'source_hash':str(source_hash),'positive_promotion_evidence':False,'runtime_eligible':False}
    payload['watermark_hash']=content_hash(payload);return payload
def validate(mark):
    return mark.get('prefix')==PREFIX and mark.get('positive_promotion_evidence') is False and mark.get('runtime_eligible') is False and mark.get('watermark_hash')==content_hash({k:v for k,v in mark.items() if k!='watermark_hash'})
