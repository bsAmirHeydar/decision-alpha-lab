#ifndef __FP_OWNERSHIP_AUDIT_MQH__
#define __FP_OWNERSHIP_AUDIT_MQH__
#property strict

#include "FP_OwnershipRules.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 10 / Ownership Audit
// ============================================================================

void FP_PrintOwnershipReport(const string tag, const FP_OwnershipReport &r)
{
   string msg = tag;
   msg += " events=" + IntegerToString(r.events_seen);
   msg += " visible_before=" + IntegerToString(r.visible_before);
   msg += " visible_after=" + IntegerToString(r.visible_after);
   msg += " phases=" + IntegerToString(r.phases_seen);
   msg += " root_candidates=" + IntegerToString(r.root_candidates);
   msg += " owner_roots=" + IntegerToString(r.owner_roots);
   msg += " competing_roots=" + IntegerToString(r.competing_roots);
   msg += " resets=" + IntegerToString(r.resets);
   msg += " hidden_roots=" + IntegerToString(r.hidden_roots);
   msg += " hidden_descendants=" + IntegerToString(r.hidden_descendants);
   msg += " orphans_hidden=" + IntegerToString(r.orphans_hidden);
   msg += " failopen_hidden=" + IntegerToString(r.failopen_hidden);
   msg += " superseded_parent_hides=" + IntegerToString(r.superseded_parent_hides);
   msg += " phase_safe_duplicate_hides=" + IntegerToString(r.phase_safe_duplicate_hides);
   msg += " max_owner_rank=" + IntegerToString(r.max_owner_rank);
   msg += " min_owner_rank=" + IntegerToString(r.min_owner_rank);
   msg += " reason=" + r.reason;
   Print(msg);
}

void FP_PrintOwnershipSamples(const string tag,
                              const FP_FlagEvent &events[],
                              const int event_count,
                              const int sample_limit)
{
   int printed = 0;
   int limit = MathMax(0, sample_limit);
   for(int i=0; i<event_count && printed<limit; i++)
   {
      if(events[i].level != FP_LEVEL_F1 && events[i].chain_index <= 1) continue;
      if(events[i].level != FP_LEVEL_F1 && events[i].level != FP_LEVEL_F2 && events[i].level != FP_LEVEL_F3) continue;

      string msg = tag + "_SAMPLE";
      msg += " id=" + IntegerToString(events[i].event_id);
      msg += " seq=" + IntegerToString(events[i].sequence_id);
      msg += " chain=" + IntegerToString(events[i].chain_index);
      msg += " level=" + FP_LevelName(events[i].level);
      msg += " dir=" + FP_DirectionName(events[i].direction);
      msg += " visible=" + FP_BoolName(events[i].visible_main);
      msg += " owner=" + IntegerToString(events[i].phase_owner_root_id);
      msg += " phase_dir=" + FP_DirectionName(events[i].phase_direction);
      msg += " chain_state=" + FP_OwnershipChainStateName(events[i].chain_state);
      msg += " next=" + FP_LevelName(events[i].next_expected_f_level);
      msg += " rank=" + IntegerToString(events[i].owner_rank_score);
      msg += " reset=" + events[i].phase_reset_reason;
      msg += " losers=" + events[i].losing_candidate_ids;
      msg += " hidden_desc=" + events[i].hidden_descendant_ids;
      msg += " hidden_reason=" + events[i].hidden_reason;
      msg += " reason=" + events[i].reason;
      Print(msg);
      printed++;
   }
}

#endif // __FP_OWNERSHIP_AUDIT_MQH__
