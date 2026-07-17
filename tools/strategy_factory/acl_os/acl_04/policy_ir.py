from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .expressions import normalize_expression
from .schema_validation import validate_instance

CLAUSE_ORDER = ["entry", "invalidation", "exit", "management", "expiry", "abstention"]


def build_policy_ir(source: dict[str, Any], *, context_id: str, context_version: str, lane: str) -> dict[str, Any]:
    clauses=[]
    for kind in CLAUSE_ORDER:
        for i, clause in enumerate(source.get("clauses", {}).get(kind, [])):
            clauses.append({
                "clause_id": clause.get("clause_id") or f"{kind.upper()}_{i+1:03d}",
                "kind": kind.upper(),
                "when": normalize_expression(clause["when"]),
                "action": clause["action"],
                "action_parameters": clause.get("action_parameters", {}),
                "priority": int(clause.get("priority", 100)),
            })
    clauses.sort(key=lambda x: (CLAUSE_ORDER.index(x["kind"].lower()), x["priority"], x["clause_id"]))
    body={
        "schema_version":"1.0.0",
        "ir_type":"ACL04_SETUP_POLICY_IR",
        "context_id":context_id,
        "context_version":context_version,
        "lane":lane,
        "treatment_family":source["treatment_family"],
        "parameters":source.get("parameters", {}),
        "risk_contract":source["risk_contract"],
        "clauses":clauses,
        "diagnostic_only":bool(source.get("diagnostic_only", False)),
        "known_time_contract":"INHERIT_ACL03_NON_BYPASSABLE",
        "execution_authority":"NONE",
    }
    ir={**body,"policy_ir_digest":digest_object(body)}
    validate_instance("setup_policy_ir", ir)
    return ir
