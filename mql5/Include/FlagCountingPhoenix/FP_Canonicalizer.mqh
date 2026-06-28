#ifndef __FP_CANONICALIZER_MQH__
#define __FP_CANONICALIZER_MQH__
#property strict

#include "FP_CanonicalAudit.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 11 / Canonicalization Engine
// ----------------------------------------------------------------------------
// Final engine-owned pass before renderer/export.  It repairs IDs, parent links,
// hidden reasons, phase-safe visible duplicates, orphan descendants, and final
// invariant counters. It never creates new market structures.
// ============================================================================

void FP_CanonicalCountVisibility(const FP_FlagEvent &events[], const int n, int &visible, int &hidden)
{
   visible = 0;
   hidden = 0;
   for(int i=0; i<n; i++)
   {
      if(events[i].visible_main) visible++;
      else hidden++;
   }
}

void FP_CanonicalAssignBaseFields(FP_FlagEvent &events[], const int n, const FP_Config &cfg, FP_CanonicalReport &report)
{
   for(int i=0; i<n; i++)
   {
      if(events[i].event_id != i)
      {
         events[i].event_id = i;
         report.event_ids_repaired++;
      }

      if(events[i].canonical_id == "")
         events[i].canonical_id = "CAN:" + FP_LevelKey(events[i].level) + ":" + IntegerToString(events[i].event_id);
      events[i].canonical_conflict_group_id = FP_CanonicalConflictGroupId(events[i]);
      events[i].canonical_rank_final = FP_CanonicalSemanticRank(events, n, events[i]);
      if(i == 0 || events[i].canonical_rank_final < report.min_canonical_rank) report.min_canonical_rank = events[i].canonical_rank_final;
      if(i == 0 || events[i].canonical_rank_final > report.max_canonical_rank) report.max_canonical_rank = events[i].canonical_rank_final;

      if(FP_CanonicalIdentityMissing(events[i]))
      {
         report.missing_identity_repaired++;
         FP_AssignEventIdentity(events[i], cfg);
      }
   }
}

void FP_CanonicalRepairParentIds(FP_FlagEvent &events[], const int n, FP_CanonicalReport &report)
{
   for(int i=0; i<n; i++)
   {
      if(!FP_CanonicalParentRequired(events[i])) continue;
      int p = FP_CanonicalFindParentIndex(events, n, events[i]);
      if(p < 0) continue;
      if(events[i].parent_event_id != events[p].event_id)
      {
         events[i].parent_event_id = events[p].event_id;
         events[i].parent_sequence_id = events[p].sequence_id;
         report.parent_ids_repaired++;
      }
   }
}

void FP_CanonicalHideInvalidAndMalformed(FP_FlagEvent &events[], const int n, const FP_Config &cfg, FP_CanonicalReport &report)
{
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;

      if(FP_CanonicalIsInvalidVisible(events[i], cfg))
      {
         FP_SetHiddenReason(events[i], "canonical_hide_invalidated_not_requested");
         FP_CanonicalSetState(events[i], FP_CANON_HIDDEN_INVALID, "invalidated_hidden_by_contract");
         report.invalid_visible_hidden++;
         continue;
      }

      if(FP_CanonicalShouldHideRenderNone(events[i]))
      {
         FP_SetHiddenReason(events[i], "canonical_hide_render_none");
         FP_CanonicalSetState(events[i], FP_CANON_HIDDEN_INVALID, "render_none_hidden_by_contract");
         report.render_none_hidden++;
         continue;
      }

      if(!FP_CanonicalHasRequiredBody(events[i]))
      {
         FP_SetHiddenReason(events[i], "canonical_hide_missing_required_body_nodes");
         FP_CanonicalSetState(events[i], FP_CANON_HIDDEN_INVALID, "missing_body_nodes_hidden_by_contract");
         report.missing_body_hidden++;
         continue;
      }
   }
}

void FP_CanonicalHideOrphans(FP_FlagEvent &events[], const int n, const FP_Config &cfg, FP_CanonicalReport &report)
{
   for(int i=0; i<n; i++)
      if(FP_CanonicalIsVisibleOrphan(events, n, events[i])) report.orphan_visible_before++;

   if(!cfg.canonical_hide_unresolved_orphans) return;

   bool changed = true;
   while(changed)
   {
      changed = false;
      for(int i=0; i<n; i++)
      {
         if(!FP_CanonicalIsVisibleOrphan(events, n, events[i])) continue;
         FP_SetHiddenReason(events[i], "canonical_hide_unresolved_orphan_descendant");
         FP_CanonicalSetState(events[i], FP_CANON_HIDDEN_ORPHAN, "orphan_hidden_by_canonicalizer");
         report.orphan_hidden++;
         changed = true;
      }
   }
}

