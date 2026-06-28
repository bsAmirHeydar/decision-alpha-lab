#ifndef __DAL_STC_SIGNALS_MQH__
#define __DAL_STC_SIGNALS_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_SMT.mqh>

string STC_SignalId(STC_Config &cfg, STC_SMTCandidateAudit &candidate)
{
   return cfg.strategy_id + "|" + candidate.stc_day_id
      + "|CHK" + IntegerToString(candidate.check_index)
      + "|" + STC_MCycleText(candidate.m_cycle)
      + "|" + STC_WCycleText(candidate.current_w_cycle)
      + "|REF" + STC_WCycleText(candidate.selected_reference_w_cycle)
      + "|" + STC_SideText(candidate.smt_side)
      + "|" + STC_DirectionText(candidate.direction)
      + "|" + candidate.trade_symbol
      + "|SIG";
}

void STC_CopyCandidateIntoSignal(STC_Config &cfg,
                                 STC_RuntimeState &state,
                                 STC_SMTCandidateAudit &candidate,
                                 STC_SignalAudit &signal)
{
   STC_ResetSignalAudit(signal);
   signal.stc_day_id = candidate.stc_day_id;
   signal.check_index = candidate.check_index;
   signal.check_minutes = candidate.check_minutes;
   signal.check_start_ny = candidate.check_start_ny;
   signal.check_end_ny = candidate.check_end_ny;
   signal.check_start_server = candidate.check_start_server;
   signal.check_end_server = candidate.check_end_server;
   signal.m_cycle = candidate.m_cycle;
   signal.current_w_cycle = candidate.current_w_cycle;
   signal.detection_allowed_for_signal = candidate.detection_allowed_for_signal;
   signal.entry_allowed_at_close = candidate.entry_allowed_at_close;
   signal.final_check_of_m = candidate.final_check_of_m;
   signal.check_pair_data_complete = candidate.check_pair_data_complete;
   signal.source_candidate_id = candidate.candidate_id;
   signal.signal_id = STC_SignalId(cfg, candidate);
   signal.entry_stc_enabled_at_confirmation = cfg.entry_stc_enabled;
   signal.entry_missed_or_late = (candidate.check_end_server < state.started_server_time);
   signal.order_attempted = false;
   signal.trade_counter_incremented = false;
   signal.smt_side = candidate.smt_side;
   signal.direction = candidate.direction;
   signal.hunted_symbol = candidate.hunted_symbol;
   signal.clean_symbol = candidate.clean_symbol;
   signal.trade_symbol = candidate.trade_symbol;
   signal.selected_reference_w_cycle = candidate.selected_reference_w_cycle;
   signal.selected_reference_w_serial = candidate.selected_reference_w_serial;
   signal.selected_reference_rank = candidate.selected_reference_rank;
   signal.selected_reference_price = candidate.selected_reference_price;
   signal.trade_symbol_check_close = candidate.trade_symbol_check_close;
   signal.provisional_stop_distance = candidate.provisional_stop_distance;
   signal.legal_reference_count = candidate.legal_reference_count;
   signal.high_raw_candidate_count = candidate.high_raw_candidate_count;
   signal.low_raw_candidate_count = candidate.low_raw_candidate_count;
   signal.selected_same_direction_count = candidate.same_direction_candidate_count;
   signal.simultaneous_buy_sell_forget = candidate.simultaneous_buy_sell_forget;
}

