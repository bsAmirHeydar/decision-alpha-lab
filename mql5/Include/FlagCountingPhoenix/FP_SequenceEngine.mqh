#ifndef __FP_SEQUENCE_ENGINE_MQH__
#define __FP_SEQUENCE_ENGINE_MQH__
#property strict

#include "FP_InternalCountEngine.mqh"

// ============================================================================
// Phoenix Sequence Engine
// ----------------------------------------------------------------------------
// This is a clean, state-first rebuild. It intentionally emits one semantic
// event per detected F-level body, not every intermediate lifecycle transition.
// Audit verbosity is available through log helpers, not by dumping raw lifecycle
// attempts into the main chart.
// ============================================================================

int FP_NextEventId(FP_FlagEvent &events[])
{
   return ArraySize(events);
}

int FP_NextSequenceId(FP_FlagEvent &events[])
{
   int max_id = -1;
   for(int i=0; i<ArraySize(events); i++)
      if(events[i].sequence_id > max_id) max_id = events[i].sequence_id;
   return max_id + 1;
}

void FP_FinalizeEventIds(FP_FlagEvent &events[])
{
   for(int i=0; i<ArraySize(events); i++)
      events[i].event_id = i;
}

int FP_AddSemanticEvent(FP_FlagEvent &events[], FP_FlagEvent &e, const FP_Config &cfg)
{
   if(cfg.max_events > 0 && ArraySize(events) >= cfg.max_events) return -1;
   e.event_id = ArraySize(events);
   FP_AddEvent(events, e);
   return e.event_id;
}

bool FP_EventIsVisibleMain(const FP_FlagEvent &e, const FP_Config &cfg)
{
   if(e.status == FP_STATUS_INVALIDATED && !cfg.show_invalidated_in_audit) return false;
   if(e.render_kind == FP_RENDER_NONE) return false;
   if(!e.visible_main) return false;
   return true;
}

void FP_UpdateEventCounters(const FP_FlagEvent &e, FP_DetectResult &r)
{
   r.events_total++;
   if(e.visible_main) r.visible_events_total++;
   if(e.level == FP_LEVEL_F1) r.f1_total++;
   if(e.level == FP_LEVEL_F2) r.f2_total++;
   if(e.level == FP_LEVEL_F3) r.f3_total++;
   if(e.status == FP_STATUS_INVALIDATED) r.invalid_total++;
}

bool FP_IsF1Confirmed(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F1 && e.status == FP_STATUS_CONFIRMED && e.has_confirm);
}

bool FP_IsF2Confirmed(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F2 && e.status == FP_STATUS_CONFIRMED && e.has_confirm);
}

bool FP_IsF3CompletedOrLocked(const FP_FlagEvent &e)
{
   return (e.level == FP_LEVEL_F3 && (e.status == FP_STATUS_COMPLETED || e.status == FP_STATUS_LOCKED));
}

void FP_ApplyPostFlagState(FP_FlagEvent &event,
                           const FP_Node &nodes[],
                           const int node_count,
                           const FP_Config &cfg)
{
   bool absorbed = FP_AbsorbPreInternalExtensions(event, nodes, node_count, cfg);
   if(absorbed)
      event.reason = event.reason + ";extension_absorption_pass_complete";

   FP_InternalPack pack;
   int confirm_pos = -1;
   int invalid_pos = -1;
   int last_pos = -1;
   bool has_pack = FP_BuildPostFlagInternalPack(nodes, node_count, event, cfg, pack, confirm_pos, invalid_pos, last_pos);
   FP_CopyInternalPackToEvent(event, pack);

   if(event.level == FP_LEVEL_F3)
   {
      event.status = FP_STATUS_COMPLETED;
      event.reason = event.reason + ";f3_body_completed";
      return;
   }

   if(invalid_pos >= 0)
   {
      event.invalid = nodes[invalid_pos];
      event.has_invalid = true;
      event.pos_invalid = invalid_pos;
      event.status = FP_STATUS_INVALIDATED;
      event.visible_main = cfg.show_invalidated_in_audit;
      event.reason = event.reason + ";invalidated_before_confirmation";
      return;
   }

   if(has_pack && pack.valid12 && confirm_pos >= 0)
   {
      event.confirm = nodes[confirm_pos];
      event.has_confirm = true;
      event.pos_confirm = confirm_pos;
      event.status = FP_STATUS_CONFIRMED;
      event.render_kind = FP_RENDER_FLAG_BODY;
      event.reason = event.reason + ";confirmed_after_internal12";
      return;
   }

   if(has_pack && pack.count > 0)
   {
      event.status = FP_STATUS_POST_FLAG;
      event.reason = event.reason + ";post_flag_internal_count_" + IntegerToString(pack.count);
      return;
   }

   event.status = FP_STATUS_LIVE_BODY;
   event.reason = event.reason + ";live_body_no_post_flag_count";
}

