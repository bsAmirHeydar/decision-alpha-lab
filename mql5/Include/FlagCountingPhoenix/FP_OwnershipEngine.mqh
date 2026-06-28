#ifndef __FP_OWNERSHIP_ENGINE_MQH__
#define __FP_OWNERSHIP_ENGINE_MQH__
#property strict

#include "FP_OwnershipAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 10 / Ownership Engine
// ----------------------------------------------------------------------------
// Main contract: a visible phase owns exactly one canonical F1 root until an
// opposite terminal F3 reset exists. Descendants of hidden roots cannot remain
// visible. Visual duplicate pruning still runs after this layer, but it cannot
// decide phase truth.
// ============================================================================

int FP_Level10CountVisible(const FP_FlagEvent &events[])
{
   int n = ArraySize(events);
   int c = 0;
   for(int i=0; i<n; i++)
      if(events[i].visible_main) c++;
   return c;
}

int FP_Level10FindRootIndexForSequence(const FP_FlagEvent &events[], const int n, const int sequence_id)
{
   int best = -1;
   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != sequence_id) continue;
      if(events[i].level != FP_LEVEL_F1) continue;
      if(events[i].chain_index != 1) continue;
      if(best < 0 || events[i].origin.index_anchor < events[best].origin.index_anchor) best = i;
   }
   return best;
}

void FP_Level10AnnotateSequence(FP_FlagEvent &events[], const int n, const int root_index, const int chain_state)
{
   if(root_index < 0 || root_index >= n) return;
   int seq_id = events[root_index].sequence_id;
   int owner_id = events[root_index].event_id;
   int dir = events[root_index].direction;
   int next_level = FP_Level10NextExpectedLevel(chain_state);

   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != seq_id) continue;
      events[i].phase_direction = dir;
      events[i].phase_owner_root_id = owner_id;
      events[i].chain_state = chain_state;
      events[i].next_expected_f_level = next_level;
      events[i].owner_rank_score = FP_Level10ChainMaturityScore(events, n, events[root_index]);
   }
}

void FP_Level10HideSequence(FP_FlagEvent &events[],
                            const int n,
                            const int root_index,
                            const string reason,
                            FP_OwnershipReport &report)
{
   if(root_index < 0 || root_index >= n) return;
   int seq_id = events[root_index].sequence_id;
   string hidden_desc = "";

   for(int i=0; i<n; i++)
   {
      if(events[i].sequence_id != seq_id) continue;
      bool was_visible = events[i].visible_main;
      if(events[i].chain_index <= 1)
      {
         events[i].chain_state = FP_CHAIN_HIDDEN_LOSER;
         FP_SetHiddenReason(events[i], reason);
         if(was_visible) report.hidden_roots++;
      }
      else
      {
         events[i].chain_state = FP_CHAIN_HIDDEN_DESCENDANT;
         hidden_desc = FP_Level10AppendId(hidden_desc, events[i].event_id);
         FP_SetHiddenReason(events[i], reason + ";hidden_descendant_of_losing_phase_root");
         if(was_visible) report.hidden_descendants++;
      }
      events[i].phase_owner_root_id = events[root_index].event_id;
      events[i].phase_direction = events[root_index].direction;
      events[i].next_expected_f_level = FP_LEVEL_NONE;
   }

   events[root_index].hidden_descendant_ids = hidden_desc;
}

void FP_Level10HideFailOpenInsidePhaseRoots(FP_FlagEvent &events[], const int n, FP_OwnershipReport &report)
{
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      if(!FP_Level10IsRootF1(events[i])) continue;
      if(!events[i].from_fail_open) continue;

      bool covered = false;
      int keeper = -1;
      for(int j=0; j<n; j++)
      {
         if(i == j) continue;
         if(FP_Level10PhaseRootCoversFailOpenRoot(events[j], events[i]))
         {
            covered = true;
            keeper = j;
            break;
         }
      }
      if(covered)
      {
         if(keeper >= 0)
            events[keeper].losing_candidate_ids = FP_Level10AppendId(events[keeper].losing_candidate_ids, events[i].event_id);
         report.failopen_hidden++;
         int keeper_id = (keeper >= 0 ? events[keeper].event_id : -1);
         FP_Level10HideSequence(events, n, i, "hidden_fail_open_inside_phase_owned_region_Q" + IntegerToString(keeper_id), report);
      }
   }
}

