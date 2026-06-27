#ifndef __FCN_DETECTOR_MQH__
#define __FCN_DETECTOR_MQH__
#property strict
#include "FCN_Types.mqh"
#include "FCN_NodeEngine.mqh"

void FCN_AppendEvent(FCN_Event &events[], FCN_Event &e)
{
   int sz = ArraySize(events);
   e.event_id = sz;
   ArrayResize(events, sz + 1);
   events[sz] = e;
}

bool FCN_SameBody(const FCN_Event &a, const FCN_Event &b)
{
   return a.level == b.level &&
          a.direction == b.direction &&
          a.scale_L == b.scale_L &&
          a.origin.index == b.origin.index &&
          a.leg1.index == b.leg1.index &&
          a.waist.index == b.waist.index &&
          a.leg2.index == b.leg2.index;
}

bool FCN_EventAlreadyExists(const FCN_Event &events[], const FCN_Event &e)
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
      if(FCN_SameBody(events[i], e))
         return true;
   return false;
}

bool FCN_IsOppositeNodeForLeg1(const FCN_Node &n, const int direction)
{
   if(direction == FCN_DIR_BULLISH) return n.kind == FCN_NODE_HIGH;
   if(direction == FCN_DIR_BEARISH) return n.kind == FCN_NODE_LOW;
   return false;
}

bool FCN_IsCorrectionNode(const FCN_Node &n, const int direction)
{
   if(direction == FCN_DIR_BULLISH) return n.kind == FCN_NODE_LOW;
   if(direction == FCN_DIR_BEARISH) return n.kind == FCN_NODE_HIGH;
   return false;
}

bool FCN_WaistInsideLegRange(const FCN_Node &origin, const FCN_Node &leg1, const FCN_Node &waist, const int direction)
{
   if(direction == FCN_DIR_BULLISH)
      return origin.price < waist.price && waist.price < leg1.price;
   if(direction == FCN_DIR_BEARISH)
      return origin.price > waist.price && waist.price > leg1.price;
   return false;
}

bool FCN_Leg2BreaksLeg1(const FCN_Node &leg1, const FCN_Node &leg2, const int direction)
{
   if(direction == FCN_DIR_BULLISH)
      return leg2.kind == FCN_NODE_HIGH && leg2.price > leg1.price;
   if(direction == FCN_DIR_BEARISH)
      return leg2.kind == FCN_NODE_LOW && leg2.price < leg1.price;
   return false;
}

bool FCN_NodeInvalidatesF1Waist(const FCN_Node &node, const FCN_Node &waist, const int direction)
{
   if(direction == FCN_DIR_BULLISH)
      return node.kind == FCN_NODE_LOW && node.price < waist.price;
   if(direction == FCN_DIR_BEARISH)
      return node.kind == FCN_NODE_HIGH && node.price > waist.price;
   return false;
}

bool FCN_NodeInvalidatesOrigin(const FCN_Node &node, const FCN_Node &origin, const int direction)
{
   if(direction == FCN_DIR_BULLISH)
      return node.kind == FCN_NODE_LOW && node.price < origin.price;
   if(direction == FCN_DIR_BEARISH)
      return node.kind == FCN_NODE_HIGH && node.price > origin.price;
   return false;
}

bool FCN_NodeBreaksLeg2(const FCN_Node &node, const FCN_Node &leg2, const int direction)
{
   if(direction == FCN_DIR_BULLISH)
      return node.kind == FCN_NODE_HIGH && node.price > leg2.price;
   if(direction == FCN_DIR_BEARISH)
      return node.kind == FCN_NODE_LOW && node.price < leg2.price;
   return false;
}

