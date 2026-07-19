from __future__ import annotations

import re

from .canonical import digest_object
from .path_policy import validate
from .registries import STATE_TRANSITIONS

REQUIRED = (
    "schema_version",
    "packet_id",
    "packet_digest",
    "identity_id",
    "identity_kind",
    "identity_resolution_status",
    "source_artifact_path",
    "source_artifact_sha256",
    "owner_role",
    "owner_status",
    "current_state",
    "proposed_state",
    "target_path",
    "target_outcome",
    "claim_ceiling",
    "known_time_status",
    "security_sensitive",
    "security_review_status",
    "evidence_refs",
)
AUTHORITY_FIELDS = (
    "source_move_authorized",
    "source_delete_authorized",
    "target_materialization_authorized",
    "semantic_refactor_authorized",
    "merge_authorized",
    "cutover_authorized",
    "runtime_authorized",
    "live_order_authorized",
    "capital_authorized",
)
IDENTITY_KINDS = {"CONTEXT", "SETUP", "TREATMENT", "VISUALIZER", "SHARED_ENGINE", "PLATFORM_ADAPTER", "EXECUTION_ADAPTER"}
KNOWN_TIME_STATUSES = {"SAFE", "FUTURE_AWARE", "UNKNOWN"}
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def validate_packet(packet, source_hash_lookup=None):
    reasons: list[str] = []
    missing = [key for key in (*REQUIRED, *AUTHORITY_FIELDS) if key not in packet]
    if missing:
        reasons.append("PACKET_FIELDS_MISSING")

    try:
        validate(packet.get("source_artifact_path", ""))
        validate(packet.get("target_path", ""))
    except Exception:
        reasons.append("UNSAFE_PATH")

    packet_digest = packet.get("packet_digest")
    if not isinstance(packet_digest, str) or digest_object(packet, "packet_digest") != packet_digest:
        reasons.append("PACKET_DIGEST_INVALID")

    if packet.get("identity_kind") not in IDENTITY_KINDS:
        reasons.append("IDENTITY_KIND_UNKNOWN")
    if packet.get("owner_status") not in ("ROLE_BOUND", "HUMAN_APPROVED"):
        reasons.append("OWNER_MISSING")
    if not isinstance(packet.get("owner_role"), str) or not packet.get("owner_role"):
        reasons.append("OWNER_ROLE_MISSING")

    current, target = packet.get("current_state"), packet.get("proposed_state")
    if target not in STATE_TRANSITIONS.get(current, set()):
        reasons.append("INVALID_STATE_TRANSITION")

    resolution_status = packet.get("identity_resolution_status")
    if resolution_status == "AMBIGUOUS":
        reasons.append("IDENTITY_AMBIGUOUS")
    elif resolution_status not in ("RESOLVED", "AMBIGUOUS"):
        reasons.append("IDENTITY_RESOLUTION_UNKNOWN")

    known_time_status = packet.get("known_time_status")
    if known_time_status == "FUTURE_AWARE":
        reasons.append("FUTURE_AWARE_EVIDENCE_BLOCKED")
    elif known_time_status not in KNOWN_TIME_STATUSES or known_time_status == "UNKNOWN":
        reasons.append("KNOWN_TIME_EVIDENCE_UNKNOWN")

    if packet.get("security_sensitive") is True and packet.get("security_review_status") != "APPROVED":
        reasons.append("SECURITY_REVIEW_REQUIRED")
    if packet.get("security_sensitive") is not True and packet.get("security_review_status") not in ("NOT_REQUIRED", "APPROVED"):
        reasons.append("SECURITY_REVIEW_STATUS_INVALID")

    source_path = packet.get("source_artifact_path")
    source_sha = packet.get("source_artifact_sha256")
    if not isinstance(source_sha, str) or not SHA256_RE.fullmatch(source_sha):
        reasons.append("SOURCE_HASH_FORMAT_INVALID")
    if source_hash_lookup is not None:
        if source_path not in source_hash_lookup:
            reasons.append("SOURCE_NOT_IN_TOPOLOGY")
        elif source_hash_lookup[source_path] != source_sha:
            reasons.append("SOURCE_HASH_MISMATCH")

    evidence_refs = packet.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs or any(not isinstance(x, str) or not x for x in evidence_refs):
        reasons.append("EVIDENCE_REFERENCES_INCOMPLETE")

    if any(packet.get(key) is not False for key in AUTHORITY_FIELDS):
        reasons.append("AUTHORITY_ESCALATION")
    if packet.get("claim_ceiling") != "MIGRATION_FRAMEWORK_REFERENCE_ONLY":
        reasons.append("CLAIM_CEILING_EXCEEDED")

    status = "VALID_REFERENCE"
    if "IDENTITY_AMBIGUOUS" in reasons:
        status = "BLOCKED_AMBIGUITY"
    elif any(code in reasons for code in ("OWNER_MISSING", "OWNER_ROLE_MISSING", "FUTURE_AWARE_EVIDENCE_BLOCKED", "KNOWN_TIME_EVIDENCE_UNKNOWN")):
        status = "BLOCKED_UNKNOWN"
    elif "SECURITY_REVIEW_REQUIRED" in reasons:
        status = "BLOCKED_SECURITY_REVIEW"
    elif reasons:
        status = "INVALID"

    result = {
        "schema_version": "1.0.0",
        "packet_id": packet.get("packet_id"),
        "validation_status": status,
        "valid": status == "VALID_REFERENCE",
        "reason_codes": sorted(set(reasons or ["PACKET_VALID"])),
        "source_mutation_performed": False,
        "authority_created": False,
        "validation_digest": None,
    }
    result["validation_digest"] = digest_object(result, "validation_digest")
    return result
