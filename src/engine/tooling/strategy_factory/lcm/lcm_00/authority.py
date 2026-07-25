from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from .canonical import digest_object
from .errors import AuthorityError, ContractViolation

ALLOWED_ACTION = "LCM00_FREEZE_REFERENCE_BASELINE"
FORBIDDEN_CAPABILITIES = (
    "move_source_files_allowed",
    "delete_source_files_allowed",
    "semantic_refactor_allowed",
    "cutover_allowed",
    "runtime_generation_allowed",
    "live_order_submission_allowed",
    "capital_activation_allowed",
    "production_key_access_allowed",
    "network_access_allowed",
    "secret_access_allowed",
)

ROLE_CONFLICTS = {
    "PROGRAM_OWNER": {"INDEPENDENT_PARITY_REVIEWER"},
    "MIGRATION_ENGINEER": {"INDEPENDENT_PARITY_REVIEWER", "RELEASE_OPERATOR"},
    "DOMAIN_OWNER": {"INDEPENDENT_PARITY_REVIEWER"},
    "SECURITY_REVIEWER": {"PRODUCTION_KEY_CUSTODIAN"},
    "RELEASE_OPERATOR": {"MIGRATION_ENGINEER"},
}


def build_reference_permit(source_digest: str, issued_at: str) -> dict:
    value = {
        "schema_version": "1.0.0",
        "permit_id": "PERMIT_LCM00_REFERENCE_FREEZE_V1",
        "phase_id": "LCM-00",
        "action": ALLOWED_ACTION,
        "issuer": "ALPHA_LAB_REFERENCE_ARCHITECTURE_AUTHORITY",
        "issued_at": issued_at,
        "expires_at": "2099-12-31T23:59:59Z",
        "source_program_digest": source_digest,
        "reference_only": True,
        "human_approval_claimed": False,
        "capabilities": {key: False for key in FORBIDDEN_CAPABILITIES},
        "permit_digest": "",
    }
    value["permit_digest"] = digest_object(value, "permit_digest")
    return value


def validate_permit(permit: dict) -> None:
    if permit.get("phase_id") != "LCM-00" or permit.get("action") != ALLOWED_ACTION:
        raise AuthorityError("permit phase/action mismatch")
    caps = permit.get("capabilities") or {}
    for key in FORBIDDEN_CAPABILITIES:
        if caps.get(key) is not False:
            raise AuthorityError(f"forbidden capability must be false: {key}")
    expected = digest_object(permit, "permit_digest")
    if permit.get("permit_digest") != expected:
        raise AuthorityError("permit digest mismatch")


def validate_ownership_registry(registry: dict) -> dict:
    assignments = registry.get("assignments") or []
    by_identity: dict[str, set[str]] = {}
    missing_required: list[str] = []
    for item in assignments:
        role = item["role"]
        identity = item.get("assignee_id")
        status = item.get("assignment_status")
        if status != "ASSIGNED" or not identity:
            if item.get("required_for_lcm01", False):
                missing_required.append(role)
            continue
        by_identity.setdefault(identity, set()).add(role)
    conflicts: list[dict] = []
    for identity, roles in sorted(by_identity.items()):
        seen_pairs: set[tuple[str, str]] = set()
        for role in sorted(roles):
            for conflict in sorted(ROLE_CONFLICTS.get(role, set())):
                if conflict not in roles:
                    continue
                role_a, role_b = sorted((role, conflict))
                pair = (role_a, role_b)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                conflicts.append({"assignee_id": identity, "role_a": role_a, "role_b": role_b})
    return {
        "schema_version": "1.0.0",
        "registry_id": registry.get("registry_id"),
        "missing_required_roles": sorted(set(missing_required)),
        "conflicts": conflicts,
        "lcm01_ownership_ready": not missing_required and not conflicts,
        "destructive_action_ownership_ready": False,
        "report_digest": "",
    }