void FP_Level10HideSupersededParentStates(FP_FlagEvent &events[], const int n, const FP_Config &cfg, FP_OwnershipReport &report)
{
   if(!cfg.hide_superseded_parent_states) return;
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      if(events[i].level != FP_LEVEL_F1 && events[i].level != FP_LEVEL_F2) continue;
      if(events[i].status == FP_STATUS_CONFIRMED || events[i].status == FP_STATUS_LOCKED || events[i].status == FP_STATUS_COMPLETED) continue;

      bool has_visible_child = false;
      for(int j=0; j<n; j++)
      {
         if(!events[j].visible_main) continue;
         if(events[j].sequence_id != events[i].sequence_id) continue;
         if(events[j].chain_index == events[i].chain_index + 1)
         {
            has_visible_child = true;
            break;
         }
      }
      if(has_visible_child)
      {
         FP_SetHiddenReason(events[i], "hidden_superseded_parent_state_with_visible_child");
         report.superseded_parent_hides++;
      }
   }
}

void FP_Level10HideOrphans(FP_FlagEvent &events[], const int n, const FP_Config &cfg, FP_OwnershipReport &report)
{
   if(!cfg.ownership_hide_orphans) return;
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
            events[i].chain_state = FP_CHAIN_ORPHAN_HIDDEN;
            events[i].next_expected_f_level = FP_LEVEL_NONE;
            FP_SetHiddenReason(events[i], "hidden_orphan_descendant_no_visible_parent");
            report.orphans_hidden++;
            changed = true;
         }
      }
   }
}

void FP_Level10ResolveDirectionalPhases(FP_FlagEvent &events[], const int n, const int direction, const FP_Config &cfg, FP_OwnershipReport &report)
{
   int keeper = -1;

   for(int i=0; i<n; i++)
   {
      if(!FP_Level10IsVisibleRootF1(events[i])) continue;
      if(events[i].direction != direction) continue;

      report.root_candidates++;
      int rank_i = FP_Level10ChainMaturityScore(events, n, events[i]);
      events[i].owner_rank_score = rank_i;
      FP_RecordOwnershipRank(report, rank_i);

      if(keeper < 0 || !events[keeper].visible_main)
      {
         keeper = i;
         report.phases_seen++;
         report.owner_roots++;
         int st = FP_Level10ChainStateForSequence(events, n, events[i].sequence_id);
         FP_Level10AnnotateSequence(events, n, i, st);
         continue;
      }

      int reset_index = -1;
      bool reset = FP_Level10HasOppositeF3ResetBetweenRoots(events,
                                                            n,
                                                            direction,
                                                            events[keeper].origin.index_anchor,
                                                            events[i].origin.index_anchor,
                                                            reset_index);
      if(reset)
      {
         report.resets++;
         events[keeper].chain_state = FP_CHAIN_RESET_ALLOWED;
         events[keeper].next_expected_f_level = FP_LEVEL_F1;
         events[keeper].phase_reset_reason = "reset_by_opposite_terminal_f3_Q" + IntegerToString(events[reset_index].event_id);
         keeper = i;
         report.phases_seen++;
         report.owner_roots++;
         int st = FP_Level10ChainStateForSequence(events, n, events[i].sequence_id);
         FP_Level10AnnotateSequence(events, n, i, st);
         events[i].phase_reset_reason = "new_phase_after_reset_Q" + IntegerToString(events[reset_index].event_id);
         continue;
      }

      report.competing_roots++;
      int rank_keep = FP_Level10ChainMaturityScore(events, n, events[keeper]);
      FP_RecordOwnershipRank(report, rank_keep);

      if(rank_i > rank_keep + MathMax(0, cfg.ownership_score_margin))
      {
         events[i].losing_candidate_ids = FP_Level10AppendId(events[i].losing_candidate_ids, events[keeper].event_id);
         FP_Level10HideSequence(events, n, keeper, "hidden_by_level10_owner_replaced_by_Q" + IntegerToString(events[i].event_id), report);
         keeper = i;
         int st = FP_Level10ChainStateForSequence(events, n, events[i].sequence_id);
         FP_Level10AnnotateSequence(events, n, i, st);
      }
      else
      {
         events[keeper].losing_candidate_ids = FP_Level10AppendId(events[keeper].losing_candidate_ids, events[i].event_id);
         FP_Level10HideSequence(events, n, i, "hidden_by_level10_same_direction_phase_owner_Q" + IntegerToString(events[keeper].event_id), report);
      }
   }
}

