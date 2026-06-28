#ifndef __FP_F1_LIFECYCLE_AUDIT_MQH__
#define __FP_F1_LIFECYCLE_AUDIT_MQH__
#property strict

#include "FP_F1LifecycleRules.mqh"

// ============================================================================
// Phoenix Level 07 - F1 Lifecycle Audit
// ----------------------------------------------------------------------------
// Structured reporting for F1 candidate/confirmed/invalidated lifecycle state.
// This report is independent from renderer output and sequence pruning.
// ============================================================================

struct FP_F1LifecycleBuildReport
{
   int scale_L;
   int node_count;
   int origin_attempts;
   int phase_origin_attempts;
   int fail_open_origin_attempts;
   int phase_gate_passed;
   int phase_gate_rejected;
   int body_missing;
   int body_complete;
   int lifecycle_candidate;
   int lifecycle_post_flag;
   int lifecycle_confirmed;
   int lifecycle_invalidated;
   int lifecycle_extended;
   int lifecycle_visible;
   int lifecycle_hidden;
   int f2_ready;
   int duplicate_rejected;
   int emitted_roots;
   int max_extension_count;
};

void FP_ResetF1LifecycleBuildReport(FP_F1LifecycleBuildReport &r)
{
   r.scale_L = 0;
   r.node_count = 0;
   r.origin_attempts = 0;
   r.phase_origin_attempts = 0;
   r.fail_open_origin_attempts = 0;
   r.phase_gate_passed = 0;
   r.phase_gate_rejected = 0;
   r.body_missing = 0;
   r.body_complete = 0;
   r.lifecycle_candidate = 0;
   r.lifecycle_post_flag = 0;
   r.lifecycle_confirmed = 0;
   r.lifecycle_invalidated = 0;
   r.lifecycle_extended = 0;
   r.lifecycle_visible = 0;
   r.lifecycle_hidden = 0;
   r.f2_ready = 0;
   r.duplicate_rejected = 0;
   r.emitted_roots = 0;
   r.max_extension_count = 0;
}

void FP_SeedF1LifecycleBuildReport(FP_F1LifecycleBuildReport &r,
                                   const int scale_L,
                                   const int node_count)
{
   r.scale_L = scale_L;
   r.node_count = node_count;
}

void FP_RecordF1OriginAttempt(FP_F1LifecycleBuildReport &r,
                              const bool from_phase_boundary,
                              const bool from_fail_open)
{
   r.origin_attempts++;
   if(from_phase_boundary) r.phase_origin_attempts++;
   if(from_fail_open) r.fail_open_origin_attempts++;
}

void FP_RecordF1LifecycleOutcome(const FP_FlagEvent &f1, FP_F1LifecycleBuildReport &r)
{
   if(f1.has_leg2) r.body_complete++;
   if(f1.leg2_extension_count > 0) r.lifecycle_extended++;
   r.max_extension_count = MathMax(r.max_extension_count, f1.leg2_extension_count);

   if(f1.status == FP_STATUS_CONFIRMED) r.lifecycle_confirmed++;
   else if(f1.status == FP_STATUS_INVALIDATED) r.lifecycle_invalidated++;
   else if(f1.status == FP_STATUS_POST_FLAG) r.lifecycle_post_flag++;
   else r.lifecycle_candidate++;

   if(f1.visible_main) r.lifecycle_visible++;
   else r.lifecycle_hidden++;
   if(f1.lifecycle_can_spawn_f2) r.f2_ready++;
}

void FP_RecordF1PhaseRejected(FP_F1LifecycleBuildReport &r)
{
   r.phase_gate_rejected++;
}

void FP_RecordF1BodyMissing(FP_F1LifecycleBuildReport &r)
{
   r.body_missing++;
}

void FP_RecordF1DuplicateRejected(FP_F1LifecycleBuildReport &r)
{
   r.duplicate_rejected++;
}

void FP_RecordF1EmittedRoot(FP_F1LifecycleBuildReport &r)
{
   r.emitted_roots++;
}

void FP_PrintF1LifecycleBuildReport(const string tag, const FP_F1LifecycleBuildReport &r)
{
   Print(tag,
         " scale_L=", r.scale_L,
         " nodes=", r.node_count,
         " attempts=", r.origin_attempts,
         " phase_attempts=", r.phase_origin_attempts,
         " failopen_attempts=", r.fail_open_origin_attempts,
         " gate_pass=", r.phase_gate_passed,
         " gate_reject=", r.phase_gate_rejected,
         " body_missing=", r.body_missing,
         " body_complete=", r.body_complete,
         " candidate=", r.lifecycle_candidate,
         " post_flag=", r.lifecycle_post_flag,
         " confirmed=", r.lifecycle_confirmed,
         " invalidated=", r.lifecycle_invalidated,
         " extended=", r.lifecycle_extended,
         " visible=", r.lifecycle_visible,
         " hidden=", r.lifecycle_hidden,
         " f2_ready=", r.f2_ready,
         " duplicate_rejected=", r.duplicate_rejected,
         " emitted_roots=", r.emitted_roots,
         " max_ext=", r.max_extension_count);
}

void FP_PrintF1LifecycleSample(const string tag, const FP_FlagEvent &e)
{
   Print(tag,
         " event=", e.event_id,
         " seq=", e.sequence_id,
         " dir=", FP_DirectionName(e.direction),
         " L=", e.scale_L,
         " status=", FP_StatusName(e.status),
         " lc_status=", FP_F1LifecycleStatusName(e.lifecycle_status),
         " lc_id=", e.lifecycle_id,
         " gate=", FP_BoolName(e.lifecycle_phase_gate_passed),
         " phase=", FP_BoolName(e.from_phase_boundary),
         " failopen=", FP_BoolName(e.from_fail_open),
         " body_complete=", FP_BoolName(e.lifecycle_body_complete),
         " internal_ready=", FP_BoolName(e.lifecycle_internal_ready),
         " can_spawn_f2=", FP_BoolName(e.lifecycle_can_spawn_f2),
         " ext=", e.leg2_extension_count,
         " visible=", FP_BoolName(e.visible_main),
         " hidden_reason=", e.hidden_reason,
         " scan=", e.lifecycle_scan_start_pos, "-", e.lifecycle_scan_end_pos,
         " reason=", e.lifecycle_reason);
}

void FP_PrintF1LifecycleSamples(const string tag,
                                const FP_FlagEvent &events[],
                                const int event_count,
                                const int limit)
{
   int printed = 0;
   int max_print = (limit <= 0 ? 6 : limit);
   for(int i=0; i<event_count && printed<max_print; i++)
   {
      if(events[i].level != FP_LEVEL_F1) continue;
      if(events[i].lifecycle_id == "") continue;
      FP_PrintF1LifecycleSample(tag, events[i]);
      printed++;
   }
}

#endif // __FP_F1_LIFECYCLE_AUDIT_MQH__
