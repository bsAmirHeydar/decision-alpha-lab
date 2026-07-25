from __future__ import annotations
from .canonical import content_hash,stable_id
def telemetry(twin_id,event_type,known_time,details):
    payload={'twin_id':twin_id,'event_type':event_type,'known_time':known_time,'details':details}
    return {**payload,'telemetry_id':stable_id('ttele',payload),'event_hash':content_hash(payload)}
