#ifndef __FP_FLAG_BODY_ENGINE_MQH__
#define __FP_FLAG_BODY_ENGINE_MQH__
#property strict

#include "FP_FlagBodyAudit.mqh"

// ============================================================================
// Phoenix Flag Body Engine - Level 05
// ----------------------------------------------------------------------------
// A flag body is always two legs:
//   Origin -> Leg1 -> Waist -> Leg2
// Bullish:
//   LOW -> HIGH -> LOW -> HIGH, where Leg2 strictly breaks Leg1.
// Bearish:
//   HIGH -> LOW -> HIGH -> LOW, where Leg2 strictly breaks Leg1.
// This layer does not confirm F1 and does not authorize F2/F3.  It only emits a
// body-stage FP_FlagEvent plus structured audit evidence.
// ============================================================================

void FP_InitializeBodyEvent(FP_FlagEvent &event,
                            const FP_Node &origin,
                            const int origin_pos,
                            const int direction,
                            const int level,
                            const int sequence_id,
                            const int parent_event_id)
{
   FP_ResetFlagEvent(event);
   event.event_id = -1;
   event.sequence_id = sequence_id;
   event.parent_event_id = parent_event_id;
   event.parent_sequence_id = -1;
   event.chain_index = 0;
   event.scale_L = origin.L;
   event.direction = direction;
   event.level = level;
   event.status = FP_STATUS_SEED;
   event.branch_kind = FP_BRANCH_NONE;
   event.render_kind = FP_RENDER_PROBABLE;
   event.origin = origin;
   event.has_origin = true;
   event.pos_origin = origin_pos;
   event.body_scan_start_pos = origin_pos;
   event.body_scan_end_pos = origin_pos;
   FP_FinalizeBodyIdentity(event, FP_BODY_SEED, "origin_seed");
}

void FP_SetBodyLeg1(FP_FlagEvent &event, const FP_Node &leg1, const int pos_leg1)
{
   event.leg1 = leg1;
   event.has_leg1 = true;
   event.pos_leg1 = pos_leg1;
   event.leg1_L = leg1.L;
   event.status = FP_STATUS_LIVE_LEG;
   event.body_scan_end_pos = pos_leg1;
   FP_FinalizeBodyIdentity(event, FP_BODY_LIVE_LEG, "leg1_found");
}

void FP_SetBodyWaist(FP_FlagEvent &event, const FP_Node &waist, const int pos_waist)
{
   event.waist = waist;
   event.has_waist = true;
   event.pos_waist = pos_waist;
   event.status = FP_STATUS_LIVE_BODY;
   event.body_scan_end_pos = pos_waist;
   FP_FinalizeBodyIdentity(event, FP_BODY_LIVE_CORRECTION, "waist_found");
}

void FP_SetBodyLeg2(FP_FlagEvent &event, const FP_Node &leg2, const int pos_leg2)
{
   event.leg2 = leg2;
   event.has_leg2 = true;
   event.pos_leg2 = pos_leg2;
   event.flag_size = FP_FlagSize(event.origin, event.leg2);
   event.status = FP_STATUS_LIVE_BODY;
   event.render_kind = FP_RENDER_FLAG_BODY;
   event.body_scan_end_pos = pos_leg2;
   event.leg1_break_status = 1;
   FP_FinalizeBodyIdentity(event, FP_BODY_COMPLETE, "two_leg_body_complete");
}

