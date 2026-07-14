from __future__ import annotations
from dataclasses import dataclass,asdict
from typing import Mapping
from .canonical import stable_id,content_hash
@dataclass(frozen=True)
class DataFoundationTelemetry:
    operation:str; object_id:str; status:str; reason_code:str; metrics:Mapping[str,float]; evidence_hashes:tuple[str,...]
    @property
    def telemetry_id(self): return stable_id('tel',asdict(self))
    @property
    def telemetry_hash(self): return content_hash(asdict(self))