bool FP_QualifyF2(FP_FlagEvent &f2, const FP_FlagEvent &f1, const FP_Config &cfg)
{
   f2.parent_flag_size = f1.flag_size;
   f2.size_ratio = (f1.flag_size > 0.0 ? f2.flag_size / f1.flag_size : 0.0);
   if(f2.flag_size + 0.0 >= cfg.f2_min_parent_size_ratio * f1.flag_size)
   {
      if(f2.status == FP_STATUS_LIVE_BODY) f2.status = FP_STATUS_QUALIFIED;
      f2.reason = f2.reason + ";f2_size_ratio_" + DoubleToString(f2.size_ratio, 3);
      return true;
   }
   f2.reason = f2.reason + ";f2_waiting_size_ratio_" + DoubleToString(f2.size_ratio, 3);
   return false;
}

bool FP_QualifyF3(FP_FlagEvent &f3, const FP_FlagEvent &f2, const FP_Config &cfg)
{
   f3.parent_flag_size = f2.flag_size;
   f3.parent_leg1_L = f2.leg1_L;
   f3.size_ratio = (f2.flag_size > 0.0 ? f3.flag_size / f2.flag_size : 0.0);
   int min_leg1_L = (int)MathCeil(cfg.f3_leg1_L_min_ratio * (double)MathMax(1, f2.leg1_L));
   bool cond_L = (f3.leg1_L >= min_leg1_L);
   bool cond_size = (f3.flag_size > cfg.f3_min_parent_size_ratio * f2.flag_size);
   if(cond_L || cond_size)
   {
      f3.status = FP_STATUS_COMPLETED;
      f3.reason = f3.reason + ";f3_or_qualified_L_" + FP_BoolName(cond_L) + "_size_" + FP_BoolName(cond_size);
      return true;
   }
   f3.status = FP_STATUS_LIVE_BODY;
   f3.reason = f3.reason + ";f3_waiting_or_qualification";
   return false;
}

bool FP_EventBodyDuplicateExists(const FP_FlagEvent &events[], const int event_count, const FP_FlagEvent &candidate)
{
   for(int i=0; i<event_count; i++)
   {
      if(!events[i].visible_main) continue;
      if(FP_SameBodyIdentity(events[i], candidate)) return true;
   }
   return false;
}

int FP_FindNodePos(const FP_Node &nodes[], const int node_count, const FP_Node &needle)
{
   for(int i=0; i<node_count; i++)
   {
      if(nodes[i].id == needle.id && nodes[i].kind == needle.kind && nodes[i].index_anchor == needle.index_anchor) return i;
   }
   return -1;
}

bool FP_BuildF1FromOrigin(const FP_Node &nodes[],
                          const int node_count,
                          const int origin_pos,
                          const int direction,
                          const int sequence_id,
                          const bool from_phase_boundary,
                          const bool from_fail_open,
                          const FP_Config &cfg,
                          FP_FlagEvent &f1)
{
   if(!FP_FindFlagBodyFromOrigin(nodes, node_count, origin_pos, direction, FP_LEVEL_F1, sequence_id, -1, cfg.boundary_epsilon_points, f1))
      return false;
   f1.from_phase_boundary = from_phase_boundary;
   f1.from_fail_open = from_fail_open;
   if(!from_phase_boundary && cfg.require_f1_phase_boundary && !from_fail_open) return false;
   FP_ApplyPostFlagState(f1, nodes, node_count, cfg);
   f1.chain_index = 1;
   return FP_EventIsVisibleMain(f1, cfg);
}

