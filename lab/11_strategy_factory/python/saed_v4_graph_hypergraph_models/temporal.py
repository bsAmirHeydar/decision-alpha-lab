from __future__ import annotations
from datetime import datetime,timezone
from .errors import CausalityError

def parse_utc(value:str)->datetime:
    try:
        dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    except Exception as e: raise CausalityError(f'invalid timestamp {value}') from e
    if dt.tzinfo is None: raise CausalityError('naive timestamp forbidden')
    return dt.astimezone(timezone.utc)

def assert_known_time(event_time:str,known_time:str,cutoff:str)->None:
    e,k,c=map(parse_utc,(event_time,known_time,cutoff))
    if k<e: raise CausalityError('known_time precedes event_time')
    if k>c: raise CausalityError('record is future-known relative to cutoff')

def seconds_between(a:str,b:str)->float: return (parse_utc(b)-parse_utc(a)).total_seconds()
