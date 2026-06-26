#ifndef __DAL_FLAG_COUNTING_DETECTOR_MQH__
#define __DAL_FLAG_COUNTING_DETECTOR_MQH__
#property strict
#include "DAL_FlagCountingTypes.mqh"
#include "DAL_FlagCountingNodeDetector.mqh"

void FC_AppendEvent(FC_FlagEvent &events[], FC_FlagEvent &event)
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

   // Bullish flag geometry:
   // - Leg1 must move away from the origin.
   // - Waist/correction must stay in front of the origin, not behind the start of the leg.
   // - Waist must also stay below Leg1, otherwise it is not a correction waist.
   // - Leg2 must break Leg1.
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

   // Bearish flag geometry is the exact mirror of bullish:
   // - Leg1 must move down away from the origin.
   // - Waist/correction must stay below the origin, not behind/above the start of the leg.
   // - Waist must also stay above Leg1, otherwise it is not a correction waist.
   // - Leg2 must break Leg1.
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

bool FC_FindBranchAfterLeg2(const FC_Node &nodes[],
                            const int leg2_pos,
                            const int direction,
                            const double waist_price,
                            const double leg2_price,
                            const bool allow_waist_break_branch,
                            const bool allow_leg2_break_before_branch,
                            const double eps,
                            FC_Node &n1,
                            FC_Node &n2,
                            int &branch_type,
                            FC_Node &pre_branch_leg2_break)
{
   FC_InitNode(n1);
   FC_InitNode(n2);
   FC_InitNode(pre_branch_leg2_break);
   branch_type = FC_BRANCH_NONE;

   bool have_internal_1 = false;
   FC_Node internal_1;
   FC_InitNode(internal_1);

   int n = ArraySize(nodes);
   for(int p=leg2_pos+1; p<n; p++)
   {
      FC_Node node = nodes[p];

      // Critical sequencing rule:
      // F1: internal 1/2 must be formed BEFORE the Leg2 extreme is rebroken.
      // F2: this pre-branch Leg2 break is allowed; F2 can extend through Leg2 first,
      //     then return into its 1/2 branch or the waist-break branch.
      if(FC_NodeBreaksLeg2(direction, node, leg2_price, eps))
      {
         if(!allow_leg2_break_before_branch)
            return false;
         if(pre_branch_leg2_break.index < 0)
            pre_branch_leg2_break = node;
         continue;
      }

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

bool FC_FindLeg2RebreakAfterBranch(const FC_Node &nodes[],
                                   const int n2_bar_index,
                                   const int direction,
                                   const double leg2_price,
                                   const double eps,
                                   FC_Node &confirm_node)
{
   FC_InitNode(confirm_node);
   int start_pos = FC_FindNodePositionByIndex(nodes, n2_bar_index);
   if(start_pos < 0) return false;

   int n = ArraySize(nodes);
   for(int p=start_pos+1; p<n; p++)
   {
      if(FC_NodeBreaksLeg2(direction, nodes[p], leg2_price, eps))
      {
         confirm_node = nodes[p];
         return true;
      }
   }
   return false;
}

bool FC_ApplyBranchAndConfirmation(const FC_Node &nodes[],
                                   const int leg2_pos,
                                   const bool allow_waist_break_branch,
                                   const bool allow_leg2_break_before_branch,
                                   const bool pre_branch_leg2_break_can_confirm,
                                   const bool require_branch12,
                                   const bool require_leg2_rebreak,
                                   const double eps,
                                   FC_FlagEvent &event)
{
   FC_Node n1, n2, pre_branch_leg2_break;
   int branch_type = FC_BRANCH_NONE;
   bool branch_found = FC_FindBranchAfterLeg2(nodes,
                                             leg2_pos,
                                             event.direction,
                                             event.waist.price,
                                             event.leg2.price,
                                             allow_waist_break_branch,
                                             allow_leg2_break_before_branch,
                                             eps,
                                             n1,
                                             n2,
                                             branch_type,
                                             pre_branch_leg2_break);

   if(!branch_found)
   {
      if(require_branch12)
         event.status = FC_STATUS_OPEN;
      return (!require_branch12);
   }

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

   if(pre_branch_leg2_break.index >= 0)
   {
      event.pre_branch_leg2_break_index = pre_branch_leg2_break.index;
      event.pre_branch_leg2_break_time = pre_branch_leg2_break.time;
      event.pre_branch_leg2_break_price = pre_branch_leg2_break.price;
   }

   FC_Node confirm_node;
   bool confirmed = FC_FindLeg2RebreakAfterBranch(nodes,
                                                  event.n2.index,
                                                  event.direction,
                                                  event.leg2.price,
                                                  eps,
                                                  confirm_node);
   if(confirmed)
   {
      event.status = FC_STATUS_CONFIRMED;
      event.confirm_index = confirm_node.index;
      event.confirm_time = confirm_node.time;
      event.confirm_price = confirm_node.price;
   }
   else if(pre_branch_leg2_break_can_confirm && pre_branch_leg2_break.index >= 0)
   {
      // F2-only rule: a Leg2 break may occur before F2 forms its final branch 2.
      // Once branch 2 is formed, that pre-branch Leg2 break is accepted as the
      // F2 confirmation break for audit/status purposes.
      event.status = FC_STATUS_CONFIRMED;
      event.confirm_index = pre_branch_leg2_break.index;
      event.confirm_time = pre_branch_leg2_break.time;
      event.confirm_price = pre_branch_leg2_break.price;
   }
   else if(require_leg2_rebreak)
   {
      event.status = FC_STATUS_OPEN;
   }
   return true;
}

bool FC_SameCore(const FC_FlagEvent &a, const FC_FlagEvent &b)
{
   return (a.direction == b.direction &&
           a.origin.index == b.origin.index &&
           a.leg1.index == b.leg1.index &&
           a.waist.index == b.waist.index &&
           a.leg2.index == b.leg2.index);
}

bool FC_F1PromotedToF2(const FC_FlagEvent &f1, const FC_FlagEvent &f2_events[])
{
   int n = ArraySize(f2_events);
   for(int i=0; i<n; i++)
   {
      if(FC_SameCore(f1, f2_events[i]))
         return true;
   }
   return false;
}

bool FC_BuildF1FromNodeWindow(const FC_Node &nodes[],
                              const int start_pos,
                              const bool scan_bullish,
                              const bool scan_bearish,
                              const bool require_branch12,
                              const bool require_leg2_rebreak,
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
   event.status = FC_STATUS_OPEN;
   event.origin = origin;
   event.leg1 = leg1;
   event.waist = waist;
   event.leg2 = leg2;
   event.body_size = FC_FlagBodySize(event);

   if(!FC_ApplyBranchAndConfirmation(nodes,
                                      start_pos+3,
                                      false,
                                      false,
                                      false,
                                      require_branch12,
                                      require_leg2_rebreak,
                                      eps,
                                      event))
      return false;
   return true;
}

bool FC_BuildF2FromParentF1(const FC_Node &nodes[],
                            const FC_FlagEvent &parent,
                            const int parent_array_index,
                            const bool require_parent_confirmed,
                            const bool require_f2_at_least_parent_size,
                            const double f2_min_parent_size_ratio,
                            const bool allow_waist_break_branch,
                            const bool require_branch12,
                            const bool require_leg2_rebreak,
                            const double eps,
                            FC_FlagEvent &event)
{
   FC_InitFlagEvent(event);
   if(parent.level != FC_LEVEL_F1) return false;
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

   double f2_body_size = FC_BodySizeFromNodes(origin, leg2);
   double min_required_size = parent_body_size * MathMax(0.0, f2_min_parent_size_ratio);

   // F2 symmetry/scale contract:
   // F2 is a continuation count after F1, so its body must not be smaller than
   // the parent F1 body when the filter is enabled. Both are measured from
   // origin/start-of-leg to Leg2 final point, using vertical price distance.
   if(require_f2_at_least_parent_size && parent_body_size > eps)
   {
      if(f2_body_size + eps < min_required_size)
         return false;
   }

   event.level = FC_LEVEL_F2;
   event.direction = parent.direction;
   event.status = FC_STATUS_OPEN;
   event.parent_event_index = parent_array_index;
   event.parent_origin_index = parent.origin.index;
   event.origin = origin;
   event.leg1 = leg1;
   event.waist = waist;
   event.leg2 = leg2;
   event.body_size = f2_body_size;
   event.parent_body_size = parent_body_size;
   event.parent_size_ratio = (parent_body_size > 0.0 ? f2_body_size / parent_body_size : 0.0);

   if(!FC_ApplyBranchAndConfirmation(nodes,
                                      start_pos+3,
                                      allow_waist_break_branch,
                                      true,
                                      true,
                                      require_branch12,
                                      require_leg2_rebreak,
                                      eps,
                                      event))
      return false;
   return true;
}

int FC_DetectFlagsFromNodes(const FC_Node &nodes[],
                            const bool scan_f1,
                            const bool scan_f2,
                            const bool scan_bullish,
                            const bool scan_bearish,
                            const bool suppress_f1_bodies_promoted_to_f2,
                            const bool require_f1_branch12,
                            const bool require_f1_leg2_rebreak,
                            const bool require_parent_f1_confirmed_for_f2,
                            const bool require_f2_at_least_parent_size,
                            const double f2_min_parent_size_ratio,
                            const bool allow_f2_waist_break_branch,
                            const bool require_f2_branch12,
                            const bool require_f2_leg2_rebreak,
                            const double eps,
                            FC_FlagEvent &events[])
{
   ArrayResize(events, 0);
   FC_FlagEvent f1_events[];
   FC_FlagEvent f2_events[];
   ArrayResize(f1_events, 0);
   ArrayResize(f2_events, 0);

   int n = ArraySize(nodes);
   if(n < 4) return 0;

   if(scan_f1)
   {
      for(int p=0; p<=n-4; p++)
      {
         FC_FlagEvent e;
         if(FC_BuildF1FromNodeWindow(nodes,
                                     p,
                                     scan_bullish,
                                     scan_bearish,
                                     require_f1_branch12,
                                     require_f1_leg2_rebreak,
                                     eps,
                                     e))
         {
            FC_AppendEvent(f1_events, e);
         }
      }
   }

   if(scan_f2)
   {
      int f1n = ArraySize(f1_events);
      for(int i=0; i<f1n; i++)
      {
         FC_FlagEvent e2;
         if(FC_BuildF2FromParentF1(nodes,
                                   f1_events[i],
                                   i,
                                   require_parent_f1_confirmed_for_f2,
                                   require_f2_at_least_parent_size,
                                   f2_min_parent_size_ratio,
                                   allow_f2_waist_break_branch,
                                   require_f2_branch12,
                                   require_f2_leg2_rebreak,
                                   eps,
                                   e2))
         {
            FC_AppendEvent(f2_events, e2);
         }
      }
   }

   if(scan_f1)
   {
      int f1_total = ArraySize(f1_events);
      for(int k=0; k<f1_total; k++)
      {
         if(suppress_f1_bodies_promoted_to_f2 && FC_F1PromotedToF2(f1_events[k], f2_events))
            continue;
         FC_AppendEvent(events, f1_events[k]);
      }
   }

   if(scan_f2)
   {
      int f2_total = ArraySize(f2_events);
      for(int k=0; k<f2_total; k++)
         FC_AppendEvent(events, f2_events[k]);
   }

   return ArraySize(events);
}

int FC_DetectFlags(const MqlRates &rates[],
                   const int total,
                   const int swing_L,
                   const bool scan_f1,
                   const bool scan_f2,
                   const bool scan_bullish,
                   const bool scan_bearish,
                   const bool suppress_f1_bodies_promoted_to_f2,
                   const bool require_f1_branch12,
                   const bool require_f1_leg2_rebreak,
                   const bool require_parent_f1_confirmed_for_f2,
                   const bool require_f2_at_least_parent_size,
                   const double f2_min_parent_size_ratio,
                   const bool allow_f2_waist_break_branch,
                   const bool require_f2_branch12,
                   const bool require_f2_leg2_rebreak,
                   const double eps,
                   FC_Node &nodes[],
                   FC_FlagEvent &events[])
{
   FC_BuildNodes(rates, total, swing_L, nodes);
   return FC_DetectFlagsFromNodes(nodes,
                                  scan_f1,
                                  scan_f2,
                                  scan_bullish,
                                  scan_bearish,
                                  suppress_f1_bodies_promoted_to_f2,
                                  require_f1_branch12,
                                  require_f1_leg2_rebreak,
                                  require_parent_f1_confirmed_for_f2,
                                  require_f2_at_least_parent_size,
                                  f2_min_parent_size_ratio,
                                  allow_f2_waist_break_branch,
                                  require_f2_branch12,
                                  require_f2_leg2_rebreak,
                                  eps,
                                  events);
}

#endif
