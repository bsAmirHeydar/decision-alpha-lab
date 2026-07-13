from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import RelationScanResult,RelationEngineSnapshot,ScanCursor
from .enums import ScanMode,SidePlanState,EngineHealth,CandidateState
from .hunt import observe_minute
from .classification import classify_first_sweep,create_candidate,reduce_candidate,close_candidate_at_window
from .errors import FPI06Error

def scan_side_plan(plan,rows,source_revision_id,scan_mode=ScanMode.BATCH,scan_end_utc_ms=None,close_at_window_end=False):
    if plan.state is not SidePlanState.ELIGIBLE: raise FPI06Error('FP_HRC_SIDE_PLAN_NOT_ELIGIBLE','cannot scan ineligible side plan',{'state':str(plan.state)})
    ordered=tuple(sorted((r for r in rows if plan.check_start_utc_ms<=r.open_utc_ms<plan.check_end_utc_ms),key=lambda r:r.open_utc_ms))
    if len({r.open_utc_ms for r in ordered})!=len(ordered): raise FPI06Error('FP_HRC_DUPLICATE_ALIGNED_MINUTE','duplicate aligned minute in scan')
    if scan_end_utc_ms is not None:ordered=tuple(r for r in ordered if r.open_utc_ms<scan_end_utc_ms)
    observations=[];facts=[]
    for row in ordered:
        obs,newfacts=observe_minute(plan,row,source_revision_id);observations.append(obs);facts.extend(newfacts)
    classification=classify_first_sweep(plan,observations)
    candidate,events=create_candidate(plan,classification,source_revision_id);events=list(events)
    if candidate:
        fact_index={f.hunt_fact_id:f for f in facts}
        for obs in observations:
            if obs.minute_utc_ms<=candidate.first_hunt_minute_utc_ms:continue
            obsfacts=tuple(fact_index[x] for x in (obs.left_hunt_fact_id,obs.right_hunt_fact_id) if x)
            candidate,event=reduce_candidate(candidate,obs,obsfacts)
            if event:events.append(event)
            if candidate.state is not CandidateState.RAW_ACTIVE:break
        if close_at_window_end and candidate.state is CandidateState.RAW_ACTIVE:
            candidate,event=close_candidate_at_window(candidate)
            if event:events.append(event)
    start=ordered[0].open_utc_ms if ordered else plan.check_start_utc_ms
    end=(ordered[-1].open_utc_ms+60_000) if ordered else plan.check_start_utc_ms
    rowhash=canonical_sha256(tuple(r.row_id for r in ordered))
    material={'plan':plan.semantic_hash,'mode':scan_mode,'start':start,'end':end,'observations':[o.evidence_hash for o in observations],'facts':[f.evidence_hash for f in facts],'classification':classification.evidence_hash,'candidate':candidate.semantic_hash if candidate else None,'candidate_state':candidate.state if candidate else None,'events':[e.event_hash for e in events],'revision':source_revision_id,'rows':rowhash}
    return RelationScanResult(stable_id('FPRELSCAN',material,32),plan.side_plan_id,scan_mode,start,end,tuple(observations),tuple(facts),classification,candidate,tuple(events),len(ordered),source_revision_id,rowhash,canonical_sha256(material))

def cursor_from_result(result):
    next_time=result.scanned_end_utc_ms;candidate=result.candidate
    material={'plan':result.side_plan_id,'next':next_time,'revision':result.source_revision_id,'rows':result.source_rows_hash,'candidate':candidate.candidate_id if candidate else '','state':candidate.state if candidate else None}
    return ScanCursor(result.side_plan_id,next_time,result.source_revision_id,result.source_rows_hash,candidate.candidate_id if candidate else '',candidate.state if candidate else None,canonical_sha256(material))

def build_engine_snapshot(config,compiler_report,scan_results,created_utc_ms):
    scans=tuple(sorted(scan_results,key=lambda r:r.side_plan_id));candidates=tuple(sorted((r.candidate for r in scans if r.candidate is not None),key=lambda c:c.candidate_id))
    if any(r.classification.outcome.value=='DATA_BLOCKED' for r in scans):health=EngineHealth.BLOCKED;reasons=('FP_HRC_ENGINE_BLOCKED_DATA',)
    elif compiler_report.blocked_items:health=EngineHealth.DEGRADED;reasons=('FP_HRC_ENGINE_DEGRADED_COMPILER_BLOCKS',)
    else:health=EngineHealth.READY;reasons=('FP_HRC_ENGINE_READY',)
    revisions={r.source_revision_id for r in scans};revision=next(iter(revisions)) if len(revisions)==1 else 'MIXED'
    material={'config':config.config_hash,'compiler':compiler_report.evidence_hash,'scans':[r.evidence_hash for r in scans],'candidates':[(c.semantic_hash,c.state,c.state_sequence) for c in candidates],'health':health,'revision':revision}
    return RelationEngineSnapshot(stable_id('FPRELSTATE',material,32),config.config_hash,compiler_report.evidence_hash,scans,candidates,health,reasons,revision,created_utc_ms,canonical_sha256(material))
