#ifndef __FC6_SEQUENCE_ENGINE_MQH__
#define __FC6_SEQUENCE_ENGINE_MQH__
#property strict
#include "FC6_Types.mqh"
#include "FC6_NodeEngine.mqh"
#include "FC6_HookEngine.mqh"
#include "FC6_FlagEngine.mqh"

// ============================================================================
// V6 Sequence Engine
// ----------------------------------------------------------------------------
// Converts scale-specific node streams into stateful F1 -> F2 -> F3 chains.
// The engine is intentionally verbose and audit-friendly. The renderer must not
// invent structures; every chart object comes from an event/hook emitted here.
// ============================================================================

bool FC6_ShouldKeepEventOnMainChart(const FC6_FlagEvent &e, const FC6_Config &cfg)
{
   if(e.status == FC6_STATUS_INVALIDATED && !cfg.show_invalidated_in_audit) return false;
   if(e.level == FC6_LEVEL_F1 && !cfg.scan_f1) return false;
   if(e.level == FC6_LEVEL_F2 && !cfg.scan_f2) return false;
   if(e.level == FC6_LEVEL_F3 && !cfg.scan_f3) return false;
   return true;
}

void FC6_FinalizeEventIds(FC6_FlagEvent &events[])
{
   for(int i=0; i<ArraySize(events); i++)
      events[i].event_id = i;
}

void FC6_FinalizeHookIds(FC6_HookBranch &hooks[])
{
   for(int i=0; i<ArraySize(hooks); i++)
      hooks[i].branch_id = i;
}

int FC6_AddUniqueEvent(FC6_FlagEvent &events[], FC6_FlagEvent &e, const double eps)
{
   int sz = ArraySize(events);
   if(FC6_EventExists(events, sz, e, eps)) return -1;
   return FC6_AddEvent(events, e);
}

// -----------------------------------------------------------------------------
// Phase boundary helpers
// -----------------------------------------------------------------------------
// The V6 contract does not allow root F1 to be created from arbitrary mid-move
// two-leg windows.  A root F1 must be anchored to a phase boundary: currently an
// ND/Hook adverse extreme for the same direction.  Opposite-F endpoints can be
// added as another boundary source later without changing the event model.

bool FC6_NodeMatchesHookOriginBoundary(const FC6_Node &origin,
                                       const int direction,
                                       const FC6_HookBranch &h,
                                       const double eps)
{
   if(!h.is_nd) return false;
   if(h.direction != direction) return false;
   if(FC6_NodeValid(h.extreme_node) && FC6_SameNodeIdentity(origin, h.extreme_node, eps)) return true;
   if(FC6_NodeValid(h.start_node)   && FC6_SameNodeIdentity(origin, h.start_node, eps)) return true;
   return false;
}

bool FC6_IsAllowedF1PhaseBoundary(const FC6_Node &origin,
                                  const int direction,
                                  const FC6_Config &cfg,
                                  const FC6_HookBranch &phase_hooks[],
                                  const double eps)
{
   if(!cfg.require_f1_phase_boundary) return true;
   int n = ArraySize(phase_hooks);
   int nd_count = 0;
   for(int i=0; i<n; i++)
      if(phase_hooks[i].is_nd && phase_hooks[i].direction == direction)
         nd_count++;
   if(nd_count <= 0) return cfg.allow_f1_fail_open_when_no_hook; // soft semantic fallback: keep the chart inspectable until Hook/ND coverage is strong enough
   for(int i=0; i<n; i++)
      if(FC6_NodeMatchesHookOriginBoundary(origin, direction, phase_hooks[i], eps))
         return true;
   return false;
}