bool FP_BuildF2FromF1(const FP_Node &nodes[],
                      const int node_count,
                      const FP_FlagEvent &f1,
                      const int sequence_id,
                      const int parent_event_id,
                      const FP_Config &cfg,
                      FP_FlagEvent &f2)
{
   FP_ResetFlagEvent(f2);
   if(!FP_IsF1Confirmed(f1)) return false;

   int deepest_pos = -1;
   FP_Node deepest;
   int to_pos = MathMax(f1.pos_leg2, f1.pos_confirm - 1);
   if(!FP_FindDeepestAdverseNode(nodes, node_count, f1.pos_leg2 + 1, to_pos, f1.direction, cfg.boundary_epsilon_points, deepest_pos, deepest))
      return false;

   if(!FP_FindFlagBodyFromOrigin(nodes, node_count, deepest_pos, f1.direction, FP_LEVEL_F2, sequence_id, parent_event_id, cfg.boundary_epsilon_points, f2))
      return false;

   f2.chain_index = 2;
   f2.parent_sequence_id = f1.sequence_id;
   f2.parent_event_id = parent_event_id;
   f2.parent_flag_size = f1.flag_size;
   f2.parent_leg1_L = f1.leg1_L;
   bool size_ok = FP_QualifyF2(f2, f1, cfg);
   FP_ApplyPostFlagState(f2, nodes, node_count, cfg);

   // Contract: F2 is a real sequence stage only after it is at least the F1
   // flag size.  A smaller body is an audit candidate, not a main-chart F2 and
   // must never become an F3 parent.  This prevents premature F2/F3 clutter.
   if(!size_ok && f2.status != FP_STATUS_INVALIDATED)
   {
      f2.status = FP_STATUS_LIVE_BODY;
      f2.visible_main = false;
      f2.reason = f2.reason + ";hidden_f2_size_below_parent_contract";
      return false;
   }
   return FP_EventIsVisibleMain(f2, cfg);
}

bool FP_BuildF3FromF2(const FP_Node &nodes[],
                      const int node_count,
                      const FP_FlagEvent &f2,
                      const int sequence_id,
                      const int parent_event_id,
                      const FP_Config &cfg,
                      FP_FlagEvent &f3)
{
   FP_ResetFlagEvent(f3);
   if(!FP_IsF2Confirmed(f2)) return false;

   int deepest_pos = -1;
   FP_Node deepest;
   int to_pos = MathMax(f2.pos_leg2, f2.pos_confirm - 1);
   if(!FP_FindDeepestAdverseNode(nodes, node_count, f2.pos_leg2 + 1, to_pos, f2.direction, cfg.boundary_epsilon_points, deepest_pos, deepest))
      return false;

   if(!FP_FindFlagBodyFromOrigin(nodes, node_count, deepest_pos, f2.direction, FP_LEVEL_F3, sequence_id, parent_event_id, cfg.boundary_epsilon_points, f3))
      return false;

   f3.chain_index = 3;
   f3.parent_sequence_id = f2.sequence_id;
   f3.parent_event_id = parent_event_id;
   f3.parent_flag_size = f2.flag_size;
   f3.parent_leg1_L = f2.leg1_L;
   FP_QualifyF3(f3, f2, cfg);
   return FP_EventIsVisibleMain(f3, cfg);
}

void FP_CollectOriginNodesFromHooksOrFallback(const FP_Node &nodes[],
                                              const int node_count,
                                              const FP_HookBranch &hooks[],
                                              const int hook_count,
                                              const int direction,
                                              const FP_Config &cfg,
                                              FP_Node &origins[],
                                              bool &using_fail_open)
{
   ArrayResize(origins, 0);
   using_fail_open = false;
   double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);
   FP_CollectHookOrigins(hooks, hook_count, direction, eps, origins);

   if(ArraySize(origins) > 0) return;

   if(cfg.require_f1_phase_boundary && !cfg.allow_f1_fail_open_when_no_hook) return;

   using_fail_open = true;
   int origin_kind = FP_OriginKindForDirection(direction);
   for(int i=0; i<node_count; i++)
   {
      if(nodes[i].kind != origin_kind) continue;
      FP_AddNode(origins, nodes[i]);
   }
}

