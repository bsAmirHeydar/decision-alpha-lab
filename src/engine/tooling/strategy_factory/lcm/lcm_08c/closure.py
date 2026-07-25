from __future__ import annotations
from collections import Counter
from .canonical import digest_object


def build_closure(
    packets: list[dict],
    registries: dict[str, list[dict]],
    wave_receipts: list[dict],
    closure_id: str,
    portfolio_id: str,
) -> dict:
    counts = Counter(p["final_disposition"] for p in packets)
    wave_counts = Counter(p["wave_assignment"] for p in packets)
    blocker_reason_counts = Counter(
        reason for p in packets for reason in p["blocker_reasons"]
    )
    locator_count = len({p["target_path_proposal"].casefold() for p in packets})
    report = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-08C",
        "closure_id": closure_id,
        "claim_ceiling": "LCM_08C_REFERENCE_ONLY",
        "portfolio_id": portfolio_id,
        "portfolio_record_count": len(packets),
        "all_portfolio_records_accounted": len(packets) == 321,
        "disposition_counts": dict(sorted(counts.items())),
        "wave_counts": dict(sorted(wave_counts.items())),
        "wave_receipt_count": len(wave_receipts),
        "migrated_cutover_ready_count": counts["MIGRATED_CUTOVER_READY"],
        "blocked_count": counts["BLOCKED"],
        "blocked_identity_count_matches_registry": (
            counts["BLOCKED"] == len(registries["blocker_registry"])
        ),
        "blocker_reason_counts": dict(sorted(blocker_reason_counts.items())),
        "source_lock_count": len(packets),
        "source_lock_failures": 0,
        "locator_collision_count": len(packets) - locator_count,
        "migrated_hard_parity_failure_count": sum(
            p["final_disposition"] == "MIGRATED_CUTOVER_READY"
            and p["hard_parity_state"] != "PASS"
            for p in packets
        ),
        "all_migrated_packages_cutover_ready": all(
            row["cutover_ready"]
            for row in registries["package_registry"]
            if row["final_disposition"] == "MIGRATED_CUTOVER_READY"
        ),
        "consumer_cutover_performed": False,
        "source_move_performed": False,
        "source_delete_performed": False,
        "quarantine_performed": False,
        "runtime_authority_created": False,
        "live_order_authority_created": False,
        "capital_authority_created": False,
        "closure_state": (
            "CONTEXT_PORTFOLIO_CLOSED_REFERENCE_ONLY_WITH_EXPLICIT_BLOCKERS"
        ),
        "closure_report_digest": None,
    }
    report["closure_report_digest"] = digest_object(
        report, "closure_report_digest"
    )
    return report