int FC6_BuildPhaseHooksForScale(const FC6_Node &nodes[],
                                const int node_count,
                                const FC6_Config &cfg,
                                const int scale_L,
                                FC6_HookBranch &hooks[])
{
   ArrayResize(hooks, 0);
   if(!cfg.scan_hooks) return 0;
   double eps = cfg.boundary_epsilon_points * _Point;
   for(int d_i=0; d_i<2; d_i++)
   {
      int direction = (d_i == 0 ? FC6_DIR_BULLISH : FC6_DIR_BEARISH);
      FC6_HookBranch hh[];
      FC6_BuildBackwardHookBranches(nodes,
                                    node_count,
                                    direction,
                                    scale_L,
                                    -1,
                                    eps,
                                    cfg.nd_min_retrace_ratio,
                                    cfg.nd_allow_below_half_cycle,
                                    hh);
      for(int h=0; h<ArraySize(hh); h++)
      {
         int sz = ArraySize(hooks);
         ArrayResize(hooks, sz + 1);
         hooks[sz] = hh[h];
      }
   }
   FC6_FinalizeHookIds(hooks);
   return ArraySize(hooks);
}


bool FC6_IntArrayContains(const int &arr[], const int value)
{
   for(int i=0; i<ArraySize(arr); i++)
      if(arr[i] == value) return true;
   return false;
}

void FC6_AddUniqueInt(int &arr[], const int value)
{
   if(value < 0) return;
   if(FC6_IntArrayContains(arr, value)) return;
   int sz = ArraySize(arr);
   ArrayResize(arr, sz + 1);
   arr[sz] = value;
}

void FC6_SortIntByNodeAnchor(const FC6_Node &nodes[], int &positions[])
{
   for(int i=1; i<ArraySize(positions); i++)
   {
      int key = positions[i];
      int j = i - 1;
      while(j >= 0 && nodes[positions[j]].index_anchor > nodes[key].index_anchor)
      {
         positions[j + 1] = positions[j];
         j--;
      }
      positions[j + 1] = key;
   }
}

int FC6_FindNodePosByIdentity(const FC6_Node &nodes[],
                              const int node_count,
                              const FC6_Node &needle,
                              const double eps)
{
   if(!FC6_NodeValid(needle)) return -1;
   for(int i=0; i<node_count; i++)
      if(FC6_SameNodeIdentity(nodes[i], needle, eps))
         return i;
   return -1;
}

int FC6_CollectF1BoundaryOriginPositions(const FC6_Node &nodes[],
                                         const int node_count,
                                         const int direction,
                                         const FC6_HookBranch &phase_hooks[],
                                         const double eps,
                                         int &positions[])
{
   ArrayResize(positions, 0);
   for(int h=0; h<ArraySize(phase_hooks); h++)
   {
      if(!phase_hooks[h].is_nd) continue;
      if(phase_hooks[h].direction != direction) continue;

      // Canonical contract: bullish F1 after a positive hook starts from the
      // lowest hook node; bearish F1 after a negative hook starts from the
      // highest hook node.  That is the hook adverse extreme, not an arbitrary
      // middle node and not every node of the branch.
      int pos = FC6_FindNodePosByIdentity(nodes, node_count, phase_hooks[h].extreme_node, eps);
      if(pos >= 0 && FC6_IsValidOriginForDirection(nodes[pos], direction))
         FC6_AddUniqueInt(positions, pos);
   }
   FC6_SortIntByNodeAnchor(nodes, positions);
   return ArraySize(positions);
}

int FC6_CollectFallbackOriginPositions(const FC6_Node &nodes[],
                                       const int node_count,
                                       const int direction,
                                       int &positions[])
{
   ArrayResize(positions, 0);
   for(int i=0; i<node_count; i++)
      if(FC6_IsValidOriginForDirection(nodes[i], direction))
         FC6_AddUniqueInt(positions, i);
   FC6_SortIntByNodeAnchor(nodes, positions);
   return ArraySize(positions);
}

void FC6_AppendHooks(FC6_HookBranch &dst[], const FC6_HookBranch &src[], const int max_hooks)
{
   for(int i=0; i<ArraySize(src); i++)
   {
      if(max_hooks > 0 && ArraySize(dst) >= max_hooks) break;
      FC6_HookBranch h = src[i];
      FC6_AddHook(dst, h);
   }
}

