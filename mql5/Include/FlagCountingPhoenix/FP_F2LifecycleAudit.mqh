#ifndef __FP_F2_LIFECYCLE_AUDIT_MQH__
#define __FP_F2_LIFECYCLE_AUDIT_MQH__
#property strict

#include "FP_F2LifecycleRules.mqh"

// ============================================================================
// Phoenix Level 08 - F2 Lifecycle Audit
// ----------------------------------------------------------------------------
// Structured report for F2 parent gate, origin backfill, size gate, internal
// confirmation, invalidation, and F3 authorization.
// ============================================================================

struct FP_F2LifecycleBuildReport
{
   int scale_L;
   int node_count;
   int parent_attempts;
   int parent_ready;
   int parent_rejected;
   int origin_scan_attempts;
   int origin_found;
   int origin_missing;
   int body_missing;
   int body_complete;
   int size_gate_pass;
   int size_gate_reject;
   int lifecycle_candidate;
   int lifecycle_post_flag;
   int lifecycle_confirmed;
   int lifecycle_invalidated;
   int lifecycle_extended;
   int lifecycle_visible;
   int lifecycle_hidden;
   int f3_ready;
   int emitted_children;
   int duplicate_rejected;
   int max_extension_count;
};

void FP_ResetF2LifecycleBuildReport(FP_F2LifecycleBuildReport &r)
{
   r.scale_L = 0;
   r.node_count = 0;
   r.parent_attempts = 0;
   r.parent_ready = 0;
   r.parent_rejected = 0;
   r.origin_scan_attempts = 0;
   r.origin_found = 0;
   r.origin_missing = 0;
   r.body_missing = 0;
   r.body_complete = 0;
   r.size_gate_pass = 0;
   r.size_gate_reject = 0;
   r.lifecycle_candidate = 0;
   r.lifecycle_post_flag = 0;
   r.lifecycle_confirmed = 0;
   r.lifecycle_invalidated = 0;
   r.lifecycle_extended = 0;
   r.lifecycle_visible = 0;
   r.lifecycle_hidden = 0;
   r.f3_ready = 0;
   r.emitted_children = 0;
   r.duplicate_rejected = 0;
   r.max_extension_count = 0;
}

void FP_SeedF2LifecycleBuildReport(FP_F2LifecycleBuildReport &r,
                                   const int scale_L,
                                   const int node_count)
{
   r.scale_L = scale_L;
   r.node_count = node_count;
}

void FP_RecordF2ParentAttempt(const FP_FlagEvent &f1, FP_F2LifecycleBuildReport &r)
{
   r.parent_attempts++;
   if(FP_F2ParentGatePasses(f1)) r.parent_ready++;
   else r.parent_rejected++;
}

void FP_RecordF2OriginScan(FP_F2LifecycleBuildReport &r, const bool found)
{
   r.origin_scan_attempts++;
   if(found) r.origin_found++;
   else r.origin_missing++;
}

void FP_RecordF2BodyMissing(FP_F2LifecycleBuildReport &r)
{
   r.body_missing++;
}

void FP_RecordF2DuplicateRejected(FP_F2LifecycleBuildReport &r)
{
   r.duplicate_rejected++;
}

void FP_RecordF2EmittedChild(FP_F2LifecycleBuildReport &r)
{
   r.emitted_children++;
}

void FP_RecordF2LifecycleOutcome(const FP_FlagEvent &f2, FP_F2LifecycleBuildReport &r)
{
   if(f2.has_leg2) r.body_complete++;
   if(f2.f2_size_gate_passed) r.size_gate_pass++;
   else r.size_gate_reject++;
   if(f2.leg2_extension_count > 0) r.lifecycle_extended++;
   r.max_extension_count = MathMax(r.max_extension_count, f2.leg2_extension_count);

   if(f2.status == FP_STATUS_CONFIRMED) r.lifecycle_confirmed++;
   else if(f2.status == FP_STATUS_INVALIDATED) r.lifecycle_invalidated++;
   else if(f2.status == FP_STATUS_POST_FLAG) r.lifecycle_post_flag++;
   else r.lifecycle_candidate++;

   if(f2.visible_main) r.lifecycle_visible++;
   else r.lifecycle_hidden++;
   if(f2.f2_can_spawn_f3) r.f3_ready++;
}

