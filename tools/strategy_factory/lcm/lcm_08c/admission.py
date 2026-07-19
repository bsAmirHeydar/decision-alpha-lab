from __future__ import annotations
from collections import defaultdict
from .canonical import digest_object

def build_wave_receipts(packets: list[dict], closure_id: str) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for packet in packets: groups[packet["wave_assignment"]].append(packet)
    receipts = []
    for wave_id in sorted(groups):
        members = sorted(groups[wave_id], key=lambda x: x["identity_id"])
        migrated = [x for x in members if x["final_disposition"] == "MIGRATED_CUTOVER_READY"]
        blocked = [x for x in members if x["final_disposition"] == "BLOCKED"]
        receipt = {
            "schema_version": "1.0.0", "phase_id": "LCM-08C", "closure_id": closure_id, "wave_id": wave_id,
            "member_count": len(members), "migrated_cutover_ready_count": len(migrated), "blocked_count": len(blocked),
            "all_members_accounted": len(members) == len(migrated) + len(blocked),
            "non_compensatory_gate_passed": all(x["hard_parity_state"] == "PASS" for x in migrated),
            "wave_closure_state": "CLOSED_WITH_MIGRATED_AND_EXPLICIT_BLOCKERS" if migrated else "CLOSED_WITH_EXPLICIT_BLOCKERS",
            "member_packet_digests": [x["packet_digest"] for x in members], "consumer_cutover_performed": False, "receipt_digest": None,
        }
        receipt["receipt_digest"] = digest_object(receipt, "receipt_digest")
        receipts.append(receipt)
    return receipts