int FP_FindOriginPosition(const FP_Node &nodes[], const int node_count, const FP_Node &origin)
{
   for(int i=0; i<node_count; i++)
   {
      if(nodes[i].kind == origin.kind && nodes[i].index_anchor == origin.index_anchor && FP_AlmostEqual(nodes[i].price, origin.price, FP_EpsilonPrice(0.0))) return i;
   }
   return -1;
}


int FP_CollectRawOriginNodesForDirection(const FP_Node &nodes[],
                                         const int node_count,
                                         const int direction,
                                         FP_Node &origins[])
{
   ArrayResize(origins, 0);
   int origin_kind = FP_OriginKindForDirection(direction);
   for(int i=0; i<node_count; i++)
   {
      if(nodes[i].kind != origin_kind) continue;
      FP_AddNode(origins, nodes[i]);
   }
   return ArraySize(origins);
}

int FP_TryBuildFlagChainsFromOrigins(const FP_Node &nodes[],
                                     const int node_count,
                                     const FP_Node &origins[],
                                     const int direction,
                                     const bool from_phase_boundary,
                                     const bool from_fail_open,
                                     const FP_Config &cfg,
                                     FP_FlagEvent &events[],
                                     int &roots_used)
{
   int added_roots = 0;
   for(int oi=0; oi<ArraySize(origins); oi++)
   {
      if(cfg.max_roots_per_scale_direction > 0 && roots_used >= cfg.max_roots_per_scale_direction) break;
      int origin_pos = FP_FindOriginPosition(nodes, node_count, origins[oi]);
      if(origin_pos < 0) continue;

      int seq_id = FP_NextSequenceId(events);
      FP_FlagEvent f1;
      if(!FP_BuildF1FromOrigin(nodes, node_count, origin_pos, direction, seq_id, from_phase_boundary, from_fail_open, cfg, f1)) continue;
      if(FP_EventBodyDuplicateExists(events, ArraySize(events), f1)) continue;

      int f1_id = FP_AddSemanticEvent(events, f1, cfg);
      if(f1_id < 0) return added_roots;
      roots_used++;
      added_roots++;

      if(cfg.scan_f2 && FP_IsF1Confirmed(f1))
      {
         FP_FlagEvent f2;
         if(FP_BuildF2FromF1(nodes, node_count, f1, seq_id, f1_id, cfg, f2))
         {
            int f2_id = FP_AddSemanticEvent(events, f2, cfg);
            if(f2_id < 0) return added_roots;

            if(cfg.scan_f3 && FP_IsF2Confirmed(f2))
            {
               FP_FlagEvent f3;
               if(FP_BuildF3FromF2(nodes, node_count, f2, seq_id, f2_id, cfg, f3))
               {
                  int f3_id = FP_AddSemanticEvent(events, f3, cfg);
                  if(f3_id < 0) return added_roots;
               }
            }
         }
      }
   }
   return added_roots;
}

