#ifndef __FP_F2_LIFECYCLE_ENGINE_MQH__
#define __FP_F2_LIFECYCLE_ENGINE_MQH__
#property strict

#include "FP_F2LifecycleAudit.mqh"

// ============================================================================
// Phoenix Level 08 - F2 Lifecycle Engine
// ----------------------------------------------------------------------------
// Converts one lifecycle-confirmed F1 into a lifecycle-owned F2 child.  F3 may
// only consume F2 events whose f2_can_spawn_f3 gate is true.
// ============================================================================

bool FP_FindF2OriginFromParentWithReport(const FP_Node &nodes[],
                                         const int node_count,
                                         const FP_FlagEvent &f1,
                                         const FP_Config &cfg,
                                         int &origin_pos,
                                         FP_Node &origin,
                                         FP_F2LifecycleBuildReport &f2_report)
{
   origin_pos = -1;
   FP_ResetNode(origin);
   int to_pos = MathMax(f1.pos_leg2, f1.pos_confirm - 1);
   bool found = FP_FindDeepestAdverseNode(nodes,
                                          node_count,
                                          f1.pos_leg2 + 1,
                                          to_pos,
                                          f1.direction,
                                          cfg.boundary_epsilon_points,
                                          origin_pos,
                                          origin);
   FP_RecordF2OriginScan(f2_report, found);
   return found;
}

void FP_ApplyF2PostBodyLifecycleWithReport(FP_FlagEvent &f2,
                                           const FP_FlagEvent &f1,
                                           const FP_Node &nodes[],
                                           const int node_count,
                                           const FP_Config &cfg,
                                           FP_FlagBodyBuildReport &body_report,
                                           FP_InternalCountBuildReport &internal_report,
                                           FP_F2LifecycleBuildReport &f2_report)
{
   int before_ext = f2.leg2_extension_count;
   bool absorbed = FP_AbsorbPreInternalExtensionsWithReport(f2, nodes, node_count, cfg, internal_report);
   if(absorbed)
   {
      int absorbed_count = MathMax(0, f2.leg2_extension_count - before_ext);
      body_report.pre_internal_extensions_absorbed += absorbed_count;
      body_report.body_extended++;
      body_report.max_extension_count = MathMax(body_report.max_extension_count, f2.leg2_extension_count);
      f2.reason = f2.reason + ";f2_extension_absorption_pass_complete";
   }

   f2.parent_flag_size = f1.flag_size;
   f2.parent_leg1_L = f1.leg1_L;
   f2.size_ratio = (f1.flag_size > 0.0 ? f2.flag_size / f1.flag_size : 0.0);
   f2.f2_parent_size_ratio = f2.size_ratio;
   f2.f2_size_gate_passed = FP_F2SizeGatePasses(f2, f1, cfg);
   f2.f2_can_spawn_f3 = false;

   if(!f2.f2_size_gate_passed)
   {
      f2.status = FP_STATUS_LIVE_BODY;
      f2.render_kind = FP_RENDER_FLAG_BODY;
      f2.visible_main = cfg.f2_show_size_rejected_candidates;
      if(!f2.visible_main) f2.hidden_reason = "hidden_f2_size_below_parent_contract";
      FP_SetF2LifecycleState(f2, FP_F2_LC_SIZE_REJECTED, "size_gate_rejected_ratio_" + DoubleToString(f2.size_ratio, 4));
      return;
   }

   FP_InternalPack pack;
   int confirm_pos = -1;
   int invalid_pos = -1;
   int last_pos = -1;
   bool has_pack = FP_BuildPostFlagInternalPackWithReport(nodes, node_count, f2, cfg, pack, confirm_pos, invalid_pos, last_pos, internal_report);
   FP_CopyInternalPackToEvent(f2, pack);

   if(invalid_pos >= 0)
   {
      f2.invalid = nodes[invalid_pos];
      f2.has_invalid = true;
      f2.pos_invalid = invalid_pos;
      f2.status = FP_STATUS_INVALIDATED;
      f2.render_kind = FP_RENDER_FLAG_BODY;
      f2.visible_main = cfg.show_invalidated_in_audit;
      if(!f2.visible_main) f2.hidden_reason = "hidden_f2_invalidated_by_origin_break";
      FP_SetF2LifecycleState(f2, FP_F2_LC_INVALIDATED, "invalidated_by_strict_origin_break_before_confirmation");
      return;
   }

   if(has_pack && pack.valid12 && confirm_pos >= 0)
   {
      f2.confirm = nodes[confirm_pos];
      f2.has_confirm = true;
      f2.pos_confirm = confirm_pos;
      f2.status = FP_STATUS_CONFIRMED;
      f2.render_kind = FP_RENDER_FLAG_BODY;
      f2.f2_can_spawn_f3 = true;
      f2.visible_main = true;
      FP_SetF2LifecycleState(f2, FP_F2_LC_CONFIRMED, "confirmed_after_valid_internal12_and_favorable_break");
      return;
   }

   if(has_pack && (pack.valid12 || pack.has_valid12))
   {
      f2.status = FP_STATUS_POST_FLAG;
      f2.render_kind = FP_RENDER_FLAG_BODY;
      f2.visible_main = cfg.f2_show_post_flag_candidates;
      if(!f2.visible_main) f2.hidden_reason = "hidden_f2_post_flag_candidate";
      FP_SetF2LifecycleState(f2, FP_F2_LC_POST_FLAG, "valid_internal12_waiting_confirmation_break");
      return;
   }

   if(has_pack && pack.count > 0)
   {
      f2.status = FP_STATUS_POST_FLAG;
      f2.render_kind = FP_RENDER_FLAG_BODY;
      f2.visible_main = cfg.f2_show_post_flag_candidates;
      if(!f2.visible_main) f2.hidden_reason = "hidden_f2_developing_internal";
      FP_SetF2LifecycleState(f2, FP_F2_LC_POST_FLAG, "developing_internal_count_" + IntegerToString(pack.count));
      return;
   }

   f2.status = FP_STATUS_LIVE_BODY;
   f2.render_kind = FP_RENDER_FLAG_BODY;
   f2.visible_main = cfg.f2_show_live_body_candidates;
   if(!f2.visible_main) f2.hidden_reason = "hidden_f2_body_without_internal_count";
   FP_SetF2LifecycleState(f2, FP_F2_LC_CANDIDATE, "body_complete_without_post_flag_internal_count");
}

