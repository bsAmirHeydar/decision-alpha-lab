from __future__ import annotations
from typing import Any
from .errors import ContractError
from .schema_validation import validate_instance
from .policy_ir import build_policy_ir


def compile_human_setup(document: dict[str, Any], *, context_id: str, context_version: str) -> dict[str, Any]:
    validate_instance("human_setup_dsl", document)
    if document["context_id"] != context_id or document["context_version"] != context_version:
        raise ContractError("ACL04_HUMAN_DSL_CONTEXT_MISMATCH")
    if document.get("lane") != "HUMAN":
        raise ContractError("ACL04_HUMAN_DSL_LANE_INVALID")
    return build_policy_ir(document, context_id=context_id, context_version=context_version, lane="HUMAN")
