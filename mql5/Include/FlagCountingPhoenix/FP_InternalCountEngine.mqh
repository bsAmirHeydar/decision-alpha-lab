#ifndef __FP_INTERNAL_COUNT_ENGINE_MQH__
#define __FP_INTERNAL_COUNT_ENGINE_MQH__
#property strict

#include "FP_InternalCountAudit.mqh"

// ============================================================================
// Phoenix Level 06 - Internal Count Engine
// ----------------------------------------------------------------------------
// Builds the post-body adverse internal pack.  It is the bridge between a
// completed flag body and later lifecycle confirmation, but it does not own
// F1/F2/F3 sequence creation, visibility pruning, renderer labels, or F3 lock.
// ============================================================================

void FP_FinalizeInternalPackIdentity(const FP_FlagEvent &flag,
                                     FP_InternalPack &pack,
                                     const string status,
                                     const string reason)
{
   pack.status = status;
   if(pack.reason == "") pack.reason = reason;
   else if(reason != "") pack.reason = pack.reason + ";" + reason;
   pack.has_valid12 = pack.valid12;
   pack.branch_id_text = FP_BuildInternalBranchIdText(flag, pack);
   pack.internal_pack_id = FP_BuildInternalPackId(flag, pack);
}

void FP_MarkValid12(FP_InternalPack &pack, const FP_Node &n, const int pos)
{
   pack.valid12 = true;
   pack.has_valid12 = true;
   pack.first_valid12_node = n;
   pack.first_valid12_pos = pos;
}

