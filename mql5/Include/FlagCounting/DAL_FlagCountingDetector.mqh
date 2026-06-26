#ifndef __DAL_FLAG_COUNTING_DETECTOR_MQH__
#define __DAL_FLAG_COUNTING_DETECTOR_MQH__
#property strict
#include "DAL_FlagCountingTypes.mqh"
#include "DAL_FlagCountingNodeDetector.mqh"

void FC_AppendEvent(FC_FlagEvent &events[], const FC_FlagEvent &event)
{
   int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n] = event;
}

bool FC_CoreTimeOrdered(const FC_Node &origin, const FC_Node &leg1, const FC_Node &waist, const FC_Node &leg2)
{
   if(origin.index < 0 || leg1.index < 0 || waist.index < 0 || leg2.index < 0) return false;
   return (origin.index < leg1.index && leg1.index < waist.index && waist.index < leg2.index);
}

bool FC_IsBullishCore(const FC_Node &origin, const FC_Node &leg1, const FC_Node &waist, const FC_Node &leg2, const double eps)
{
   if(!FC_CoreTimeOrdered(origin, leg1, waist, leg2)) return false;
   if(origin.kind != FC_NODE_LOW)  return false;
   if(leg1.kind   != FC_NODE_HIGH) return false;
   if(waist.kind  != FC_NODE_LOW)  return false;
   if(leg2.kind   != FC_NODE_HIGH) return false;

   if(!(leg1.price  > origin.price + eps)) return false;
   if(!(waist.price > origin.price + eps)) return false;
   if(!(waist.price < leg1.price  - eps)) return false;
   if(!(leg2.price  > leg1.price  + eps)) return false;
   return true;
}

bool FC_IsBearishCore(const FC_Node &origin, const FC_Node &leg1, const FC_Node &waist, const FC_Node &leg2, const double eps)
{
   if(!FC_CoreTimeOrdered(origin, leg1, waist, leg2)) return false;
   if(origin.kind != FC_NODE_HIGH) return false;
   if(leg1.kind   != FC_NODE_LOW)  return false;
   if(waist.kind  != FC_NODE_HIGH) return false;
   if(leg2.kind   != FC_NODE_LOW)  return false;

   if(!(leg1.price  < origin.price - eps)) return false;
   if(!(waist.price < origin.price - eps)) return false;
   if(!(waist.price > leg1.price  + eps)) return false;
   if(!(leg2.price  < leg1.price  - eps)) return false;
   return true;
}

bool FC_InternalNodeProtectsWaist(const int direction, const FC_Node &node, const double waist_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return node.kind == FC_NODE_LOW && node.price > waist_price + eps;
   if(direction == FC_DIR_BEARISH)
      return node.kind == FC_NODE_HIGH && node.price < waist_price - eps;
   return false;
}

bool FC_NodeBreaksWaist(const int direction, const FC_Node &node, const double waist_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return node.kind == FC_NODE_LOW && node.price <= waist_price + eps;
   if(direction == FC_DIR_BEARISH)
      return node.kind == FC_NODE_HIGH && node.price >= waist_price - eps;
   return false;
}

bool FC_NodeBreaksInvalidation(const int direction, const FC_Node &node, const double invalidation_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return node.kind == FC_NODE_LOW && node.price <= invalidation_price + eps;
   if(direction == FC_DIR_BEARISH)
      return node.kind == FC_NODE_HIGH && node.price >= invalidation_price - eps;
   return false;
}

bool FC_NodeBreaksLeg2(const int direction, const FC_Node &node, const double leg2_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return node.kind == FC_NODE_HIGH && node.price >= leg2_price + eps;
   if(direction == FC_DIR_BEARISH)
      return node.kind == FC_NODE_LOW && node.price <= leg2_price - eps;
   return false;
}

bool FC_Internal2ValidAgainstInternal1(const int direction, const FC_Node &n1, const FC_Node &n2, const double waist_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
   {
      if(n2.kind != FC_NODE_LOW) return false;
      if(n2.price <= waist_price + eps) return false;
      return n2.price < n1.price - eps;
   }
   if(direction == FC_DIR_BEARISH)
   {
      if(n2.kind != FC_NODE_HIGH) return false;
      if(n2.price >= waist_price - eps) return false;
      return n2.price > n1.price + eps;
   }
   return false;
}

