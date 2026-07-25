from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .errors import ContractError
from .schema_validation import validate_instance

DEFAULT_ATOMS: list[dict[str, Any]] = [
    {"atom_id":"ALWAYS_TRUE","kind":"PREDICATE","arity":0,"known_time_safe":True,"allowed_lanes":["HUMAN","AI","BASELINE"]},
    {"atom_id":"CONTEXT_STATE_IS","kind":"PREDICATE","arity":1,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"FEATURE_COMPARE","kind":"PREDICATE","arity":3,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"ELAPSED_BARS_COMPARE","kind":"PREDICATE","arity":2,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"SESSION_PHASE_IS","kind":"PREDICATE","arity":1,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"OCCURRENCE_AGE_COMPARE","kind":"PREDICATE","arity":2,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"MISSINGNESS_IS_CLEAR","kind":"PREDICATE","arity":1,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"FRESHNESS_WITHIN","kind":"PREDICATE","arity":2,"known_time_safe":True,"allowed_lanes":["HUMAN","AI"]},
    {"atom_id":"MANUAL_CONFIRMATION_IS","kind":"PREDICATE","arity":1,"known_time_safe":True,"allowed_lanes":["HUMAN","BASELINE"]},
    {"atom_id":"FUTURE_OUTCOME_IS","kind":"DIAGNOSTIC_PREDICATE","arity":1,"known_time_safe":False,"allowed_lanes":["BASELINE"]},
]
DEFAULT_ACTIONS = ["ENTER_LONG","ENTER_SHORT","ABSTAIN","CANCEL","EXIT_FULL","REDUCE","MOVE_PROTECTIVE_REFERENCE","NO_ACTION"]


def build_default_registry() -> dict[str, Any]:
    body = {"schema_version":"1.0.0","registry_id":"ACL04_SETUP_ATOMS_V1","atoms":DEFAULT_ATOMS,"actions":DEFAULT_ACTIONS}
    return {**body, "registry_digest": digest_object(body)}


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    validate_instance("atom_registry", registry)
    expected = digest_object({k:v for k,v in registry.items() if k != "registry_digest"})
    if registry.get("registry_digest") != expected:
        raise ContractError("ACL04_ATOM_REGISTRY_DIGEST_MISMATCH")
    ids = [a["atom_id"] for a in registry["atoms"]]
    if len(ids) != len(set(ids)):
        raise ContractError("ACL04_DUPLICATE_ATOM_ID")
    return registry


def atom_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {a["atom_id"]: a for a in registry["atoms"]}
