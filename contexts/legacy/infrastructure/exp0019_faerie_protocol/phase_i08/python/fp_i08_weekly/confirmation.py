from __future__ import annotations
from fp_i02_kernel.enums import RelationCode
from fp_i07_confirmation.projection import project_candidate
from fp_i07_confirmation.engine import admit_candidate,finalize
from fp_i07_confirmation.enums import ConfirmationOutcome
from .canonical import canonical_sha256,stable_id
from .contracts import WWContext,WWTransitionRecord
from .enums import WWLifecycleState,WWTransition
from .errors import FPI08Error

def confirm_ww(scan_record,side_plan,relation_instance,bars,observation,confirmation_config,ww_config,admitted_utc_ms):
    candidate=scan_record.relation_scan.candidate
    if candidate is None: raise FPI08Error("FP_WRC_WW_CANDIDATE_MISSING","WW scan has no candidate")
    if candidate.relation is not RelationCode.WW: raise FPI08Error("FP_WRC_NON_WW_CANDIDATE","candidate relation must be WW")
    projection=project_candidate(candidate,bars,confirmation_config)
    pending,admit_event=admit_candidate(candidate,projection,scan_record.source_revision_id,admitted_utc_ms)
    bar=next((b for b in bars if b.host_bar_id==projection.target_host_bar_id),None)
    if bar is None: raise FPI08Error("FP_WRC_TARGET_HOST_BAR_MISSING","projected host bar missing")
    result,final_event=finalize(pending,bar,observation,confirmation_config)
    if result.outcome is not ConfirmationOutcome.CONFIRMED: return result,None,(admit_event,final_event)
    signal=result.confirmed_signal
    hunter_left=signal.hunter_symbol==side_plan.left_symbol
    href=side_plan.left_reference_id if hunter_left else side_plan.right_reference_id; hp=side_plan.left_reference_price if hunter_left else side_plan.right_reference_price
    pref=side_plan.right_reference_id if hunter_left else side_plan.left_reference_id; pp=side_plan.right_reference_price if hunter_left else side_plan.left_reference_price
    mat={"signal":signal.signal_hash,"plan":side_plan.semantic_hash,"instance":relation_instance.semantic_hash,"previous_week":relation_instance.previous_week_id,"current_week":relation_instance.current_week_id,"week_end":relation_instance.check_end_utc_ms,"config":ww_config.config_hash}
    ctx=WWContext(stable_id("FPWWCTX",mat,36),signal,result.result_id,side_plan.side_plan_id,signal.direction,signal.side,signal.hunter_symbol,signal.protected_symbol,href,hp,pref,pp,relation_instance.previous_week_id,relation_instance.current_week_id,relation_instance.check_end_utc_ms,WWLifecycleState.CONFIRMED,signal.confirmation_close_utc_ms,0,"",0,"FP_WRC_WW_CONFIRMED_ACTIVE",signal.source_revision_id,ww_config.config_hash,canonical_sha256(mat))
    em={"context":ctx.ww_context_id,"transition":WWTransition.CONFIRMED,"time":ctx.confirmed_utc_ms,"signal":signal.signal_id}
    evt=WWTransitionRecord(stable_id("FPWWEVT",em,32),ctx.ww_context_id,0,WWTransition.CONFIRMED,None,WWLifecycleState.CONFIRMED,ctx.confirmed_utc_ms,signal.signal_id,"FP_WRC_WW_CONFIRMED_ACTIVE",canonical_sha256(em))
    return result,ctx,(admit_event,final_event,evt)
