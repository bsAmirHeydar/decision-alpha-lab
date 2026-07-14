from __future__ import annotations
from datetime import timedelta
from .canonical import parse_time,normalize_time
from .errors import TemporalError

def validate_event_times(event):
    et=parse_time(event.event_time);kt=parse_time(event.known_time)
    if kt<et:raise TemporalError('known_time before event_time')
    return et,kt
def canonical_event_key(event,source_priority:int=0):
    return (parse_time(event.event_time),parse_time(event.known_time),int(source_priority),event.stream_id,event.source_sequence,event.event_id)
def subtract_ms(value:str,milliseconds:int)->str:return normalize_time((parse_time(value)-timedelta(milliseconds=milliseconds)).isoformat())
def age_ms(event_time:str,event_as_of:str)->int:return max(0,int((parse_time(event_as_of)-parse_time(event_time)).total_seconds()*1000))
