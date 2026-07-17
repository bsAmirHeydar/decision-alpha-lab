from __future__ import annotations
import hashlib,json
from typing import Any

def canonical_json(obj:Any)->str:
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False)

def digest_object(obj:Any)->str:
    return "sha256:"+hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()
