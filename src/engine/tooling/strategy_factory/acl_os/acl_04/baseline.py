from __future__ import annotations
from typing import Any
from .policy_ir import build_policy_ir


def _clause(kind: str, action: str, atom_id: str="ALWAYS_TRUE", args: list[Any]|None=None) -> dict[str, Any]:
    return {"clause_id":f"{kind.upper()}_{action}","when":{"op":"ATOM","atom_id":atom_id,"args":args or []},"action":action,"priority":1}


def compile_baselines(context_id: str, context_version: str) -> list[tuple[str, dict[str, Any]]]:
    risk={"sizing_mode":"UNIT_RISK","max_risk_units":1.0,"protective_reference_required":True}
    specs=[
        ("BASELINE_NEVER_TRADE", {"treatment_family":"BASELINE_NEVER_TRADE","risk_contract":risk,"clauses":{"entry":[],"abstention":[_clause("abstention","ABSTAIN")]}}),
        ("BASELINE_ALWAYS_TAKE_LONG", {"treatment_family":"BASELINE_ALWAYS_TAKE_LONG","risk_contract":risk,"clauses":{"entry":[_clause("entry","ENTER_LONG")],"expiry":[_clause("expiry","CANCEL")]}}),
        ("BASELINE_ALWAYS_TAKE_SHORT", {"treatment_family":"BASELINE_ALWAYS_TAKE_SHORT","risk_contract":risk,"clauses":{"entry":[_clause("entry","ENTER_SHORT")],"expiry":[_clause("expiry","CANCEL")]}}),
        ("BASELINE_MANUAL_GATE", {"treatment_family":"BASELINE_MANUAL_GATE","risk_contract":risk,"clauses":{"entry":[_clause("entry","ENTER_LONG","MANUAL_CONFIRMATION_IS",[True])],"expiry":[_clause("expiry","CANCEL")]}}),
        ("BASELINE_DIAGNOSTIC_ORACLE", {"treatment_family":"BASELINE_DIAGNOSTIC_ORACLE","risk_contract":risk,"diagnostic_only":True,"clauses":{"entry":[_clause("entry","ENTER_LONG","FUTURE_OUTCOME_IS",["POSITIVE"])],"expiry":[_clause("expiry","CANCEL")]}}),
    ]
    return [(name, build_policy_ir(spec, context_id=context_id, context_version=context_version, lane="BASELINE")) for name,spec in specs]
