from __future__ import annotations
import itertools
from copy import deepcopy
from typing import Any
from .errors import ContractError
from .schema_validation import validate_instance
from .search_authority import domain_values
from .policy_ir import build_policy_ir


def _replace(value: Any, assignment: dict[str, Any]) -> Any:
    if isinstance(value, dict): return {k:_replace(v, assignment) for k,v in value.items()}
    if isinstance(value, list): return [_replace(v, assignment) for v in value]
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        key=value[2:-1]
        if key not in assignment: raise ContractError(f"ACL04_AI_TEMPLATE_PARAMETER_UNBOUND:{key}")
        return assignment[key]
    return value


def generate_ai_setups(request: dict[str, Any], authority: dict[str, Any], *, context_id: str, context_version: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    validate_instance("ai_generation_request", request)
    if request["context_id"] != context_id or request["context_version"] != context_version:
        raise ContractError("ACL04_AI_REQUEST_CONTEXT_MISMATCH")
    if request["generator"] != "DETERMINISTIC_CARTESIAN_V1":
        raise ContractError("ACL04_AI_GENERATOR_NOT_REGISTERED")
    if request["generator"] not in authority.get("generator_allowlist", []):
        raise ContractError("ACL04_AI_GENERATOR_OUTSIDE_SEARCH_AUTHORITY")
    requested=request["requested_candidates"]
    if requested > authority["max_candidates"]:
        raise ContractError("ACL04_AI_CANDIDATE_BUDGET_EXCEEDED")
    names=request.get("vary_parameters", [])
    values=[domain_values(authority, n) for n in names]
    combinations=list(itertools.product(*values)) if names else [tuple()]
    combinations=combinations[:requested]
    compute_units=len(combinations) * max(1, len(request["template"].get("clauses", {})))
    if compute_units > authority["max_compute_units"]:
        raise ContractError("ACL04_AI_COMPUTE_BUDGET_EXCEEDED")
    outputs=[]
    for combo in combinations:
        assignment=dict(zip(names, combo))
        source=_replace(deepcopy(request["template"]), assignment)
        source["parameters"]={**source.get("parameters", {}), **assignment}
        source["treatment_family"]=request["treatment_family"]
        outputs.append(build_policy_ir(source, context_id=context_id, context_version=context_version, lane="AI"))
    exposure={
        "schema_version":"1.0.0",
        "request_id":request["request_id"],
        "generator":request["generator"],
        "seed":request["seed"],
        "requested_candidates":requested,
        "materialized_candidates":len(outputs),
        "compute_units":compute_units,
        "vary_parameters":names,
        "complete_enumeration":len(combinations) == min(requested, len(list(itertools.product(*values))) if names else 1),
    }
    return outputs, exposure
