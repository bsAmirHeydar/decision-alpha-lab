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
   string msg = tag;
   msg += " scale_L=" + IntegerToString(r.scale_L);
   msg += " nodes=" + IntegerToString(r.node_count);
   msg += " attempts=" + IntegerToString(r.origin_attempts);
   msg += " phase_attempts=" + IntegerToString(r.phase_origin_attempts);
   msg += " failopen_attempts=" + IntegerToString(r.fail_open_origin_attempts);
   msg += " gate_pass=" + IntegerToString(r.phase_gate_passed);
   msg += " gate_reject=" + IntegerToString(r.phase_gate_rejected);
   msg += " body_missing=" + IntegerToString(r.body_missing);
   msg += " body_complete=" + IntegerToString(r.body_complete);
   msg += " candidate=" + IntegerToString(r.lifecycle_candidate);
   msg += " post_flag=" + IntegerToString(r.lifecycle_post_flag);
   msg += " confirmed=" + IntegerToString(r.lifecycle_confirmed);
   msg += " invalidated=" + IntegerToString(r.lifecycle_invalidated);
   msg += " extended=" + IntegerToString(r.lifecycle_extended);
   msg += " visible=" + IntegerToString(r.lifecycle_visible);
   msg += " hidden=" + IntegerToString(r.lifecycle_hidden);
   msg += " f2_ready=" + IntegerToString(r.f2_ready);
   msg += " duplicate_rejected=" + IntegerToString(r.duplicate_rejected);
   msg += " emitted_roots=" + IntegerToString(r.emitted_roots);
   msg += " max_ext=" + IntegerToString(r.max_extension_count);
   Print(msg);
}

void FP_PrintF1LifecycleSample(const string tag, const FP_FlagEvent &e)
{
   string msg = tag;
   msg += " event=" + IntegerToString(e.event_id);
   msg += " seq=" + IntegerToString(e.sequence_id);
   msg += " dir=" + FP_DirectionName(e.direction);
   msg += " L=" + IntegerToString(e.scale_L);
   msg += " status=" + FP_StatusName(e.status);
   msg += " lc_status=" + FP_F1LifecycleStatusName(e.lifecycle_status);
   msg += " lc_id=" + e.lifecycle_id;
   msg += " gate=" + FP_BoolName(e.lifecycle_phase_gate_passed);
   msg += " phase=" + FP_BoolName(e.from_phase_boundary);
   msg += " failopen=" + FP_BoolName(e.from_fail_open);
   msg += " body_complete=" + FP_BoolName(e.lifecycle_body_complete);
   msg += " internal_ready=" + FP_BoolName(e.lifecycle_internal_ready);
   msg += " can_spawn_f2=" + FP_BoolName(e.lifecycle_can_spawn_f2);
   msg += " ext=" + IntegerToString(e.leg2_extension_count);
   msg += " visible=" + FP_BoolName(e.visible_main);
   msg += " hidden_reason=" + e.hidden_reason;
   msg += " scan=" + IntegerToString(e.lifecycle_scan_start_pos) + "-" + IntegerToString(e.lifecycle_scan_end_pos);
   msg += " reason=" + e.lifecycle_reason;
   Print(msg);
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
