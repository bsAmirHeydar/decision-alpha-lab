from __future__ import annotations

def build_registries(packets: list[dict], pilot_handoff: dict) -> dict[str, list[dict]]:
    package, parity, variance, blockers = [], [], [], []
    for p in sorted(packets, key=lambda x: x["identity_id"]):
        migrated = p["final_disposition"] == "MIGRATED_CUTOVER_READY"
        package.append({"schema_version":"1.0.0","identity_id":p["identity_id"],"wave_assignment":p["wave_assignment"],"final_disposition":p["final_disposition"],"canonical_package_root":p["canonical_package_root"],"canonical_package_digest":pilot_handoff["canonical_package_digest"] if migrated else None,"packet_id":p["packet_id"],"packet_digest":p["packet_digest"],"cutover_ready":migrated,"consumer_cutover_performed":False})
        parity.append({"schema_version":"1.0.0","identity_id":p["identity_id"],"wave_assignment":p["wave_assignment"],"parity_state":p["hard_parity_state"],"hard_parity_passed":migrated,"mandatory_unknown_count":0 if migrated else None,"parity_digest":p["parity_digest"],"blocked_reason_count":len(p["blocker_reasons"])})
        variance.append({"schema_version":"1.0.0","identity_id":p["identity_id"],"variance_state":p["variance_state"],"accepted_variance_count":0,"unresolved_variance_count":0 if migrated else None,"variance_decision_digest":None})
        if p["blocker_reasons"]:
            blockers.append({"schema_version":"1.0.0","identity_id":p["identity_id"],"wave_assignment":p["wave_assignment"],"blocker_count":len(p["blocker_reasons"]),"blocker_reasons":p["blocker_reasons"],"owner_state":p["owner_state"]["human_assignee_status"],"characterization_packet_status":p["characterization_state"]["packet_status"],"blocking":True})
    return {"package_registry":package,"parity_registry":parity,"variance_registry":variance,"blocker_registry":blockers}
