#ifndef __DAL_STC_SMT_MQH__
#define __DAL_STC_SMT_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Hunts.mqh>

void STC_FillSMTBaseFromCheck(STC_Config &cfg,
                              STC_TimeSnapshot &snap,
                              const int check_index,
                              STC_SMTCandidateAudit &audit)
{
   STC_ResetSMTCandidateAudit(audit);
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   audit.stc_day_id = check_audit.stc_day_id;
   audit.check_index = check_audit.check_index;
   audit.check_minutes = check_audit.check_minutes;
   audit.check_start_ny = check_audit.check_start_ny;
   audit.check_end_ny = check_audit.check_end_ny;
   audit.check_start_server = check_audit.check_start_server;
   audit.check_end_server = check_audit.check_end_server;
   audit.m_cycle = check_audit.m_cycle;
   audit.current_w_cycle = check_audit.w_cycle;
   audit.detection_allowed_for_signal = check_audit.detection_allowed_for_signal;
   audit.entry_allowed_at_close = check_audit.entry_allowed_at_close;
   audit.final_check_of_m = check_audit.final_check_of_m;
   audit.check_pair_data_complete = check_audit.pair_data_complete;
   audit.legal_reference_count = STC_HuntReferenceCount(check_audit.w_cycle);
}

string STC_CandidateId(STC_Config &cfg,
                       STC_SMTCandidateAudit &audit)
{
   return cfg.strategy_id + "|" + audit.stc_day_id
      + "|CHK" + IntegerToString(audit.check_index)
      + "|" + STC_MCycleText(audit.m_cycle)
      + "|" + STC_WCycleText(audit.current_w_cycle)
      + "|REF" + STC_WCycleText(audit.selected_reference_w_cycle)
      + "|" + STC_SideText(audit.smt_side)
      + "|" + STC_DirectionText(audit.direction)
      + "|" + audit.trade_symbol;
}

bool STC_BuildCandidateFromRaw(STC_Config &cfg,
                               STC_TimeSnapshot &snap,
                               STC_CheckCandleAudit &check_audit,
                               STC_ReferenceHuntAudit &raw,
                               const STC_Side side,
                               STC_SMTCandidateAudit &candidate)
{
   STC_FillSMTBaseFromCheck(cfg, snap, raw.check_index, candidate);
   candidate.smt_side = side;
   candidate.selected_reference_w_cycle = raw.reference_w_cycle;
   candidate.selected_reference_w_serial = raw.reference_w_serial;
   candidate.selected_reference_rank = raw.reference_rank;
   candidate.status = "candidate_not_selected_yet";
   candidate.rule_note = "level06_SMT_candidate_from_raw_exactly_one_hunt_used_by_level07_signal_registry; reference selection uses largest provisional stop distance on clean traded symbol at check close";

   if(side == STC_SIDE_HIGH)
   {
      if(!raw.high_exactly_one_hunted)
      {
         candidate.candidate_status = STC_CANDIDATE_REJECTED_NO_EXACTLY_ONE_HUNT;
         candidate.status = "raw_high_hunt_not_exactly_one";
         return false;
      }
      candidate.direction = STC_DIR_SELL;
      candidate.hunted_symbol = raw.high_hunted_symbol;
      candidate.clean_symbol = raw.high_clean_symbol;
      candidate.trade_symbol = raw.high_clean_symbol;
      if(candidate.trade_symbol == cfg.symbol1)
      {
         candidate.selected_reference_price = raw.s1_reference_high;
         candidate.trade_symbol_check_close = check_audit.symbol1.close;
      }
      else
      {
         candidate.selected_reference_price = raw.s2_reference_high;
         candidate.trade_symbol_check_close = check_audit.symbol2.close;
      }
      candidate.provisional_stop_distance = candidate.selected_reference_price - candidate.trade_symbol_check_close;
   }
   else if(side == STC_SIDE_LOW)
   {
      if(!raw.low_exactly_one_hunted)
      {
         candidate.candidate_status = STC_CANDIDATE_REJECTED_NO_EXACTLY_ONE_HUNT;
         candidate.status = "raw_low_hunt_not_exactly_one";
         return false;
      }
      candidate.direction = STC_DIR_BUY;
      candidate.hunted_symbol = raw.low_hunted_symbol;
      candidate.clean_symbol = raw.low_clean_symbol;
      candidate.trade_symbol = raw.low_clean_symbol;
      if(candidate.trade_symbol == cfg.symbol1)
      {
         candidate.selected_reference_price = raw.s1_reference_low;
         candidate.trade_symbol_check_close = check_audit.symbol1.close;
      }
      else
      {
         candidate.selected_reference_price = raw.s2_reference_low;
         candidate.trade_symbol_check_close = check_audit.symbol2.close;
      }
      candidate.provisional_stop_distance = candidate.trade_symbol_check_close - candidate.selected_reference_price;
   }
   else
   {
      candidate.candidate_status = STC_CANDIDATE_NONE;
      candidate.status = "side_none_no_candidate";
      return false;
   }

   if(candidate.provisional_stop_distance <= 0.0)
   {
      candidate.candidate_status = STC_CANDIDATE_REJECTED_INVALID_STOP_DISTANCE;
      candidate.status = "invalid_non_positive_provisional_stop_distance";
      candidate.is_trade_candidate = false;
      return false;
   }

   candidate.is_trade_candidate = true;
   candidate.candidate_status = STC_CANDIDATE_VALID_AUDIT_ONLY;
   candidate.status = "valid_SMT_candidate_audit_only_no_confirmation_no_entry";
   candidate.candidate_id = STC_CandidateId(cfg, candidate);
   return true;
}

