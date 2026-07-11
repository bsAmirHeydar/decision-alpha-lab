from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any
from .schema import SchemaIdentity
from .time import MarketTimestamp

class ContractJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.name if hasattr(obj, "name") else obj.value
        if isinstance(obj, SchemaIdentity):
            return {"namespace": obj.schema_namespace, "name": obj.schema_name,
                    "major": obj.major, "minor": obj.minor, "patch": obj.patch}
        if isinstance(obj, MarketTimestamp):
            return {"utc_epoch_milliseconds": obj.utc_epoch_milliseconds,
                    "source_timezone_id": obj.source_timezone_id,
                    "source_utc_offset_minutes": obj.source_utc_offset_minutes,
                    "source_clock_id": obj.source_clock_id,
                    "precision": int(obj.precision)}
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)

def canonical_json(value: Any) -> str:
    return json.dumps(value, cls=ContractJSONEncoder, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def jsonl_line(value: Any) -> str:
    return canonical_json(value) + "\n"
