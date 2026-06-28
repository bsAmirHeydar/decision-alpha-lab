#ifndef __FP_F3_LIFECYCLE_ENGINE_MQH__
#define __FP_F3_LIFECYCLE_ENGINE_MQH__
#property strict

#include "FP_F3LifecycleAudit.mqh"

// ============================================================================
// Phoenix Level 09 - F3 Lifecycle Engine
// ----------------------------------------------------------------------------
// Converts one lifecycle-confirmed/authorized F2 into a terminal F3 child.
// F3 uses body completion plus OR qualification; post-body internal counting is
// intentionally not required in this layer.
// ============================================================================

bool FP_FindF3OriginFromParentWithReport(const FP_Node &nodes[],
                                         const int node_count,
                                         const FP_FlagEvent &f2,
                                         const FP_Config &cfg,
                                         int &origin_pos,
                                         FP_Node &origin,
                                         FP_F3LifecycleBuildReport &f3_report)
{
   origin_pos = -1;
   FP_ResetNode(origin);
   int to_pos = MathMax(f2.pos_leg2, f2.pos_confirm - 1);
   bool found = FP_FindDeepestAdverseNode(nodes,
                                          node_count,
                                          f2.pos_leg2 + 1,
                                          to_pos,
                                          f2.direction,
                                          cfg.boundary_epsilon_points,
                                          origin_pos,
                                          origin);
   FP_RecordF3OriginScan(f3_report, found);
   return found;
}

void FP_ApplyF3TerminalLifecycleWithReport(FP_FlagEvent &f3,
                                           const FP_FlagEvent &f2,
                                           const FP_Config &cfg,
                                           FP_F3LifecycleBuildReport &f3_report)
{
   f3.parent_flag_size = f2.flag_size;
   f3.parent_leg1_L = f2.leg1_L;
   f3.size_ratio = (f2.flag_size > 0.0 ? f3.flag_size / f2.flag_size : 0.0);
   f3.f3_parent_size_ratio = f3.size_ratio;
   f3.f3_parent_leg1_L_ratio = ((double)MathMax(0, f3.leg1_L) / (double)MathMax(1, f2.leg1_L));
   f3.f3_size_gate_passed = FP_F3SizeGatePasses(f3, f2, cfg);
   f3.f3_leg1_L_gate_passed = FP_F3Leg1LGatePasses(f3, f2, cfg);
   f3.f3_or_gate_passed = (f3.f3_size_gate_passed || f3.f3_leg1_L_gate_passed);
   f3.f3_terminal_complete = false;
   f3.f3_lock_ready = false;
   f3.f3_locked = false;
   f3.f3_lock_event_id = -1;
   f3.f3_lock_reason = "";

   if(f3.f3_or_gate_passed)
   {
      f3.status = FP_STATUS_COMPLETED;
      f3.render_kind = FP_RENDER_FLAG_BODY;
      f3.visible_main = true;
      f3.f3_terminal_complete = true;
      f3.f3_lock_ready = true;
      string why = "terminal_or_qualified_size_" + FP_BoolName(f3.f3_size_gate_passed) + "_L_" + FP_BoolName(f3.f3_leg1_L_gate_passed);
      FP_SetF3LifecycleState(f3, FP_F3_LC_COMPLETED, why);
      FP_RecordF3LifecycleOutcome(f3, f3_report);
      return;
   }

   f3.status = FP_STATUS_LIVE_BODY;
   f3.render_kind = FP_RENDER_FLAG_BODY;
   f3.visible_main = cfg.f3_show_or_rejected_candidates;
   if(!f3.visible_main) f3.hidden_reason = "hidden_f3_or_gate_rejected";
   FP_SetF3LifecycleState(f3, FP_F3_LC_OR_REJECTED, "or_gate_rejected_waiting_size_or_L_contract");
   FP_RecordF3LifecycleOutcome(f3, f3_report);
}