bool FCN_FindCoreBodyFromOrigin(const FCN_Node &nodes[],
                                const int origin_pos,
                                const int direction,
                                const int level,
                                const int scale_L,
                                const int max_lookahead,
                                FCN_Event &event)
{
   FCN_ResetEvent(event);
   int n = ArraySize(nodes);
   if(origin_pos < 0 || origin_pos >= n-3) return false;

   FCN_Node origin = nodes[origin_pos];
   if(direction == FCN_DIR_BULLISH && origin.kind != FCN_NODE_LOW)  return false;
   if(direction == FCN_DIR_BEARISH && origin.kind != FCN_NODE_HIGH) return false;

   int end = n - 1;
   if(max_lookahead > 0)
      end = MathMin(n - 1, origin_pos + max_lookahead);

   for(int i=origin_pos+1; i<=end-2; i++)
   {
      if(!FCN_IsOppositeNodeForLeg1(nodes[i], direction)) continue;
      FCN_Node leg1 = nodes[i];

      for(int j=i+1; j<=end-1; j++)
      {
         if(!FCN_IsCorrectionNode(nodes[j], direction)) continue;
         FCN_Node waist = nodes[j];
         if(!FCN_WaistInsideLegRange(origin, leg1, waist, direction)) continue;

         for(int k=j+1; k<=end; k++)
         {
            if(!FCN_IsOppositeNodeForLeg1(nodes[k], direction)) continue;
            FCN_Node leg2 = nodes[k];
            if(!FCN_Leg2BreaksLeg1(leg1, leg2, direction)) continue;

            event.level = level;
            event.direction = direction;
            event.scale_L = scale_L;
            event.origin = origin;
            event.leg1 = leg1;
            event.waist = waist;
            event.leg2 = leg2;
            event.status = FCN_STATUS_LIVE;
            event.size = FCN_BodySize(origin, leg2);
            event.reason = "core_body";
            return true;
         }
      }
   }

   return false;
}

bool FCN_IsValidInternal1(const FCN_Node &node, const FCN_Event &e)
{
   if(e.direction == FCN_DIR_BULLISH)
      return node.kind == FCN_NODE_LOW && node.price > e.waist.price;
   if(e.direction == FCN_DIR_BEARISH)
      return node.kind == FCN_NODE_HIGH && node.price < e.waist.price;
   return false;
}

bool FCN_IsValidInternal2After1(const FCN_Node &node, const FCN_Node &n1, const FCN_Event &e)
{
   if(e.direction == FCN_DIR_BULLISH)
      return node.kind == FCN_NODE_LOW && node.price < n1.price && node.price > e.waist.price;
   if(e.direction == FCN_DIR_BEARISH)
      return node.kind == FCN_NODE_HIGH && node.price > n1.price && node.price < e.waist.price;
   return false;
}

void FCN_UpdateLeg2Extension(FCN_Event &e, const FCN_Node &new_leg2)
{
   e.leg2 = new_leg2;
   e.size = FCN_BodySize(e.origin, e.leg2);
   e.reason = "leg2_extended";
}

