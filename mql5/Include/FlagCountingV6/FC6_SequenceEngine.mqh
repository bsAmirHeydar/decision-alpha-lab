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
      if(events[i].has_confirm && f3.has_confirm && events[i].confirm.index_anchor <= f3.confirm.index_anchor) continue;
      if(!events[i].has_confirm) continue;
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
                             FC6_FlagEvent &events[],
                             FC6_HookBranch &hooks[])
{
   int added = 0;
   double eps = cfg.boundary_epsilon_points * _Point;
   int roots_bull = 0;
   int roots_bear = 0;

   for(int i=0; i<node_count; i++)
   {
      for(int d_i=0; d_i<2; d_i++)
      {
         int direction = (d_i == 0 ? FC6_DIR_BULLISH : FC6_DIR_BEARISH);
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
         FC6_EvaluateF1PostFlag(nodes, node_count, f1, eps);

         // F1 is shown after body has been hit. Rejected/invalidation can remain
         // in audit if requested, but main renderer filters them.
         int eid = FC6_AddUniqueEvent(events, f1, eps);
         if(eid >= 0)
         {
            added++;
            if(direction == FC6_DIR_BULLISH) roots_bull++; else roots_bear++;
         }

         // Hook/ND after the F1 body, regardless of F1 confirmation, because the
         // hook is a first-class phase object. It is rendered as a gray arc.
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
                                                     -1);
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
                                                     -1);
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
   if(cfg.scan_f1)
      FC6_BuildF1RootsForScale(nodes, node_count, cfg, scale_L, events, hooks);

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
                        const int scales[],
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

   FC6_SortEventsChronological(events);
   FC6_FinalizeHookIds(hooks);
   FC6_RemoveInvalidatedForMainIfNeeded(events, cfg);

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