void FP_CanonicalHideVisibleDuplicates(FP_FlagEvent &events[], const int n, FP_CanonicalReport &report)
{
   for(int i=0; i<n; i++)
   {
      if(!events[i].visible_main) continue;
      bool group_seen = false;
      for(int j=i+1; j<n; j++)
      {
         if(!events[j].visible_main) continue;
         if(!FP_CanonicalSameVisibleConflict(events[i], events[j])) continue;

         if(!group_seen)
         {
            report.visible_duplicate_groups++;
            group_seen = true;
         }
         report.visual_id_duplicate_conflicts++;

         int score_i = FP_CanonicalSemanticRank(events, n, events[i]);
         int score_j = FP_CanonicalSemanticRank(events, n, events[j]);
         int dead = j;
         int keep = i;
         if(score_j > score_i)
         {
            dead = i;
            keep = j;
         }

         string why = "canonical_hide_phase_safe_duplicate_kept_Q" + IntegerToString(events[keep].event_id);
         FP_SetHiddenReason(events[dead], why);
         FP_CanonicalSetState(events[dead], FP_CANON_HIDDEN_DUPLICATE, why);
         report.visible_duplicates_hidden++;
         report.phase_safe_duplicate_hides++;
         if(FP_SameBodyIdentity(events[i], events[j])) report.exact_duplicate_hides++;
         if(dead == i) break;
      }
   }
}

void FP_CanonicalNormalizeReasonsAndStates(FP_FlagEvent &events[], const int n, FP_HookBranch &hooks[], const int hook_count, FP_CanonicalReport &report)
{
   for(int i=0; i<n; i++)
   {
      if(events[i].visible_main)
      {
         if(events[i].hidden_reason != "")
         {
            events[i].hidden_reason = "";
            report.visible_reason_cleaned++;
         }
         if(events[i].canonical_state == FP_CANON_NONE) FP_CanonicalSetState(events[i], FP_CANON_VISIBLE, "visible_canonical_output");
      }
      else
      {
         if(events[i].hidden_reason == "")
         {
            events[i].hidden_reason = "canonical_hidden_without_prior_reason";
            events[i].reason = events[i].reason + ";" + events[i].hidden_reason;
            report.hidden_reason_repaired++;
         }
         if(events[i].canonical_state == FP_CANON_NONE) FP_CanonicalSetState(events[i], FP_CANON_HIDDEN, events[i].hidden_reason);
      }
      events[i].canonical_rank_final = FP_CanonicalSemanticRank(events, n, events[i]);
      events[i].canonical_conflict_group_id = FP_CanonicalConflictGroupId(events[i]);
   }

   for(int h=0; h<hook_count; h++)
   {
      if(hooks[h].visible_main) report.hooks_visible_after++;
      else
      {
         report.hooks_hidden_after++;
         if(hooks[h].hidden_reason == "")
         {
            hooks[h].hidden_reason = "canonical_hidden_hook_without_prior_reason";
            hooks[h].reason = hooks[h].reason + ";" + hooks[h].hidden_reason;
            report.hooks_hidden_reason_repaired++;
         }
      }
   }
}

