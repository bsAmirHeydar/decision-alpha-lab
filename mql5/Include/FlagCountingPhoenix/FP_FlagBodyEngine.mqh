#ifndef __FP_FLAG_BODY_ENGINE_MQH__
#define __FP_FLAG_BODY_ENGINE_MQH__
#property strict

#include "FP_HookEngine.mqh"

// ============================================================================
// Phoenix Flag Body Engine
// ----------------------------------------------------------------------------
// A flag body is always two legs:
//   Origin -> Leg1 -> Waist -> Leg2
// Bullish:
//   Origin = LOW, Leg1 = highest HIGH before correction, Waist = deepest LOW
//   after Leg1 that does not break Origin, Leg2 = HIGH that breaks Leg1.
// Bearish is symmetric.
// ============================================================================

bool FP_NodeIsOriginKind(const FP_Node &n, const int direction)
{
   return (n.kind == FP_OriginKindForDirection(direction));
}

bool FP_NodeIsLegKind(const FP_Node &n, const int direction)
{
   return (n.kind == FP_OppositeKind(FP_OriginKindForDirection(direction)));
}

bool FP_WaistStaysInsideOrigin(const FP_Node &waist, const FP_Node &origin, const int direction, const double eps)
{
   if(direction == FP_DIR_BULLISH) return !FP_BreaksBelow(waist.price, origin.price, eps);
   if(direction == FP_DIR_BEARISH) return !FP_BreaksAbove(waist.price, origin.price, eps);
   return false;
}

bool FP_BodyOriginInvalidatedByNode(const FP_Node &n, const FP_Node &origin, const int direction, const double eps)
{
   if(direction == FP_DIR_BULLISH) return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, origin.price, eps));
   if(direction == FP_DIR_BEARISH) return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, origin.price, eps));
   return false;
}

bool FP_LegBreaksLeg1(const FP_Node &n, const FP_Node &leg1, const int direction, const double eps)
{
   if(direction == FP_DIR_BULLISH) return (n.kind == FP_NODE_HIGH && FP_BreaksAbove(n.price, leg1.price, eps));
   if(direction == FP_DIR_BEARISH) return (n.kind == FP_NODE_LOW && FP_BreaksBelow(n.price, leg1.price, eps));
   return false;
}

bool FP_LegExtendsLeg1(const FP_Node &n, const FP_Node &leg1, const int direction, const double eps)
{
   return FP_LegBreaksLeg1(n, leg1, direction, eps);
}

double FP_FlagSize(const FP_Node &origin, const FP_Node &leg2)
{
   return MathAbs(leg2.price - origin.price);
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
   FP_ResetFlagEvent(event);
   if(origin_pos < 0 || origin_pos >= node_count) return false;

   double eps = FP_EpsilonPrice(epsilon_points);
   FP_Node origin = nodes[origin_pos];
   if(!FP_NodeIsOriginKind(origin, direction)) return false;

   int state = 0; // 0: seek leg1, 1: seek waist while leg1 can extend, 2: seek leg2 while waist can deepen
   FP_Node leg1; FP_ResetNode(leg1);
   FP_Node waist; FP_ResetNode(waist);
   int pos_leg1 = -1;
   int pos_waist = -1;

   for(int i=origin_pos + 1; i<node_count; i++)
   {
      FP_Node n = nodes[i];

      if(FP_BodyOriginInvalidatedByNode(n, origin, direction, eps))
      {
         return false;
      }

      if(state == 0)
      {
         if(FP_NodeIsLegKind(n, direction))
         {
            leg1 = n;
            pos_leg1 = i;
            state = 1;
         }
         continue;
      }

      if(state == 1)
      {
         if(FP_NodeIsLegKind(n, direction) && FP_IsMoreFavorable(direction, n.price, leg1.price, eps))
         {
            leg1 = n;
            pos_leg1 = i;
            continue;
         }

         if(FP_NodeIsOriginKind(n, direction))
         {
            if(!FP_WaistStaysInsideOrigin(n, origin, direction, eps)) return false;
            waist = n;
            pos_waist = i;
            state = 2;
            continue;
         }
      }

      if(state == 2)
      {
         if(FP_NodeIsOriginKind(n, direction))
         {
            if(!FP_WaistStaysInsideOrigin(n, origin, direction, eps)) return false;
            if(FP_IsMoreAdverse(direction, n.price, waist.price, eps))
            {
               waist = n;
               pos_waist = i;
            }
            continue;
         }

         if(FP_LegBreaksLeg1(n, leg1, direction, eps))
         {
            event.event_id = -1;
            event.sequence_id = sequence_id;
            event.parent_event_id = parent_event_id;
            event.parent_sequence_id = -1;
            event.chain_index = 0;
            event.scale_L = origin.L;
            event.direction = direction;
            event.level = level;
            event.status = FP_STATUS_LIVE_BODY;
            event.branch_kind = FP_BRANCH_NONE;
            event.render_kind = FP_RENDER_FLAG_BODY;

            event.origin = origin;
            event.leg1 = leg1;
            event.waist = waist;
            event.leg2 = n;
            event.has_origin = true;
            event.has_leg1 = true;
            event.has_waist = true;
            event.has_leg2 = true;
            event.pos_origin = origin_pos;
            event.pos_leg1 = pos_leg1;
            event.pos_waist = pos_waist;
            event.pos_leg2 = i;
            event.flag_size = FP_FlagSize(origin, n);
            event.leg1_L = leg1.L;
            event.reason = "two_leg_body";
            return true;
         }
      }
   }

   // For F2/F3 we want probable leg display. If there is at least origin and leg1,
   // expose a seed/live-leg event so the development stage is auditable.
   if(level != FP_LEVEL_F1 && pos_leg1 >= 0)
   {
      event.event_id = -1;
      event.sequence_id = sequence_id;
      event.parent_event_id = parent_event_id;
      event.scale_L = origin.L;
      event.direction = direction;
      event.level = level;
      event.status = FP_STATUS_LIVE_LEG;
      event.branch_kind = FP_BRANCH_NONE;
      event.render_kind = FP_RENDER_PROBABLE;
      event.origin = origin;
      event.leg1 = leg1;
      event.has_origin = true;
      event.has_leg1 = true;
      event.pos_origin = origin_pos;
      event.pos_leg1 = pos_leg1;
      event.leg1_L = leg1.L;
      event.reason = "probable_child_leg";
      return true;
   }

   return false;
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
