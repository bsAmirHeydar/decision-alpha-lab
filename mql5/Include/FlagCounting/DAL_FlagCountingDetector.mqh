#ifndef __DAL_FLAG_COUNTING_DETECTOR_MQH__
#define __DAL_FLAG_COUNTING_DETECTOR_MQH__
#property strict
#include "DAL_FlagCountingTypes.mqh"
#include "DAL_FlagCountingNodeDetector.mqh"

// -----------------------------------------------------------------------------
// Flag-counting detector contract
// -----------------------------------------------------------------------------
// This module is intentionally a CHAIN COUNTER, not a loose pattern scanner.
// It accepts one forward chain at a time:
//   ND/unused nodes -> F1 -> F2 -> F3 -> ND/unused nodes -> F1 -> ...
//
// Root rule:
//   F1 is the only root level. After an accepted F1 is confirmed, the continuation
//   of that same movement is F2, not another overlapping F1.
//
// Continuation rule:
//   F2 starts from parent F1 internal 2.
//   F3 starts from parent F2 internal 2.
//
// Confirmation rule:
//   every F confirms by rebreaking its own Leg2 before its invalidation boundary.
//
// Invalidation boundary:
//   F1 invalidates at its waist.
//   F2/F3 invalidate at their own origin / start-of-leg.
//
// Visual rule is handled by renderer: only body is drawn; 1/2 are labels only.
// -----------------------------------------------------------------------------

void FC_AppendEvent(FC_FlagEvent &events[], const FC_FlagEvent &event)
{
   int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n] = event;
}

bool FC_ShouldAppendLevel(const int level, const bool scan_f1, const bool scan_f2, const bool scan_f3)
{
   if(level == FC_LEVEL_F1) return scan_f1;
   if(level == FC_LEVEL_F2) return scan_f2;
   if(level == FC_LEVEL_F3) return scan_f3;
   return false;
}

int FC_MaxRequestedLevel(const bool scan_f1, const bool scan_f2, const bool scan_f3)
{
   if(scan_f3) return FC_LEVEL_F3;
   if(scan_f2) return FC_LEVEL_F2;
   if(scan_f1) return FC_LEVEL_F1;
   return FC_LEVEL_NONE;
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

   // Waist must be inside the leg range. It cannot fall behind the leg origin.
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

   // Waist must be inside the leg range. It cannot fall behind the leg origin.
   if(!(leg1.price  < origin.price - eps)) return false;
   if(!(waist.price < origin.price - eps)) return false;
   if(!(waist.price > leg1.price  + eps)) return false;
   if(!(leg2.price  < leg1.price  - eps)) return false;
   return true;
}

bool FC_InternalNodeProtectsWaist(const int direction, const FC_Node &node, const double waist_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return (node.kind == FC_NODE_LOW && node.price > waist_price + eps);
   if(direction == FC_DIR_BEARISH)
      return (node.kind == FC_NODE_HIGH && node.price < waist_price - eps);
   return false;
}

bool FC_NodeBreaksWaist(const int direction, const FC_Node &node, const double waist_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return (node.kind == FC_NODE_LOW && node.price <= waist_price + eps);
   if(direction == FC_DIR_BEARISH)
      return (node.kind == FC_NODE_HIGH && node.price >= waist_price - eps);
   return false;
}

bool FC_NodeBreaksInvalidation(const int direction, const FC_Node &node, const double invalidation_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return (node.kind == FC_NODE_LOW && node.price <= invalidation_price + eps);
   if(direction == FC_DIR_BEARISH)
      return (node.kind == FC_NODE_HIGH && node.price >= invalidation_price - eps);
   return false;
}

bool FC_NodeBreaksLeg2(const int direction, const FC_Node &node, const double leg2_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return (node.kind == FC_NODE_HIGH && node.price >= leg2_price + eps);
   if(direction == FC_DIR_BEARISH)
      return (node.kind == FC_NODE_LOW && node.price <= leg2_price - eps);
   return false;
}

