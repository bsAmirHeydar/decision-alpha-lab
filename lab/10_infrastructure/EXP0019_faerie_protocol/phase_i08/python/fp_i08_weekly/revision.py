from __future__ import annotations
from dataclasses import dataclass
from .canonical import canonical_sha256,stable_id
from .enums import WWLifecycleState
@dataclass(frozen=True,slots=True)
class WWRevisionImpact:
    impact_id:str; revision_id:str; affected_ww_context_ids:tuple[str,...]; preserved_confirmed_context_ids:tuple[str,...]; reason_code:str; evidence_hash:str

def assess_revision(contexts,revision_id,affected_start_utc_ms,affected_end_utc_ms):
    affected=[];preserved=[]
    for c in contexts:
        overlap=affected_start_utc_ms<c.check_week_end_utc_ms and affected_end_utc_ms>c.source_signal.first_hunt_minute_utc_ms
        if overlap and c.state is WWLifecycleState.RAW: affected.append(c.ww_context_id)
        elif overlap and c.state in (WWLifecycleState.CONFIRMED,WWLifecycleState.NEUTRALIZED,WWLifecycleState.EXPIRED): preserved.append(c.ww_context_id)
    mat={"revision":revision_id,"affected":sorted(affected),"preserved":sorted(preserved),"start":affected_start_utc_ms,"end":affected_end_utc_ms}
    return WWRevisionImpact(stable_id("FPWWREV",mat,32),revision_id,tuple(sorted(affected)),tuple(sorted(preserved)),"FP_WRC_CONFIRMED_WW_EVIDENCE_PRESERVED",canonical_sha256(mat))