int FC6_FindDeepestAdversePosInRange(const FC6_Node &nodes[],
                                     const int count,
                                     const int direction,
                                     const int start_index_anchor,
                                     const int end_index_anchor)
{
   int best = -1;
   int kind = FC6_AdverseNodeKind(direction);
   for(int i=0; i<count; i++)
   {
      if(nodes[i].kind != kind) continue;
      if(nodes[i].index_anchor <= start_index_anchor) continue;
      if(end_index_anchor >= 0 && nodes[i].index_anchor >= end_index_anchor) continue;
      if(best < 0) { best = i; continue; }
      if(direction == FC6_DIR_BULLISH)
      {
         if(nodes[i].price < nodes[best].price) best = i;
      }
      else if(direction == FC6_DIR_BEARISH)
      {
         if(nodes[i].price > nodes[best].price) best = i;
      }
   }
   return best;
}

int FC6_FindFirstConfirmedOppositeF1After(const FC6_FlagEvent &events[],
                                          const int event_count,
                                          const FC6_FlagEvent &f3)
{
   int best = -1;
   for(int i=0; i<event_count; i++)
   {
      if(events[i].level != FC6_LEVEL_F1) continue;
      if(events[i].direction == f3.direction) continue;
      if(events[i].status != FC6_STATUS_CONFIRMED) continue;
      if(!events[i].has_confirm) continue;
      if(!f3.has_confirm) continue;
      // The lock trigger must be a future opposite F1, not an unrelated historical
      // confirmation.  Both its origin and confirmation must occur after F3 has
      // completed.
      if(events[i].origin.index_anchor <= f3.confirm.index_anchor) continue;
      if(events[i].confirm.index_anchor <= f3.confirm.index_anchor) continue;
      if(best < 0 || events[i].confirm.time_anchor < events[best].confirm.time_anchor)
         best = i;
   }
   return best;
}

void FC6_LockCompletedF3s(FC6_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(events[i].level != FC6_LEVEL_F3) continue;
      if(events[i].status != FC6_STATUS_COMPLETED) continue;
      int opp = FC6_FindFirstConfirmedOppositeF1After(events, n, events[i]);
      if(opp >= 0)
      {
         events[i].status = FC6_STATUS_LOCKED;
         events[i].extension_end = events[opp].origin;
         events[i].has_extension = true;
         events[i].reason = "f3_locked_by_first_confirmed_opposite_f1";
      }
   }
}

int FC6_BuildF1RootsForScale(const FC6_Node &nodes[],
                             const int node_count,
                             const FC6_Config &cfg,
                             const int scale_L,
                             const FC6_HookBranch &phase_hooks[],
                             FC6_FlagEvent &events[],
                             FC6_HookBranch &hooks[])
{
   int added = 0;
   double eps = cfg.boundary_epsilon_points * _Point;
   int roots_bull = 0;
   int roots_bear = 0;

   for(int d_i=0; d_i<2; d_i++)
   {
      int direction = (d_i == 0 ? FC6_DIR_BULLISH : FC6_DIR_BEARISH);
      int origin_positions[];
      int boundary_count = 0;

      if(cfg.require_f1_phase_boundary)
         boundary_count = FC6_CollectF1BoundaryOriginPositions(nodes, node_count, direction, phase_hooks, eps, origin_positions);

      if(!cfg.require_f1_phase_boundary)
      {
         FC6_CollectFallbackOriginPositions(nodes, node_count, direction, origin_positions);
      }
      else if(boundary_count <= 0)
      {
         // Soft semantic fallback: if the Hook/ND engine has not produced any
         // readable boundary for this scale/direction, do not hard-block the
         // whole visual engine.  The previous strict default produced an empty
         // chart.  Fallback roots are still marked by reason so audit can tell
         // they were not hook-gated roots.
         if(cfg.allow_f1_fail_open_when_no_hook)
            FC6_CollectFallbackOriginPositions(nodes, node_count, direction, origin_positions);
      }

      for(int op=0; op<ArraySize(origin_positions); op++)
      {
         int i = origin_positions[op];
         if(i < 0 || i >= node_count) continue;
         if(!FC6_IsValidOriginForDirection(nodes[i], direction)) continue;

         if(cfg.max_roots_per_scale_direction > 0)
         {
            if(direction == FC6_DIR_BULLISH && roots_bull >= cfg.max_roots_per_scale_direction) continue;
            if(direction == FC6_DIR_BEARISH && roots_bear >= cfg.max_roots_per_scale_direction) continue;
         }

         FC6_FlagEvent f1;
         bool ok = FC6_BuildBodyFromOriginPosition(nodes,
                                                   node_count,
                                                   i,
                                                   FC6_LEVEL_F1,
                                                   direction,
                                                   -1,
                                                   -1,
                                                   1,
                                                   eps,
                                                   f1,
                                                   false);
         if(!ok) continue;
         f1.level = FC6_LEVEL_F1;
         f1.sequence_id = ArraySize(events) + 1;
         f1.parent_event_id = -1;
         f1.chain_index = 1;
         f1.reason = (boundary_count > 0 ? "f1_root_from_hook_phase_boundary" : "f1_root_fail_open_no_hook_boundary_audit_mode");
         FC6_EvaluateF1PostFlag(nodes, node_count, f1, eps);

         int eid = FC6_AddUniqueEvent(events, f1, eps);
         if(eid >= 0)
         {
            added++;
            if(direction == FC6_DIR_BULLISH) roots_bull++; else roots_bear++;
         }

         if(cfg.scan_hooks && f1.has_leg2)
         {
            FC6_Node ctx[];
            int end_idx = f1.has_confirm ? f1.confirm.index_anchor : -1;
            int ctx_count = FC6_CollectContextNodes(nodes, node_count, f1.leg2.index_anchor, end_idx, ctx);
            if(ctx_count > 0)
            {
               FC6_HookBranch hh[];
               FC6_BuildBackwardHookBranches(ctx,
                                             ctx_count,
                                             direction,
                                             scale_L,
                                             f1.sequence_id,
                                             eps,
                                             cfg.nd_min_retrace_ratio,
                                             cfg.nd_allow_below_half_cycle,
                                             hh);
               for(int h=0; h<ArraySize(hh); h++)
               {
                  int sz = ArraySize(hooks);
                  if(sz >= cfg.max_hooks) break;
                  FC6_AddHook(hooks, hh[h]);
               }
            }
         }
      }
   }
   return added;
}