void FP_CanonicalVerifyInvariants(FP_FlagEvent &events[], const int n, FP_CanonicalReport &report)
{
   report.invariant_checks += 7;

   for(int i=0; i<n; i++)
   {
      events[i].canonical_invariant_flags = 0;
      if(!events[i].visible_main && events[i].hidden_reason == "")
      {
         report.hidden_no_reason_after++;
         events[i].canonical_invariant_flags |= 1;
      }
      if(events[i].visible_main && FP_CanonicalIdentityMissing(events[i]))
      {
         report.visible_missing_identity++;
         events[i].canonical_invariant_flags |= 2;
      }
      if(events[i].visible_main && FP_CanonicalIsVisibleOrphan(events, n, events[i]))
      {
         report.orphan_visible_after++;
         events[i].canonical_invariant_flags |= 4;
      }

      if(events[i].visible_main && FP_CanonicalParentRequired(events[i]))
      {
         int p = FP_CanonicalFindParentIndex(events, n, events[i]);
         if(p < 0)
         {
            report.parent_missing_after++;
            events[i].canonical_invariant_flags |= 8;
         }
         else
         {
            if(events[p].direction != events[i].direction)
            {
               report.parent_mismatch_after++;
               events[i].canonical_invariant_flags |= 16;
            }
            if(events[p].sequence_id != events[i].sequence_id)
            {
               report.parent_mismatch_after++;
               events[i].canonical_invariant_flags |= 16;
            }
            if(events[p].chain_index != events[i].chain_index - 1)
            {
               report.broken_chain_after++;
               events[i].canonical_invariant_flags |= 32;
            }
         }
      }

      if(events[i].visible_main && events[i].level == FP_LEVEL_F1 && events[i].phase_owner_root_id < 0)
      {
         report.phase_owner_missing_after++;
         events[i].canonical_invariant_flags |= 64;
      }

      for(int j=i+1; j<n; j++)
      {
         if(events[i].visible_main && events[j].visible_main && FP_CanonicalSameVisibleConflict(events[i], events[j]))
         {
            report.visible_duplicate_visual_after++;
            events[i].canonical_invariant_flags |= 128;
            events[j].canonical_invariant_flags |= 128;
         }
         if(events[i].structural_id != "" && events[i].structural_id == events[j].structural_id && i != j)
            report.structural_id_duplicate_conflicts++;
      }
   }

   for(int fi=0; fi<n; fi++)
   {
      if(events[fi].canonical_invariant_flags != 0 && events[fi].canonical_state == FP_CANON_VISIBLE)
         FP_CanonicalSetState(events[fi], FP_CANON_INVARIANT_FAILED, "visible_event_failed_canonical_invariants");
   }

   report.invariant_failures = report.hidden_no_reason_after +
                               report.visible_missing_identity +
                               report.visible_duplicate_visual_after +
                               report.parent_missing_after +
                               report.parent_mismatch_after +
                               report.phase_owner_missing_after +
                               report.broken_chain_after +
                               report.orphan_visible_after;

   if(report.invariant_failures == 0)
   {
      report.status = "ok";
      report.reason = "canonical_invariants_passed";
   }
   else
   {
      report.status = "failed";
      report.reason = "canonical_invariants_failed";
   }
}

void FP_ApplyCanonicalizationWithReport(FP_FlagEvent &events[],
                                        FP_HookBranch &hooks[],
                                        const FP_Config &cfg,
                                        FP_CanonicalReport &report)
{
   FP_ResetCanonicalReport(report);
   int n = ArraySize(events);
   int hook_count = ArraySize(hooks);
   report.events_seen = n;
   report.hooks_seen = hook_count;
   FP_CanonicalCountVisibility(events, n, report.visible_before, report.hidden_before);

   FP_FinalizeEventIds(events);
   FP_RebuildParentIdsAfterSort(events);
   FP_CanonicalAssignBaseFields(events, n, cfg, report);
   FP_CanonicalRepairParentIds(events, n, report);
   FP_CanonicalHideInvalidAndMalformed(events, n, cfg, report);
   FP_CanonicalHideOrphans(events, n, cfg, report);
   FP_CanonicalHideVisibleDuplicates(events, n, report);
   FP_NormalizeHiddenReasons(events);
   FP_CanonicalNormalizeReasonsAndStates(events, n, hooks, hook_count, report);

   FP_FinalizeEventIds(events);
   FP_RebuildParentIdsAfterSort(events);
   FP_AssignEventIdentities(events, cfg);
   FP_AssignHookIdentities(hooks, cfg);
   report.ids_reassigned = n + hook_count;

   FP_CanonicalCountVisibility(events, n, report.visible_after, report.hidden_after);
   FP_CanonicalVerifyInvariants(events, n, report);
   if(report.invariant_failures > 0 && !cfg.canonical_strict_invariants)
   {
      report.status = "diagnostic_failed";
      report.reason = "canonical_invariants_failed_non_strict";
   }

   // Canonical invariant flags/states are part of the final audit identity.
   FP_AssignEventIdentities(events, cfg);
   FP_AssignHookIdentities(hooks, cfg);
}

#endif // __FP_CANONICALIZER_MQH__