void STC_CopySMTCandidate(STC_SMTCandidateAudit &src, STC_SMTCandidateAudit &dst)
{
   dst = src;
}

void STC_AppendSMTSkipRow(STC_Config &cfg,
                          STC_RuntimeState &state,
                          STC_TimeSnapshot &snap,
                          const int check_index,
                          const STC_CandidateStatus status,
                          const string status_text,
                          const string rule_note,
                          const int legal_refs,
                          const int high_count,
                          const int low_count)
{
   STC_SMTCandidateAudit row;
   STC_FillSMTBaseFromCheck(cfg, snap, check_index, row);
   row.candidate_status = status;
   row.status = status_text;
   row.rule_note = rule_note;
   row.legal_reference_count = legal_refs;
   row.high_raw_candidate_count = high_count;
   row.low_raw_candidate_count = low_count;
   row.same_direction_candidate_count = 0;
   row.simultaneous_buy_sell_forget = (status == STC_CANDIDATE_FORGOTTEN_SIMULTANEOUS_BUY_SELL);
   STC_AppendSMTCandidateAuditCsv(cfg, state, row);
   state.smt_candidate_rows_audited++;
}

void STC_ConsiderBestCandidate(STC_SMTCandidateAudit &candidate,
                               bool &has_best,
                               STC_SMTCandidateAudit &best)
{
   if(!candidate.is_trade_candidate)
      return;
   if(!has_best || candidate.provisional_stop_distance > best.provisional_stop_distance)
   {
      STC_CopySMTCandidate(candidate, best);
      has_best = true;
   }
}