void FP_DetectScale(const MqlRates &rates[],
                    const int total,
                    const int scale_L,
                    const FP_Config &cfg,
                    FP_FlagEvent &events[],
                    FP_HookBranch &all_hooks[],
                    FP_DetectResult &result)
{
   FP_Node raw_nodes[];
   FP_Node nodes[];
   int raw_count = FP_ExtractNodesForL(rates, total, scale_L, cfg.include_pending_nodes, cfg.boundary_epsilon_points, raw_nodes);
   int node_count = FP_CompressAlternatingExtreme(raw_nodes, raw_count, nodes);
   result.nodes_total += node_count;
   if(node_count < 4) return;

   FP_HookBranch hooks[];
   int hook_count = FP_BuildHookBranches(nodes, node_count, scale_L, cfg, hooks);
   for(int h=0; h<hook_count; h++)
   {
      hooks[h].branch_id = ArraySize(all_hooks);
      FP_AddHook(all_hooks, hooks[h]);
      result.hooks_total++;
      if(hooks[h].is_nd) result.nd_total++;
   }

   if(!cfg.scan_f1) return;

   for(int d_index=0; d_index<2; d_index++)
   {
      int direction = (d_index == 0 ? FP_DIR_BULLISH : FP_DIR_BEARISH);
      double eps = FP_EpsilonPrice(cfg.boundary_epsilon_points);

      FP_Node phase_origins[];
      FP_CollectHookOrigins(hooks, hook_count, direction, eps, phase_origins);

      int roots_used = 0;
      int added_from_phase = FP_TryBuildFlagChainsFromOrigins(nodes,
                                                              node_count,
                                                              phase_origins,
                                                              direction,
                                                              true,
                                                              false,
                                                              cfg,
                                                              events,
                                                              roots_used);

      // Critical fail-safe: Hook/ND is context, not a hard visibility gate.
      // Build Hook-derived roots first, then let raw-origin fail-open inspect the
      // same scale/direction as a recovery layer.  Visual duplicate pruning below
      // keeps main-chart output canonical while preventing Hook mistakes from
      // erasing valid F bodies.
      if(cfg.allow_f1_fail_open_when_no_hook)
      {
         FP_Node fallback_origins[];
         FP_CollectRawOriginNodesForDirection(nodes, node_count, direction, fallback_origins);
         FP_TryBuildFlagChainsFromOrigins(nodes,
                                          node_count,
                                          fallback_origins,
                                          direction,
                                          false,
                                          true,
                                          cfg,
                                          events,
                                          roots_used);
      }
   }
}

void FP_HideSupersededParentStates(FP_FlagEvent &events[], const FP_Config &cfg)
{
   if(!cfg.hide_superseded_parent_states) return;
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].level != FP_LEVEL_F1 && events[i].level != FP_LEVEL_F2) continue;
      if(events[i].status == FP_STATUS_CONFIRMED || events[i].status == FP_STATUS_LOCKED || events[i].status == FP_STATUS_COMPLETED) continue;

      bool has_visible_child = false;
      for(int j=0; j<n; j++)
      {
         if(!events[j].visible_main) continue;
         if(events[j].parent_sequence_id == events[i].sequence_id && events[j].chain_index == events[i].chain_index + 1)
         {
            has_visible_child = true;
            break;
         }
      }
      if(has_visible_child)
      {
         events[i].visible_main = false;
         events[i].reason = events[i].reason + ";hidden_superseded_parent_state_with_visible_child";
      }
   }
}

void FP_RebuildParentIdsAfterSort(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(events[i].chain_index <= 1) continue;
      int parent_chain = events[i].chain_index - 1;
      int best = -1;
      for(int j=0; j<n; j++)
      {
         if(events[j].sequence_id != events[i].sequence_id) continue;
         if(events[j].chain_index != parent_chain) continue;
         if(events[j].origin.index_anchor > events[i].origin.index_anchor) continue;
         if(best < 0 || events[j].origin.index_anchor > events[best].origin.index_anchor) best = j;
      }
      if(best >= 0)
      {
         events[i].parent_event_id = events[best].event_id;
         events[i].parent_sequence_id = events[best].sequence_id;
      }
   }
}

void FP_PruneFailOpenRootsWhenPhaseRootsExist(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].level != FP_LEVEL_F1) continue;
      if(!events[i].from_fail_open) continue;

      bool phase_root_same_zone = false;
      for(int j=0; j<n; j++)
      {
         if(i == j) continue;
         if(!events[j].visible_main) continue;
         if(events[j].level != FP_LEVEL_F1) continue;
         if(events[j].direction != events[i].direction) continue;
         if(events[j].scale_L != events[i].scale_L) continue;
         if(!events[j].from_phase_boundary) continue;
         // If a phase-root body starts before this fail-open origin and extends beyond it,
         // the fail-open root is only an audit fallback inside an owned phase.
         if(events[j].origin.index_anchor <= events[i].origin.index_anchor && events[j].leg2.index_anchor >= events[i].origin.index_anchor)
         {
            phase_root_same_zone = true;
            break;
         }
      }
      if(phase_root_same_zone)
      {
         int dead_seq = events[i].sequence_id;
         for(int k=0; k<n; k++)
         {
            if(events[k].sequence_id == dead_seq)
            {
               events[k].visible_main = false;
               events[k].reason = events[k].reason + ";hidden_fail_open_inside_phase_owned_region";
            }
         }
      }
   }
}

