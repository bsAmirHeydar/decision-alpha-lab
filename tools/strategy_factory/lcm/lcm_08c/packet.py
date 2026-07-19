from __future__ import annotations
from .canonical import content_id, digest_object
from .policy import blocking_reasons

PILOT_ID = "CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1"
CLAIM = "LCM_08C_REFERENCE_ONLY"

def build_packet(row: dict, closure_id: str, pilot_handoff: dict) -> dict:
    identity = row["identity_id"]
    migrated = identity == PILOT_ID
    blockers = [] if migrated else blocking_reasons(row)
    disposition = "MIGRATED_CUTOVER_READY" if migrated else "BLOCKED"
    seed = {"identity_id": identity, "source_sha256": row["source_artifact_sha256"], "wave_assignment": row["wave_assignment"], "disposition": disposition, "blockers": blockers}
    packet = {
        "schema_version": "1.0.0", "phase_id": "LCM-08C", "claim_ceiling": CLAIM, "closure_id": closure_id,
        "packet_id": content_id("CTXMIGPACKET", seed), "identity_id": identity, "identity_status": row["identity_status"],
        "identity_digest": row["identity_digest"], "source_artifact_path": row["source_artifact_path"],
        "source_artifact_sha256": row["source_artifact_sha256"], "source_language": row["source_language"],
        "family_candidate": row["family_candidate"], "granularity_class": row["granularity_class"], "risk_class": row["risk_class"],
        "aggregate_risk_score": row["aggregate_risk_score"], "critical_dimensions": row["critical_dimensions"],
        "wave_assignment": row["wave_assignment"], "owner_state": row["owner_state"], "characterization_state": row["characterization_state"],
        "shared_engine_candidate_ids": row["shared_engine_candidate_ids"], "target_path_proposal": row["target_path_proposal"],
        "canonical_package_root": pilot_handoff["canonical_package_root"] if migrated else None,
        "admission_state": "ACCEPTED_MIGRATED_REFERENCE_ONLY" if migrated else "ADMITTED_WITH_EXPLICIT_BLOCKERS",
        "final_disposition": disposition, "blocker_reasons": blockers, "hard_parity_state": "PASS" if migrated else "NOT_EXECUTED_BLOCKED",
        "parity_digest": pilot_handoff["parity_digest"] if migrated else None, "variance_state": "NO_VARIANCE" if migrated else "NOT_EVALUATED_BLOCKED",
        "consumer_cutover_performed": False, "source_move_performed": False, "source_delete_performed": False,
        "semantic_refactor_performed": False, "runtime_authority_created": False, "live_order_authority_created": False,
        "capital_authority_created": False, "packet_digest": None,
    }
    packet["packet_digest"] = digest_object(packet, "packet_digest")
    return packet