void FC6_BuildChildF2ForF1(const FC6_Node &nodes[],
                           const int node_count,
                           const FC6_Config &cfg,
                           const FC6_FlagEvent &f1,
                           FC6_FlagEvent &events[],
                           FC6_HookBranch &hooks[])
{
   if(!cfg.scan_f2) return;
   if(f1.level != FC6_LEVEL_F1 || f1.status != FC6_STATUS_CONFIRMED || !f1.has_confirm) return;

   double eps = cfg.boundary_epsilon_points * _Point;
   // F2 is authorized after F1 confirmation but backfilled from the deepest
   // adverse correction after the F1 flag body. If a previous F2 dies, the same
   // post-F1 context is recomputed and a new F2 candidate can form from the next
   // valid deepest node.
   int origin_pos = FC6_FindDeepestAdversePosInRange(nodes,
                                                     node_count,
                                                     f1.direction,
                                                     f1.leg2.index_anchor,
                                                     f1.confirm.index_anchor);
   if(origin_pos < 0) return;

   FC6_FlagEvent f2;
   bool ok = FC6_BuildBodyFromOriginPosition(nodes,
                                             node_count,
                                             origin_pos,
                                             FC6_LEVEL_F2,
                                             f1.direction,
                                             f1.sequence_id,
                                             f1.event_id,
                                             2,
                                             eps,
                                             f2,
                                             true);
   if(!ok && !f2.has_leg1) return;
   f2.level = FC6_LEVEL_F2;
   f2.sequence_id = f1.sequence_id;
   f2.parent_event_id = f1.event_id;
   f2.chain_index = 2;
   f2.parent_flag_size = f1.flag_size;
   f2.parent_leg1_L = f1.leg1_L;
   if(f2.has_leg2)
      FC6_EvaluateF2PostFlag(nodes, node_count, f2, eps, cfg.f2_min_parent_size_ratio);
   else
   {
      f2.status = FC6_STATUS_RAW_SEED;
      f2.draw_kind = FC6_DRAW_PROBABLE_LEG;
      f2.reason = "f2_seed_from_post_f1_correction";
   }
   int eid = FC6_AddUniqueEvent(events, f2, eps);
   if(eid < 0) return;

   if(cfg.scan_hooks && f2.has_leg2)
   {
      FC6_Node ctx[];
      int end_idx = f2.has_confirm ? f2.confirm.index_anchor : -1;
      int ctx_count = FC6_CollectContextNodes(nodes, node_count, f2.leg2.index_anchor, end_idx, ctx);
      if(ctx_count > 0)
      {
         FC6_HookBranch hh[];
         FC6_BuildBackwardHookBranches(ctx,
                                       ctx_count,
                                       f2.direction,
                                       f2.scale_L,
                                       f2.sequence_id,
                                       eps,
                                       cfg.nd_min_retrace_ratio,
                                       cfg.nd_allow_below_half_cycle,
                                       hh);
         for(int h=0; h<ArraySize(hh); h++)
         {
            if(ArraySize(hooks) >= cfg.max_hooks) break;
            FC6_AddHook(hooks, hh[h]);
         }
      }
   }
}

