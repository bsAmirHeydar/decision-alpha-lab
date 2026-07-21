from __future__ import annotations
from .canonical import stable_id

def evaluate(object_row,binding,anchor,lifecycle):
    reasons=[];remediations=[]
    if binding.get("binding_status")=="BLOCKED":reasons.append("SOURCE_EVENT_BINDING_BLOCKED")
    if anchor.get("validation_status")!="PASS":reasons.append("ANCHOR_SEMANTICS_BLOCKED")
    if str(lifecycle.get("backfill_policy","")).startswith("UNKNOWN"):reasons.append("BACKFILL_PARITY_UNKNOWN")
    if lifecycle.get("validation_status")!="PASS":
        if object_row.get("surface_kind")=="INDICATOR_BUFFER":remediations.append("PLATFORM_MANAGED_BUFFER_LIFECYCLE")
        elif lifecycle.get("observed_delete_policy")=="NO_DELETE_EVIDENCE":remediations.append("CANONICAL_INSTANCE_OWNED_CLEANUP")
        else:reasons.append("LIFECYCLE_SEMANTICS_BLOCKED")
    status="ELIGIBLE_REFERENCE_CUTOVER" if not reasons else "BLOCKED_EXPLICIT"
    rid=stable_id("VISELIG",object_row["visual_object_id"],status,*reasons,*remediations)
    return {"eligibility_id":rid,"visual_object_id":object_row["visual_object_id"],"status":status,"blocking_reasons":reasons,"remediations":remediations,"production_cutover_allowed":False,"reference_harness_cutover_allowed":not reasons}
