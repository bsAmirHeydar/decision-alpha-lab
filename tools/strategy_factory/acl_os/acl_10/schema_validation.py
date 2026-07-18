from __future__ import annotations
import json
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker
from .errors import ContractError
from .policies import SCHEMA_ROOT
def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_ROOT/f'{name}.schema.json'
    if not path.is_file(): raise ContractError(f'schema not registered: {name}')
    return json.loads(path.read_text(encoding='utf-8'))
def validate_instance(name: str, instance: Any) -> None:
    schema = load_schema(name)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance), key=lambda e:list(e.absolute_path))
    if errors:
        detail = '; '.join(f"/{'/'.join(map(str,e.absolute_path))}: {e.message}" for e in errors[:8])
        raise ContractError(f'{name} schema rejected: {detail}')
