"""Load and validate UC-02 machine-readable contracts."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

from .constants import CONTRACT_ROOT, POLICY_ROOT, SCHEMA_ROOT, STATIC_CONTRACT_FILES, STATIC_POLICY_FILES
from .io_utils import sha256_file


def _load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"YAML root is not a mapping: {path}")
    return value


def load_contracts(repo_root: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for relative in (*STATIC_POLICY_FILES, *STATIC_CONTRACT_FILES):
        path = repo_root / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        result[relative.as_posix()] = _load_yaml(path)
    return result


def validate_contracts(repo_root: Path) -> dict:
    errors: list[str] = []
    contracts: dict[str, dict] = {}
    try:
        contracts = load_contracts(repo_root)
    except Exception as exc:
        return {"status": "FAILED", "errors": [f"contract load failure: {type(exc).__name__}: {exc}"]}

    policy_schema_path = repo_root / SCHEMA_ROOT / "policy_contract.schema.json"
    schema = json.loads(policy_schema_path.read_text(encoding="utf-8"))
    for relative, value in contracts.items():
        try:
            jsonschema.validate(value, schema)
        except Exception as exc:
            errors.append(f"contract schema failure {relative}: {exc}")
        for flag in ("destructive_authority", "runtime_authority", "order_authority", "broker_authority", "capital_authority"):
            if value.get(flag) is not False:
                errors.append(f"forbidden authority flag {relative}:{flag}={value.get(flag)!r}")

    constitution = contracts.get((POLICY_ROOT / "architecture_constitution.yaml").as_posix(), {})
    if constitution.get("product_name") != "Alpha Lab":
        errors.append("product name must remain Alpha Lab")
    if constitution.get("canonical_production_root") != "src/engine":
        errors.append("canonical production root must be src/engine")
    ownership = contracts.get((CONTRACT_ROOT / "capability_ownership.yaml").as_posix(), {})
    if ownership.get("ownership_cardinality") != "exactly_one_canonical_owner":
        errors.append("capability ownership must be exactly one")

    system_disposition = contracts.get((CONTRACT_ROOT / "system_disposition.yaml").as_posix(), {})
    required_systems = {"STRATEGY_FACTORY", "ACL_OS", "UCEE", "SAED_V3", "SAED_V4", "AIEOS", "LCM", "RTHP", "NDS", "EXPERIMENTS"}
    actual_systems = set(system_disposition.get("systems", {}))
    if actual_systems != required_systems:
        errors.append(f"system disposition set mismatch: missing={sorted(required_systems-actual_systems)} extra={sorted(actual_systems-required_systems)}")

    digests = {relative: sha256_file(repo_root / relative) for relative in sorted(contracts)}
    return {"status": "PASS" if not errors else "FAILED", "errors": errors, "contract_count": len(contracts), "digests": digests}