void STC_ProcessOneSMTCheck(STC_Config &cfg,
                            STC_RuntimeState &state,
                            STC_TimeSnapshot &snap,
                            const int check_index)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);
   if(!check_audit.start_inside_active_m || !check_audit.detection_allowed_for_signal)
   {
      STC_AppendSMTSkipRow(cfg, state, snap, check_index, STC_CANDIDATE_REJECTED_NOT_DETECTION_ELIGIBLE,
                           "check_not_detection_eligible_no_SMT_candidate", check_audit.skip_reason, legal_refs, 0, 0);
      return;
   }

   if(!check_audit.pair_data_complete)
   {
      STC_AppendSMTSkipRow(cfg, state, snap, check_index, STC_CANDIDATE_REJECTED_INCOMPLETE_DATA,
                           "check_pair_data_incomplete_no_SMT_candidate", check_audit.skip_reason, legal_refs, 0, 0);
      return;
   }

   if(legal_refs <= 0)
   {
      STC_AppendSMTSkipRow(cfg, state, snap, check_index, STC_CANDIDATE_REJECTED_NO_REFERENCE,
                           "no_legal_previous_W_reference_no_SMT_candidate", "W1 has no signal and no W is compared with itself", legal_refs, 0, 0);
      return;
   }

   int high_count = 0;
   int low_count = 0;
   int invalid_stop_count = 0;

   bool has_sell_s1 = false;
   bool has_sell_s2 = false;
   bool has_buy_s1 = false;
   bool has_buy_s2 = false;
   STC_SMTCandidateAudit best_sell_s1;
   STC_SMTCandidateAudit best_sell_s2;
   STC_SMTCandidateAudit best_buy_s1;
   STC_SMTCandidateAudit best_buy_s2;
   STC_ResetSMTCandidateAudit(best_sell_s1);
   STC_ResetSMTCandidateAudit(best_sell_s2);
   STC_ResetSMTCandidateAudit(best_buy_s1);
   STC_ResetSMTCandidateAudit(best_buy_s2);

   for(int rank = 0; rank < legal_refs; rank++)
   {
      STC_ReferenceHuntAudit raw;
      STC_BuildReferenceHuntAudit(cfg, snap, check_index, rank, raw);
      if(raw.high_exactly_one_hunted)
      {
         high_count++;
         STC_SMTCandidateAudit c;
         if(STC_BuildCandidateFromRaw(cfg, snap, check_audit, raw, STC_SIDE_HIGH, c))
         {
            if(c.trade_symbol == cfg.symbol1)
               STC_ConsiderBestCandidate(c, has_sell_s1, best_sell_s1);
            else
               STC_ConsiderBestCandidate(c, has_sell_s2, best_sell_s2);
         }
         else if(c.candidate_status == STC_CANDIDATE_REJECTED_INVALID_STOP_DISTANCE)
            invalid_stop_count++;
      }
      if(raw.low_exactly_one_hunted)
      {
         low_count++;
         STC_SMTCandidateAudit c;
         if(STC_BuildCandidateFromRaw(cfg, snap, check_audit, raw, STC_SIDE_LOW, c))
         {
            if(c.trade_symbol == cfg.symbol1)
               STC_ConsiderBestCandidate(c, has_buy_s1, best_buy_s1);
            else
               STC_ConsiderBestCandidate(c, has_buy_s2, best_buy_s2);
         }
         else if(c.candidate_status == STC_CANDIDATE_REJECTED_INVALID_STOP_DISTANCE)
            invalid_stop_count++;
      }
   }

   if(high_count > 0 && low_count > 0)
   {
      STC_AppendSMTSkipRow(cfg, state, snap, check_index, STC_CANDIDATE_FORGOTTEN_SIMULTANEOUS_BUY_SELL,
                           "forgotten_simultaneous_buy_and_sell_in_same_check_candle",
                           "locked owner rule: if buy-side and sell-side SMT exist in the same check candle, forget the whole check candle and do not carry candidates forward",
                           legal_refs, high_count, low_count);
      return;
   }

   if(high_count <= 0 && low_count <= 0)
   {
      STC_AppendSMTSkipRow(cfg, state, snap, check_index, STC_CANDIDATE_REJECTED_NO_EXACTLY_ONE_HUNT,
                           "no_exactly_one_symbol_hunt_no_SMT_candidate",
                           "raw hunt audit produced no legal exactly-one-symbol high or low SMT material",
                           legal_refs, high_count, low_count);
      return;
   }

   int selected_count = 0;
   if(high_count > 0)
   {
      if(has_sell_s1) selected_count++;
      if(has_sell_s2) selected_count++;
      if(has_sell_s1)
      {
         best_sell_s1.high_raw_candidate_count = high_count;
         best_sell_s1.low_raw_candidate_count = low_count;
         best_sell_s1.same_direction_candidate_count = selected_count;
         STC_AppendSMTCandidateAuditCsv(cfg, state, best_sell_s1);
         state.smt_candidate_rows_audited++;
      }
      if(has_sell_s2)
      {
         best_sell_s2.high_raw_candidate_count = high_count;
         best_sell_s2.low_raw_candidate_count = low_count;
         best_sell_s2.same_direction_candidate_count = selected_count;
         STC_AppendSMTCandidateAuditCsv(cfg, state, best_sell_s2);
         state.smt_candidate_rows_audited++;
      }
   }
   else if(low_count > 0)
   {
      if(has_buy_s1) selected_count++;
      if(has_buy_s2) selected_count++;
      if(has_buy_s1)
      {
         best_buy_s1.high_raw_candidate_count = high_count;
         best_buy_s1.low_raw_candidate_count = low_count;
         best_buy_s1.same_direction_candidate_count = selected_count;
         STC_AppendSMTCandidateAuditCsv(cfg, state, best_buy_s1);
         state.smt_candidate_rows_audited++;
      }
      if(has_buy_s2)
      {
         best_buy_s2.high_raw_candidate_count = high_count;
         best_buy_s2.low_raw_candidate_count = low_count;
         best_buy_s2.same_direction_candidate_count = selected_count;
         STC_AppendSMTCandidateAuditCsv(cfg, state, best_buy_s2);
         state.smt_candidate_rows_audited++;
      }
   }

   if(selected_count <= 0)
   {
      STC_AppendSMTSkipRow(cfg, state, snap, check_index, STC_CANDIDATE_REJECTED_INVALID_STOP_DISTANCE,
                           "all_raw_candidates_rejected_by_invalid_stop_distance",
                           "raw candidates existed but no candidate had a positive provisional stop distance; invalidStopCount=" + IntegerToString(invalid_stop_count),
                           legal_refs, high_count, low_count);
   }
}

void STC_ProcessClosedSMTCandidates(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_smt_candidate_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 1;
   if(closed_index > max_allowed_index)
      closed_index = max_allowed_index;

   if(state.last_smt_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_smt_audit_stc_day_id = snap.stc_day_id;
      int backfill = cfg.max_smt_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_smt_audit_check_index = closed_index - backfill;
      if(state.last_smt_audit_check_index < -1) state.last_smt_audit_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "SMT_DAY_RESET", "stc_day=" + snap.stc_day_id + "; closed_index=" + IntegerToString(closed_index));
   }

   int start_index = state.last_smt_audit_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > closed_index)
      return;

   int catchup = cfg.max_smt_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = closed_index;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_ProcessOneSMTCheck(cfg, state, snap, idx);
      state.last_smt_audit_check_index = idx;
   }
}

#endif
