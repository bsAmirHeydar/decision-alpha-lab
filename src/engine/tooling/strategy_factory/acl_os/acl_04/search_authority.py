from __future__ import annotations
from typing import Any
from .canonical import verify_embedded_digest
from .errors import AuthorityError, ContractError
from .schema_validation import validate_instance


def validate_search_authority(authority: dict[str, Any], handoff: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    validate_instance("search_authority", authority)
    failures=[]
    if not verify_embedded_digest(authority, "authority_digest"): failures.append("ACL04_SEARCH_AUTHORITY_DIGEST_MISMATCH")
    if authority.get("decision") != "ALLOW": failures.append("ACL04_SEARCH_AUTHORITY_DENIED")
    if authority.get("context_id") != handoff.get("context_id") or authority.get("context_version") != handoff.get("context_version"):
        failures.append("ACL04_SEARCH_AUTHORITY_CONTEXT_MISMATCH")
    if authority.get("upstream_handoff_digest") != handoff.get("handoff_digest"):
        failures.append("ACL04_SEARCH_AUTHORITY_HANDOFF_MISMATCH")
    known_atoms={a["atom_id"] for a in registry["atoms"]}; known_actions=set(registry["actions"])
    if not set(authority.get("allowed_atoms", [])).issubset(known_atoms): failures.append("ACL04_SEARCH_AUTHORITY_UNKNOWN_ATOM")
    if not set(authority.get("allowed_actions", [])).issubset(known_actions): failures.append("ACL04_SEARCH_AUTHORITY_UNKNOWN_ACTION")
    if authority.get("max_candidates", 0) < 1 or authority.get("max_compute_units", 0) < 1:
        failures.append("ACL04_SEARCH_BUDGET_INVALID")
    if authority.get("live_order_submission_allowed") is not False or authority.get("capital_activation_allowed") is not False:
        failures.append("ACL04_SEARCH_AUTHORITY_ILLEGAL_EXECUTION_SCOPE")
    if failures: raise AuthorityError(",".join(failures))
    return authority


def domain_values(authority: dict[str, Any], name: str) -> list[Any]:
    domains=authority.get("parameter_domains", {})
    if name not in domains: raise ContractError(f"ACL04_PARAMETER_DOMAIN_UNDECLARED:{name}")
    values=domains[name]
    if not isinstance(values, list) or not values: raise ContractError(f"ACL04_PARAMETER_DOMAIN_EMPTY:{name}")
    return values