// This function does not mutate the flag body. It returns post-flag count,
// confirmation/invalid position and the internal pack.  If a pre-1/2 extension
// occurs, the report stores it and the caller may absorb it into Leg2 before
// rebuilding the pack.
bool FP_BuildPostFlagInternalPackWithReport(const FP_Node &nodes[],
                                            const int node_count,
                                            const FP_FlagEvent &flag,
                                            const FP_Config &cfg,
                                            FP_InternalPack &pack,
                                            int &confirm_pos,
                                            int &invalid_pos,
                                            int &last_scanned_pos,
                                            FP_InternalCountBuildReport &report)
{
   FP_ResetInternalPack(pack);
   confirm_pos = -1;
   invalid_pos = -1;
   last_scanned_pos = flag.pos_leg2;

   report.bodies_seen++;
   if(flag.level == FP_LEVEL_F1) report.f1_bodies++;
   else if(flag.level == FP_LEVEL_F2) report.f2_bodies++;
   else if(flag.level == FP_LEVEL_F3) report.f3_bodies++;
   report.packs_attempted++;

   pack.branch_id = report.packs_attempted - 1;
   pack.scan_start_pos = (flag.pos_leg2 >= 0 ? flag.pos_leg2 + 1 : -1);
   pack.scan_end_pos = flag.pos_leg2;
   pack.confirm_pos = -1;
   pack.invalid_pos = -1;

   if(flag.pos_leg2 < 0)
   {
      FP_FinalizeInternalPackIdentity(flag, pack, "invalid_input", "missing_leg2");
      FP_CountInternalPackInReport(pack, report);
      return false;
   }

   if(flag.level == FP_LEVEL_F3)
   {
      // F3 completion is body-level/lifecycle-level in the current Phoenix
      // contract.  Internal scanning is not required to make F3 complete.
      report.f3_body_completed_without_pack++;
      last_scanned_pos = flag.pos_leg2;
      pack.scan_end_pos = flag.pos_leg2;
      FP_FinalizeInternalPackIdentity(flag, pack, "f3_body_only", "f3_does_not_require_post_body_internal_pack");
      FP_CountInternalPackInReport(pack, report);
      return true;
   }

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   int adverse_kind = FP_AdverseKindForDirection(flag.direction);
   int max_internal = FP_MAX_INTERNAL_NODES;
   int last_adverse_pos = -1;
   bool have_valid12 = false;

   for(int i=flag.pos_leg2 + 1; i<node_count; i++)
   {
      last_scanned_pos = i;
      pack.scan_end_pos = i;
      FP_Node n = nodes[i];

      if(FP_InternalInvalidationBreaks(flag, n, eps))
      {
         invalid_pos = i;
         pack.invalid_pos = i;
         FP_FinalizeInternalPackIdentity(flag, pack, "invalidated", "strict_" + FP_InternalInvalidationBoundaryName(flag.level) + "_break_before_confirmation");
         FP_CountInternalPackInReport(pack, report);
         return (pack.count > 0);
      }

      if(FP_NodeBreaksFlagEnd(n, flag.direction, flag.leg2.price, eps))
      {
         if(have_valid12)
         {
            confirm_pos = i;
            pack.confirm_pos = i;
            FP_FinalizeInternalPackIdentity(flag, pack, "confirmation_ready", "favorable_break_after_valid12");
            FP_CountInternalPackInReport(pack, report);
            return true;
         }

         // Before valid 1/2 this is body extension in the contract, not
         // confirmation.  Keep evidence in the pack; a stricter caller can
         // absorb the extension and rebuild from the new Leg2 endpoint.
         if(!pack.has_pre_internal_leg2_extension)
         {
            pack.pre_internal_leg2_extension_node = n;
            pack.has_pre_internal_leg2_extension = true;
            pack.pre_internal_leg2_extension_pos = i;
         }
         continue;
      }

      if(n.kind != adverse_kind) continue;
      if(pack.count >= max_internal) continue;

      int next_num = pack.count + 1;
      if(next_num > 1 && !FP_InternalNodeIsMoreAdverseThanPrevious(pack, next_num, n, flag.direction, eps))
      {
         report.non_deeper_rejected++;
         continue;
      }

      if(next_num > 1 && last_adverse_pos >= 0)
      {
         FP_Node mid;
         bool has_mid = FP_FindBestMiddleBetween(nodes, last_adverse_pos, i, flag.direction, eps, mid);
         if(!has_mid)
         {
            report.missing_middle_rejected++;
            continue;
         }

         if(flag.level == FP_LEVEL_F1 && next_num == 2)
         {
            pack.middle_opposite_node = mid;
            pack.has_middle_opposite_node = true;
            pack.middle_opposite_breaks_leg2 = FP_NodeBreaksFlagEnd(mid, flag.direction, flag.leg2.price, eps);
            if(!FP_F1MiddleNodeAllowed(mid, flag, eps))
            {
               report.f1_middle_rejected++;
               continue;
            }
         }

         FP_SetInternalMid(pack, next_num - 1, mid);
      }

      FP_SetInternalNode(pack, next_num, n);
      pack.count = next_num;
      last_adverse_pos = i;

      if(pack.count >= 2 && !have_valid12)
      {
         FP_MarkValid12(pack, n, i);
         have_valid12 = true;
      }
      if(pack.count == 3 || pack.count == 4)
      {
         pack.is_nd = true;
      }
   }

   string status = (pack.count <= 0 ? "post_flag_no_count" : (pack.valid12 ? "valid12_waiting_confirm" : "developing_internal"));
   FP_FinalizeInternalPackIdentity(flag, pack, status, "scan_ended_without_confirmation");
   FP_CountInternalPackInReport(pack, report);
   return (pack.count > 0);
}

bool FP_BuildPostFlagInternalPack(const FP_Node &nodes[],
                                  const int node_count,
                                  const FP_FlagEvent &flag,
                                  const FP_Config &cfg,
                                  FP_InternalPack &pack,
                                  int &confirm_pos,
                                  int &invalid_pos,
                                  int &last_scanned_pos)
{
   FP_InternalCountBuildReport report;
   FP_ResetInternalCountBuildReport(report);
   FP_SeedInternalCountBuildReport(report, flag.scale_L, node_count);
   return FP_BuildPostFlagInternalPackWithReport(nodes, node_count, flag, cfg, pack, confirm_pos, invalid_pos, last_scanned_pos, report);
}