bool FC_FindFirstLeg2BreakBeforeInvalidation(const FC_Node &nodes[],
                                             const int leg2_pos,
                                             const int direction,
                                             const double leg2_price,
                                             const double invalidation_price,
                                             const double eps,
                                             FC_Node &confirm_node,
                                             FC_Node &invalid_node)
{
   FC_InitNode(confirm_node);
   FC_InitNode(invalid_node);

   int n = ArraySize(nodes);
   for(int p=leg2_pos+1; p<n; p++)
   {
      FC_Node node = nodes[p];
      if(FC_NodeBreaksInvalidation(direction, node, invalidation_price, eps))
      {
         invalid_node = node;
         return false;
      }
      if(FC_NodeBreaksLeg2(direction, node, leg2_price, eps))
      {
         confirm_node = node;
         return true;
      }
   }
   return false;
}

bool FC_FindBranchAfterLeg2UntilBoundary(const FC_Node &nodes[],
                                         const int leg2_pos,
                                         const int direction,
                                         const double waist_price,
                                         const double invalidation_price,
                                         const bool allow_waist_break_branch,
                                         const bool stop_at_first_leg2_break,
                                         const double leg2_price,
                                         const double eps,
                                         FC_Node &n1,
                                         FC_Node &n2,
                                         int &branch_type)
{
   FC_InitNode(n1);
   FC_InitNode(n2);
   branch_type = FC_BRANCH_NONE;

   bool have_internal_1 = false;
   FC_Node internal_1;
   FC_InitNode(internal_1);

   int n = ArraySize(nodes);
   for(int p=leg2_pos+1; p<n; p++)
   {
      FC_Node node = nodes[p];

      if(FC_NodeBreaksInvalidation(direction, node, invalidation_price, eps))
         return false;

      // F1: branch 1/2 belongs before the confirming Leg2 rebreak.
      // F2/F3: branch can be found after a Leg2 extension until origin invalidates.
      if(stop_at_first_leg2_break && FC_NodeBreaksLeg2(direction, node, leg2_price, eps))
         return false;

      if(allow_waist_break_branch && FC_NodeBreaksWaist(direction, node, waist_price, eps))
      {
         n1 = FC_MakeNode(-1, 0, waist_price, direction == FC_DIR_BULLISH ? FC_NODE_LOW : FC_NODE_HIGH);
         n2 = node;
         branch_type = FC_BRANCH_WAIST_BREAK;
         return true;
      }

      if(!have_internal_1)
      {
         if(FC_InternalNodeProtectsWaist(direction, node, waist_price, eps))
         {
            internal_1 = node;
            have_internal_1 = true;
         }
         continue;
      }

      if(FC_Internal2ValidAgainstInternal1(direction, internal_1, node, waist_price, eps))
      {
         n1 = internal_1;
         n2 = node;
         branch_type = FC_BRANCH_INTERNAL12;
         return true;
      }
   }
   return false;
}

void FC_ApplyBranchAndConfirmation(const FC_Node &nodes[],
                                   const int leg2_pos,
                                   const bool continuation_level,
                                   const bool allow_waist_break_branch,
                                   const double eps,
                                   FC_FlagEvent &event)
{
   // Confirmation contract:
   // every F confirms by rebreaking Leg2 before invalidation.
   // F1 invalidates at waist. F2/F3 invalidates at origin/start-of-leg.
   double invalidation_price = (continuation_level ? event.origin.price : event.waist.price);

   FC_Node confirm_node, invalid_node;
   bool confirmed = FC_FindFirstLeg2BreakBeforeInvalidation(nodes,
                                                            leg2_pos,
                                                            event.direction,
                                                            event.leg2.price,
                                                            invalidation_price,
                                                            eps,
                                                            confirm_node,
                                                            invalid_node);
   if(confirmed)
   {
      event.status = FC_STATUS_CONFIRMED;
      event.confirm_index = confirm_node.index;
      event.confirm_time = confirm_node.time;
      event.confirm_price = confirm_node.price;
   }
   else if(invalid_node.index >= 0)
   {
      event.status = FC_STATUS_INVALIDATED;
      event.invalid_index = invalid_node.index;
      event.invalid_time = invalid_node.time;
      event.invalid_price = invalid_node.price;
   }
   else
   {
      event.status = FC_STATUS_OPEN;
   }

   // Branch 1/2 is counting/audit/labels, not a hard validity gate.
   FC_Node n1, n2;
   int branch_type = FC_BRANCH_NONE;
   bool branch_found = FC_FindBranchAfterLeg2UntilBoundary(nodes,
                                                           leg2_pos,
                                                           event.direction,
                                                           event.waist.price,
                                                           invalidation_price,
                                                           continuation_level && allow_waist_break_branch,
                                                           !continuation_level,
                                                           event.leg2.price,
                                                           eps,
                                                           n1,
                                                           n2,
                                                           branch_type);
   if(branch_found)
   {
      if(branch_type == FC_BRANCH_WAIST_BREAK)
      {
         n1.index = event.waist.index;
         n1.time  = event.waist.time;
         n1.price = event.waist.price;
         n1.kind  = event.waist.kind;
      }
      event.n1 = n1;
      event.n2 = n2;
      event.has_n1 = true;
      event.has_n2 = true;
      event.branch_type = branch_type;
   }
}