void FC6_BuildChildF3ForF2(const FC6_Node &nodes[],
                           const int node_count,
                           const FC6_Config &cfg,
                           const FC6_FlagEvent &f2,
                           FC6_FlagEvent &events[],
                           FC6_HookBranch &hooks[])
{
   if(!cfg.scan_f3) return;
   if(f2.level != FC6_LEVEL_F2 || f2.status != FC6_STATUS_CONFIRMED || !f2.has_confirm) return;

   double eps = cfg.boundary_epsilon_points * _Point;
   int origin_pos = FC6_FindDeepestAdversePosInRange(nodes,
                                                     node_count,
                                                     f2.direction,
                                                     f2.leg2.index_anchor,
                                                     f2.confirm.index_anchor);
   if(origin_pos < 0) return;

   FC6_FlagEvent f3;
   bool ok = FC6_BuildBodyFromOriginPosition(nodes,
                                             node_count,
                                             origin_pos,
                                             FC6_LEVEL_F3,
                                             f2.direction,
                                             f2.sequence_id,
                                             f2.event_id,
                                             3,
                                             eps,
                                             f3,
                                             true);
   if(!ok && !f3.has_leg1) return;
   f3.level = FC6_LEVEL_F3;
   f3.sequence_id = f2.sequence_id;
   f3.parent_event_id = f2.event_id;
   f3.chain_index = 3;
   f3.parent_flag_size = f2.flag_size;
   f3.parent_leg1_L = f2.leg1_L;
   if(f3.has_leg2)
      FC6_EvaluateF3BodyAndExtension(nodes, node_count, f3, cfg);
   else
   {
      f3.status = FC6_STATUS_RAW_SEED;
      f3.draw_kind = FC6_DRAW_PROBABLE_LEG;
      f3.reason = "f3_seed_from_post_f2_correction";
   }
   FC6_AddUniqueEvent(events, f3, eps);

   if(cfg.scan_hooks && f3.has_leg2)
   {
      FC6_Node ctx[];
      int ctx_count = FC6_CollectContextNodes(nodes, node_count, f3.leg2.index_anchor, -1, ctx);
      if(ctx_count > 0)
      {
         FC6_HookBranch hh[];
         FC6_BuildBackwardHookBranches(ctx,
                                       ctx_count,
                                       f3.direction,
                                       f3.scale_L,
                                       f3.sequence_id,
                                       eps,
                                       cfg.nd_min_retrace_ratio,
                                       cfg.nd_allow_below_half_cycle,
                                       hh);
         for(int h=0; h<ArraySize(hh); h++)
         {
            if(ArraySize(hooks) >= cfg.max_hooks) break;
            FC6_AddHook(hooks, hh[h]);
         }
      }
   }
}

void FC6_BuildChildrenPass(const FC6_Node &nodes[],
                           const int node_count,
                           const FC6_Config &cfg,
                           FC6_FlagEvent &events[],
                           FC6_HookBranch &hooks[])
{
   int initial_count = ArraySize(events);
   for(int i=0; i<initial_count; i++)
      FC6_BuildChildF2ForF1(nodes, node_count, cfg, events[i], events, hooks);

   int after_f2 = ArraySize(events);
   for(int i=0; i<after_f2; i++)
      FC6_BuildChildF3ForF2(nodes, node_count, cfg, events[i], events, hooks);
}



