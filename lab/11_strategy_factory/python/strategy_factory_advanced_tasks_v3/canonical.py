from dataclasses import asdict,is_dataclass
from enum import Enum
from collections.abc import Mapping,Sequence
from decimal import Decimal,ROUND_HALF_EVEN
from hashlib import sha256
import json
SCALE=12

def fixed_float(value:float)->str:
    if value!=value or value in (float('inf'),float('-inf')): raise ValueError('non_finite')
    d=Decimal(str(value)).quantize(Decimal(1).scaleb(-SCALE),rounding=ROUND_HALF_EVEN)
    if d==0:d=abs(d)
    return format(d,f'.{SCALE}f')

def normalize(value):
    if value is None or isinstance(value,(str,bool,int)):return value
    if isinstance(value,float):return fixed_float(value)
    if isinstance(value,Enum):return value.value
    if is_dataclass(value):return normalize(asdict(value))
    if isinstance(value,Mapping):return {str(k):normalize(v) for k,v in sorted(value.items(),key=lambda x:str(x[0]))}
    if isinstance(value,Sequence) and not isinstance(value,(str,bytes,bytearray)):return [normalize(x) for x in value]
    raise TypeError(type(value).__name__)

def canonical_json(value)->str:return json.dumps(normalize(value),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def canonical_sha256(value)->str:return sha256(canonical_json(value).encode()).hexdigest()
def stable_id(prefix:str,value)->str:return f'{prefix}_{canonical_sha256(value)[:24]}'