bool FP_BuildF2LifecycleFromF1WithReport(const FP_Node &nodes[],
                                         const int node_count,
                                         const FP_FlagEvent &f1,
                                         const int sequence_id,
                                         const int parent_event_id,
                                         const FP_Config &cfg,
                                         FP_FlagEvent &f2,
                                         FP_FlagBodyBuildReport &body_report,
                                         FP_InternalCountBuildReport &internal_report,
                                         FP_F2LifecycleBuildReport &f2_report)
{
   FP_ResetFlagEvent(f2);
   FP_RecordF2ParentAttempt(f1, f2_report);
   if(!FP_F2ParentGatePasses(f1))
      return false;

   int origin_pos = -1;
   FP_Node origin;
   if(!FP_FindF2OriginFromParentWithReport(nodes, node_count, f1, cfg, origin_pos, origin, f2_report))
      return false;

   bool body_ok = FP_FindFlagBodyFromOriginWithReport(nodes,
                                                      node_count,
                                                      origin_pos,
                                                      f1.direction,
                                                      FP_LEVEL_F2,
                                                      sequence_id,
                                                      parent_event_id,
                                                      cfg.boundary_epsilon_points,
                                                      f2,
                                                      body_report);
   if(!body_ok)
   {
      FP_RecordF2BodyMissing(f2_report);
      return false;
   }

   f2.chain_index = 2;
   f2.parent_sequence_id = f1.sequence_id;
   f2.parent_event_id = parent_event_id;
   f2.f2_parent_ready = true;
   f2.f2_origin_found = true;
   f2.f2_origin_scan_start_pos = f1.pos_leg2 + 1;
   f2.f2_lifecycle_scan_end_pos = f2.body_scan_end_pos;
   f2.from_phase_boundary = f1.from_phase_boundary;
   f2.from_fail_open = f1.from_fail_open;

   FP_ApplyF2PostBodyLifecycleWithReport(f2, f1, nodes, node_count, cfg, body_report, internal_report, f2_report);
   f2.f2_lifecycle_id = FP_BuildF2LifecycleId(f2);
   f2.visible_main = FP_F2ShouldBeVisibleForLifecycle(f2, cfg);
   if(!f2.visible_main && f2.hidden_reason == "")
      f2.hidden_reason = "hidden_by_f2_lifecycle_visibility_policy";
   FP_RecordF2LifecycleOutcome(f2, f2_report);
   return f2.visible_main;
}

bool FP_BuildF2LifecycleFromF1(const FP_Node &nodes[],
                               const int node_count,
                               const FP_FlagEvent &f1,
                               const int sequence_id,
                               const int parent_event_id,
                               const FP_Config &cfg,
                               FP_FlagEvent &f2)
{
   FP_FlagBodyBuildReport body_report;
   FP_ResetFlagBodyBuildReport(body_report);
   FP_SeedFlagBodyBuildReport(body_report, f1.scale_L, node_count, f1.direction, FP_LEVEL_F2);

   FP_InternalCountBuildReport internal_report;
   FP_ResetInternalCountBuildReport(internal_report);
   FP_SeedInternalCountBuildReport(internal_report, f1.scale_L, node_count);

   FP_F2LifecycleBuildReport f2_report;
   FP_ResetF2LifecycleBuildReport(f2_report);
   FP_SeedF2LifecycleBuildReport(f2_report, f1.scale_L, node_count);

   return FP_BuildF2LifecycleFromF1WithReport(nodes,
                                              node_count,
                                              f1,
                                              sequence_id,
                                              parent_event_id,
                                              cfg,
                                              f2,
                                              body_report,
                                              internal_report,
                                              f2_report);
}

#endif // __FP_F2_LIFECYCLE_ENGINE_MQH__
