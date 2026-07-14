"""Closed-contract loading and validation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from .errors import ContractError


def load_document(path: str | Path) -> Any:
    p = Path(path)
    if p.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    if p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    raise ContractError(f"unsupported document extension: {p.suffix}")


def load_schema(path: str | Path) -> Mapping[str, Any]:
    value = load_document(path)
    if not isinstance(value, Mapping):
        raise ContractError("schema root must be an object")
    return value


def validate_closed(document: Any, schema: Mapping[str, Any]) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path))
    if errors:
        fragments = []
        for error in errors[:20]:
            path = ".".join(str(x) for x in error.absolute_path) or "$"
            fragments.append(f"{path}: {error.message}")
        raise ContractError("; ".join(fragments))


def require_keys(value: Mapping[str, Any], required: set[str], allowed: set[str], name: str) -> None:
    unknown = set(value) - allowed
    missing = required - set(value)
    if unknown:
        raise ContractError(f"{name} contains unknown fields: {sorted(unknown)}")
    if missing:
        raise ContractError(f"{name} is missing required fields: {sorted(missing)}")