bool FC6_StatusIsTerminalF3(const int status)
{
   return (status == FC6_STATUS_COMPLETED || status == FC6_STATUS_LOCKED || status == FC6_STATUS_CONFIRMED);
}

bool FC6_IsRootF1Event(const FC6_FlagEvent &e)
{
   return (e.level == FC6_LEVEL_F1 && e.chain_index == 1 && e.parent_event_id < 0 && e.has_origin);
}

bool FC6_HasOppositeF3Between(const FC6_FlagEvent &events[],
                              const int count,
                              const int scale_L,
                              const int direction,
                              const int from_index_anchor,
                              const int to_index_anchor)
{
   for(int i=0; i<count; i++)
   {
      if(events[i].level != FC6_LEVEL_F3) continue;
      if(events[i].scale_L != scale_L) continue;
      if(events[i].direction == direction) continue;
      if(!FC6_StatusIsTerminalF3(events[i].status)) continue;
      if(!events[i].has_confirm) continue;
      int ci = events[i].confirm.index_anchor;
      if(ci > from_index_anchor && ci < to_index_anchor)
         return true;
   }
   return false;
}


bool FC6_HasOppositeF3BetweenAnyScale(const FC6_FlagEvent &events[],
                                      const int count,
                                      const int direction,
                                      const int from_index_anchor,
                                      const int to_index_anchor)
{
   for(int i=0; i<count; i++)
   {
      if(events[i].level != FC6_LEVEL_F3) continue;
      if(events[i].direction == direction) continue;
      if(!FC6_StatusIsTerminalF3(events[i].status)) continue;
      if(!events[i].has_confirm) continue;
      int ci = events[i].confirm.index_anchor;
      if(ci > from_index_anchor && ci < to_index_anchor)
         return true;
   }
   return false;
}

bool FC6_SequenceIdMarked(const int &ids[], const int sequence_id)
{
   for(int i=0; i<ArraySize(ids); i++)
      if(ids[i] == sequence_id) return true;
   return false;
}

void FC6_MarkSequenceId(int &ids[], const int sequence_id)
{
   if(sequence_id < 0) return;
   if(FC6_SequenceIdMarked(ids, sequence_id)) return;
   int sz = ArraySize(ids);
   ArrayResize(ids, sz + 1);
   ids[sz] = sequence_id;
}

int FC6_PruneSameDirectionRestartsBeforeOppositeF3(FC6_FlagEvent &events[], const FC6_Config &cfg)
{
   if(!cfg.enforce_single_chain_per_direction_scale) return 0;
   int n = ArraySize(events);
   int remove_seq[];
   ArrayResize(remove_seq, 0);

   for(int i=0; i<n; i++)
   {
      if(!FC6_IsRootF1Event(events[i])) continue;
      int prev = -1;
      for(int j=0; j<n; j++)
      {
         if(i == j) continue;
         if(!FC6_IsRootF1Event(events[j])) continue;
         if(events[j].scale_L != events[i].scale_L) continue;
         if(events[j].direction != events[i].direction) continue;
         if(events[j].origin.index_anchor >= events[i].origin.index_anchor) continue;
         if(FC6_SequenceIdMarked(remove_seq, events[j].sequence_id)) continue;
         if(prev < 0 || events[j].origin.index_anchor > events[prev].origin.index_anchor)
            prev = j;
      }
      if(prev < 0) continue;
      if(!FC6_HasOppositeF3Between(events, n, events[i].scale_L, events[i].direction, events[prev].origin.index_anchor, events[i].origin.index_anchor))
         FC6_MarkSequenceId(remove_seq, events[i].sequence_id);
   }

   if(ArraySize(remove_seq) <= 0) return 0;

   FC6_FlagEvent kept[];
   ArrayResize(kept, 0);
   for(int i=0; i<n; i++)
   {
      if(FC6_SequenceIdMarked(remove_seq, events[i].sequence_id)) continue;
      FC6_AddEvent(kept, events[i]);
   }
   int removed = n - ArraySize(kept);
   ArrayResize(events, ArraySize(kept));
   for(int k=0; k<ArraySize(kept); k++) events[k] = kept[k];
   FC6_FinalizeEventIds(events);
   return removed;
}