bool FC_SameCore(const FC_FlagEvent &a, const FC_FlagEvent &b)
{
   return (a.direction == b.direction &&
           a.origin.index == b.origin.index &&
           a.leg1.index == b.leg1.index &&
           a.waist.index == b.waist.index &&
           a.leg2.index == b.leg2.index);
}

bool FC_CoreExistsIn(const FC_FlagEvent &e, const FC_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(FC_SameCore(e, events[i]))
         return true;
   }
   return false;
}

bool FC_BuildF1FromNodeWindow(const FC_Node &nodes[],
                              const int start_pos,
                              const bool scan_bullish,
                              const bool scan_bearish,
                              const double eps,
                              FC_FlagEvent &event)
{
   FC_InitFlagEvent(event);
   int n = ArraySize(nodes);
   if(start_pos + 3 >= n) return false;

   FC_Node origin = nodes[start_pos];
   FC_Node leg1   = nodes[start_pos+1];
   FC_Node waist  = nodes[start_pos+2];
   FC_Node leg2   = nodes[start_pos+3];

   int direction = FC_DIR_NONE;
   if(scan_bullish && FC_IsBullishCore(origin, leg1, waist, leg2, eps))
      direction = FC_DIR_BULLISH;
   if(scan_bearish && FC_IsBearishCore(origin, leg1, waist, leg2, eps))
      direction = FC_DIR_BEARISH;
   if(direction == FC_DIR_NONE) return false;

   event.level = FC_LEVEL_F1;
   event.direction = direction;
   event.origin = origin;
   event.leg1 = leg1;
   event.waist = waist;
   event.leg2 = leg2;
   event.body_size = FC_FlagBodySize(event);

   FC_ApplyBranchAndConfirmation(nodes, start_pos+3, false, false, eps, event);
   return true;
}

bool FC_BuildContinuationFromParent(const FC_Node &nodes[],
                                    const FC_FlagEvent &parent,
                                    const int parent_array_index,
                                    const int child_level,
                                    const bool require_parent_confirmed,
                                    const bool require_child_at_least_parent_size,
                                    const double child_min_parent_size_ratio,
                                    const bool allow_waist_break_branch,
                                    const double eps,
                                    FC_FlagEvent &event)
{
   FC_InitFlagEvent(event);
   if(parent.level <= FC_LEVEL_NONE) return false;
   if(!parent.has_n2) return false;
   if(require_parent_confirmed && parent.status != FC_STATUS_CONFIRMED) return false;

   int start_pos = FC_FindNodePositionByIndex(nodes, parent.n2.index);
   if(start_pos < 0) return false;
   if(start_pos + 3 >= ArraySize(nodes)) return false;

   FC_Node origin = nodes[start_pos];
   FC_Node leg1   = nodes[start_pos+1];
   FC_Node waist  = nodes[start_pos+2];
   FC_Node leg2   = nodes[start_pos+3];

   bool core_ok = false;
   if(parent.direction == FC_DIR_BULLISH)
      core_ok = FC_IsBullishCore(origin, leg1, waist, leg2, eps);
   else if(parent.direction == FC_DIR_BEARISH)
      core_ok = FC_IsBearishCore(origin, leg1, waist, leg2, eps);
   if(!core_ok) return false;

   double parent_body_size = parent.body_size;
   if(parent_body_size <= 0.0)
      parent_body_size = FC_FlagBodySize(parent);

   double child_body_size = FC_BodySizeFromNodes(origin, leg2);
   double min_required_size = parent_body_size * MathMax(0.0, child_min_parent_size_ratio);

   if(require_child_at_least_parent_size && parent_body_size > eps)
   {
      if(child_body_size + eps < min_required_size)
         return false;
   }

   event.level = child_level;
   event.direction = parent.direction;
   event.status = FC_STATUS_OPEN;
   event.parent_event_index = parent_array_index;
   event.parent_origin_index = parent.origin.index;
   event.parent_level = parent.level;
   event.origin = origin;
   event.leg1 = leg1;
   event.waist = waist;
   event.leg2 = leg2;
   event.body_size = child_body_size;
   event.parent_body_size = parent_body_size;
   event.parent_size_ratio = (parent_body_size > 0.0 ? child_body_size / parent_body_size : 0.0);

   FC_ApplyBranchAndConfirmation(nodes, start_pos+3, true, allow_waist_break_branch, eps, event);
   return true;
}

