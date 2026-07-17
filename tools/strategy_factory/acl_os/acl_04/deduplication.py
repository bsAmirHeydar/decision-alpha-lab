from __future__ import annotations
from collections import defaultdict
from typing import Any
from .canonical import digest_object


def deduplicate(candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups=defaultdict(list)
    for c in candidates: groups[c["behavior_digest"]].append(c)
    canonical=[]; records=[]
    lane_order={"HUMAN":0,"AI":1,"BASELINE":2}
    for behavior_digest, group in sorted(groups.items()):
        group.sort(key=lambda c:(lane_order.get(c["origin"],99), c["candidate_id"]))
        winner=group[0]
        if winner["status"] != "INVALID": canonical.append(winner)
        records.append({
            "behavior_digest":behavior_digest,
            "canonical_candidate_id":winner["candidate_id"],
            "member_candidate_ids":[c["candidate_id"] for c in group],
            "origins":sorted(set(c["origin"] for c in group)),
            "duplicate_count":max(0,len(group)-1),
        })
    body={"schema_version":"1.0.0","group_count":len(records),"input_count":len(candidates),"canonical_count":len(canonical),"groups":records}
    return canonical,{**body,"report_digest":digest_object(body)}