void FCN_AnalyzeF1AfterLeg2(const FCN_Node &nodes[], FCN_Event &e)
{
   int n = ArraySize(nodes);
   int pos = FCN_FindNodePositionByIndex(nodes, e.leg2.index);
   if(pos < 0) return;

   int guard = 0;
   while(pos < n-1 && guard < 2000)
   {
      guard++;
      bool restarted = false;
      FCN_ResetNode(e.internal1);
      FCN_ResetNode(e.internal2);
      FCN_ResetNode(e.confirm);
      FCN_ResetNode(e.invalid);
      e.has_internal1 = false;
      e.has_internal2 = false;
      e.has_confirm = false;
      e.has_invalid = false;
      e.branch_mode = FCN_BRANCH_NONE;

      // First internal node. If Leg2 extends before Internal 1, still the same leg2.
      for(int i=pos+1; i<n; i++)
      {
         FCN_Node node = nodes[i];
         if(FCN_NodeInvalidatesF1Waist(node, e.waist, e.direction))
         {
            e.invalid = node;
            e.has_invalid = true;
            e.status = FCN_STATUS_INVALID;
            e.reason = "f1_waist_invalid_before_internal1";
            return;
         }
         if(FCN_NodeBreaksLeg2(node, e.leg2, e.direction))
         {
            FCN_UpdateLeg2Extension(e, node);
            pos = i;
            restarted = true;
            break;
         }
         if(FCN_IsValidInternal1(node, e))
         {
            e.internal1 = node;
            e.has_internal1 = true;
            e.branch_mode = FCN_BRANCH_PARTIAL_1;
            pos = i;
            break;
         }
      }
      if(restarted) continue;
      if(!e.has_internal1)
      {
         e.status = FCN_STATUS_LIVE;
         e.reason = "f1_waiting_internal1";
         return;
      }

      // Second internal node. If Leg2 extends before Internal 2, still the same leg2.
      for(int i=pos+1; i<n; i++)
      {
         FCN_Node node = nodes[i];
         if(FCN_NodeInvalidatesF1Waist(node, e.waist, e.direction))
         {
            e.invalid = node;
            e.has_invalid = true;
            e.status = FCN_STATUS_INVALID;
            e.reason = "f1_waist_invalid_before_internal2";
            return;
         }
         if(FCN_NodeBreaksLeg2(node, e.leg2, e.direction))
         {
            FCN_UpdateLeg2Extension(e, node);
            pos = i;
            restarted = true;
            break;
         }
         if(FCN_IsValidInternal2After1(node, e.internal1, e))
         {
            e.internal2 = node;
            e.has_internal2 = true;
            e.branch_mode = FCN_BRANCH_INTERNAL12;
            pos = i;
            break;
         }
      }
      if(restarted) continue;
      if(!e.has_internal2)
      {
         e.status = FCN_STATUS_LIVE;
         e.reason = "f1_waiting_internal2";
         return;
      }

      // Confirmation after Internal 1/2 only.
      for(int i=pos+1; i<n; i++)
      {
         FCN_Node node = nodes[i];
         if(FCN_NodeInvalidatesF1Waist(node, e.waist, e.direction))
         {
            e.invalid = node;
            e.has_invalid = true;
            e.status = FCN_STATUS_INVALID;
            e.reason = "f1_waist_invalid_before_confirm";
            return;
         }
         if(FCN_NodeBreaksLeg2(node, e.leg2, e.direction))
         {
            e.confirm = node;
            e.has_confirm = true;
            e.status = FCN_STATUS_CONFIRMED;
            e.reason = "f1_confirmed_after_internal12";
            return;
         }
      }

      e.status = FCN_STATUS_LIVE;
      e.reason = "f1_waiting_confirm";
      return;
   }
}

bool FCN_NodeBreaksWaistForContinuation(const FCN_Node &node, const FCN_Event &e)
{
   if(e.direction == FCN_DIR_BULLISH)
      return node.kind == FCN_NODE_LOW && node.price < e.waist.price && node.price > e.origin.price;
   if(e.direction == FCN_DIR_BEARISH)
      return node.kind == FCN_NODE_HIGH && node.price > e.waist.price && node.price < e.origin.price;
   return false;
}

void FCN_AnalyzeContinuationAfterLeg2(const FCN_Node &nodes[], FCN_Event &e)
{
   int n = ArraySize(nodes);
   int start = FCN_FindNodePositionByIndex(nodes, e.leg2.index);
   if(start < 0) return;

   bool saw_leg2_rebreak = false;
   FCN_Node prebreak;
   FCN_ResetNode(prebreak);

   for(int i=start+1; i<n; i++)
   {
      FCN_Node node = nodes[i];
      if(FCN_NodeInvalidatesOrigin(node, e.origin, e.direction))
      {
         e.invalid = node;
         e.has_invalid = true;
         e.status = FCN_STATUS_INVALID;
         e.reason = "continuation_origin_invalid";
         return;
      }

      if(FCN_NodeBreaksLeg2(node, e.leg2, e.direction))
      {
         if(!saw_leg2_rebreak)
         {
            prebreak = node;
            saw_leg2_rebreak = true;
            e.has_pre_branch_leg2_break = true;
         }
         // Continuation can extend the same Leg2 before later correction.
         FCN_UpdateLeg2Extension(e, node);
         continue;
      }

      if(FCN_NodeBreaksWaistForContinuation(node, e))
      {
         e.internal1 = e.waist;
         e.internal2 = node;
         e.has_internal1 = true;
         e.has_internal2 = true;
         e.branch_mode = FCN_BRANCH_WAIST_BREAK;
         if(saw_leg2_rebreak)
         {
            e.confirm = prebreak;
            e.has_confirm = true;
            e.status = FCN_STATUS_CONFIRMED;
            e.reason = "continuation_confirmed_prebreak_with_waist_branch";
         }
         else
         {
            e.status = FCN_STATUS_LIVE;
            e.reason = "continuation_waist_branch_waiting_confirm";
         }
         return;
      }

      if(!e.has_internal1 && FCN_IsValidInternal1(node, e))
      {
         e.internal1 = node;
         e.has_internal1 = true;
         e.branch_mode = FCN_BRANCH_PARTIAL_1;
         continue;
      }

      if(e.has_internal1 && !e.has_internal2 && FCN_IsValidInternal2After1(node, e.internal1, e))
      {
         e.internal2 = node;
         e.has_internal2 = true;
         e.branch_mode = FCN_BRANCH_INTERNAL12;
         if(saw_leg2_rebreak)
         {
            e.confirm = prebreak;
            e.has_confirm = true;
            e.status = FCN_STATUS_CONFIRMED;
            e.reason = "continuation_confirmed_prebreak_with_internal12";
         }
         else
         {
            e.status = FCN_STATUS_LIVE;
            e.reason = "continuation_internal12_waiting_confirm";
         }
         return;
      }
   }

   if(saw_leg2_rebreak)
   {
      e.confirm = prebreak;
      e.has_confirm = true;
      e.status = FCN_STATUS_CONFIRMED;
      e.reason = "continuation_confirmed_extension_waiting_branch";
   }
   else
   {
      e.status = FCN_STATUS_LIVE;
      e.reason = "continuation_live_waiting_extension_or_branch";
   }
}