void STC_FinalizeSignalFromCandidate(STC_Config &cfg,
                                     STC_RuntimeState &state,
                                     STC_SMTCandidateAudit &candidate,
                                     STC_SignalAudit &signal)
{
   STC_CopyCandidateIntoSignal(cfg, state, candidate, signal);

   if(!candidate.is_trade_candidate)
   {
      signal.signal_status = STC_SIGNAL_REJECTED_NO_CANDIDATE;
      signal.is_confirmed_signal = false;
      signal.signal_consumed = true;
      signal.status = "candidate_not_trade_eligible_signal_rejected_consumed";
      signal.rule_note = "level07 registry consumes rejected candidate rows to prevent delayed entry";
      return;
   }

   if(!candidate.check_pair_data_complete)
   {
      signal.signal_status = STC_SIGNAL_REJECTED_INCOMPLETE_DATA;
      signal.is_confirmed_signal = false;
      signal.signal_consumed = true;
      signal.status = "candidate_pair_data_incomplete_signal_rejected_consumed";
      signal.rule_note = "both symbols must have complete data at confirmation";
      return;
   }

   if(candidate.final_check_of_m || !candidate.entry_allowed_at_close)
   {
      signal.signal_status = STC_SIGNAL_REJECTED_FINAL_CHECK_NO_ENTRY;
      signal.is_confirmed_signal = false;
      signal.signal_consumed = true;
      signal.status = "final_or_non_entry_check_signal_rejected_consumed";
      signal.rule_note = "locked owner rule: the final check candle of each M is audited but never entered";
      return;
   }

   if(candidate.provisional_stop_distance <= 0.0)
   {
      signal.signal_status = STC_SIGNAL_REJECTED_INVALID_STOP_DISTANCE;
      signal.is_confirmed_signal = false;
      signal.signal_consumed = true;
      signal.status = "invalid_stop_distance_signal_rejected_consumed";
      signal.rule_note = "selected reference must produce positive stop distance on clean traded symbol";
      return;
   }

   signal.is_confirmed_signal = true;
   signal.signal_consumed = true;
   signal.order_attempted = false;
   signal.trade_counter_incremented = false;

   if(!cfg.entry_stc_enabled)
   {
      signal.signal_status = STC_SIGNAL_CONFIRMED_ENTRY_OFF_CONSUMED;
      signal.status = "confirmed_signal_entry_off_audit_only_consumed_no_late_entry";
      signal.rule_note = "locked owner rule: Entry STC OFF records the signal for audit only and never enters later";
      return;
   }

   signal.signal_status = STC_SIGNAL_CONFIRMED_AUDIT_ONLY;
   signal.status = "confirmed_signal_registry_audit_only_no_paper_trade_no_order";
   signal.rule_note = "level07 confirms and consumes the signal at check close; paper execution and real orders are deferred to later levels; no late entry is allowed";
   if(signal.entry_missed_or_late)
      signal.rule_note = signal.rule_note + "; check close happened before this EA instance started, so this is audit-only and cannot be entered late";
}

void STC_AppendSignalSkipRow(STC_Config &cfg,
                             STC_RuntimeState &state,
                             STC_TimeSnapshot &snap,
                             const int check_index,
                             const STC_SignalStatus signal_status,
                             const string status_text,
                             const string rule_note,
                             const int legal_refs,
                             const int high_count,
                             const int low_count,
                             const bool simultaneous_forget)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   STC_SignalAudit row;
   STC_ResetSignalAudit(row);
   row.stc_day_id = check_audit.stc_day_id;
   row.check_index = check_audit.check_index;
   row.check_minutes = check_audit.check_minutes;
   row.check_start_ny = check_audit.check_start_ny;
   row.check_end_ny = check_audit.check_end_ny;
   row.check_start_server = check_audit.check_start_server;
   row.check_end_server = check_audit.check_end_server;
   row.m_cycle = check_audit.m_cycle;
   row.current_w_cycle = check_audit.w_cycle;
   row.detection_allowed_for_signal = check_audit.detection_allowed_for_signal;
   row.entry_allowed_at_close = check_audit.entry_allowed_at_close;
   row.final_check_of_m = check_audit.final_check_of_m;
   row.check_pair_data_complete = check_audit.pair_data_complete;
   row.signal_status = signal_status;
   row.signal_id = cfg.strategy_id + "|" + row.stc_day_id + "|CHK" + IntegerToString(row.check_index) + "|SKIP";
   row.is_confirmed_signal = false;
   row.signal_consumed = true;
   row.entry_stc_enabled_at_confirmation = cfg.entry_stc_enabled;
   row.entry_missed_or_late = (check_audit.check_end_server < state.started_server_time);
   row.order_attempted = false;
   row.trade_counter_incremented = false;
   row.legal_reference_count = legal_refs;
   row.high_raw_candidate_count = high_count;
   row.low_raw_candidate_count = low_count;
   row.selected_same_direction_count = 0;
   row.simultaneous_buy_sell_forget = simultaneous_forget;
   row.status = status_text;
   row.rule_note = rule_note;
   STC_AppendSignalRegistryCsv(cfg, state, row);
   state.signal_rows_audited++;
}

