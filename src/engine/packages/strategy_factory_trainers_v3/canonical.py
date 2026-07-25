from dataclasses import asdict,is_dataclass
from decimal import Decimal,ROUND_HALF_EVEN
from enum import Enum
from hashlib import sha256
from collections.abc import Mapping,Sequence
import json
SCALE=12
def fixed_float(v):
 if v!=v or v in (float('inf'),float('-inf')): raise ValueError('non_finite')
 d=Decimal(str(v)).quantize(Decimal(1).scaleb(-SCALE),rounding=ROUND_HALF_EVEN)
 if d==0:d=abs(d)
 return format(d,f'.{SCALE}f')
def normalize(v):
 if v is None or isinstance(v,(str,bool,int)):return v
 if isinstance(v,float):return fixed_float(v)
 if isinstance(v,Enum):return v.value
 if is_dataclass(v):return normalize(asdict(v))
 if isinstance(v,Mapping):return {str(k):normalize(x) for k,x in sorted(v.items(),key=lambda z:str(z[0]))}
 if isinstance(v,Sequence) and not isinstance(v,(str,bytes,bytearray)):return [normalize(x) for x in v]
 raise TypeError(type(v).__name__)
def canonical_json(v):return json.dumps(normalize(v),sort_keys=True,separators=(',',':'),ensure_ascii=True)
def canonical_sha256(v):return sha256(canonical_json(v).encode()).hexdigest()
def stable_id(prefix,v):return f'{prefix}_{canonical_sha256(v)[:24]}'
