from __future__ import annotations
from functools import reduce
from .canonical import parse_time
from .enums import ProjectionReducer
from .errors import ProjectionError

def payload_get(payload,path):
    cur=payload
    if not path:return cur
    for p in path.split('.'):
        if not isinstance(cur,dict) or p not in cur:raise KeyError(path)
        cur=cur[p]
    return cur

def reduce_values(reducer,items,event_as_of,window_seconds=None):
    vals=[v for _,v in items]
    if reducer==ProjectionReducer.LAST:return vals[-1]
    if reducer==ProjectionReducer.COUNT:return len(vals)
    if reducer==ProjectionReducer.SUM:return sum(vals)
    if reducer==ProjectionReducer.MIN:return min(vals)
    if reducer==ProjectionReducer.MAX:return max(vals)
    if reducer==ProjectionReducer.MEAN:return sum(vals)/len(vals)
    if reducer==ProjectionReducer.BOOLEAN_ANY:return any(vals)
    if reducer==ProjectionReducer.BOOLEAN_ALL:return all(vals)
    if reducer==ProjectionReducer.TIME_SINCE:return (parse_time(event_as_of)-parse_time(items[-1][0].event_time)).total_seconds()
    if reducer==ProjectionReducer.EVENT_RATE:
        if not window_seconds or window_seconds<=0:raise ProjectionError('window required for event rate')
        return len(vals)/window_seconds
    if reducer==ProjectionReducer.DELTA:
        if len(vals)<2:return 0
        return vals[-1]-vals[0]
    raise ProjectionError('unsupported reducer')