void FP_ApplySequenceOwnershipWithReport(FP_FlagEvent &events[], const FP_Config &cfg, FP_OwnershipReport &report)
{
   FP_ResetOwnershipReport(report);
   int n = ArraySize(events);
   report.events_seen = n;
   report.visible_before = FP_Level10CountVisible(events);

   // Initialize all events with chain-derived state before pruning.
   for(int i=0; i<n; i++)
   {
      int root = FP_Level10FindRootIndexForSequence(events, n, events[i].sequence_id);
      if(root >= 0)
      {
         int st = FP_Level10ChainStateForSequence(events, n, events[root].sequence_id);
         events[i].phase_direction = events[root].direction;
         events[i].phase_owner_root_id = events[root].event_id;
         events[i].chain_state = st;
         events[i].next_expected_f_level = FP_Level10NextExpectedLevel(st);
         events[i].owner_rank_score = FP_Level10ChainMaturityScore(events, n, events[root]);
      }
      else
      {
         events[i].phase_direction = events[i].direction;
         events[i].phase_owner_root_id = -1;
         events[i].chain_state = FP_CHAIN_NONE;
         events[i].next_expected_f_level = FP_LEVEL_F1;
      }
   }

   if(cfg.strict_main_chart_ownership)
   {
      FP_Level10HideFailOpenInsidePhaseRoots(events, n, report);
      FP_Level10ResolveDirectionalPhases(events, n, FP_DIR_BULLISH, cfg, report);
      FP_Level10ResolveDirectionalPhases(events, n, FP_DIR_BEARISH, cfg, report);
   }
   else
   {
      report.reason = "strict_main_chart_ownership_disabled";
   }

   FP_Level10HideSupersededParentStates(events, n, cfg, report);
   FP_Level10HideOrphans(events, n, cfg, report);

   // Final owner count is recomputed after possible owner replacement and
   // orphan/superseded hiding so the audit line reflects the final main-chart
   // phase owners, not intermediate candidates that briefly held ownership.
   int final_owner_roots = 0;
   for(int k=0; k<n; k++)
   {
      if(!events[k].visible_main) continue;
      if(!FP_Level10IsRootF1(events[k])) continue;
      if(events[k].phase_owner_root_id == events[k].event_id || events[k].phase_owner_root_id < 0)
         final_owner_roots++;
   }
   report.owner_roots = final_owner_roots;
   report.phases_seen = final_owner_roots;

   report.visible_after = FP_Level10CountVisible(events);
   if(report.root_candidates <= 0)
   {
      report.max_owner_rank = 0;
      report.min_owner_rank = 0;
   }
   if(report.reason == "") report.reason = "ownership_applied";
}

#endif // __FP_OWNERSHIP_ENGINE_MQH__
