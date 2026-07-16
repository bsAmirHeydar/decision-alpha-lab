from __future__ import annotations
import hashlib
import json
import math

def _normalize(value):
    if isinstance(value, dict):
        return {str(key): _normalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError('non-finite float')
        return float(format(value, '.15g'))
    return value

def canonical_bytes(value) -> bytes:
    return json.dumps(_normalize(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def content_hash(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def stable_id(prefix: str, value, length: int = 24) -> str:
    return f'{prefix}_{content_hash(value)[:length]}'

def seal(value: dict, field: str = 'artifact_hash') -> dict:
    output = dict(value)
    output[field] = content_hash({key: item for key, item in output.items() if key != field})
    return output
