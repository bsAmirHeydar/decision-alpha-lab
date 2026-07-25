from __future__ import annotations
from .canonical import content_hash,stable_id
def quarantine(source_id:str,source_hash:str,reason_code:str,detail:str)->dict:
    seed={'source_id':source_id,'source_hash':source_hash,'reason_code':reason_code,'detail':detail}
    return {'quarantine_id':stable_id('latticequarantine',seed),'quarantine_hash':content_hash(seed),**seed,'release_allowed':False}