int FC6_PruneSameDirectionRestartsBeforeOppositeF3Global(FC6_FlagEvent &events[], const FC6_Config &cfg)
{
   if(!cfg.enforce_single_chain_per_direction_global) return 0;
   int n = ArraySize(events);
   int remove_seq[];
   ArrayResize(remove_seq, 0);

   for(int i=0; i<n; i++)
   {
      if(!FC6_IsRootF1Event(events[i])) continue;
      int prev = -1;
      for(int j=0; j<n; j++)
      {
         if(i == j) continue;
         if(!FC6_IsRootF1Event(events[j])) continue;
         if(events[j].direction != events[i].direction) continue;
         if(events[j].origin.index_anchor >= events[i].origin.index_anchor) continue;
         if(FC6_SequenceIdMarked(remove_seq, events[j].sequence_id)) continue;

         // Choose the latest earlier same-direction root, regardless of scale.
         // This enforces the user's phase rule: while a direction already has
         // an active F1/F2 chain, another same-direction root is not allowed
         // until an opposite F3 has appeared between the two phase roots.
         if(prev < 0 || events[j].origin.index_anchor > events[prev].origin.index_anchor)
            prev = j;
      }
      if(prev < 0) continue;
      if(!FC6_HasOppositeF3BetweenAnyScale(events, n, events[i].direction, events[prev].origin.index_anchor, events[i].origin.index_anchor))
         FC6_MarkSequenceId(remove_seq, events[i].sequence_id);
   }

   if(ArraySize(remove_seq) <= 0) return 0;

   FC6_FlagEvent kept[];
   ArrayResize(kept, 0);
   for(int i=0; i<n; i++)
   {
      if(FC6_SequenceIdMarked(remove_seq, events[i].sequence_id)) continue;
      FC6_AddEvent(kept, events[i]);
   }
   int removed = n - ArraySize(kept);
   ArrayResize(events, ArraySize(kept));
   for(int k=0; k<ArraySize(kept); k++) events[k] = kept[k];
   FC6_FinalizeEventIds(events);
   return removed;
}

void FC6_RebuildParentEventIds(FC6_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(events[i].chain_index <= 1)
      {
         events[i].parent_event_id = -1;
         continue;
      }
      int want_chain = events[i].chain_index - 1;
      int best = -1;
      for(int j=0; j<n; j++)
      {
         if(events[j].sequence_id != events[i].sequence_id) continue;
         if(events[j].chain_index != want_chain) continue;
         if(events[j].direction != events[i].direction) continue;
         if(best < 0 || events[j].origin.index_anchor <= events[i].origin.index_anchor)
            best = j;
      }
      events[i].parent_event_id = (best >= 0 ? events[best].event_id : -1);
   }
}

void FC6_PostProcessSemanticEvents(FC6_FlagEvent &events[], const FC6_Config &cfg)
{
   FC6_LockCompletedF3s(events);
   FC6_PruneSameDirectionRestartsBeforeOppositeF3(events, cfg);
   FC6_PruneSameDirectionRestartsBeforeOppositeF3Global(events, cfg);
   FC6_FinalizeEventIds(events);
   FC6_RebuildParentEventIds(events);
}

void FC6_RemoveInvalidatedForMainIfNeeded(FC6_FlagEvent &events[], const FC6_Config &cfg)
{
   if(cfg.show_invalidated_in_audit) return;
   FC6_FlagEvent kept[];
   ArrayResize(kept, 0);
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].status == FC6_STATUS_INVALIDATED) continue;
      FC6_AddEvent(kept, events[i]);
   }
   ArrayResize(events, ArraySize(kept));
   for(int k=0; k<ArraySize(kept); k++) events[k] = kept[k];
   FC6_FinalizeEventIds(events);
}

