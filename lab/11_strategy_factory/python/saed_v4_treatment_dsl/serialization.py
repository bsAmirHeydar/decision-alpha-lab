from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .models import CanonicalComponent, CanonicalTreatmentProgram, DescriptorBinding, TreatmentDslPackage


def to_document(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, CanonicalComponent):
        return value.semantic_payload() | {"component_hash": value.component_hash}
    if isinstance(value, CanonicalTreatmentProgram):
        return value.semantic_payload() | {"program_hash": value.program_hash}
    if isinstance(value, DescriptorBinding):
        return value.semantic_payload() | {"binding_hash": value.binding_hash}
    if isinstance(value, TreatmentDslPackage):
        return value.semantic_payload() | {"package_hash": value.package_hash}
    if is_dataclass(value):
        return {field.name: to_document(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, dict):
        return {str(key): to_document(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_document(item) for item in value]
    if isinstance(value, set):
        return sorted(to_document(item) for item in value)
    return value


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(to_document(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
