from __future__ import annotations
import hashlib,json
from typing import Any
def canonical_json(value:Any)->str:return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def object_digest(value:Any,field:str|None=None)->str:
 if field and isinstance(value,dict):value={k:v for k,v in value.items() if k!=field}
 return 'sha256:'+hashlib.sha256(canonical_json(value).encode('utf-8')).hexdigest()
