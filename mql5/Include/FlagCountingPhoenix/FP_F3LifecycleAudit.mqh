#ifndef __FP_F3_LIFECYCLE_AUDIT_MQH__
#define __FP_F3_LIFECYCLE_AUDIT_MQH__
#property strict

#include "FP_F3LifecycleRules.mqh"

// ============================================================================
// Phoenix Level 09 - F3 Lifecycle Audit
// ----------------------------------------------------------------------------
// Structured report for F3 parent gate, terminal body, OR qualification, emitted
// terminal children, and post-build lock evidence.
// ============================================================================

struct FP_F3LifecycleBuildReport
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
   int leg1_L_gate_pass;
   int or_gate_pass;
   int or_gate_reject;
   int lifecycle_candidate;
   int lifecycle_completed;
   int lifecycle_locked;
   int lifecycle_visible;
   int lifecycle_hidden;
   int emitted_children;
   int duplicate_rejected;
   int lock_scans;
   int lock_opposite_found;
   int lock_opposite_missing;
   int max_parent_size_ratio_x10000;
   int max_parent_L_ratio_x10000;
};

void FP_ResetF3LifecycleBuildReport(FP_F3LifecycleBuildReport &r)
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
   r.leg1_L_gate_pass = 0;
   r.or_gate_pass = 0;
   r.or_gate_reject = 0;
   r.lifecycle_candidate = 0;
   r.lifecycle_completed = 0;
   r.lifecycle_locked = 0;
   r.lifecycle_visible = 0;
   r.lifecycle_hidden = 0;
   r.emitted_children = 0;
   r.duplicate_rejected = 0;
   r.lock_scans = 0;
   r.lock_opposite_found = 0;
   r.lock_opposite_missing = 0;
   r.max_parent_size_ratio_x10000 = 0;
   r.max_parent_L_ratio_x10000 = 0;
}

void FP_SeedF3LifecycleBuildReport(FP_F3LifecycleBuildReport &r,
                                   const int scale_L,
                                   const int node_count)
{
   r.scale_L = scale_L;
   r.node_count = node_count;
}

void FP_RecordF3ParentAttempt(const FP_FlagEvent &f2, FP_F3LifecycleBuildReport &r)
{
   r.parent_attempts++;
   if(FP_F3ParentGatePasses(f2)) r.parent_ready++;
   else r.parent_rejected++;
}

void FP_RecordF3OriginScan(FP_F3LifecycleBuildReport &r, const bool found)
{
   r.origin_scan_attempts++;
   if(found) r.origin_found++;
   else r.origin_missing++;
}

void FP_RecordF3BodyMissing(FP_F3LifecycleBuildReport &r)
{
   r.body_missing++;
}

void FP_RecordF3DuplicateRejected(FP_F3LifecycleBuildReport &r)
{
   r.duplicate_rejected++;
}

void FP_RecordF3EmittedChild(FP_F3LifecycleBuildReport &r)
{
   r.emitted_children++;
}

void FP_RecordF3LockScan(FP_F3LifecycleBuildReport &r, const bool found)
{
   r.lock_scans++;
   if(found) r.lock_opposite_found++;
   else r.lock_opposite_missing++;
}

void FP_RecordF3LifecycleOutcome(const FP_FlagEvent &f3, FP_F3LifecycleBuildReport &r)
{
   if(f3.has_leg2) r.body_complete++;
   if(f3.f3_size_gate_passed) r.size_gate_pass++;
   if(f3.f3_leg1_L_gate_passed) r.leg1_L_gate_pass++;
   if(f3.f3_or_gate_passed) r.or_gate_pass++;
   else r.or_gate_reject++;

   if(f3.status == FP_STATUS_LOCKED) r.lifecycle_locked++;
   else if(f3.status == FP_STATUS_COMPLETED) r.lifecycle_completed++;
   else r.lifecycle_candidate++;

   if(f3.visible_main) r.lifecycle_visible++;
   else r.lifecycle_hidden++;

   r.max_parent_size_ratio_x10000 = MathMax(r.max_parent_size_ratio_x10000, (int)MathRound(f3.f3_parent_size_ratio * 10000.0));
   r.max_parent_L_ratio_x10000 = MathMax(r.max_parent_L_ratio_x10000, (int)MathRound(f3.f3_parent_leg1_L_ratio * 10000.0));
}