void FC6_SortEventsChronological(FC6_FlagEvent &events[])
{
   for(int i=1; i<ArraySize(events); i++)
   {
      FC6_FlagEvent key = events[i];
      int j = i - 1;
      while(j >= 0 && events[j].origin.time_anchor > key.origin.time_anchor)
      {
         events[j + 1] = events[j];
         j--;
      }
      events[j + 1] = key;
   }
   FC6_FinalizeEventIds(events);
}

int FC6_DetectForScale(const MqlRates &rates[],
                       const int bar_count,
                       const int scale_L,
                       const FC6_Config &cfg,
                       FC6_FlagEvent &events[],
                       FC6_HookBranch &hooks[],
                       const bool append)
{
   if(!append)
   {
      ArrayResize(events, 0);
      ArrayResize(hooks, 0);
   }

   double eps = cfg.boundary_epsilon_points * _Point;
   FC6_Node raw[];
   int raw_count = FC6_BuildLRuleNodes(rates, bar_count, scale_L, cfg.include_pending_nodes, eps, raw);
   if(raw_count <= 4) return 0;

   FC6_Node nodes[];
   int node_count = FC6_BuildAlternatingView(raw, raw_count, eps, nodes);
   if(node_count <= 4) return 0;

   int before = ArraySize(events);

   FC6_HookBranch phase_hooks[];
   FC6_BuildPhaseHooksForScale(nodes, node_count, cfg, scale_L, phase_hooks);
   FC6_AppendHooks(hooks, phase_hooks, cfg.max_hooks);

   if(cfg.scan_f1)
      FC6_BuildF1RootsForScale(nodes, node_count, cfg, scale_L, phase_hooks, events, hooks);

   FC6_FinalizeEventIds(events);
   // Two passes catch F2s added from F1 and F3s added from F2.
   FC6_BuildChildrenPass(nodes, node_count, cfg, events, hooks);
   FC6_FinalizeEventIds(events);
   FC6_LockCompletedF3s(events);
   FC6_FinalizeEventIds(events);
   FC6_FinalizeHookIds(hooks);

   return ArraySize(events) - before;
}

int FC6_DetectAllScales(const MqlRates &rates[],
                        const int bar_count,
                        const int &scales[],
                        const int scale_count,
                        const FC6_Config &cfg,
                        FC6_FlagEvent &events[],
                        FC6_HookBranch &hooks[],
                        FC6_DetectResult &result)
{
   ArrayResize(events, 0);
   ArrayResize(hooks, 0);
   result.nodes_total = 0;
   result.hooks_total = 0;
   result.events_total = 0;
   result.f1_total = 0;
   result.f2_total = 0;
   result.f3_total = 0;
   result.nd_total = 0;

   for(int s=0; s<scale_count; s++)
   {
      if(ArraySize(events) >= cfg.max_events) break;
      FC6_DetectForScale(rates, bar_count, scales[s], cfg, events, hooks, true);
      if(ArraySize(events) > cfg.max_events)
         ArrayResize(events, cfg.max_events);
      if(ArraySize(hooks) > cfg.max_hooks)
         ArrayResize(hooks, cfg.max_hooks);
   }

   // Cross-scale semantic post-processing must happen after every scale has
   // contributed its candidate structures.  This is where future opposite F1s
   // can lock completed F3s and where same-direction restarts are removed until
   // an opposite F3 actually resets the phase.
   FC6_PostProcessSemanticEvents(events, cfg);
   FC6_SortEventsChronological(events);
   FC6_RebuildParentEventIds(events);
   FC6_FinalizeHookIds(hooks);
   FC6_RemoveInvalidatedForMainIfNeeded(events, cfg);
   FC6_RebuildParentEventIds(events);

   result.events_total = ArraySize(events);
   result.hooks_total = ArraySize(hooks);
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].level == FC6_LEVEL_F1) result.f1_total++;
      if(events[i].level == FC6_LEVEL_F2) result.f2_total++;
      if(events[i].level == FC6_LEVEL_F3) result.f3_total++;
   }
   for(int h=0; h<ArraySize(hooks); h++)
      if(hooks[h].is_nd) result.nd_total++;

   return result.events_total;
}

#endif // __FC6_SEQUENCE_ENGINE_MQH__