void FCN_FinalizeF3Terminal(FCN_Event &e)
{
   // F3 is terminal after the two-leg body is complete. Post-body movement is special and not invalidated here.
   e.status = FCN_STATUS_TERMINAL;
   e.has_confirm = true;
   e.confirm = e.leg2;
   e.reason = "f3_terminal_after_two_leg_body";
}

void FCN_AnalyzeEventByLevel(const FCN_Node &nodes[], FCN_Event &e)
{
   if(e.level == FCN_LEVEL_F1)
      FCN_AnalyzeF1AfterLeg2(nodes, e);
   else if(e.level == FCN_LEVEL_F2)
      FCN_AnalyzeContinuationAfterLeg2(nodes, e);
   else if(e.level == FCN_LEVEL_F3)
      FCN_FinalizeF3Terminal(e);
}

bool FCN_SizeSymmetryPass(const FCN_Event &child, const FCN_Event &parent, const FCN_Config &cfg)
{
   if(child.level != FCN_LEVEL_F2) return true;
   if(!cfg.require_f2_parent_size) return true;
   if(parent.size <= 0.0) return true;
   return child.size >= parent.size * cfg.f2_min_parent_size_ratio;
}

bool FCN_CreateChildFromParent(const FCN_Node &nodes[],
                               const FCN_Event &parent,
                               const int child_level,
                               const FCN_Config &cfg,
                               FCN_Event &child)
{
   FCN_ResetEvent(child);
   if(!parent.has_internal2) return false;
   if(cfg.require_parent_confirmed && parent.status != FCN_STATUS_CONFIRMED && parent.status != FCN_STATUS_TERMINAL)
      return false;

   int origin_pos = FCN_FindNodePositionByIndex(nodes, parent.internal2.index);
   if(origin_pos < 0) return false;

   int lookahead = 0; // mandatory continuation can extend until invalidation/end.
   if(!FCN_FindCoreBodyFromOrigin(nodes, origin_pos, parent.direction, child_level, parent.scale_L, lookahead, child))
      return false;

   child.parent_event_id = parent.event_id;
   child.sequence_id = parent.sequence_id;
   child.chain_step = parent.chain_step + 1;
   child.parent_size = parent.size;
   child.size_ratio = (parent.size > 0.0 ? child.size / parent.size : 0.0);

   if(!FCN_SizeSymmetryPass(child, parent, cfg))
   {
      child.status = FCN_STATUS_INVALID;
      child.reason = "f2_size_symmetry_failed";
      return false;
   }

   FCN_AnalyzeEventByLevel(nodes, child);
   return child.status != FCN_STATUS_INVALID;
}



