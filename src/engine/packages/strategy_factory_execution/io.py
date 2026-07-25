from __future__ import annotations
from dataclasses import asdict, is_dataclass
from enum import IntEnum
import json

def _convert(value):
    if isinstance(value, IntEnum): return int(value)
    if is_dataclass(value): return {k:_convert(v) for k,v in asdict(value).items()}
    if isinstance(value, dict): return {k:_convert(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [_convert(v) for v in value]
    return value

def write_json(path, value) -> None:
    with open(path,"w",encoding="utf-8",newline="\n") as handle:
        json.dump(_convert(value),handle,indent=2,sort_keys=True)
        handle.write("\n")