void FP_PrintF3LifecycleBuildReport(const string tag, const FP_F3LifecycleBuildReport &r)
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
   msg += " L_pass=" + IntegerToString(r.leg1_L_gate_pass);
   msg += " or_pass=" + IntegerToString(r.or_gate_pass);
   msg += " or_reject=" + IntegerToString(r.or_gate_reject);
   msg += " candidate=" + IntegerToString(r.lifecycle_candidate);
   msg += " completed=" + IntegerToString(r.lifecycle_completed);
   msg += " locked=" + IntegerToString(r.lifecycle_locked);
   msg += " visible=" + IntegerToString(r.lifecycle_visible);
   msg += " hidden=" + IntegerToString(r.lifecycle_hidden);
   msg += " emitted_children=" + IntegerToString(r.emitted_children);
   msg += " duplicate_rejected=" + IntegerToString(r.duplicate_rejected);
   msg += " lock_scans=" + IntegerToString(r.lock_scans);
   msg += " lock_found=" + IntegerToString(r.lock_opposite_found);
   msg += " lock_missing=" + IntegerToString(r.lock_opposite_missing);
   msg += " max_size_ratio=" + DoubleToString((double)r.max_parent_size_ratio_x10000 / 10000.0, 4);
   msg += " max_L_ratio=" + DoubleToString((double)r.max_parent_L_ratio_x10000 / 10000.0, 4);
   Print(msg);
}

void FP_PrintF3LifecycleSample(const string tag, const FP_FlagEvent &e)
{
   string msg = tag;
   msg += " event=" + IntegerToString(e.event_id);
   msg += " seq=" + IntegerToString(e.sequence_id);
   msg += " parent=" + IntegerToString(e.parent_event_id);
   msg += " dir=" + FP_DirectionName(e.direction);
   msg += " L=" + IntegerToString(e.scale_L);
   msg += " status=" + FP_StatusName(e.status);
   msg += " f3_status=" + FP_F3LifecycleStatusName(e.f3_lifecycle_status);
   msg += " f3_id=" + e.f3_lifecycle_id;
   msg += " parent_ready=" + FP_BoolName(e.f3_parent_ready);
   msg += " origin_found=" + FP_BoolName(e.f3_origin_found);
   msg += " body_complete=" + FP_BoolName(e.f3_body_complete);
   msg += " size_gate=" + FP_BoolName(e.f3_size_gate_passed);
   msg += " L_gate=" + FP_BoolName(e.f3_leg1_L_gate_passed);
   msg += " or_gate=" + FP_BoolName(e.f3_or_gate_passed);
   msg += " size_ratio=" + DoubleToString(e.f3_parent_size_ratio, 4);
   msg += " L_ratio=" + DoubleToString(e.f3_parent_leg1_L_ratio, 4);
   msg += " terminal=" + FP_BoolName(e.f3_terminal_complete);
   msg += " lock_ready=" + FP_BoolName(e.f3_lock_ready);
   msg += " locked=" + FP_BoolName(e.f3_locked);
   msg += " lock_event=" + IntegerToString(e.f3_lock_event_id);
   msg += " visible=" + FP_BoolName(e.visible_main);
   msg += " hidden_reason=" + e.hidden_reason;
   msg += " scan=" + IntegerToString(e.f3_origin_scan_start_pos) + "-" + IntegerToString(e.f3_lifecycle_scan_end_pos);
   msg += " reason=" + e.f3_lifecycle_reason;
   Print(msg);
}

void FP_PrintF3LifecycleSamples(const string tag,
                                const FP_FlagEvent &events[],
                                const int event_count,
                                const int limit)
{
   int printed = 0;
   int max_print = (limit <= 0 ? 6 : limit);
   for(int i=0; i<event_count && printed<max_print; i++)
   {
      if(events[i].level != FP_LEVEL_F3) continue;
      if(events[i].f3_lifecycle_id == "") continue;
      FP_PrintF3LifecycleSample(tag, events[i]);
      printed++;
   }
}

#endif // __FP_F3_LIFECYCLE_AUDIT_MQH__