bool FCN_NodePositionCoveredByScaleEvents(const FCN_Event &events[],
                                          const int from_event,
                                          const int to_event_exclusive,
                                          const int scale_L,
                                          const int node_index)
{
   for(int i=from_event; i<to_event_exclusive; i++)
   {
      if(events[i].scale_L != scale_L)
         continue;
      if(events[i].level == FCN_LEVEL_ND)
         continue;
      if(events[i].status == FCN_STATUS_INVALID)
         continue;
      int a = MathMin(events[i].origin.index, events[i].leg2.index);
      int b = MathMax(events[i].origin.index, events[i].leg2.index);
      if(node_index >= a && node_index <= b)
         return true;
   }
   return false;
}

void FCN_AppendProvisionalNDGapsForScale(const FCN_Node &nodes[],
                                         const int scale_L,
                                         const int first_scale_event,
                                         FCN_Event &events[],
                                         int &next_sequence_id,
                                         const int max_nd_per_scale)
{
   int n = ArraySize(nodes);
   if(n < 3)
      return;

   int current_event_count = ArraySize(events);
   int nd_count = 0;
   int i = 0;
   while(i < n)
   {
      if(FCN_NodePositionCoveredByScaleEvents(events, first_scale_event, current_event_count, scale_L, nodes[i].index))
      {
         i++;
         continue;
      }

      int start = i;
      while(i < n && !FCN_NodePositionCoveredByScaleEvents(events, first_scale_event, current_event_count, scale_L, nodes[i].index))
         i++;
      int end = i - 1;
      int len = end - start + 1;

      // ND / Hook is a provisional unowned cycle of at least 3 nodes in this scale.
      if(len >= 3)
      {
         if(max_nd_per_scale > 0 && nd_count >= max_nd_per_scale)
            return;

         FCN_Event nd;
         FCN_ResetEvent(nd);
         nd.level = FCN_LEVEL_ND;
         nd.scale_L = scale_L;
         nd.sequence_id = next_sequence_id++;
         nd.chain_step = 0;
         nd.parent_event_id = -1;
         nd.origin = nodes[start];
         nd.leg1 = nodes[MathMin(start + 1, end)];
         nd.waist = nodes[MathMin(start + 2, end)];
         nd.leg2 = nodes[end];
         nd.direction = (nd.leg2.price >= nd.origin.price ? FCN_DIR_BULLISH : FCN_DIR_BEARISH);
         nd.status = FCN_STATUS_LIVE;
         nd.size = FCN_BodySize(nd.origin, nd.leg2);
         nd.reason = "provisional_nd_unowned_node_run";
         FCN_AppendEvent(events, nd);
         nd_count++;
      }
   }
}

void FCN_PrintEvent(const FCN_Event &e)
{
   Print("FC_EVENT",
         " scaleL=", e.scale_L,
         " seq=", e.sequence_id,
         " step=", e.chain_step,
         " level=", FCN_LevelToString(e.level),
         " dir=", FCN_DirectionToString(e.direction),
         " status=", FCN_StatusToString(e.status),
         " branch=", FCN_BranchToString(e.branch_mode),
         " origin=", TimeToString(e.origin.time), "@", DoubleToString(e.origin.price, _Digits),
         " leg1=", TimeToString(e.leg1.time), "@", DoubleToString(e.leg1.price, _Digits),
         " waist=", TimeToString(e.waist.time), "@", DoubleToString(e.waist.price, _Digits),
         " leg2=", TimeToString(e.leg2.time), "@", DoubleToString(e.leg2.price, _Digits),
         " i1=", (e.has_internal1 ? TimeToString(e.internal1.time) : "none"),
         " i2=", (e.has_internal2 ? TimeToString(e.internal2.time) : "none"),
         " size=", DoubleToString(e.size, _Digits),
         " parentSize=", DoubleToString(e.parent_size, _Digits),
         " reason=", e.reason);
}