bool FP_FindFlagBodyFromOriginWithReport(const FP_Node &nodes[],
                                         const int node_count,
                                         const int origin_pos,
                                         const int direction,
                                         const int level,
                                         const int sequence_id,
                                         const int parent_event_id,
                                         const double epsilon_points,
                                         FP_FlagEvent &event,
                                         FP_FlagBodyBuildReport &report)
{
   FP_ResetFlagEvent(event);
   FP_SeedFlagBodyBuildReport(report, (origin_pos >= 0 && origin_pos < node_count ? nodes[origin_pos].L : 0), node_count, direction, level);
   report.body_attempts++;

   if(origin_pos < 0 || origin_pos >= node_count)
   {
      report.invalid_origin_pos++;
      report.body_invalid++;
      FP_Node dummy; FP_ResetNode(dummy);
      FP_FlagBodyReportReason(report, dummy, "invalid_origin_pos", -1);
      return false;
   }

   double eps = FP_EpsilonPrice(epsilon_points);
   FP_Node origin = nodes[origin_pos];
   FP_InitializeBodyEvent(event, origin, origin_pos, direction, level, sequence_id, parent_event_id);

   if(!FP_NodeIsOriginKind(origin, direction))
   {
      report.origin_kind_mismatch++;
      report.body_invalid++;
      FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "origin_kind_mismatch");
      FP_FlagBodyReportReason(report, origin, "origin_kind_mismatch", origin_pos);
      return false;
   }

   int state = 0; // 0 seek Leg1, 1 seek Waist while Leg1 can extend, 2 seek Leg2 while Waist can deepen.
   FP_Node leg1; FP_ResetNode(leg1);
   FP_Node waist; FP_ResetNode(waist);
   int pos_leg1 = -1;
   int pos_waist = -1;

   for(int i=origin_pos + 1; i<node_count; i++)
   {
      event.body_scan_end_pos = i;
      FP_Node n = nodes[i];

      if(FP_BodyOriginInvalidatedByNode(n, origin, direction, eps))
      {
         report.origin_break_invalidations++;
         report.body_invalid++;
         event.invalid = n;
         event.has_invalid = true;
         event.pos_invalid = i;
         event.origin_hit_status = -1;
         event.status = FP_STATUS_INVALIDATED;
         event.visible_main = false;
         FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "origin_broken_before_body_complete");
         FP_FlagBodyReportReason(report, origin, "origin_broken_before_body_complete", i);
         return false;
      }

      if(state == 0)
      {
         if(FP_NodeIsLegKind(n, direction))
         {
            report.leg1_candidates++;
            leg1 = n;
            pos_leg1 = i;
            FP_SetBodyLeg1(event, leg1, pos_leg1);
            state = 1;
         }
         continue;
      }

      if(state == 1)
      {
         if(FP_NodeIsLegKind(n, direction))
         {
            if(FP_IsMoreFavorable(direction, n.price, leg1.price, eps))
            {
               report.leg1_extensions++;
               leg1 = n;
               pos_leg1 = i;
               FP_SetBodyLeg1(event, leg1, pos_leg1);
            }
            else if(FP_LegEqualsLeg1(n, leg1, eps))
            {
               // Equal to Leg1 is intentionally not a break and not an extension.
               report.leg2_equal_touches++;
            }
            continue;
         }

         if(FP_NodeIsOriginKind(n, direction))
         {
            if(!FP_WaistStaysInsideOrigin(n, origin, direction, eps))
            {
               report.origin_break_invalidations++;
               report.body_invalid++;
               event.invalid = n;
               event.has_invalid = true;
               event.pos_invalid = i;
               event.origin_hit_status = -1;
               event.status = FP_STATUS_INVALIDATED;
               event.visible_main = false;
               FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "waist_broke_origin_before_leg2");
               FP_FlagBodyReportReason(report, origin, "waist_broke_origin_before_leg2", i);
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
         if(FP_NodeIsOriginKind(n, direction))
         {
            if(!FP_WaistStaysInsideOrigin(n, origin, direction, eps))
            {
               report.origin_break_invalidations++;
               report.body_invalid++;
               event.invalid = n;
               event.has_invalid = true;
               event.pos_invalid = i;
               event.origin_hit_status = -1;
               event.status = FP_STATUS_INVALIDATED;
               event.visible_main = false;
               FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "waist_broke_origin_before_leg2");
               FP_FlagBodyReportReason(report, origin, "waist_broke_origin_before_leg2", i);
               return false;
            }
            if(FP_WaistEqualsOrigin(n, origin, eps)) report.waist_equal_origin_touches++;
            if(FP_IsMoreAdverse(direction, n.price, waist.price, eps))
            {
               report.waist_deepenings++;
               waist = n;
               pos_waist = i;
               FP_SetBodyWaist(event, waist, pos_waist);
            }
            continue;
         }

         if(FP_NodeIsLegKind(n, direction))
         {
            if(FP_LegEqualsLeg1(n, leg1, eps))
            {
               report.leg2_equal_touches++;
               continue;
            }
            if(FP_LegBreaksLeg1(n, leg1, direction, eps))
            {
               report.leg2_strict_breaks++;
               report.body_complete++;
               FP_SetBodyLeg2(event, n, i);
               event.reason = "two_leg_body";
               FP_FlagBodyReportReason(report, origin, "two_leg_body", i);
               return true;
            }
         }
      }
   }

   if(state == 0)
   {
      report.no_leg1++;
      report.body_invalid++;
      FP_FinalizeBodyIdentity(event, FP_BODY_INVALID, "no_leg1_after_origin");
      FP_FlagBodyReportReason(report, origin, "no_leg1_after_origin", event.body_scan_end_pos);
      return false;
   }

   if(state == 1)
   {
      report.no_waist++;
      report.body_live_leg++;
      // For F2/F3, probable leg display is useful; for F1 it is audit-only.
      if(level != FP_LEVEL_F1 && pos_leg1 >= 0)
      {
         report.probable_child_legs++;
         event.render_kind = FP_RENDER_PROBABLE;
         event.reason = "probable_child_leg_no_waist";
         FP_FinalizeBodyIdentity(event, FP_BODY_LIVE_LEG, "probable_child_leg_no_waist");
         FP_FlagBodyReportReason(report, origin, "probable_child_leg_no_waist", event.body_scan_end_pos);
         return true;
      }
      FP_FlagBodyReportReason(report, origin, "no_waist_after_leg1", event.body_scan_end_pos);
      return false;
   }

   report.no_leg2++;
   report.body_live_correction++;
   if(level != FP_LEVEL_F1 && pos_leg1 >= 0)
   {
      report.probable_child_legs++;
      event.render_kind = FP_RENDER_PROBABLE;
      event.reason = "probable_child_correction_no_leg2";
      FP_FinalizeBodyIdentity(event, FP_BODY_LIVE_CORRECTION, "probable_child_correction_no_leg2");
      FP_FlagBodyReportReason(report, origin, "probable_child_correction_no_leg2", event.body_scan_end_pos);
      return true;
   }
   FP_FlagBodyReportReason(report, origin, "no_leg2_strict_break", event.body_scan_end_pos);
   return false;
}

bool FP_FindFlagBodyFromOrigin(const FP_Node &nodes[],
                               const int node_count,
                               const int origin_pos,
                               const int direction,
                               const int level,
                               const int sequence_id,
                               const int parent_event_id,
                               const double epsilon_points,
                               FP_FlagEvent &event)
{
   FP_FlagBodyBuildReport report;
   FP_ResetFlagBodyBuildReport(report);
   return FP_FindFlagBodyFromOriginWithReport(nodes,
                                              node_count,
                                              origin_pos,
                                              direction,
                                              level,
                                              sequence_id,
                                              parent_event_id,
                                              epsilon_points,
                                              event,
                                              report);
}

bool FP_BodyBoundaryHitAfterEvent(const FP_Node &nodes[], const int node_count, const FP_FlagEvent &e, const int start_pos, const double boundary, const double epsilon_points, int &hit_pos)
{
   hit_pos = -1;
   double eps = FP_EpsilonPrice(epsilon_points);
   for(int i=start_pos; i<node_count; i++)
   {
      if(FP_NodeBreaksBoundary(nodes[i], e.direction, boundary, eps))
      {
         hit_pos = i;
         return true;
      }
   }
   return false;
}

#endif // __FP_FLAG_BODY_ENGINE_MQH__
