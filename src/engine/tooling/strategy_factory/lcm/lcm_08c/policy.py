from __future__ import annotations
from typing import Any

MIGRATED = "MIGRATED_CUTOVER_READY"
BLOCKED = "BLOCKED"

def blocking_reasons(row: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if not row.get("source_exists", False): reasons.append("SOURCE_ARTIFACT_UNREACHABLE")
    if row.get("identity_collision", False): reasons.append("IDENTITY_COLLISION_UNRESOLVED")
    if row.get("identity_status") == "SECURITY_REVIEW_BLOCKED" or row.get("security_sensitive", False): reasons.append("SECURITY_REVIEW_REQUIRED")
    owner = row.get("owner_state", {})
    if owner.get("human_assignee_status") not in {"ASSIGNED", "RESOLVED", "APPROVED"}: reasons.append("HUMAN_SEMANTIC_OWNER_APPROVAL_MISSING")
    characterization = row.get("characterization_state", {})
    if not characterization.get("observed_behavior_captured", False): reasons.append("OBSERVED_BEHAVIOR_NOT_CAPTURED")
    if characterization.get("packet_status") not in {"ACCEPTED", "COMPLETE", "VERIFIED"}: reasons.append("CHARACTERIZATION_PACKET_NOT_ACCEPTED")
    if row.get("granularity_class") != "PACKAGE_CONTEXT": reasons.append("CANONICAL_CONTEXT_BOUNDARY_NOT_PROVEN")
    if row.get("risk_class") == "UNKNOWN": reasons.append("RISK_CLASS_UNKNOWN")
    if row.get("critical_dimensions"): reasons.append("CRITICAL_RISK_DIMENSION_REQUIRES_ADJUDICATION")
    if not row.get("target_materialized", False): reasons.append("CANONICAL_PACKAGE_NOT_MATERIALIZED")
    return sorted(set(reasons or ["MIGRATION_EVIDENCE_INCOMPLETE"]))