void STC_RegisterCandidateSignal(STC_Config &cfg,
                                 STC_RuntimeState &state,
                                 STC_SMTCandidateAudit &candidate)
{
   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, state, candidate, signal);
   STC_AppendSignalRegistryCsv(cfg, state, signal);
   state.signal_rows_audited++;
}

void STC_ProcessOneSignalRegistryCheck(STC_Config &cfg,
                                       STC_RuntimeState &state,
                                       STC_TimeSnapshot &snap,
                                       const int check_index)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);
   if(!check_audit.start_inside_active_m || !check_audit.detection_allowed_for_signal)
   {
      STC_AppendSignalSkipRow(cfg, state, snap, check_index, STC_SIGNAL_REJECTED_NOT_ENTRY_ELIGIBLE,
                              "check_not_detection_or_entry_eligible_no_signal", check_audit.skip_reason, legal_refs, 0, 0, false);
      return;
   }

   if(!check_audit.pair_data_complete)
   {
      STC_AppendSignalSkipRow(cfg, state, snap, check_index, STC_SIGNAL_REJECTED_INCOMPLETE_DATA,
                              "check_pair_data_incomplete_no_signal", check_audit.skip_reason, legal_refs, 0, 0, false);
      return;
   }

   if(legal_refs <= 0)
   {
      STC_AppendSignalSkipRow(cfg, state, snap, check_index, STC_SIGNAL_REJECTED_NO_CANDIDATE,
                              "no_legal_previous_W_reference_no_signal", "W1 has no signal and no W is compared with itself", legal_refs, 0, 0, false);
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
      STC_AppendSignalSkipRow(cfg, state, snap, check_index, STC_SIGNAL_FORGOTTEN_SIMULTANEOUS_BUY_SELL,
                              "forgotten_simultaneous_buy_and_sell_in_same_check_candle",
                              "locked owner rule: if buy and sell appear in the same check candle, forget the whole check candle and never carry it forward",
                              legal_refs, high_count, low_count, true);
      return;
   }

   if(high_count <= 0 && low_count <= 0)
   {
      STC_AppendSignalSkipRow(cfg, state, snap, check_index, STC_SIGNAL_REJECTED_NO_CANDIDATE,
                              "no_exactly_one_symbol_hunt_no_signal",
                              "no valid SMT material at this closed check candle",
                              legal_refs, high_count, low_count, false);
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
         STC_RegisterCandidateSignal(cfg, state, best_sell_s1);
      }
      if(has_sell_s2)
      {
         best_sell_s2.high_raw_candidate_count = high_count;
         best_sell_s2.low_raw_candidate_count = low_count;
         best_sell_s2.same_direction_candidate_count = selected_count;
         STC_RegisterCandidateSignal(cfg, state, best_sell_s2);
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
         STC_RegisterCandidateSignal(cfg, state, best_buy_s1);
      }
      if(has_buy_s2)
      {
         best_buy_s2.high_raw_candidate_count = high_count;
         best_buy_s2.low_raw_candidate_count = low_count;
         best_buy_s2.same_direction_candidate_count = selected_count;
         STC_RegisterCandidateSignal(cfg, state, best_buy_s2);
      }
   }

   if(selected_count <= 0)
   {
      STC_AppendSignalSkipRow(cfg, state, snap, check_index, STC_SIGNAL_REJECTED_INVALID_STOP_DISTANCE,
                              "all_candidates_rejected_by_invalid_stop_distance",
                              "raw SMT candidates existed but no selected candidate produced a positive stop distance; invalidStopCount=" + IntegerToString(invalid_stop_count),
                              legal_refs, high_count, low_count, false);
   }
}

void STC_ProcessClosedSignalRegistry(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_signal_registry_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 1;
   if(closed_index > max_allowed_index)
      closed_index = max_allowed_index;

   if(state.last_signal_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_signal_audit_stc_day_id = snap.stc_day_id;
      int backfill = cfg.max_signal_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_signal_audit_check_index = closed_index - backfill;
      if(state.last_signal_audit_check_index < -1) state.last_signal_audit_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "SIGNAL_DAY_RESET", "stc_day=" + snap.stc_day_id + "; closed_index=" + IntegerToString(closed_index));
   }

   int start_index = state.last_signal_audit_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > closed_index)
      return;

   int catchup = cfg.max_signal_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = closed_index;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_ProcessOneSignalRegistryCheck(cfg, state, snap, idx);
      state.last_signal_audit_check_index = idx;
   }
}

#endif
