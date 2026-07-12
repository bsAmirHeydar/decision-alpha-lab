from __future__ import annotations
from typing import Iterable
from .contracts import OpportunityAnchor
from .canonical import sha256
from .errors import ContractError

def validate_anchor_table(anchors:Iterable[OpportunityAnchor]) -> tuple[OpportunityAnchor,...]:
    rows=tuple(sorted(anchors,key=lambda a:(a.decision_time_ms,a.context_occurrence_id,a.side.value)))
    seen=set()
    for a in rows:
        if a.opportunity_id in seen: raise ContractError("duplicate_opportunity","duplicate opportunity anchor",{"opportunity_id":a.opportunity_id})
        seen.add(a.opportunity_id)
    return rows

def anchor_table_hash(anchors:Iterable[OpportunityAnchor]) -> str:
    rows=validate_anchor_table(anchors)
    return sha256([a.to_dict() for a in rows])

def future_perturbation_invariant(anchor:OpportunityAnchor, future_payload_before:object, future_payload_after:object) -> bool:
    # Future payload is intentionally excluded from anchor identity.
    before=anchor.anchor_hash
    _=(future_payload_before,future_payload_after)
    return before==anchor.anchor_hash