void FP_SortEventsByTime(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n-1; i++)
   {
      int best = i;
      for(int j=i+1; j<n; j++)
      {
         if(events[j].origin.index_anchor < events[best].origin.index_anchor) best = j;
         else if(events[j].origin.index_anchor == events[best].origin.index_anchor && events[j].level < events[best].level) best = j;
      }
      if(best != i)
      {
         FP_FlagEvent tmp = events[i];
         events[i] = events[best];
         events[best] = tmp;
      }
   }
}

bool FP_HasOppositeF3Between(const FP_FlagEvent &events[], const int event_count, const int direction, const int from_anchor, const int to_anchor, const bool require_locked_or_completed)
{
   for(int i=0; i<event_count; i++)
   {
      if(events[i].direction == direction) continue;
      if(events[i].level != FP_LEVEL_F3) continue;
      if(require_locked_or_completed && !FP_IsF3CompletedOrLocked(events[i])) continue;
      int t = events[i].leg2.index_anchor;
      if(t > from_anchor && t < to_anchor) return true;
   }
   return false;
}

void FP_PruneSameDirectionRestarts(FP_FlagEvent &events[], const FP_Config &cfg)
{
   if(!cfg.enforce_single_chain_per_direction_scale && !cfg.enforce_single_chain_per_direction_global) return;
   int n = ArraySize(events);

   for(int i=0; i<n; i++)
   {
      if(events[i].level != FP_LEVEL_F1) continue;
      if(!events[i].visible_main) continue;

      for(int j=i+1; j<n; j++)
      {
         if(events[j].level != FP_LEVEL_F1) continue;
         if(!events[j].visible_main) continue;
         if(events[j].direction != events[i].direction) continue;

         bool same_scale_guard = cfg.enforce_single_chain_per_direction_scale && (events[j].scale_L == events[i].scale_L);
         bool global_guard = cfg.enforce_single_chain_per_direction_global;
         if(!same_scale_guard && !global_guard) continue;

         bool has_opposite_f3 = FP_HasOppositeF3Between(events, n, events[i].direction, events[i].origin.index_anchor, events[j].origin.index_anchor, true);
         if(!has_opposite_f3)
         {
            // Hide the later restart and any descendants that point to it.
            int dead_seq = events[j].sequence_id;
            events[j].visible_main = false;
            events[j].reason = events[j].reason + ";hidden_same_direction_restart_without_opposite_f3";
            for(int k=0; k<n; k++)
            {
               if(events[k].sequence_id == dead_seq && k != j)
               {
                  events[k].visible_main = false;
                  events[k].reason = events[k].reason + ";hidden_descendant_of_pruned_root";
               }
            }
         }
      }
   }
}

void FP_LockF3WithFirstOppositeF1(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(events[i].level != FP_LEVEL_F3) continue;
      if(events[i].status != FP_STATUS_COMPLETED) continue;
      int complete_anchor = events[i].leg2.index_anchor;
      int best = -1;
      for(int j=0; j<n; j++)
      {
         if(events[j].level != FP_LEVEL_F1) continue;
         if(events[j].direction == events[i].direction) continue;
         if(events[j].status != FP_STATUS_CONFIRMED) continue;
         if(!events[j].has_confirm) continue;
         if(events[j].origin.index_anchor <= complete_anchor) continue;
         if(events[j].confirm.index_anchor <= complete_anchor) continue;
         if(best < 0 || events[j].confirm.index_anchor < events[best].confirm.index_anchor) best = j;
      }
      if(best >= 0)
      {
         events[i].status = FP_STATUS_LOCKED;
         events[i].extension_end = events[best].origin;
         events[i].has_extension = true;
         events[i].pos_extension_end = events[best].pos_origin;
         events[i].reason = events[i].reason + ";locked_by_opposite_F1_Q" + IntegerToString(events[best].event_id);
      }
   }
}