bool FC_Internal2ValidAgainstInternal1(const int direction, const FC_Node &n1, const FC_Node &n2, const double waist_price, const double eps)
{
   if(direction == FC_DIR_BULLISH)
   {
      if(n1.kind != FC_NODE_LOW || n2.kind != FC_NODE_LOW) return false;
      if(n1.price <= waist_price + eps) return false;
      if(n2.price <= waist_price + eps) return false;
      return (n2.price < n1.price - eps);
   }
   if(direction == FC_DIR_BEARISH)
   {
      if(n1.kind != FC_NODE_HIGH || n2.kind != FC_NODE_HIGH) return false;
      if(n1.price >= waist_price - eps) return false;
      if(n2.price >= waist_price - eps) return false;
      return (n2.price > n1.price + eps);
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

      // For F1, internal 1/2 belongs before Leg2 confirmation.
      // For F2/F3, Leg2 may be extended first and the counting branch may appear after.
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

int FC_EventTerminalNodePosition(const FC_Node &nodes[], const FC_FlagEvent &event)
{
   if(event.confirm_index >= 0)
   {
      int pc = FC_FindNodePositionByIndex(nodes, event.confirm_index);
      if(pc >= 0) return pc;
   }
   if(event.invalid_index >= 0)
   {
      int pi = FC_FindNodePositionByIndex(nodes, event.invalid_index);
      if(pi >= 0) return pi;
   }
   int pl2 = FC_FindNodePositionByIndex(nodes, event.leg2.index);
   return pl2;
}

void FC_ApplyBranchAndConfirmation(const FC_Node &nodes[],
                                   const int leg2_pos,
                                   const bool continuation_level,
                                   const bool allow_waist_break_branch,
                                   const double eps,
                                   FC_FlagEvent &event)
{
   // Confirmation and invalidation are deliberately separated from counting labels.
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

   // Branch 1/2 is for counting/audit and for the next continuation origin.
   // It is not a hard gate for confirming the current body.
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
   else if(scan_bearish && FC_IsBearishCore(origin, leg1, waist, leg2, eps))
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
                                    const int continuation_core_search_max_nodes,
                                    const double eps,
                                    FC_FlagEvent &event)
{
   FC_InitFlagEvent(event);
   if(parent.level <= FC_LEVEL_NONE) return false;
   if(child_level <= parent.level) return false;
   if(!parent.has_n2) return false;
   if(require_parent_confirmed && parent.status != FC_STATUS_CONFIRMED) return false;

   int start_pos = FC_FindNodePositionByIndex(nodes, parent.n2.index);
   if(start_pos < 0) return false;

   int total_nodes = ArraySize(nodes);
   if(start_pos + 3 >= total_nodes) return false;

   FC_Node origin = nodes[start_pos];
   double invalidation_price = origin.price;

   double parent_body_size = parent.body_size;
   if(parent_body_size <= 0.0)
      parent_body_size = FC_FlagBodySize(parent);

   int max_scan = MathMax(3, continuation_core_search_max_nodes);
   int last_leg1_pos = total_nodes - 3;
   int requested_last_leg1_pos = start_pos + max_scan;
   if(requested_last_leg1_pos < last_leg1_pos)
      last_leg1_pos = requested_last_leg1_pos;

   // Continuation is not a new loose F1. Its origin is fixed at parent internal 2.
   // However, the next valid Leg1/Waist/Leg2 body may be a few nodes later because
   // the compressed node stream can contain small hooks before the real child body.
   for(int leg1_pos=start_pos+1; leg1_pos<=last_leg1_pos; leg1_pos++)
   {
      // If the child origin is invalidated before a valid child body appears, the
      // continuation attempt is dead. This is the F2/F3 invalidation contract.
      if(FC_NodeBreaksInvalidation(parent.direction, nodes[leg1_pos], invalidation_price, eps))
         return false;

      FC_Node leg1  = nodes[leg1_pos];
      FC_Node waist = nodes[leg1_pos+1];
      FC_Node leg2  = nodes[leg1_pos+2];

      bool core_ok = false;
      if(parent.direction == FC_DIR_BULLISH)
         core_ok = FC_IsBullishCore(origin, leg1, waist, leg2, eps);
      else if(parent.direction == FC_DIR_BEARISH)
         core_ok = FC_IsBearishCore(origin, leg1, waist, leg2, eps);
      if(!core_ok)
         continue;

      double child_body_size = FC_BodySizeFromNodes(origin, leg2);
      double min_required_size = parent_body_size * MathMax(0.0, child_min_parent_size_ratio);
      if(require_child_at_least_parent_size && parent_body_size > eps)
      {
         if(child_body_size + eps < min_required_size)
            continue;
      }

      event.level = child_level;
      event.direction = parent.direction;
      event.status = FC_STATUS_OPEN;
      event.parent_event_index = parent_array_index;
      event.parent_origin_index = parent.origin.index;
      event.parent_level = parent.level;
      event.chain_id = parent.chain_id;
      event.chain_step = parent.chain_step + 1;
      event.origin = origin;
      event.leg1 = leg1;
      event.waist = waist;
      event.leg2 = leg2;
      event.body_size = child_body_size;
      event.parent_body_size = parent_body_size;
      event.parent_size_ratio = (parent_body_size > 0.0 ? child_body_size / parent_body_size : 0.0);

      FC_ApplyBranchAndConfirmation(nodes, leg1_pos+2, true, allow_waist_break_branch, eps, event);
      return true;
   }

   return false;
}

int FC_FindNextOppositeRootPosition(const FC_Node &nodes[],
                                    const int cursor_pos,
                                    const int blocked_direction,
                                    const bool scan_bullish,
                                    const bool scan_bearish,
                                    const double eps)
{
   int n = ArraySize(nodes);
   for(int p=cursor_pos; p<=n-4; p++)
   {
      FC_FlagEvent candidate;
      if(!FC_BuildF1FromNodeWindow(nodes, p, scan_bullish, scan_bearish, eps, candidate))
         continue;
      if(candidate.status == FC_STATUS_INVALIDATED)
         continue;
      if(candidate.direction != blocked_direction)
         return p;
   }
   return -1;
}

bool FC_FindNextAcceptedRootF1(const FC_Node &nodes[],
                               const int cursor_pos,
                               const bool scan_bullish,
                               const bool scan_bearish,
                               const double eps,
                               FC_FlagEvent &event,
                               int &root_pos)
{
   FC_InitFlagEvent(event);
   root_pos = -1;

   int n = ArraySize(nodes);
   for(int p=cursor_pos; p<=n-4; p++)
   {
      FC_FlagEvent candidate;
      if(!FC_BuildF1FromNodeWindow(nodes, p, scan_bullish, scan_bearish, eps, candidate))
         continue;

      // Invalid root bodies are failed attempts inside an ND/hook phase, not accepted flags.
      if(candidate.status == FC_STATUS_INVALIDATED)
         continue;

      event = candidate;
      root_pos = p;
      return true;
   }
   return false;
}

void FC_AppendIfRequested(FC_FlagEvent &events[],
                          const FC_FlagEvent &event,
                          const bool scan_f1,
                          const bool scan_f2,
                          const bool scan_f3)
{
   if(FC_ShouldAppendLevel(event.level, scan_f1, scan_f2, scan_f3))
      FC_AppendEvent(events, event);
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
                            const int continuation_core_search_max_nodes,
                            const bool avoid_same_direction_f1_restarts,
                            const double eps,
                            FC_FlagEvent &events[])
{
   ArrayResize(events, 0);
   int n = ArraySize(nodes);
   if(n < 4) return 0;

   int max_level = FC_MaxRequestedLevel(scan_f1, scan_f2, scan_f3);
   if(max_level == FC_LEVEL_NONE) return 0;

   int cursor = 0;
   int chain_id = 0;

   // Greedy market partition: do not draw all possible overlapping candidates.
   // Pick the next accepted root, then walk its F1->F2->F3 continuation chain.
   while(cursor <= n - 4)
   {
      FC_FlagEvent root;
      int root_pos = -1;
      if(!FC_FindNextAcceptedRootF1(nodes, cursor, scan_bullish, scan_bearish, eps, root, root_pos))
         break;

      chain_id++;
      root.chain_id = chain_id;
      root.chain_step = 1;

      FC_FlagEvent chain_events[];
      ArrayResize(chain_events, 0);
      FC_AppendEvent(chain_events, root);

      int terminal_pos = FC_EventTerminalNodePosition(nodes, root);
      if(terminal_pos < root_pos + 3)
         terminal_pos = root_pos + 3;

      FC_FlagEvent parent = root;
      int parent_array_index = 0;

      for(int level=FC_LEVEL_F2; level<=max_level; level++)
      {
         if(parent.status != FC_STATUS_CONFIRMED)
            break;
         if(!parent.has_n2)
            break;

         FC_FlagEvent child;
         if(!FC_BuildContinuationFromParent(nodes,
                                            parent,
                                            parent_array_index,
                                            level,
                                            require_parent_confirmed_for_next_f,
                                            require_child_at_least_parent_size,
                                            child_min_parent_size_ratio,
                                            allow_child_waist_break_branch,
                                            continuation_core_search_max_nodes,
                                            eps,
                                            child))
            break;

         if(child.status == FC_STATUS_INVALIDATED)
            break;

         FC_AppendEvent(chain_events, child);
         int child_terminal = FC_EventTerminalNodePosition(nodes, child);
         if(child_terminal > terminal_pos)
            terminal_pos = child_terminal;

         parent = child;
         parent_array_index = ArraySize(chain_events) - 1;
      }

      int chain_count = ArraySize(chain_events);
      for(int i=0; i<chain_count; i++)
         FC_AppendIfRequested(events, chain_events[i], scan_f1, scan_f2, scan_f3);

      // Accepted chain consumes the movement up to its terminal node.
      // This is the key fix: after an F1, the same flow continues as F2/F3,
      // not as a new overlapping F1 candidate.
      int next_cursor = terminal_pos + 1;
      if(next_cursor <= cursor)
         next_cursor = cursor + 1;

      // Partition rule: after a confirmed chain, do not immediately restart
      // another same-direction F1 on the same flow. If no child continuation was
      // accepted, that region is treated as the unresolved ND/hook/transition
      // phase until the opposite root direction appears or the scan ends.
      if(avoid_same_direction_f1_restarts && root.status == FC_STATUS_CONFIRMED)
      {
         int reset_pos = FC_FindNextOppositeRootPosition(nodes,
                                                         next_cursor,
                                                         root.direction,
                                                         scan_bullish,
                                                         scan_bearish,
                                                         eps);
         if(reset_pos >= 0)
            next_cursor = reset_pos;
         else
            break;
      }

      cursor = next_cursor;
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
                   const int continuation_core_search_max_nodes,
                   const bool avoid_same_direction_f1_restarts,
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
                                  continuation_core_search_max_nodes,
                                  avoid_same_direction_f1_restarts,
                                  eps,
                                  events);
}

#endif
