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


bool FC_HasInvalidationBetween(const FC_Node &nodes[],
                               const int from_pos,
                               const int to_pos,
                               const int direction,
                               const double invalidation_price,
                               const double eps)
{
   int n = ArraySize(nodes);
   int a = from_pos;
   if(a < 0) a = 0;
   int b = to_pos;
   if(b > n - 1) b = n - 1;
   for(int p=a; p<=b; p++)
   {
      if(FC_NodeBreaksInvalidation(direction, nodes[p], invalidation_price, eps))
         return true;
   }
   return false;
}

bool FC_CoreMatchesDirection(const int direction,
                             const FC_Node &origin,
                             const FC_Node &leg1,
                             const FC_Node &waist,
                             const FC_Node &leg2,
                             const double eps)
{
   if(direction == FC_DIR_BULLISH)
      return FC_IsBullishCore(origin, leg1, waist, leg2, eps);
   if(direction == FC_DIR_BEARISH)
      return FC_IsBearishCore(origin, leg1, waist, leg2, eps);
   return false;
}

void FC_FillCoreEvent(FC_FlagEvent &event,
                      const int level,
                      const int direction,
                      const FC_Node &origin,
                      const FC_Node &leg1,
                      const FC_Node &waist,
                      const FC_Node &leg2,
                      const int parent_event_index,
                      const int parent_origin_index,
                      const int parent_level,
                      const int chain_id,
                      const int chain_step,
                      const double parent_body_size)
{
   FC_InitFlagEvent(event);
   event.level = level;
   event.direction = direction;
   event.status = FC_STATUS_OPEN;
   event.parent_event_index = parent_event_index;
   event.parent_origin_index = parent_origin_index;
   event.parent_level = parent_level;
   event.chain_id = chain_id;
   event.chain_step = chain_step;
   event.origin = origin;
   event.leg1 = leg1;
   event.waist = waist;
   event.leg2 = leg2;
   event.body_size = FC_BodySizeFromNodes(origin, leg2);
   event.parent_body_size = parent_body_size;
   event.parent_size_ratio = (parent_body_size > 0.0 ? event.body_size / parent_body_size : 0.0);
}

bool FC_BetterCoreCandidate(const FC_FlagEvent &candidate, const FC_FlagEvent &best, const bool have_best)
{
   if(!have_best) return true;
   if(candidate.status == FC_STATUS_CONFIRMED && best.status != FC_STATUS_CONFIRMED) return true;
   if(candidate.status != FC_STATUS_CONFIRMED && best.status == FC_STATUS_CONFIRMED) return false;

   // While an F is live, its body is allowed to extend. Prefer the larger/further
   // body when neither candidate is clearly superior by status.
   if(candidate.body_size > best.body_size) return true;
   if(candidate.body_size < best.body_size) return false;
   return (candidate.leg2.index > best.leg2.index);
}

