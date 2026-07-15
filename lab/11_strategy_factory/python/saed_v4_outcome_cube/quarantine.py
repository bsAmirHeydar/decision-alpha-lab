from __future__ import annotations
from .canonical import content_hash,stable_id

def quarantine(reason_code:str,detail:str,source_hashes:list[str])->dict:
    payload={'phase':'SAED_V4_08','reason_code':reason_code,'detail':detail,'source_hashes':sorted(source_hashes),'fail_closed':True,'production_authorization':False};payload['quarantine_id']=stable_id('cubequarantine',payload);payload['quarantine_hash']=content_hash(payload);return payload
