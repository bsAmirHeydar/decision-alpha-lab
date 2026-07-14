from __future__ import annotations
import math
from .enums import TransformKind
from .errors import TransformError

def apply_transform(kind,values,event_as_of=None,event_times=None):
    if kind==TransformKind.IDENTITY:
        if len(values)!=1:raise TransformError('identity needs one input')
        return values[0]
    if kind==TransformKind.MIDPOINT:
        if len(values)!=2:return _arity('midpoint',2)
        return (float(values[0])+float(values[1]))/2.0
    if kind==TransformKind.SPREAD:
        if len(values)!=2:return _arity('spread',2)
        return float(values[1])-float(values[0])
    if kind==TransformKind.DIFFERENCE:
        if len(values)!=2:return _arity('difference',2)
        return float(values[0])-float(values[1])
    if kind==TransformKind.RATIO:
        if len(values)!=2:return _arity('ratio',2)
        if float(values[1])==0:raise TransformError('division by zero')
        return float(values[0])/float(values[1])
    if kind==TransformKind.LOG_RETURN:
        if len(values)!=2:return _arity('log_return',2)
        if float(values[0])<=0 or float(values[1])<=0:raise TransformError('log return requires positive inputs')
        return math.log(float(values[0])/float(values[1]))
    if kind==TransformKind.BOOLEAN_AND:return all(bool(x) for x in values)
    if kind==TransformKind.BOOLEAN_OR:return any(bool(x) for x in values)
    if kind==TransformKind.CONCAT:return '|'.join(str(x) for x in values)
    if kind==TransformKind.VECTOR:return [float(x) if isinstance(x,(int,float)) and not isinstance(x,bool) else x for x in values]
    if kind==TransformKind.AGE_SECONDS:
        if len(values)!=1 or not event_as_of or not event_times:return _arity('age_seconds',1)
        from .canonical import parse_time
        return max(0.0,(parse_time(event_as_of)-parse_time(event_times[0])).total_seconds())
    raise TransformError('unsupported transform')
def _arity(name,n):raise TransformError(f'{name} needs {n} inputs')