bool FC_BuildCoreFromFixedOrigin(const FC_Node &nodes[],
                                 const int origin_pos,
                                 const int direction,
                                 const int level,
                                 const bool continuation_level,
                                 const bool allow_waist_break_branch,
                                 const bool require_at_least_parent_size,
                                 const double min_parent_size_ratio,
                                 const double parent_body_size,
                                 const int max_core_search_nodes,
                                 const int parent_event_index,
                                 const int parent_origin_index,
                                 const int parent_level,
                                 const int chain_id,
                                 const int chain_step,
                                 const double eps,
                                 FC_FlagEvent &event,
                                 int &core_leg2_pos)
{
   FC_InitFlagEvent(event);
   core_leg2_pos = -1;

   int total_nodes = ArraySize(nodes);
   if(origin_pos < 0 || origin_pos + 3 >= total_nodes) return false;

   FC_Node origin = nodes[origin_pos];
   double invalidation_price = (continuation_level ? origin.price : 0.0);

   int last_pos = total_nodes - 1;
   if(max_core_search_nodes > 0)
   {
      int requested_last_pos = origin_pos + max_core_search_nodes;
      if(requested_last_pos < last_pos)
         last_pos = requested_last_pos;
   }
   if(origin_pos + 3 > last_pos) return false;

   FC_FlagEvent best;
   FC_InitFlagEvent(best);
   int best_l2_pos = -1;
   bool have_best = false;

   for(int leg1_pos=origin_pos+1; leg1_pos<=last_pos-2; leg1_pos++)
   {
      if(continuation_level && FC_NodeBreaksInvalidation(direction, nodes[leg1_pos], invalidation_price, eps))
         break;

      for(int waist_pos=leg1_pos+1; waist_pos<=last_pos-1; waist_pos++)
      {
         if(continuation_level && FC_HasInvalidationBetween(nodes, leg1_pos, waist_pos, direction, invalidation_price, eps))
            break;

         for(int leg2_pos=waist_pos+1; leg2_pos<=last_pos; leg2_pos++)
         {
            if(continuation_level && FC_HasInvalidationBetween(nodes, waist_pos, leg2_pos, direction, invalidation_price, eps))
               break;

            FC_Node leg1 = nodes[leg1_pos];
            FC_Node waist = nodes[waist_pos];
            FC_Node leg2 = nodes[leg2_pos];

            if(!FC_CoreMatchesDirection(direction, origin, leg1, waist, leg2, eps))
               continue;

            FC_FlagEvent candidate;
            FC_FillCoreEvent(candidate,
                             level,
                             direction,
                             origin,
                             leg1,
                             waist,
                             leg2,
                             parent_event_index,
                             parent_origin_index,
                             parent_level,
                             chain_id,
                             chain_step,
                             parent_body_size);

            if(require_at_least_parent_size && parent_body_size > eps)
            {
               double min_required_size = parent_body_size * MathMax(0.0, min_parent_size_ratio);
               if(candidate.body_size + eps < min_required_size)
                  continue;
            }

            FC_ApplyBranchAndConfirmation(nodes,
                                          leg2_pos,
                                          continuation_level,
                                          allow_waist_break_branch,
                                          eps,
                                          candidate);

            // Root F1 can repair an early waist choice by selecting a later waist.
            // Therefore invalidated F1 core candidates are skipped, not used to end
            // the whole root search. Continuations only die on origin invalidation,
            // already checked above.
            if(candidate.status == FC_STATUS_INVALIDATED)
               continue;

            // Do NOT discard a valid F1 only because its continuation origin
            // is not available yet. In live/partition mode that means the F1 is
            // still the owner of this market segment and the next level is pending.
            // The previous build skipped confirmed F1 events without internal 2;
            // this could make the whole chart draw nothing.

            if(FC_BetterCoreCandidate(candidate, best, have_best))
            {
               best = candidate;
               best_l2_pos = leg2_pos;
               have_best = true;
            }
         }
      }
   }

   if(!have_best) return false;
   event = best;
   core_leg2_pos = best_l2_pos;
   return true;
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
   int direction = FC_DIR_NONE;
   if(scan_bullish && origin.kind == FC_NODE_LOW)
      direction = FC_DIR_BULLISH;
   else if(scan_bearish && origin.kind == FC_NODE_HIGH)
      direction = FC_DIR_BEARISH;
   if(direction == FC_DIR_NONE) return false;

   int core_pos = -1;
   // Backward compatible wrapper: use a small local search rather than exactly
   // start,start+1,start+2,start+3. This lets F1 repair its waist before confirm.
   return FC_BuildCoreFromFixedOrigin(nodes,
                                      start_pos,
                                      direction,
                                      FC_LEVEL_F1,
                                      false,
                                      false,
                                      false,
                                      1.0,
                                      0.0,
                                      24,
                                      -1,
                                      -1,
                                      FC_LEVEL_NONE,
                                      -1,
                                      1,
                                      eps,
                                      event,
                                      core_pos);
}

bool FC_BuildRootF1FromOriginSearch(const FC_Node &nodes[],
                                    const int origin_pos,
                                    const bool scan_bullish,
                                    const bool scan_bearish,
                                    const int root_core_search_max_nodes,
                                    const double eps,
                                    FC_FlagEvent &event,
                                    int &root_leg2_pos)
{
   FC_InitFlagEvent(event);
   root_leg2_pos = -1;
   int n = ArraySize(nodes);
   if(origin_pos + 3 >= n) return false;

   FC_Node origin = nodes[origin_pos];
   int direction = FC_DIR_NONE;
   if(scan_bullish && origin.kind == FC_NODE_LOW)
      direction = FC_DIR_BULLISH;
   else if(scan_bearish && origin.kind == FC_NODE_HIGH)
      direction = FC_DIR_BEARISH;
   if(direction == FC_DIR_NONE) return false;

   return FC_BuildCoreFromFixedOrigin(nodes,
                                      origin_pos,
                                      direction,
                                      FC_LEVEL_F1,
                                      false,
                                      false,
                                      false,
                                      1.0,
                                      0.0,
                                      root_core_search_max_nodes,
                                      -1,
                                      -1,
                                      FC_LEVEL_NONE,
                                      -1,
                                      1,
                                      eps,
                                      event,
                                      root_leg2_pos);
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

   double parent_body_size = parent.body_size;
   if(parent_body_size <= 0.0)
      parent_body_size = FC_FlagBodySize(parent);

   int core_pos = -1;
   bool ok = FC_BuildCoreFromFixedOrigin(nodes,
                                         start_pos,
                                         parent.direction,
                                         child_level,
                                         true,
                                         allow_waist_break_branch,
                                         require_child_at_least_parent_size,
                                         child_min_parent_size_ratio,
                                         parent_body_size,
                                         continuation_core_search_max_nodes,
                                         parent_array_index,
                                         parent.origin.index,
                                         parent.level,
                                         parent.chain_id,
                                         parent.chain_step + 1,
                                         eps,
                                         event,
                                         core_pos);
   return ok;
}

