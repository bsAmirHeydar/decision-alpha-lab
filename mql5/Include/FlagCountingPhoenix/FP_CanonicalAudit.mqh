#ifndef __FP_CANONICAL_AUDIT_MQH__
#define __FP_CANONICAL_AUDIT_MQH__
#property strict

#include "FP_CanonicalRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 11 / Canonicalization Audit
// ============================================================================

void FP_PrintCanonicalReport(const string tag, const FP_CanonicalReport &r)
{
   string msg = tag;
   msg += " status=" + r.status;
   msg += " events=" + IntegerToString(r.events_seen);
   msg += " hooks=" + IntegerToString(r.hooks_seen);
   msg += " visible_before=" + IntegerToString(r.visible_before);
   msg += " visible_after=" + IntegerToString(r.visible_after);
   msg += " hidden_before=" + IntegerToString(r.hidden_before);
   msg += " hidden_after=" + IntegerToString(r.hidden_after);
   msg += " ids_reassigned=" + IntegerToString(r.ids_reassigned);
   msg += " event_ids_repaired=" + IntegerToString(r.event_ids_repaired);
   msg += " parent_ids_repaired=" + IntegerToString(r.parent_ids_repaired);
   msg += " missing_identity_repaired=" + IntegerToString(r.missing_identity_repaired);
   msg += " hidden_reason_repaired=" + IntegerToString(r.hidden_reason_repaired);
   msg += " visible_reason_cleaned=" + IntegerToString(r.visible_reason_cleaned);
   msg += " hidden_no_reason_after=" + IntegerToString(r.hidden_no_reason_after);
   msg += " duplicate_groups=" + IntegerToString(r.visible_duplicate_groups);
   msg += " duplicates_hidden=" + IntegerToString(r.visible_duplicates_hidden);
   msg += " visual_conflicts=" + IntegerToString(r.visual_id_duplicate_conflicts);
   msg += " structural_conflicts=" + IntegerToString(r.structural_id_duplicate_conflicts);
   msg += " phase_safe_duplicate_hides=" + IntegerToString(r.phase_safe_duplicate_hides);
   msg += " exact_duplicate_hides=" + IntegerToString(r.exact_duplicate_hides);
   msg += " orphan_visible_before=" + IntegerToString(r.orphan_visible_before);
   msg += " orphan_hidden=" + IntegerToString(r.orphan_hidden);
   msg += " orphan_visible_after=" + IntegerToString(r.orphan_visible_after);
   msg += " invalid_visible_hidden=" + IntegerToString(r.invalid_visible_hidden);
   msg += " render_none_hidden=" + IntegerToString(r.render_none_hidden);
   msg += " missing_body_hidden=" + IntegerToString(r.missing_body_hidden);
   msg += " chain_index_repaired=" + IntegerToString(r.chain_index_repaired);
   msg += " invariant_checks=" + IntegerToString(r.invariant_checks);
   msg += " invariant_failures=" + IntegerToString(r.invariant_failures);
   msg += " visible_missing_identity=" + IntegerToString(r.visible_missing_identity);
   msg += " visible_duplicate_visual_after=" + IntegerToString(r.visible_duplicate_visual_after);
   msg += " parent_missing_after=" + IntegerToString(r.parent_missing_after);
   msg += " parent_mismatch_after=" + IntegerToString(r.parent_mismatch_after);
   msg += " phase_owner_missing_after=" + IntegerToString(r.phase_owner_missing_after);
   msg += " broken_chain_after=" + IntegerToString(r.broken_chain_after);
   msg += " hook_hidden_reason_repaired=" + IntegerToString(r.hooks_hidden_reason_repaired);
   msg += " hook_visible_after=" + IntegerToString(r.hooks_visible_after);
   msg += " hook_hidden_after=" + IntegerToString(r.hooks_hidden_after);
   msg += " rank_min=" + IntegerToString(r.min_canonical_rank);
   msg += " rank_max=" + IntegerToString(r.max_canonical_rank);
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintCanonicalSamples(const string tag,
                              const FP_FlagEvent &events[],
                              const int event_count,
                              const int limit)
{
   int lim = MathMax(0, limit);
   int printed = 0;
   for(int i=0; i<event_count && printed<lim; i++)
   {
      string msg = tag + "_SAMPLE";
      msg += " id=" + IntegerToString(events[i].event_id);
      msg += " seq=" + IntegerToString(events[i].sequence_id);
      msg += " level=" + FP_LevelName(events[i].level);
      msg += " dir=" + FP_DirectionName(events[i].direction);
      msg += " status=" + FP_StatusName(events[i].status);
      msg += " canonical_state=" + FP_CanonicalStateName(events[i].canonical_state);
      msg += " canonical_id=" + events[i].canonical_id;
      msg += " conflict_group=" + events[i].canonical_conflict_group_id;
      msg += " final_rank=" + IntegerToString(events[i].canonical_rank_final);
      msg += " invariant_flags=" + IntegerToString(events[i].canonical_invariant_flags);
      msg += " visible=" + FP_BoolName(events[i].visible_main);
      msg += " hidden_reason=" + events[i].hidden_reason;
      msg += " phase_owner=" + IntegerToString(events[i].phase_owner_root_id);
      msg += " chain_state=" + FP_OwnershipChainStateName(events[i].chain_state);
      msg += " parent=" + IntegerToString(events[i].parent_event_id);
      msg += " visual_id=" + events[i].visual_id;
      msg += " canonical_reason=" + events[i].canonical_reason;
      Print(msg);
      printed++;
   }
}

#endif // __FP_CANONICAL_AUDIT_MQH__