void FCN_BuildSequencesForScale(const FCN_Node &nodes[],
                                const int scale_L,
                                const FCN_Config &cfg,
                                FCN_Event &events[],
                                int &next_sequence_id)
{
   int n = ArraySize(nodes);
   int roots = 0;
   int first_scale_event = ArraySize(events);
   for(int p=0; p<n-3; p++)
   {
      if(cfg.max_events > 0 && ArraySize(events) >= cfg.max_events) return;
      if(cfg.max_roots_per_scale > 0 && roots >= cfg.max_roots_per_scale) return;

      for(int d=0; d<2; d++)
      {
         int direction = (d == 0 ? FCN_DIR_BULLISH : FCN_DIR_BEARISH);
         if(direction == FCN_DIR_BULLISH && nodes[p].kind != FCN_NODE_LOW) continue;
         if(direction == FCN_DIR_BEARISH && nodes[p].kind != FCN_NODE_HIGH) continue;

         FCN_Event f1;
         if(!FCN_FindCoreBodyFromOrigin(nodes, p, direction, FCN_LEVEL_F1, scale_L, 0, f1))
            continue;
         FCN_AnalyzeEventByLevel(nodes, f1);
         if(f1.status == FCN_STATUS_INVALID)
            continue;
         if(FCN_EventAlreadyExists(events, f1))
            continue;

         f1.sequence_id = next_sequence_id++;
         f1.parent_event_id = -1;
         f1.chain_step = 1;
         FCN_AppendEvent(events, f1);
         int f1_id = ArraySize(events) - 1;
         roots++;
         if(cfg.verbose_logs) FCN_PrintEvent(events[f1_id]);

         if(cfg.scan_f2)
         {
            FCN_Event f2;
            if(FCN_CreateChildFromParent(nodes, events[f1_id], FCN_LEVEL_F2, cfg, f2))
            {
               FCN_AppendEvent(events, f2);
               int f2_id = ArraySize(events) - 1;
               if(cfg.verbose_logs) FCN_PrintEvent(events[f2_id]);

               if(cfg.scan_f3)
               {
                  FCN_Event f3;
                  if(FCN_CreateChildFromParent(nodes, events[f2_id], FCN_LEVEL_F3, cfg, f3))
                  {
                     FCN_AppendEvent(events, f3);
                     if(cfg.verbose_logs) FCN_PrintEvent(events[ArraySize(events)-1]);
                  }
               }
            }
         }
      }
   }

   if(cfg.scan_nd)
      FCN_AppendProvisionalNDGapsForScale(nodes, scale_L, first_scale_event, events, next_sequence_id, cfg.max_nd_per_scale);
}

bool FCN_ScaleAlreadyListed(const int &scales[], const int count, const int value)
{
   for(int i=0; i<count; i++)
      if(scales[i] == value)
         return true;
   return false;
}

int FCN_BuildScaleList(const bool use_multi_scale,
                       const int L1,
                       const int L2,
                       const int L3,
                       const int L4,
                       const int L5,
                       const int L6,
                       int &scales[])
{
   ArrayResize(scales, 0);
   int raw[6];
   raw[0] = L1; raw[1] = L2; raw[2] = L3; raw[3] = L4; raw[4] = L5; raw[5] = L6;
   int count = 0;
   int max_i = (use_multi_scale ? 6 : 1);
   for(int i=0; i<max_i; i++)
   {
      int v = raw[i];
      if(v < 1) continue;
      if(FCN_ScaleAlreadyListed(scales, count, v)) continue;
      ArrayResize(scales, count + 1);
      scales[count] = v;
      count++;
   }
   return count;
}

int FCN_DetectFractalFlagCounting(const MqlRates &rates[],
                                  const int total,
                                  const int &scales[],
                                  const int scale_count,
                                  const FCN_Config &cfg,
                                  FCN_Event &events[])
{
   ArrayResize(events, 0);
   int next_sequence_id = 1;

   for(int s=0; s<scale_count; s++)
   {
      int L = scales[s];
      FCN_Node nodes[];
      FCN_BuildNodes(rates, total, L, nodes);
      if(cfg.verbose_logs)
         Print("FC_SCALE scaleL=", L, " nodes=", ArraySize(nodes));
      if(ArraySize(nodes) < 4) continue;
      FCN_BuildSequencesForScale(nodes, L, cfg, events, next_sequence_id);
   }

   return ArraySize(events);
}

#endif