int FC_FindNextOppositeRootPosition(const FC_Node &nodes[],
                                    const int cursor_pos,
                                    const int blocked_direction,
                                    const bool scan_bullish,
                                    const bool scan_bearish,
                                    const int root_core_search_max_nodes,
                                    const double eps)
{
   int n = ArraySize(nodes);
   for(int p=cursor_pos; p<=n-4; p++)
   {
      FC_FlagEvent candidate;
      int l2_pos = -1;
      if(!FC_BuildRootF1FromOriginSearch(nodes, p, scan_bullish, scan_bearish, root_core_search_max_nodes, eps, candidate, l2_pos))
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
                               const int root_core_search_max_nodes,
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
      int l2_pos = -1;
      if(!FC_BuildRootF1FromOriginSearch(nodes, p, scan_bullish, scan_bearish, root_core_search_max_nodes, eps, candidate, l2_pos))
         continue;

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



// -----------------------------------------------------------------------------
// Parallel / fractal sequence layer
// -----------------------------------------------------------------------------
// The earlier detector accepted one global chain. The user contract is fractal:
// every valid F1 opens its own sequence and waits for F2, while other sequences
// can exist in parallel on the same or other swing scales.

void FC_AppendNodes(FC_Node &dst[], const FC_Node &src[])
{
   int n0 = ArraySize(dst);
   int n1 = ArraySize(src);
   ArrayResize(dst, n0 + n1);
   for(int i=0; i<n1; i++)
      dst[n0+i] = src[i];
}

int FC_MaxChainId(const FC_FlagEvent &events[])
{
   int m = 0;
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
      if(events[i].chain_id > m) m = events[i].chain_id;
   return m;
}

void FC_AppendEventWithScaleAndOffset(FC_FlagEvent &events[],
                                      const FC_FlagEvent &src,
                                      const int scale_L,
                                      const int chain_offset)
{
   FC_FlagEvent e = src;
   e.scale_L = scale_L;
   if(e.chain_id > 0)
      e.chain_id += chain_offset;
   FC_AppendEvent(events, e);
}

bool FC_ScaleAlreadyListed(const int &scales[], const int count, const int value)
{
   for(int i=0; i<count; i++)
      if(scales[i] == value) return true;
   return false;
}

int FC_AddScaleIfValid(int &scales[], int count, const int value)
{
   if(value <= 0) return count;
   if(FC_ScaleAlreadyListed(scales, count, value)) return count;
   scales[count] = value;
   return count + 1;
}

int FC_DetectParallelSequencesFromNodes(const FC_Node &nodes[],
                                        const int scale_L,
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
                                        const int root_core_search_max_nodes,
                                        const int continuation_core_search_max_nodes,
                                        const bool force_continuation_after_confirmed_parent,
                                        const int max_root_sequences_per_scale,
                                        const double eps,
                                        FC_FlagEvent &events[])
{
   ArrayResize(events, 0);
   int n = ArraySize(nodes);
   if(n < 4) return 0;

   int max_level = FC_MaxRequestedLevel(scan_f1, scan_f2, scan_f3);
   if(max_level == FC_LEVEL_NONE) return 0;

   int chain_counter = 0;

   // This is intentionally NOT a single cursor partition. Each root candidate can
   // create its own live sequence. Continuations remain children of that root.
   for(int p=0; p<=n-4; p++)
   {
      if(max_root_sequences_per_scale > 0 && chain_counter >= max_root_sequences_per_scale)
         break;

      FC_FlagEvent root;
      int root_leg2_pos = -1;
      if(!FC_BuildRootF1FromOriginSearch(nodes,
                                         p,
                                         scan_bullish,
                                         scan_bearish,
                                         root_core_search_max_nodes,
                                         eps,
                                         root,
                                         root_leg2_pos))
         continue;

      if(root.status == FC_STATUS_INVALIDATED)
         continue;

      chain_counter++;
      root.chain_id = chain_counter;
      root.chain_step = 1;
      root.scale_L = scale_L;

      FC_FlagEvent chain_events[];
      ArrayResize(chain_events, 0);
      FC_AppendEvent(chain_events, root);

      FC_FlagEvent parent = root;
      int parent_local_index = 0;

      for(int level=FC_LEVEL_F2; level<=max_level; level++)
      {
         // After F1/F2, the next level is mandatory conceptually, but it can be
         // live/unavailable for a long time. If it cannot be constructed yet, we
         // keep the parent sequence visible and simply stop this sequence here.
         if(require_parent_confirmed_for_next_f && parent.status != FC_STATUS_CONFIRMED)
            break;

         if(!parent.has_n2)
            break;

         FC_FlagEvent child;
         if(!FC_BuildContinuationFromParent(nodes,
                                            parent,
                                            parent_local_index,
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

         child.chain_id = chain_counter;
         child.chain_step = parent.chain_step + 1;
         child.scale_L = scale_L;
         FC_AppendEvent(chain_events, child);

         parent = child;
         parent_local_index = ArraySize(chain_events) - 1;
      }

      int c = ArraySize(chain_events);
      for(int k=0; k<c; k++)
         FC_AppendIfRequested(events, chain_events[k], scan_f1, scan_f2, scan_f3);
   }

   return ArraySize(events);
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
                            const int root_core_search_max_nodes,
                            const int continuation_core_search_max_nodes,
                            const bool force_continuation_after_confirmed_parent,
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

   while(cursor <= n - 4)
   {
      FC_FlagEvent root;
      int root_pos = -1;
      if(!FC_FindNextAcceptedRootF1(nodes, cursor, scan_bullish, scan_bearish, root_core_search_max_nodes, eps, root, root_pos))
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
      bool unresolved_mandatory_continuation = false;

      for(int level=FC_LEVEL_F2; level<=max_level; level++)
      {
         if(parent.status != FC_STATUS_CONFIRMED)
            break;

         // The user's grammar is mandatory: after F1 we search F2; after F2 we
         // search F3. The only way this does not happen is that the parent has no
         // usable internal 2, or the child origin is invalidated before a child body
         // appears. In both cases we do NOT restart the same flow as another F1.
         if(!parent.has_n2)
         {
            unresolved_mandatory_continuation = force_continuation_after_confirmed_parent;
            break;
         }

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
         {
            unresolved_mandatory_continuation = force_continuation_after_confirmed_parent;
            break;
         }

         if(child.status == FC_STATUS_INVALIDATED)
         {
            unresolved_mandatory_continuation = force_continuation_after_confirmed_parent;
            break;
         }

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

      // If the live/current chain is open, or a mandatory F2/F3 continuation is
      // unresolved, do not allow the same flow to be reinterpreted as a new F1.
      // This is the core partition rule: an active chain owns the future until it
      // confirms into the next F-level or invalidates into a reset/ND phase.
      if(parent.status == FC_STATUS_OPEN || unresolved_mandatory_continuation)
         break;

      int next_cursor = terminal_pos + 1;
      if(next_cursor <= cursor)
         next_cursor = cursor + 1;
      cursor = next_cursor;
   }

   return ArraySize(events);
}

int FC_DetectFlags(const MqlRates &rates[],
                   const int total,
                   const int swing_L,
                   const bool use_multi_scale,
                   const int swing_L2,
                   const int swing_L3,
                   const int swing_L4,
                   const int swing_L5,
                   const int swing_L6,
                   const int max_root_sequences_per_scale,
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
                   const int root_core_search_max_nodes,
                   const int continuation_core_search_max_nodes,
                   const bool force_continuation_after_confirmed_parent,
                   const double eps,
                   FC_Node &nodes[],
                   FC_FlagEvent &events[])
{
   ArrayResize(nodes, 0);
   ArrayResize(events, 0);

   int scales[6];
   int scale_count = 0;
   scale_count = FC_AddScaleIfValid(scales, scale_count, swing_L);
   if(use_multi_scale)
   {
      scale_count = FC_AddScaleIfValid(scales, scale_count, swing_L2);
      scale_count = FC_AddScaleIfValid(scales, scale_count, swing_L3);
      scale_count = FC_AddScaleIfValid(scales, scale_count, swing_L4);
      scale_count = FC_AddScaleIfValid(scales, scale_count, swing_L5);
      scale_count = FC_AddScaleIfValid(scales, scale_count, swing_L6);
   }

   if(scale_count <= 0) return 0;

   for(int si=0; si<scale_count; si++)
   {
      int L = scales[si];
      FC_Node scale_nodes[];
      FC_BuildNodes(rates, total, L, scale_nodes);
      FC_AppendNodes(nodes, scale_nodes);

      FC_FlagEvent scale_events[];
      FC_DetectParallelSequencesFromNodes(scale_nodes,
                                          L,
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
                                          root_core_search_max_nodes,
                                          continuation_core_search_max_nodes,
                                          force_continuation_after_confirmed_parent,
                                          max_root_sequences_per_scale,
                                          eps,
                                          scale_events);

      int offset = FC_MaxChainId(events);
      int ec = ArraySize(scale_events);
      for(int i=0; i<ec; i++)
         FC_AppendEventWithScaleAndOffset(events, scale_events[i], L, offset);
   }

   return ArraySize(events);
}

#endif
