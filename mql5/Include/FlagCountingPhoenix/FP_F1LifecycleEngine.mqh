#ifndef __FP_F1_LIFECYCLE_ENGINE_MQH__
#define __FP_F1_LIFECYCLE_ENGINE_MQH__
#property strict

#include "FP_F1LifecycleAudit.mqh"

// ============================================================================
// Phoenix Level 07 - F1 Lifecycle Engine
// ----------------------------------------------------------------------------
// Converts audited Level 05 bodies and Level 06 internal packs into one
// lifecycle-owned F1 root.  F2/F3 construction is deliberately outside this
// file and may only consume lifecycle_can_spawn_f2 F1 roots.
// ============================================================================

void FP_ApplyF1PostBodyLifecycleWithReport(FP_FlagEvent &f1,
                                           const FP_Node &nodes[],
                                           const int node_count,
                                           const FP_Config &cfg,
                                           FP_FlagBodyBuildReport &body_report,
                                           FP_InternalCountBuildReport &internal_report,
                                           FP_F1LifecycleBuildReport &f1_report)
{
   int before_ext = f1.leg2_extension_count;
   bool absorbed = FP_AbsorbPreInternalExtensionsWithReport(f1, nodes, node_count, cfg, internal_report);
   if(absorbed)
   {
      int absorbed_count = MathMax(0, f1.leg2_extension_count - before_ext);
      body_report.pre_internal_extensions_absorbed += absorbed_count;
      body_report.body_extended++;
      body_report.max_extension_count = MathMax(body_report.max_extension_count, f1.leg2_extension_count);
      f1.reason = f1.reason + ";f1_extension_absorption_pass_complete";
   }

   FP_InternalPack pack;
   int confirm_pos = -1;
   int invalid_pos = -1;
   int last_pos = -1;
   bool has_pack = FP_BuildPostFlagInternalPackWithReport(nodes, node_count, f1, cfg, pack, confirm_pos, invalid_pos, last_pos, internal_report);
   FP_CopyInternalPackToEvent(f1, pack);

   f1.lifecycle_can_spawn_f2 = false;

   if(invalid_pos >= 0)
   {
      f1.invalid = nodes[invalid_pos];
      f1.has_invalid = true;
      f1.pos_invalid = invalid_pos;
      f1.status = FP_STATUS_INVALIDATED;
      f1.visible_main = cfg.show_invalidated_in_audit;
      f1.render_kind = FP_RENDER_FLAG_BODY;
      FP_SetF1LifecycleState(f1, FP_F1_LC_INVALIDATED, "invalidated_by_strict_waist_break_before_confirmation");
      return;
   }

   if(has_pack && pack.valid12 && confirm_pos >= 0)
   {
      f1.confirm = nodes[confirm_pos];
      f1.has_confirm = true;
      f1.pos_confirm = confirm_pos;
      f1.status = FP_STATUS_CONFIRMED;
      f1.render_kind = FP_RENDER_FLAG_BODY;
      f1.lifecycle_can_spawn_f2 = true;
      f1.visible_main = true;
      FP_SetF1LifecycleState(f1, FP_F1_LC_CONFIRMED, "confirmed_after_valid_internal12_and_favorable_break");
      return;
   }

   if(has_pack && (pack.valid12 || pack.has_valid12))
   {
      f1.status = FP_STATUS_POST_FLAG;
      f1.render_kind = FP_RENDER_FLAG_BODY;
      f1.visible_main = cfg.f1_show_post_flag_candidates;
      FP_SetF1LifecycleState(f1, FP_F1_LC_POST_FLAG, "valid_internal12_waiting_confirmation_break");
      return;
   }

   if(has_pack && pack.count > 0)
   {
      f1.status = FP_STATUS_POST_FLAG;
      f1.render_kind = FP_RENDER_FLAG_BODY;
      f1.visible_main = cfg.f1_show_post_flag_candidates;
      FP_SetF1LifecycleState(f1, FP_F1_LC_POST_FLAG, "developing_internal_count_" + IntegerToString(pack.count));
      return;
   }

   f1.status = FP_STATUS_LIVE_BODY;
   f1.render_kind = FP_RENDER_FLAG_BODY;
   f1.visible_main = cfg.f1_show_live_body_candidates;
   FP_SetF1LifecycleState(f1, FP_F1_LC_CANDIDATE, "body_complete_without_post_flag_internal_count");
}