// ------------------------- Main-chart canonicalization ----------------------

int FP_EventStatusRank(const FP_FlagEvent &e)
{
   if(e.status == FP_STATUS_LOCKED) return 80;
   if(e.status == FP_STATUS_COMPLETED) return 70;
   if(e.status == FP_STATUS_CONFIRMED) return 60;
   if(e.status == FP_STATUS_QUALIFIED) return 50;
   if(e.status == FP_STATUS_POST_FLAG) return 40;
   if(e.status == FP_STATUS_LIVE_BODY) return 30;
   if(e.status == FP_STATUS_LIVE_LEG) return 20;
   if(e.status == FP_STATUS_SEED) return 10;
   return 0;
}

bool FP_EventHasVisibleChild(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &root)
{
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].sequence_id != root.sequence_id) continue;
      if(events[i].chain_index > root.chain_index) return true;
   }
   return false;
}

int FP_MainChartRootScore(const FP_FlagEvent &events[], const int n, const FP_FlagEvent &e)
{
   int score = 0;
   if(e.from_phase_boundary) score += 200;
   if(!e.from_fail_open) score += 40;
   score += FP_EventStatusRank(e);
   if(FP_EventHasVisibleChild(events, n, e)) score += 25;
   // On equal semantic quality, prefer the local/lower-L representation so a
   // high-L umbrella does not dominate the main M1 chart.
   score -= MathMax(0, e.scale_L);
   return score;
}

bool FP_NodeVisualClose(const FP_Node &a, const FP_Node &b, const int bar_tol, const double price_tol)
{
   if(a.kind != b.kind) return false;
   if(a.index_anchor < 0 || b.index_anchor < 0) return false;
   if(MathAbs(a.index_anchor - b.index_anchor) > bar_tol) return false;
   if(MathAbs(a.price - b.price) > price_tol) return false;
   return true;
}

bool FP_EventBodiesVisuallyEquivalent(const FP_FlagEvent &a, const FP_FlagEvent &b)
{
   if(a.level != b.level) return false;
   if(a.direction != b.direction) return false;
   if(!a.has_origin || !a.has_leg1 || !b.has_origin || !b.has_leg1) return false;

   int tol = MathMax(2, MathMin(MathMax(1, a.scale_L), MathMax(1, b.scale_L)) / 2);
   double ptol = MathMax(_Point * 2.0, MathAbs(a.flag_size + b.flag_size) * 0.0005);

   if(!FP_NodeVisualClose(a.origin, b.origin, tol, ptol)) return false;
   if(!FP_NodeVisualClose(a.leg1, b.leg1, tol, ptol)) return false;

   if(a.has_waist != b.has_waist) return false;
   if(a.has_leg2 != b.has_leg2) return false;
   if(a.has_waist && !FP_NodeVisualClose(a.waist, b.waist, tol, ptol)) return false;
   if(a.has_leg2 && !FP_NodeVisualClose(a.leg2, b.leg2, tol, ptol)) return false;
   return true;
}

void FP_HideSequenceById(FP_FlagEvent &events[], const int sequence_id, const string reason)
{
   for(int i=0; i<ArraySize(events); i++)
   {
      if(events[i].sequence_id != sequence_id) continue;
      events[i].visible_main = false;
      events[i].reason = events[i].reason + reason;
   }
}

void FP_PruneDuplicateRootSequences(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].level != FP_LEVEL_F1) continue;
      if(events[i].chain_index != 1) continue;

      for(int j=i+1; j<n; j++)
      {
         if(!events[j].visible_main) continue;
         if(events[j].level != FP_LEVEL_F1) continue;
         if(events[j].chain_index != 1) continue;
         if(!FP_EventBodiesVisuallyEquivalent(events[i], events[j])) continue;

         int score_i = FP_MainChartRootScore(events, n, events[i]);
         int score_j = FP_MainChartRootScore(events, n, events[j]);
         int dead = (score_j > score_i ? i : j);
         int keep = (dead == i ? j : i);
         string why = ";hidden_duplicate_root_sequence_kept_Q" + IntegerToString(events[keep].event_id);
         FP_HideSequenceById(events, events[dead].sequence_id, why);
         if(dead == i) break;
      }
   }
}

