#ifndef __DAL_STC_HUNTS_MQH__
#define __DAL_STC_HUNTS_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_WLevels.mqh>

int STC_HuntReferenceCount(const STC_WCycle current_w)
{
   if(current_w == STC_W2) return 1;
   if(current_w == STC_W3) return 2;
   if(current_w == STC_W4) return 3;
   return 0;
}

STC_WCycle STC_HuntReferenceByRank(const STC_WCycle current_w, const int rank)
{
   // Rank order is nearest previous W first. This is audit order only.
   // Later risk/reference selection layers may choose the largest-stop reference
   // across these legal references, per the locked owner decision.
   if(current_w == STC_W2)
   {
      if(rank == 0) return STC_W1;
   }
   if(current_w == STC_W3)
   {
      if(rank == 0) return STC_W2;
      if(rank == 1) return STC_W1;
   }
   if(current_w == STC_W4)
   {
      if(rank == 0) return STC_W3;
      if(rank == 1) return STC_W2;
      if(rank == 2) return STC_W1;
   }
   return STC_W_NONE;
}

STC_HuntPattern STC_DeriveHuntPattern(const bool symbol1_hunt, const bool symbol2_hunt)
{
   if(symbol1_hunt && symbol2_hunt) return STC_HUNT_BOTH;
   if(symbol1_hunt) return STC_HUNT_SYMBOL1_ONLY;
   if(symbol2_hunt) return STC_HUNT_SYMBOL2_ONLY;
   return STC_HUNT_NONE;
}

void STC_FillHuntSymbolNames(STC_Config &cfg, STC_ReferenceHuntAudit &audit)
{
   audit.high_hunted_symbol = "";
   audit.high_clean_symbol = "";
   audit.low_hunted_symbol = "";
   audit.low_clean_symbol = "";

   if(audit.high_hunt_pattern == STC_HUNT_SYMBOL1_ONLY)
   {
      audit.high_hunted_symbol = cfg.symbol1;
      audit.high_clean_symbol = cfg.symbol2;
   }
   else if(audit.high_hunt_pattern == STC_HUNT_SYMBOL2_ONLY)
   {
      audit.high_hunted_symbol = cfg.symbol2;
      audit.high_clean_symbol = cfg.symbol1;
   }

   if(audit.low_hunt_pattern == STC_HUNT_SYMBOL1_ONLY)
   {
      audit.low_hunted_symbol = cfg.symbol1;
      audit.low_clean_symbol = cfg.symbol2;
   }
   else if(audit.low_hunt_pattern == STC_HUNT_SYMBOL2_ONLY)
   {
      audit.low_hunted_symbol = cfg.symbol2;
      audit.low_clean_symbol = cfg.symbol1;
   }
}