bool FP_BuildF1LifecycleFromOriginWithReport(const FP_Node &nodes[],
                                             const int node_count,
                                             const int origin_pos,
                                             const int direction,
                                             const int sequence_id,
                                             const bool from_phase_boundary,
                                             const bool from_fail_open,
                                             const FP_Config &cfg,
                                             FP_FlagEvent &f1,
                                             FP_FlagBodyBuildReport &body_report,
                                             FP_InternalCountBuildReport &internal_report,
                                             FP_F1LifecycleBuildReport &f1_report)
{
   FP_ResetFlagEvent(f1);
   FP_RecordF1OriginAttempt(f1_report, from_phase_boundary, from_fail_open);

   bool phase_ok = FP_F1PhaseGatePasses(from_phase_boundary, from_fail_open, cfg);
   if(phase_ok) f1_report.phase_gate_passed++;
   if(!phase_ok)
   {
      FP_RecordF1PhaseRejected(f1_report);
      return false;
   }

   bool body_ok = FP_FindFlagBodyFromOriginWithReport(nodes,
                                                      node_count,
                                                      origin_pos,
                                                      direction,
                                                      FP_LEVEL_F1,
                                                      sequence_id,
                                                      -1,
                                                      cfg.boundary_epsilon_points,
                                                      f1,
                                                      body_report);
   if(!body_ok)
   {
      FP_RecordF1BodyMissing(f1_report);
      return false;
   }

   f1.from_phase_boundary = from_phase_boundary;
   f1.from_fail_open = from_fail_open;
   f1.lifecycle_phase_gate_passed = true;
   f1.chain_index = 1;
   f1.parent_event_id = -1;
   f1.parent_sequence_id = -1;

   FP_ApplyF1PostBodyLifecycleWithReport(f1, nodes, node_count, cfg, body_report, internal_report, f1_report);
   f1.lifecycle_id = FP_BuildF1LifecycleId(f1);
   f1.visible_main = FP_F1ShouldBeVisibleForLifecycle(f1, cfg);
   if(!f1.visible_main && f1.hidden_reason == "")
      f1.hidden_reason = "hidden_by_f1_lifecycle_visibility_policy";
   FP_RecordF1LifecycleOutcome(f1, f1_report);
   return f1.visible_main;
}

bool FP_BuildF1LifecycleFromOrigin(const FP_Node &nodes[],
                                   const int node_count,
                                   const int origin_pos,
                                   const int direction,
                                   const int sequence_id,
                                   const bool from_phase_boundary,
                                   const bool from_fail_open,
                                   const FP_Config &cfg,
                                   FP_FlagEvent &f1)
{
   FP_FlagBodyBuildReport body_report;
   FP_ResetFlagBodyBuildReport(body_report);
   FP_SeedFlagBodyBuildReport(body_report, (origin_pos >= 0 && origin_pos < node_count ? nodes[origin_pos].L : 0), node_count, direction, FP_LEVEL_F1);

   FP_InternalCountBuildReport internal_report;
   FP_ResetInternalCountBuildReport(internal_report);
   FP_SeedInternalCountBuildReport(internal_report, (origin_pos >= 0 && origin_pos < node_count ? nodes[origin_pos].L : 0), node_count);

   FP_F1LifecycleBuildReport f1_report;
   FP_ResetF1LifecycleBuildReport(f1_report);
   FP_SeedF1LifecycleBuildReport(f1_report, (origin_pos >= 0 && origin_pos < node_count ? nodes[origin_pos].L : 0), node_count);

   return FP_BuildF1LifecycleFromOriginWithReport(nodes,
                                                  node_count,
                                                  origin_pos,
                                                  direction,
                                                  sequence_id,
                                                  from_phase_boundary,
                                                  from_fail_open,
                                                  cfg,
                                                  f1,
                                                  body_report,
                                                  internal_report,
                                                  f1_report);
}

#endif // __FP_F1_LIFECYCLE_ENGINE_MQH__
