from __future__ import annotations
from typing import Any
from .errors import ContractError

COMMUTATIVE = {"ALL", "ANY"}


def normalize_expression(expr: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(expr, dict):
        raise ContractError("ACL04_EXPRESSION_NOT_OBJECT")
    op = expr.get("op")
    if op in {"ALL", "ANY"}:
        children = [normalize_expression(x) for x in expr.get("children", [])]
        if not children:
            raise ContractError("ACL04_EMPTY_BOOLEAN_EXPRESSION")
        children.sort(key=lambda x: repr(x))
        return {"op": op, "children": children}
    if op == "NOT":
        return {"op": "NOT", "child": normalize_expression(expr.get("child"))}
    if op == "ATOM":
        args = expr.get("args", [])
        if not isinstance(args, list):
            raise ContractError("ACL04_ATOM_ARGS_NOT_LIST")
        return {"op":"ATOM","atom_id":expr.get("atom_id"),"args":args}
    raise ContractError(f"ACL04_UNKNOWN_EXPRESSION_OPERATOR:{op}")


def walk_atoms(expr: dict[str, Any]) -> list[dict[str, Any]]:
    op = expr["op"]
    if op == "ATOM": return [expr]
    if op in {"ALL", "ANY"}:
        out=[]
        for child in expr["children"]: out.extend(walk_atoms(child))
        return out
    if op == "NOT": return walk_atoms(expr["child"])
    return []


def expression_depth(expr: dict[str, Any]) -> int:
    if expr["op"] == "ATOM": return 1
    if expr["op"] == "NOT": return 1 + expression_depth(expr["child"])
    return 1 + max(expression_depth(c) for c in expr["children"])