void FP_HideOrphanDescendants(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   bool changed = true;
   while(changed)
   {
      changed = false;
      for(int i=0; i<n; i++)
      {
         if(!events[i].visible_main) continue;
         if(events[i].chain_index <= 1) continue;
         bool parent_visible = false;
         for(int j=0; j<n; j++)
         {
            if(!events[j].visible_main) continue;
            if(events[j].sequence_id != events[i].sequence_id) continue;
            if(events[j].chain_index == events[i].chain_index - 1)
            {
               parent_visible = true;
               break;
            }
         }
         if(!parent_visible)
         {
            events[i].visible_main = false;
            events[i].reason = events[i].reason + ";hidden_orphan_descendant_no_visible_parent";
            changed = true;
         }
      }
   }
}

void FP_MergeVisualBodyDuplicates(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      for(int j=i+1; j<n; j++)
      {
         if(!events[j].visible_main) continue;
         if(!FP_EventBodiesVisuallyEquivalent(events[i], events[j])) continue;
         int score_i = FP_EventStatusRank(events[i]) - events[i].scale_L;
         int score_j = FP_EventStatusRank(events[j]) - events[j].scale_L;
         int dead = (score_j > score_i ? i : j);
         int keep = (dead == i ? j : i);
         events[dead].visible_main = false;
         events[dead].reason = events[dead].reason + ";hidden_visual_body_duplicate_of_Q" + IntegerToString(events[keep].event_id);
         if(dead == i) break;
      }
   }
}

void FP_MergeExactVisualDuplicates(FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      for(int j=i+1; j<n; j++)
      {
         if(!events[j].visible_main) continue;
         if(FP_SameBodyIdentity(events[i], events[j]))
         {
            // Keep the older event close to price and hide exact duplicate geometry.
            events[j].visible_main = false;
            events[j].reason = events[j].reason + ";hidden_exact_visual_duplicate_of_Q" + IntegerToString(events[i].event_id);
         }
      }
   }
}

void FP_RecountResult(FP_FlagEvent &events[], const FP_HookBranch &hooks[], FP_DetectResult &result)
{
   int nodes_prev = result.nodes_total;
   int hooks_prev = result.hooks_total;
   int nd_prev = result.nd_total;
   FP_ResetDetectResult(result);
   result.nodes_total = nodes_prev;
   result.hooks_total = hooks_prev;
   result.nd_total = nd_prev;
   for(int i=0; i<ArraySize(events); i++)
      FP_UpdateEventCounters(events[i], result);
}

int FP_DetectAllScales(const MqlRates &rates[],
                       const int total,
                       const int &scales[],
                       const int scale_count,
                       const FP_Config &cfg,
                       FP_FlagEvent &events[],
                       FP_HookBranch &hooks[],
                       FP_DetectResult &result)
{
   ArrayResize(events, 0);
   ArrayResize(hooks, 0);
   FP_ResetDetectResult(result);

   for(int s=0; s<scale_count; s++)
   {
      if(scales[s] <= 0) continue;
      FP_DetectScale(rates, total, scales[s], cfg, events, hooks, result);
   }

   FP_SortEventsByTime(events);
   FP_FinalizeEventIds(events);
   FP_PruneFailOpenRootsWhenPhaseRootsExist(events);
   FP_LockF3WithFirstOppositeF1(events);
   FP_PruneSameDirectionRestarts(events, cfg);
   FP_HideSupersededParentStates(events, cfg);
   FP_PruneDuplicateRootSequences(events);
   FP_MergeVisualBodyDuplicates(events);
   FP_MergeExactVisualDuplicates(events);
   FP_HideOrphanDescendants(events);
   FP_FinalizeEventIds(events);
   FP_RebuildParentIdsAfterSort(events);
   FP_RecountResult(events, hooks, result);
   return ArraySize(events);
}

#endif // __FP_SEQUENCE_ENGINE_MQH__