int FC_DetectFlagsFromNodes(const FC_Node &nodes[],
                            const bool scan_f1,
                            const bool scan_f2,
                            const bool scan_f3,
                            const bool scan_bullish,
                            const bool scan_bearish,
                            const bool suppress_promoted_lower_level_bodies,
                            const bool require_parent_confirmed_for_next_f,
                            const bool require_child_at_least_parent_size,
                            const double child_min_parent_size_ratio,
                            const bool allow_child_waist_break_branch,
                            const double eps,
                            FC_FlagEvent &events[])
{
   ArrayResize(events, 0);
   FC_FlagEvent f1_events[];
   FC_FlagEvent f2_events[];
   FC_FlagEvent f3_events[];
   ArrayResize(f1_events, 0);
   ArrayResize(f2_events, 0);
   ArrayResize(f3_events, 0);

   int n = ArraySize(nodes);
   if(n < 4) return 0;

   if(scan_f1)
   {
      for(int p=0; p<=n-4; p++)
      {
         FC_FlagEvent e;
         if(FC_BuildF1FromNodeWindow(nodes, p, scan_bullish, scan_bearish, eps, e))
            FC_AppendEvent(f1_events, e);
      }
   }

   if(scan_f2)
   {
      int f1n = ArraySize(f1_events);
      for(int i=0; i<f1n; i++)
      {
         FC_FlagEvent e2;
         if(FC_BuildContinuationFromParent(nodes,
                                           f1_events[i],
                                           i,
                                           FC_LEVEL_F2,
                                           require_parent_confirmed_for_next_f,
                                           require_child_at_least_parent_size,
                                           child_min_parent_size_ratio,
                                           allow_child_waist_break_branch,
                                           eps,
                                           e2))
            FC_AppendEvent(f2_events, e2);
      }
   }

   if(scan_f3)
   {
      int f2n = ArraySize(f2_events);
      for(int j=0; j<f2n; j++)
      {
         FC_FlagEvent e3;
         if(FC_BuildContinuationFromParent(nodes,
                                           f2_events[j],
                                           j,
                                           FC_LEVEL_F3,
                                           require_parent_confirmed_for_next_f,
                                           require_child_at_least_parent_size,
                                           child_min_parent_size_ratio,
                                           allow_child_waist_break_branch,
                                           eps,
                                           e3))
            FC_AppendEvent(f3_events, e3);
      }
   }

   if(scan_f1)
   {
      int f1_total = ArraySize(f1_events);
      for(int k=0; k<f1_total; k++)
      {
         if(suppress_promoted_lower_level_bodies && (FC_CoreExistsIn(f1_events[k], f2_events) || FC_CoreExistsIn(f1_events[k], f3_events)))
            continue;
         FC_AppendEvent(events, f1_events[k]);
      }
   }

   if(scan_f2)
   {
      int f2_total = ArraySize(f2_events);
      for(int k=0; k<f2_total; k++)
      {
         if(suppress_promoted_lower_level_bodies && FC_CoreExistsIn(f2_events[k], f3_events))
            continue;
         FC_AppendEvent(events, f2_events[k]);
      }
   }

   if(scan_f3)
   {
      int f3_total = ArraySize(f3_events);
      for(int k=0; k<f3_total; k++)
         FC_AppendEvent(events, f3_events[k]);
   }

   return ArraySize(events);
}

int FC_DetectFlags(const MqlRates &rates[],
                   const int total,
                   const int swing_L,
                   const bool scan_f1,
                   const bool scan_f2,
                   const bool scan_f3,
                   const bool scan_bullish,
                   const bool scan_bearish,
                   const bool suppress_promoted_lower_level_bodies,
                   const bool require_parent_confirmed_for_next_f,
                   const bool require_child_at_least_parent_size,
                   const double child_min_parent_size_ratio,
                   const bool allow_child_waist_break_branch,
                   const double eps,
                   FC_Node &nodes[],
                   FC_FlagEvent &events[])
{
   FC_BuildNodes(rates, total, swing_L, nodes);
   return FC_DetectFlagsFromNodes(nodes,
                                  scan_f1,
                                  scan_f2,
                                  scan_f3,
                                  scan_bullish,
                                  scan_bearish,
                                  suppress_promoted_lower_level_bodies,
                                  require_parent_confirmed_for_next_f,
                                  require_child_at_least_parent_size,
                                  child_min_parent_size_ratio,
                                  allow_child_waist_break_branch,
                                  eps,
                                  events);
}

#endif