bool FP_BuildF3LifecycleFromF2WithReport(const FP_Node &nodes[],
                                         const int node_count,
                                         const FP_FlagEvent &f2,
                                         const int sequence_id,
                                         const int parent_event_id,
                                         const FP_Config &cfg,
                                         FP_FlagEvent &f3,
                                         FP_FlagBodyBuildReport &body_report,
                                         FP_F3LifecycleBuildReport &f3_report)
{
   FP_ResetFlagEvent(f3);
   FP_RecordF3ParentAttempt(f2, f3_report);
   if(!FP_F3ParentGatePasses(f2))
      return false;

   int origin_pos = -1;
   FP_Node origin;
   if(!FP_FindF3OriginFromParentWithReport(nodes, node_count, f2, cfg, origin_pos, origin, f3_report))
      return false;

   bool body_ok = FP_FindFlagBodyFromOriginWithReport(nodes,
                                                      node_count,
                                                      origin_pos,
                                                      f2.direction,
                                                      FP_LEVEL_F3,
                                                      sequence_id,
                                                      parent_event_id,
                                                      cfg.boundary_epsilon_points,
                                                      f3,
                                                      body_report);
   if(!body_ok)
   {
      FP_RecordF3BodyMissing(f3_report);
      return false;
   }

   f3.chain_index = 3;
   f3.parent_sequence_id = f2.sequence_id;
   f3.parent_event_id = parent_event_id;
   f3.f3_parent_ready = true;
   f3.f3_origin_found = true;
   f3.f3_origin_scan_start_pos = f2.pos_leg2 + 1;
   f3.f3_lifecycle_scan_end_pos = f3.body_scan_end_pos;
   f3.from_phase_boundary = f2.from_phase_boundary;
   f3.from_fail_open = f2.from_fail_open;

   FP_ApplyF3TerminalLifecycleWithReport(f3, f2, cfg, f3_report);
   f3.f3_lifecycle_id = FP_BuildF3LifecycleId(f3);
   f3.visible_main = FP_F3ShouldBeVisibleForLifecycle(f3, cfg);
   if(!f3.visible_main && f3.hidden_reason == "")
      f3.hidden_reason = "hidden_by_f3_lifecycle_visibility_policy";
   return f3.visible_main;
}

bool FP_BuildF3LifecycleFromF2(const FP_Node &nodes[],
                               const int node_count,
                               const FP_FlagEvent &f2,
                               const int sequence_id,
                               const int parent_event_id,
                               const FP_Config &cfg,
                               FP_FlagEvent &f3)
{
   FP_FlagBodyBuildReport body_report;
   FP_ResetFlagBodyBuildReport(body_report);
   FP_SeedFlagBodyBuildReport(body_report, f2.scale_L, node_count, f2.direction, FP_LEVEL_F3);

   FP_F3LifecycleBuildReport f3_report;
   FP_ResetF3LifecycleBuildReport(f3_report);
   FP_SeedF3LifecycleBuildReport(f3_report, f2.scale_L, node_count);

   return FP_BuildF3LifecycleFromF2WithReport(nodes,
                                              node_count,
                                              f2,
                                              sequence_id,
                                              parent_event_id,
                                              cfg,
                                              f3,
                                              body_report,
                                              f3_report);
}

bool FP_FindFirstOppositeConfirmedF1After(const FP_FlagEvent &events[],
                                          const int event_count,
                                          const FP_FlagEvent &f3,
                                          int &best_index)
{
   best_index = -1;
   int complete_anchor = (f3.has_leg2 ? f3.leg2.index_anchor : -1);
   if(complete_anchor < 0) return false;

   for(int j=0; j<event_count; j++)
   {
      if(events[j].level != FP_LEVEL_F1) continue;
      if(events[j].direction == f3.direction) continue;
      if(events[j].status != FP_STATUS_CONFIRMED) continue;
      if(!events[j].has_confirm) continue;
      if(events[j].origin.index_anchor <= complete_anchor) continue;
      if(events[j].confirm.index_anchor <= complete_anchor) continue;
      if(best_index < 0 || events[j].confirm.index_anchor < events[best_index].confirm.index_anchor)
         best_index = j;
   }
   return (best_index >= 0);
}

void FP_LockF3WithFirstOppositeF1WithReport(FP_FlagEvent &events[],
                                            FP_F3LifecycleBuildReport &lock_report)
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(events[i].level != FP_LEVEL_F3) continue;
      if(!FP_F3StatusCanLock(events[i])) continue;
      if(events[i].status == FP_STATUS_LOCKED) continue;

      int best = -1;
      bool found = FP_FindFirstOppositeConfirmedF1After(events, n, events[i], best);
      FP_RecordF3LockScan(lock_report, found);
      if(!found) continue;

      events[i].status = FP_STATUS_LOCKED;
      events[i].extension_end = events[best].origin;
      events[i].has_extension = true;
      events[i].pos_extension_end = events[best].pos_origin;
      events[i].f3_locked = true;
      events[i].f3_lock_ready = true;
      events[i].f3_lock_event_id = events[best].event_id;
      events[i].f3_lock_reason = "locked_by_opposite_confirmed_F1_Q" + IntegerToString(events[best].event_id);
      FP_SetF3LifecycleState(events[i], FP_F3_LC_LOCKED, events[i].f3_lock_reason);
      FP_RecordF3LifecycleOutcome(events[i], lock_report);
   }
}

void FP_LockF3WithFirstOppositeF1(FP_FlagEvent &events[])
{
   FP_F3LifecycleBuildReport report;
   FP_ResetF3LifecycleBuildReport(report);
   FP_LockF3WithFirstOppositeF1WithReport(events, report);
}

#endif // __FP_F3_LIFECYCLE_ENGINE_MQH__