bool STC_BuildReferenceHuntAudit(STC_Config &cfg,
                                 STC_TimeSnapshot &base_snap,
                                 const int check_index,
                                 const int reference_rank,
                                 STC_ReferenceHuntAudit &audit)
{
   STC_ResetReferenceHuntAudit(audit);

   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, base_snap, check_index, check_audit);

   audit.stc_day_id = check_audit.stc_day_id;
   audit.check_index = check_audit.check_index;
   audit.check_minutes = check_audit.check_minutes;
   audit.check_start_ny = check_audit.check_start_ny;
   audit.check_end_ny = check_audit.check_end_ny;
   audit.check_start_server = check_audit.check_start_server;
   audit.check_end_server = check_audit.check_end_server;
   audit.m_cycle = check_audit.m_cycle;
   audit.current_w_cycle = check_audit.w_cycle;
   audit.reference_rank = reference_rank;
   audit.detection_allowed_for_signal = check_audit.detection_allowed_for_signal;
   audit.entry_allowed_at_close = check_audit.entry_allowed_at_close;
   audit.final_check_of_m = check_audit.final_check_of_m;
   audit.check_pair_data_complete = check_audit.pair_data_complete;
   audit.rule_note = "raw_hunt_layer_input_to_level06_SMT_candidate_engine_no_confirmation_no_entry";

   if(check_index < 0)
   {
      audit.status = "invalid_check_index";
      return false;
   }

   if(!check_audit.start_inside_active_m)
   {
      audit.status = "check_start_in_gap_no_detection_no_data_extraction";
      audit.rule_note = check_audit.skip_reason;
      return true;
   }

   if(!check_audit.detection_allowed_for_signal)
   {
      audit.status = "check_not_detection_eligible_final_or_invalid";
      audit.rule_note = check_audit.skip_reason;
      return true;
   }

   if(!check_audit.pair_data_complete)
   {
      audit.status = "check_pair_data_incomplete_no_hunt_detection";
      audit.rule_note = check_audit.skip_reason;
      return true;
   }

   int ref_count = STC_HuntReferenceCount(check_audit.w_cycle);
   if(ref_count <= 0)
   {
      audit.status = "no_legal_previous_W_reference_W1_has_no_signal";
      audit.rule_note = "W1 never produces an SMT signal and no W is compared with itself";
      return true;
   }

   if(reference_rank < 0 || reference_rank >= ref_count)
   {
      audit.status = "invalid_reference_rank_for_current_W";
      return false;
   }

   STC_WCycle reference_w = STC_HuntReferenceByRank(check_audit.w_cycle, reference_rank);
   if(reference_w == STC_W_NONE)
   {
      audit.status = "reference_w_not_resolved";
      return false;
   }

   audit.reference_w_cycle = reference_w;
   audit.reference_w_serial = STC_WLevel_Serial(check_audit.m_cycle, reference_w);

   STC_WLevelAudit reference_level;
   STC_BuildWLevelAudit(cfg, base_snap, audit.reference_w_serial, reference_level);
   audit.reference_pair_data_complete = reference_level.pair_data_complete;

   if(!reference_level.pair_data_complete)
   {
      audit.status = "reference_pair_data_incomplete_no_hunt_detection";
      audit.rule_note = reference_level.status;
      return true;
   }

   audit.pair_data_complete = true;
   audit.s1_reference_high = reference_level.symbol1.high;
   audit.s1_reference_low = reference_level.symbol1.low;
   audit.s1_check_high = check_audit.symbol1.high;
   audit.s1_check_low = check_audit.symbol1.low;
   audit.s2_reference_high = reference_level.symbol2.high;
   audit.s2_reference_low = reference_level.symbol2.low;
   audit.s2_check_high = check_audit.symbol2.high;
   audit.s2_check_low = check_audit.symbol2.low;

   // Locked rule: equality is touch; no tolerance is applied.
   audit.s1_high_hunt = (audit.s1_check_high >= audit.s1_reference_high);
   audit.s1_low_hunt = (audit.s1_check_low <= audit.s1_reference_low);
   audit.s2_high_hunt = (audit.s2_check_high >= audit.s2_reference_high);
   audit.s2_low_hunt = (audit.s2_check_low <= audit.s2_reference_low);

   audit.high_hunt_pattern = STC_DeriveHuntPattern(audit.s1_high_hunt, audit.s2_high_hunt);
   audit.low_hunt_pattern = STC_DeriveHuntPattern(audit.s1_low_hunt, audit.s2_low_hunt);
   audit.high_exactly_one_hunted = (audit.high_hunt_pattern == STC_HUNT_SYMBOL1_ONLY || audit.high_hunt_pattern == STC_HUNT_SYMBOL2_ONLY);
   audit.low_exactly_one_hunted = (audit.low_hunt_pattern == STC_HUNT_SYMBOL1_ONLY || audit.low_hunt_pattern == STC_HUNT_SYMBOL2_ONLY);
   STC_FillHuntSymbolNames(cfg, audit);

   audit.status = "raw_hunt_audited_no_signal_generated";
   return true;
}

void STC_AppendNoReferenceOrSkipHuntAudit(STC_Config &cfg,
                                          STC_RuntimeState &state,
                                          STC_TimeSnapshot &snap,
                                          const int check_index)
{
   STC_ReferenceHuntAudit audit;
   STC_BuildReferenceHuntAudit(cfg, snap, check_index, -1, audit);
   STC_AppendReferenceHuntAuditCsv(cfg, state, audit);
   state.hunt_rows_audited++;
}

void STC_ProcessClosedReferenceHunts(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_hunt_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 1;
   if(closed_index > max_allowed_index)
      closed_index = max_allowed_index;

   if(state.last_hunt_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_hunt_audit_stc_day_id = snap.stc_day_id;
      int backfill = cfg.max_hunt_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_hunt_audit_check_index = closed_index - backfill;
      if(state.last_hunt_audit_check_index < -1) state.last_hunt_audit_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "HUNT_DAY_RESET", "stc_day=" + snap.stc_day_id + "; closed_index=" + IntegerToString(closed_index));
   }

   int start_index = state.last_hunt_audit_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > closed_index)
      return;

   int catchup = cfg.max_hunt_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = closed_index;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_CheckCandleAudit check_audit;
      STC_BuildCheckCandleAudit(cfg, snap, idx, check_audit);

      int ref_count = 0;
      if(check_audit.start_inside_active_m && check_audit.detection_allowed_for_signal && check_audit.pair_data_complete)
         ref_count = STC_HuntReferenceCount(check_audit.w_cycle);

      if(ref_count <= 0)
      {
         STC_AppendNoReferenceOrSkipHuntAudit(cfg, state, snap, idx);
      }
      else
      {
         for(int rank = 0; rank < ref_count; rank++)
         {
            STC_ReferenceHuntAudit audit;
            STC_BuildReferenceHuntAudit(cfg, snap, idx, rank, audit);
            STC_AppendReferenceHuntAuditCsv(cfg, state, audit);
            state.hunt_rows_audited++;
         }
      }

      state.last_hunt_audit_check_index = idx;
   }
}

#endif
