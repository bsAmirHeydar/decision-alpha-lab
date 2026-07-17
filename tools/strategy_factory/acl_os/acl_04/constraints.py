from __future__ import annotations
from typing import Any
from .atom_registry import atom_map
from .expressions import walk_atoms, expression_depth


def evaluate_policy(ir: dict[str, Any], registry: dict[str, Any], authority: dict[str, Any], envelope: dict[str, Any]) -> list[dict[str, Any]]:
    findings=[]; amap=atom_map(registry)
    allowed_atoms=set(authority["allowed_atoms"]); allowed_actions=set(authority["allowed_actions"])
    envelope_actions=set(envelope["allowed_actions"]); lane=ir["lane"]
    allowed_treatments=set(envelope["allowed_treatment_families"])
    atom_count=0; entry_actions=[]
    clause_kinds={clause["kind"] for clause in ir["clauses"]}
    if ir["treatment_family"] not in allowed_treatments:
        findings.append({"code":"ACL04_TREATMENT_FAMILY_FORBIDDEN","severity":"BLOCKER","path":"treatment_family","details":{"treatment_family":ir["treatment_family"]}})
    for required_kind in envelope.get("required_clause_kinds", []):
        if required_kind not in clause_kinds and lane != "BASELINE" and not ir.get("diagnostic_only"):
            findings.append({"code":"ACL04_REQUIRED_CLAUSE_KIND_MISSING","severity":"BLOCKER","path":"clauses","details":{"required_kind":required_kind}})
    for clause in ir["clauses"]:
        action=clause["action"]
        if action not in allowed_actions or action not in envelope_actions:
            findings.append({"code":"ACL04_ACTION_OUTSIDE_AUTHORITY","severity":"BLOCKER","path":clause["clause_id"],"details":{"action":action}})
        if clause["kind"] == "ENTRY": entry_actions.append(action)
        depth=expression_depth(clause["when"])
        if depth > authority["max_expression_depth"]:
            findings.append({"code":"ACL04_EXPRESSION_DEPTH_EXCEEDED","severity":"BLOCKER","path":clause["clause_id"],"details":{"depth":depth}})
        for atom in walk_atoms(clause["when"]):
            atom_count += 1; atom_id=atom["atom_id"]; definition=amap.get(atom_id)
            if definition is None:
                findings.append({"code":"ACL04_UNKNOWN_ATOM","severity":"BLOCKER","path":clause["clause_id"],"details":{"atom_id":atom_id}}); continue
            if atom_id not in allowed_atoms and not (lane=="BASELINE" and atom_id in {"ALWAYS_TRUE","MANUAL_CONFIRMATION_IS","FUTURE_OUTCOME_IS"}):
                findings.append({"code":"ACL04_ATOM_OUTSIDE_SEARCH_AUTHORITY","severity":"BLOCKER","path":clause["clause_id"],"details":{"atom_id":atom_id}})
            if lane not in definition["allowed_lanes"]:
                findings.append({"code":"ACL04_ATOM_LANE_FORBIDDEN","severity":"BLOCKER","path":clause["clause_id"],"details":{"atom_id":atom_id,"lane":lane}})
            if len(atom.get("args",[])) != definition["arity"]:
                findings.append({"code":"ACL04_ATOM_ARITY_MISMATCH","severity":"BLOCKER","path":clause["clause_id"],"details":{"atom_id":atom_id}})
            if not definition["known_time_safe"] and not ir.get("diagnostic_only"):
                findings.append({"code":"ACL04_FUTURE_DERIVED_ATOM_FORBIDDEN","severity":"BLOCKER","path":clause["clause_id"],"details":{"atom_id":atom_id}})
    if atom_count > authority["max_atoms_per_candidate"]:
        findings.append({"code":"ACL04_ATOM_BUDGET_EXCEEDED","severity":"BLOCKER","path":"clauses","details":{"atom_count":atom_count}})
    if "ENTER_LONG" in entry_actions and "ENTER_SHORT" in entry_actions:
        findings.append({"code":"ACL04_CONFLICTING_ENTRY_DIRECTIONS","severity":"BLOCKER","path":"clauses.entry","details":{}})
    risk=ir["risk_contract"]
    if risk["max_risk_units"] > envelope["max_risk_units"]:
        findings.append({"code":"ACL04_RISK_OUTSIDE_TREATMENT_ENVELOPE","severity":"BLOCKER","path":"risk_contract.max_risk_units","details":{}})
    if risk["sizing_mode"] not in envelope["allowed_sizing_modes"]:
        findings.append({"code":"ACL04_SIZING_MODE_FORBIDDEN","severity":"BLOCKER","path":"risk_contract.sizing_mode","details":{}})
    if envelope.get("protective_reference_required") and not risk.get("protective_reference_required"):
        findings.append({"code":"ACL04_PROTECTIVE_REFERENCE_REQUIRED","severity":"BLOCKER","path":"risk_contract.protective_reference_required","details":{}})
    if not ir.get("diagnostic_only") and lane != "BASELINE" and not any(c["kind"]=="EXPIRY" for c in ir["clauses"]):
        findings.append({"code":"ACL04_EXPIRY_CONTRACT_REQUIRED","severity":"BLOCKER","path":"clauses.expiry","details":{}})
    return findings
