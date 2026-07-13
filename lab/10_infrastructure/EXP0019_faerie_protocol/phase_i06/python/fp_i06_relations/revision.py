from __future__ import annotations
from .canonical import canonical_sha256,stable_id

def affected_side_plans(compilation_report,affected_pair_window_ids,changed_minutes):
    windows=set(affected_pair_window_ids);minutes=set(changed_minutes);affected=[]
    instance_index={i.relation_instance_id:i for i in compilation_report.compiled_instances}
    for plan in compilation_report.side_plans:
        inst=instance_index[plan.relation_instance_id]
        if inst.reference_pair_window_id in windows or inst.check_pair_window_id in windows or any(plan.check_start_utc_ms<=m<plan.check_end_utc_ms for m in minutes):affected.append(plan.side_plan_id)
    return tuple(sorted(set(affected)))
def revision_impact(compilation_report,revision_id,affected_pair_window_ids,changed_minutes):
    plans=affected_side_plans(compilation_report,affected_pair_window_ids,changed_minutes)
    material={'compiler':compilation_report.evidence_hash,'revision':revision_id,'windows':sorted(affected_pair_window_ids),'minutes':sorted(changed_minutes),'plans':plans}
    return {'impact_id':stable_id('FPRELREV',material,32),'revision_id':revision_id,'affected_side_plan_ids':plans,'reason_code':'FP_HRC_BOUNDED_RELATION_INVALIDATION','evidence_hash':canonical_sha256(material)}