// Finds the first flag-end break that happens before a valid internal 1/2
// exists.  This formalizes the extension rule: a favorable break before valid
// 1/2 is not confirmation and must be folded back into current body as Leg2.
bool FP_FindPreInternalExtensionBreakWithReport(const FP_Node &nodes[],
                                                const int node_count,
                                                const FP_FlagEvent &flag,
                                                const FP_Config &cfg,
                                                int &extension_pos,
                                                FP_InternalCountBuildReport &report)
{
   extension_pos = -1;
   if(flag.pos_leg2 < 0) return false;
   if(flag.level == FP_LEVEL_F3) return false;

   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   int adverse_kind = FP_AdverseKindForDirection(flag.direction);
   int last_adverse_pos = -1;
   int count = 0;

   FP_InternalPack pack;
   FP_ResetInternalPack(pack);

   for(int i=flag.pos_leg2 + 1; i<node_count; i++)
   {
      FP_Node n = nodes[i];

      if(FP_InternalInvalidationBreaks(flag, n, eps)) return false;

      if(FP_NodeBreaksFlagEnd(n, flag.direction, flag.leg2.price, eps))
      {
         if(count < 2)
         {
            extension_pos = i;
            report.pre_internal_extensions_seen++;
            return true;
         }
         return false;
      }

      if(n.kind != adverse_kind) continue;
      if(count >= FP_MAX_INTERNAL_NODES) continue;

      int next_num = count + 1;
      if(next_num > 1 && !FP_InternalNodeIsMoreAdverseThanPrevious(pack, next_num, n, flag.direction, eps)) continue;
      if(next_num > 1 && last_adverse_pos >= 0)
      {
         FP_Node mid;
         bool has_mid = FP_FindBestMiddleBetween(nodes, last_adverse_pos, i, flag.direction, eps, mid);
         if(!has_mid) continue;
         if(flag.level == FP_LEVEL_F1 && next_num == 2)
         {
            if(!FP_F1MiddleNodeAllowed(mid, flag, eps)) continue;
         }
      }

      FP_SetInternalNode(pack, next_num, n);
      count = next_num;
      last_adverse_pos = i;
      if(count >= 2) return false;
   }
   return false;
}

bool FP_FindPreInternalExtensionBreak(const FP_Node &nodes[],
                                      const int node_count,
                                      const FP_FlagEvent &flag,
                                      const FP_Config &cfg,
                                      int &extension_pos)
{
   FP_InternalCountBuildReport report;
   FP_ResetInternalCountBuildReport(report);
   FP_SeedInternalCountBuildReport(report, flag.scale_L, node_count);
   return FP_FindPreInternalExtensionBreakWithReport(nodes, node_count, flag, cfg, extension_pos, report);
}

void FP_SetEventLeg2(FP_FlagEvent &event, const FP_Node &new_leg2, const int new_pos)
{
   event.leg2 = new_leg2;
   event.has_leg2 = true;
   event.pos_leg2 = new_pos;
   event.flag_size = FP_FlagSize(event.origin, event.leg2);
   event.leg2_extension_count++;
   event.body_scan_end_pos = new_pos;
   FP_FinalizeBodyIdentity(event, FP_BODY_EXTENDED, "pre_internal_leg2_extension_absorbed");
   event.reason = event.reason + ";absorbed_pre_internal_leg2_extension_to_node_" + IntegerToString(new_leg2.id);
}

bool FP_AbsorbPreInternalExtensionsWithReport(FP_FlagEvent &event,
                                              const FP_Node &nodes[],
                                              const int node_count,
                                              const FP_Config &cfg,
                                              FP_InternalCountBuildReport &report)
{
   if(!cfg.absorb_pre_internal_extensions) return false;
   if(event.level == FP_LEVEL_F3) return false;
   if(!event.has_leg2) return false;

   bool changed = false;
   int guard = 0;
   while(guard < 64)
   {
      guard++;
      int extension_pos = -1;
      if(!FP_FindPreInternalExtensionBreakWithReport(nodes, node_count, event, cfg, extension_pos, report)) break;
      if(extension_pos <= event.pos_leg2 || extension_pos >= node_count) break;
      FP_SetEventLeg2(event, nodes[extension_pos], extension_pos);
      report.pre_internal_extensions_absorbed++;
      report.max_extension_count = MathMax(report.max_extension_count, event.leg2_extension_count);
      changed = true;
   }
   return changed;
}

bool FP_AbsorbPreInternalExtensions(FP_FlagEvent &event,
                                    const FP_Node &nodes[],
                                    const int node_count,
                                    const FP_Config &cfg)
{
   FP_InternalCountBuildReport report;
   FP_ResetInternalCountBuildReport(report);
   FP_SeedInternalCountBuildReport(report, event.scale_L, node_count);
   return FP_AbsorbPreInternalExtensionsWithReport(event, nodes, node_count, cfg, report);
}

void FP_CopyInternalPackToEvent(FP_FlagEvent &e, const FP_InternalPack &pack)
{
   e.internal_pack = pack;
}

#endif // __FP_INTERNAL_COUNT_ENGINE_MQH__
