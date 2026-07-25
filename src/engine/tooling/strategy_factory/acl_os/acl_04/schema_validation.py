from __future__ import annotations
from functools import lru_cache
from typing import Any
from jsonschema import Draft202012Validator
from .policies import SCHEMA_ROOT
from .io import load_json
from .errors import ContractError


@lru_cache(maxsize=64)
def _validator(name: str) -> Draft202012Validator:
    schema_path = SCHEMA_ROOT / f"{name}.schema.json"
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_instance(name: str, value: Any) -> None:
    errors = sorted(_validator(name).iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, e.absolute_path)) or '$'}: {e.message}"
            for e in errors[:12]
        )
        raise ContractError(f"{name} schema validation failed: {details}")