void FP_PrintF2LifecycleBuildReport(const string tag, const FP_F2LifecycleBuildReport &r)
{
   string msg = tag;
   msg += " scale_L=" + IntegerToString(r.scale_L);
   msg += " nodes=" + IntegerToString(r.node_count);
   msg += " parent_attempts=" + IntegerToString(r.parent_attempts);
   msg += " parent_ready=" + IntegerToString(r.parent_ready);
   msg += " parent_rejected=" + IntegerToString(r.parent_rejected);
   msg += " origin_scans=" + IntegerToString(r.origin_scan_attempts);
   msg += " origin_found=" + IntegerToString(r.origin_found);
   msg += " origin_missing=" + IntegerToString(r.origin_missing);
   msg += " body_missing=" + IntegerToString(r.body_missing);
   msg += " body_complete=" + IntegerToString(r.body_complete);
   msg += " size_pass=" + IntegerToString(r.size_gate_pass);
   msg += " size_reject=" + IntegerToString(r.size_gate_reject);
   msg += " candidate=" + IntegerToString(r.lifecycle_candidate);
   msg += " post_flag=" + IntegerToString(r.lifecycle_post_flag);
   msg += " confirmed=" + IntegerToString(r.lifecycle_confirmed);
   msg += " invalidated=" + IntegerToString(r.lifecycle_invalidated);
   msg += " extended=" + IntegerToString(r.lifecycle_extended);
   msg += " visible=" + IntegerToString(r.lifecycle_visible);
   msg += " hidden=" + IntegerToString(r.lifecycle_hidden);
   msg += " f3_ready=" + IntegerToString(r.f3_ready);
   msg += " emitted_children=" + IntegerToString(r.emitted_children);
   msg += " duplicate_rejected=" + IntegerToString(r.duplicate_rejected);
   msg += " max_ext=" + IntegerToString(r.max_extension_count);
   Print(msg);
}

void FP_PrintF2LifecycleSample(const string tag, const FP_FlagEvent &e)
{
   string msg = tag;
   msg += " event=" + IntegerToString(e.event_id);
   msg += " seq=" + IntegerToString(e.sequence_id);
   msg += " parent=" + IntegerToString(e.parent_event_id);
   msg += " dir=" + FP_DirectionName(e.direction);
   msg += " L=" + IntegerToString(e.scale_L);
   msg += " status=" + FP_StatusName(e.status);
   msg += " f2_status=" + FP_F2LifecycleStatusName(e.f2_lifecycle_status);
   msg += " f2_id=" + e.f2_lifecycle_id;
   msg += " parent_ready=" + FP_BoolName(e.f2_parent_ready);
   msg += " origin_found=" + FP_BoolName(e.f2_origin_found);
   msg += " body_complete=" + FP_BoolName(e.f2_body_complete);
   msg += " size_gate=" + FP_BoolName(e.f2_size_gate_passed);
   msg += " ratio=" + DoubleToString(e.size_ratio, 4);
   msg += " internal_ready=" + FP_BoolName(e.f2_internal_ready);
   msg += " can_spawn_f3=" + FP_BoolName(e.f2_can_spawn_f3);
   msg += " ext=" + IntegerToString(e.leg2_extension_count);
   msg += " visible=" + FP_BoolName(e.visible_main);
   msg += " hidden_reason=" + e.hidden_reason;
   msg += " scan=" + IntegerToString(e.f2_origin_scan_start_pos) + "-" + IntegerToString(e.f2_lifecycle_scan_end_pos);
   msg += " reason=" + e.f2_lifecycle_reason;
   Print(msg);
}

void FP_PrintF2LifecycleSamples(const string tag,
                                const FP_FlagEvent &events[],
                                const int event_count,
                                const int limit)
{
   int printed = 0;
   int max_print = (limit <= 0 ? 6 : limit);
   for(int i=0; i<event_count && printed<max_print; i++)
   {
      if(events[i].level != FP_LEVEL_F2) continue;
      if(events[i].f2_lifecycle_id == "") continue;
      FP_PrintF2LifecycleSample(tag, events[i]);
      printed++;
   }
}

#endif // __FP_F2_LIFECYCLE_AUDIT_MQH__
