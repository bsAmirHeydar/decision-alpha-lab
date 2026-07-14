from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from .canonical import content_hash
@dataclass(frozen=True)
class ConformanceResult:
    vector_id:str; passed:bool; observed:Mapping[str,Any]; result_hash:str
def result(vector_id:str,passed:bool,observed:Mapping[str,Any])->ConformanceResult:
    p={'vector_id':vector_id,'passed':passed,'observed':dict(observed)}; return ConformanceResult(vector_id,passed,dict(observed),content_hash(p))
