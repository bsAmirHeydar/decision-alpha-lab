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
   if(!f2.has_confirm || f2.pos_confirm <= f2.pos_leg2 + 1)
   {
      FP_RecordF3OriginScan(f3_report, false);
      return false;
   }

   int from_pos = f2.pos_leg2 + 1;
   int to_pos = f2.pos_confirm - 1;
   bool found = FP_FindDeepestAdverseNode(nodes,
                                          node_count,
                                          from_pos,
                                          to_pos,
                                          f2.direction,
                                          cfg.boundary_epsilon_points,
                                          origin_pos,
                                          origin);
   FP_RecordF3OriginScan(f3_report, found);
   return found;
}


bool FP_FindF3BodyFromOriginAfterParentConfirmWithReport(const FP_Node &nodes[],
                                                        const int node_count,
                                                        const int origin_pos,
                                                        const FP_FlagEvent &f2,
                                                        const int sequence_id,
                                                        const int parent_event_id,
                                                        const FP_Config &cfg,
                                                        FP_FlagEvent &event,
                                                        FP_FlagBodyBuildReport &report)
{
   FP_ResetFlagEvent(event);
   FP_SeedFlagBodyBuildReport(report, (origin_pos >= 0 && origin_pos < node_count ? nodes[origin_pos].L : 0), node_count, f2.direction, FP_LEVEL_F3);
   report.body_attempts++;

   if(origin_pos < 0 || origin_pos >= node_count)
   {
      report.invalid_origin_pos++;
      report.body_invalid++;
      FP_Node dummy; FP_ResetNode(dummy);
      FP_FlagBodyReportReason(report, dummy, "f3_invalid_origin_pos", -1);
      return false;
   }

   if(!f2.has_confirm || f2.pos_confirm <= f2.pos_leg2 || f2.pos_confirm <= origin_pos || f2.pos_confirm >= node_count)
   {
      report.no_leg1++;
      report.body_invalid++;
      FP_Node dummy; FP_ResetNode(dummy);
      FP_FlagBodyReportReason(report, dummy, "f3_parent_f2_not_confirmed_before_body_start", f2.pos_confirm);
      return false;
   }

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   FP_Node origin = nodes[origin_pos];
   FP_InitializeBodyEvent(event, origin, origin_pos, f2.direction, FP_LEVEL_F3, sequence_id, parent_event_id);

   if(!FP_NodeIsOriginKind(origin, f2.direction))
   {
      report.origin_kind_mismatch++;
      report.body_invalid++;
      FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "f3_origin_kind_mismatch");
      FP_FlagBodyReportReason(report, origin, "f3_origin_kind_mismatch", origin_pos);
      return false;
   }

   FP_Node leg1 = f2.confirm;
   int pos_leg1 = f2.pos_confirm;
   if(!FP_NodeIsLegKind(leg1, f2.direction))
   {
      report.no_leg1++;
      report.body_invalid++;
      FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "f3_parent_confirm_not_leg_kind");
      FP_FlagBodyReportReason(report, origin, "f3_parent_confirm_not_leg_kind", pos_leg1);
      return false;
   }

   // F3-specific contract:
   // F2 is not complete until its own flag-end has been re-hit/confirmed.
   // Therefore the first leg of F3 is forced to the F2 confirmation node.
   // Any favorable node between the F3 origin and the F2 confirmation belongs
   // to the still-unfinished F2 correction/hit process and must not become F3
   // Leg1.  After that forced Leg1, normal body rules resume.
   report.leg1_candidates++;
   FP_SetBodyLeg1(event, leg1, pos_leg1);

   int state = 1; // 1 seek Waist while Leg1 can extend, 2 seek Leg2 while Waist can deepen.
   FP_Node waist; FP_ResetNode(waist);
   int pos_waist = -1;

   for(int i=pos_leg1 + 1; i<node_count; i++)
   {
      event.body_scan_end_pos = i;
      FP_Node n = nodes[i];

      if(FP_BodyOriginInvalidatedByNode(n, origin, f2.direction, eps))
      {
         report.origin_break_invalidations++;
         report.body_invalid++;
         event.invalid = n;
         event.has_invalid = true;
         event.pos_invalid = i;
         event.origin_hit_status = -1;
         event.status = FP_STATUS_INVALIDATED;
         event.visible_main = false;
         FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "f3_origin_broken_after_parent_confirm_before_body_complete");
         FP_FlagBodyReportReason(report, origin, "f3_origin_broken_after_parent_confirm_before_body_complete", i);
         return false;
      }

      if(state == 1)
      {
         if(FP_NodeIsLegKind(n, f2.direction))
         {
            if(FP_IsMoreFavorable(f2.direction, n.price, leg1.price, eps))
            {
               report.leg1_extensions++;
               leg1 = n;
               pos_leg1 = i;
               FP_SetBodyLeg1(event, leg1, pos_leg1);
            }
            else if(FP_LegEqualsLeg1(n, leg1, eps))
            {
               report.leg2_equal_touches++;
            }
            continue;
         }

         if(FP_NodeIsOriginKind(n, f2.direction))
         {
            if(!FP_WaistStaysInsideOrigin(n, origin, f2.direction, eps))
            {
               report.origin_break_invalidations++;
               report.body_invalid++;
               event.invalid = n;
               event.has_invalid = true;
               event.pos_invalid = i;
               event.origin_hit_status = -1;
               event.status = FP_STATUS_INVALIDATED;
               event.visible_main = false;
               FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "f3_waist_broke_origin_before_leg2");
               FP_FlagBodyReportReason(report, origin, "f3_waist_broke_origin_before_leg2", i);
               return false;
            }
            report.waist_candidates++;
            if(FP_WaistEqualsOrigin(n, origin, eps)) report.waist_equal_origin_touches++;
            waist = n;
            pos_waist = i;
            FP_SetBodyWaist(event, waist, pos_waist);
            state = 2;
            continue;
         }
      }

      if(state == 2)
      {
         if(FP_NodeIsOriginKind(n, f2.direction))
         {
            if(!FP_WaistStaysInsideOrigin(n, origin, f2.direction, eps))
            {
               report.origin_break_invalidations++;
               report.body_invalid++;
               event.invalid = n;
               event.has_invalid = true;
               event.pos_invalid = i;
               event.origin_hit_status = -1;
               event.status = FP_STATUS_INVALIDATED;
               event.visible_main = false;
               FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "f3_waist_broke_origin_before_leg2");
               FP_FlagBodyReportReason(report, origin, "f3_waist_broke_origin_before_leg2", i);
               return false;
            }
            if(FP_WaistEqualsOrigin(n, origin, eps)) report.waist_equal_origin_touches++;
            if(FP_IsMoreAdverse(f2.direction, n.price, waist.price, eps))
            {
               report.waist_deepenings++;
               waist = n;
               pos_waist = i;
               FP_SetBodyWaist(event, waist, pos_waist);
            }
            continue;
         }

         if(FP_NodeIsLegKind(n, f2.direction))
         {
            if(FP_LegEqualsLeg1(n, leg1, eps))
            {
               report.leg2_equal_touches++;
               continue;
            }
            if(FP_LegBreaksLeg1(n, leg1, f2.direction, eps))
            {
               report.leg2_strict_breaks++;
               report.body_complete++;
               FP_SetBodyLeg2(event, n, i);
               event.reason = "f3_two_leg_body_after_parent_f2_confirm";
               FP_FlagBodyReportReason(report, origin, "f3_two_leg_body_after_parent_f2_confirm", i);
               return true;
            }
         }
      }
   }

   if(state == 1)
   {
      report.no_waist++;
      report.body_live_leg++;
      report.probable_child_legs++;
      event.render_kind = FP_RENDER_PROBABLE;
      event.reason = "f3_probable_child_leg_after_parent_confirm_no_waist";
      FP_FinalizeBodyIdentity(event, FP_BODY_LIVE_LEG, "f3_probable_child_leg_after_parent_confirm_no_waist");
      FP_FlagBodyReportReason(report, origin, "f3_probable_child_leg_after_parent_confirm_no_waist", event.body_scan_end_pos);
      return true;
   }

   report.no_leg2++;
   report.body_live_correction++;
   report.probable_child_legs++;
   event.render_kind = FP_RENDER_PROBABLE;
   event.reason = "f3_probable_child_correction_after_parent_confirm_no_leg2";
   FP_FinalizeBodyIdentity(event, FP_BODY_LIVE_CORRECTION, "f3_probable_child_correction_after_parent_confirm_no_leg2");
   FP_FlagBodyReportReason(report, origin, "f3_probable_child_correction_after_parent_confirm_no_leg2", event.body_scan_end_pos);
   return true;
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
   bool body_complete = (f3.has_origin && f3.has_leg1 && f3.has_waist && f3.has_leg2 &&
                         (f3.body_status == FP_BODY_COMPLETE || f3.body_status == FP_BODY_EXTENDED));
   f3.f3_size_gate_passed = (body_complete ? FP_F3SizeGatePasses(f3, f2, cfg) : false);
   f3.f3_leg1_L_gate_passed = (body_complete ? FP_F3Leg1LGatePasses(f3, f2, cfg) : false);
   f3.f3_or_gate_passed = (body_complete && (f3.f3_size_gate_passed || f3.f3_leg1_L_gate_passed));
   f3.f3_terminal_complete = false;
   f3.f3_lock_ready = false;
   f3.f3_locked = false;
   f3.f3_lock_event_id = -1;
   f3.f3_lock_reason = "";

   if(!body_complete)
   {
      f3.status = (f3.has_waist ? FP_STATUS_LIVE_BODY : FP_STATUS_LIVE_LEG);
      f3.render_kind = FP_RENDER_PROBABLE;
      f3.visible_main = cfg.f3_show_live_body_candidates;
      if(!f3.visible_main) f3.hidden_reason = "hidden_f3_body_not_complete";
      FP_SetF3LifecycleState(f3, FP_F3_LC_BODY_MISSING, "body_waiting_after_parent_f2_confirm");
      FP_RecordF3LifecycleOutcome(f3, f3_report);
      return;
   }

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

   bool body_ok = FP_FindF3BodyFromOriginAfterParentConfirmWithReport(nodes,
                                                                  node_count,
                                                                  origin_pos,
                                                                  f2,
                                                                  sequence_id,
                                                                  parent_event_id,
                                                                  cfg,
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
   f3.reason = f3.reason + ";f3_origin_backfilled_between_f2_leg2_and_f2_confirm;f3_leg1_forced_to_f2_confirm";
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
