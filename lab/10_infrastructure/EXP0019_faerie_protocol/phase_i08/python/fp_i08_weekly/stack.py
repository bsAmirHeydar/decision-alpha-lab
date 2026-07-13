from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import WWStackEntry,WWActiveStack
from .enums import *

def resolve_active_stack(pair_id,contexts,data_state,evaluated_utc_ms,config):
    ordered=tuple(sorted(contexts,key=lambda c:(c.confirmed_utc_ms,c.source_signal.signal_id,c.ww_context_id),reverse=True))
    active=[c for c in ordered if c.state is WWLifecycleState.CONFIRMED and c.confirmed_utc_ms<=evaluated_utc_ms<c.check_week_end_utc_ms]
    winner=active[0] if active else None; entries=[]
    for rank,c in enumerate(ordered,1):
        if c.state is WWLifecycleState.NEUTRALIZED: disp=WWStackDisposition.NEUTRALIZED;reason="FP_RC_WW_NEUTRALIZED"
        elif c.state is WWLifecycleState.EXPIRED or evaluated_utc_ms>=c.check_week_end_utc_ms: disp=WWStackDisposition.EXPIRED;reason="FP_WRC_WW_CHECK_WEEK_EXPIRED"
        elif c.state is WWLifecycleState.INVALID_DATA: disp=WWStackDisposition.INVALID;reason="FP_RC_WW_DATA_INCOMPLETE"
        elif winner and c.ww_context_id==winner.ww_context_id: disp=WWStackDisposition.ACTIVE_WINNER;reason="FP_WRC_NEWEST_ACTIVE_WW_WINNER"
        else: disp=WWStackDisposition.ACTIVE_SHADOWED;reason="FP_WRC_OLDER_ACTIVE_WW_SHADOWED"
        mat={"context":c.ww_context_id,"signal":c.source_signal.signal_id,"direction":c.direction,"confirmed":c.confirmed_utc_ms,"state":c.state,"disposition":disp,"rank":rank,"winner":winner.ww_context_id if winner else ""}
        entries.append(WWStackEntry(c.ww_context_id,c.source_signal.signal_id,c.direction,c.confirmed_utc_ms,c.state,disp,rank,winner.ww_context_id if winner else "",reason,canonical_sha256(mat)))
    if data_state is not WWDataState.COMPLETE: reason="FP_RC_WW_DATA_INCOMPLETE";active_id="";sig="";direction=None
    elif winner: reason="FP_WRC_NEWEST_ACTIVE_WW_WINS";active_id=winner.ww_context_id;sig=winner.source_signal.signal_id;direction=winner.direction
    else: reason="FP_RC_WW_NONE_ALLOW_BOTH";active_id="";sig="";direction=None
    material={"pair":pair_id,"entries":[e.entry_hash for e in entries],"active":active_id,"direction":direction,"data_state":data_state,"at":evaluated_utc_ms,"policy":config.resolution_policy,"config":config.config_hash}
    return WWActiveStack(stable_id("FPWWSTACK",material,32),pair_id,tuple(entries),active_id,sig,direction,data_state,evaluated_utc_ms,config.resolution_policy,reason,config.config_hash,canonical_sha256(material))
