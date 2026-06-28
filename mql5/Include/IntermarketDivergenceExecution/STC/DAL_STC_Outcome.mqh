#ifndef __DAL_STC_OUTCOME_MQH__
#define __DAL_STC_OUTCOME_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Paper.mqh>

int STC_GetOutcomeMTradeCount(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.outcome_trade_count_m1;
   if(m == STC_M2) return state.outcome_trade_count_m2;
   if(m == STC_M3) return state.outcome_trade_count_m3;
   return 0;
}

STC_Direction STC_GetOutcomeMDirectionLock(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.outcome_direction_lock_m1;
   if(m == STC_M2) return state.outcome_direction_lock_m2;
   if(m == STC_M3) return state.outcome_direction_lock_m3;
   return STC_DIR_NONE;
}

void STC_SetOutcomeMTradeCount(STC_RuntimeState &state, const STC_MCycle m, const int value)
{
   if(m == STC_M1) state.outcome_trade_count_m1 = value;
   else if(m == STC_M2) state.outcome_trade_count_m2 = value;
   else if(m == STC_M3) state.outcome_trade_count_m3 = value;
}

void STC_SetOutcomeMDirectionLock(STC_RuntimeState &state, const STC_MCycle m, const STC_Direction direction)
{
   if(m == STC_M1) state.outcome_direction_lock_m1 = direction;
   else if(m == STC_M2) state.outcome_direction_lock_m2 = direction;
   else if(m == STC_M3) state.outcome_direction_lock_m3 = direction;
}

void STC_CopyOutcomeCountersIntoPaperCounters(STC_RuntimeState &dst)
{
   dst.paper_trade_count_m1 = dst.outcome_trade_count_m1;
   dst.paper_trade_count_m2 = dst.outcome_trade_count_m2;
   dst.paper_trade_count_m3 = dst.outcome_trade_count_m3;
   dst.paper_direction_lock_m1 = dst.outcome_direction_lock_m1;
   dst.paper_direction_lock_m2 = dst.outcome_direction_lock_m2;
   dst.paper_direction_lock_m3 = dst.outcome_direction_lock_m3;
}

void STC_CopyPaperCountersBackToOutcomeCounters(STC_RuntimeState &src, STC_RuntimeState &dst)
{
   dst.outcome_trade_count_m1 = src.paper_trade_count_m1;
   dst.outcome_trade_count_m2 = src.paper_trade_count_m2;
   dst.outcome_trade_count_m3 = src.paper_trade_count_m3;
   dst.outcome_direction_lock_m1 = src.paper_direction_lock_m1;
   dst.outcome_direction_lock_m2 = src.paper_direction_lock_m2;
   dst.outcome_direction_lock_m3 = src.paper_direction_lock_m3;
}

double STC_OutcomeSymbolHigh(STC_CheckCandleAudit &check, const string symbol, STC_Config &cfg)
{
   if(symbol == cfg.symbol1) return check.symbol1.high;
   if(symbol == cfg.symbol2) return check.symbol2.high;
   return 0.0;
}

double STC_OutcomeSymbolLow(STC_CheckCandleAudit &check, const string symbol, STC_Config &cfg)
{
   if(symbol == cfg.symbol1) return check.symbol1.low;
   if(symbol == cfg.symbol2) return check.symbol2.low;
   return 0.0;
}

double STC_OutcomeSymbolClose(STC_CheckCandleAudit &check, const string symbol, STC_Config &cfg)
{
   if(symbol == cfg.symbol1) return check.symbol1.close;
   if(symbol == cfg.symbol2) return check.symbol2.close;
   return 0.0;
}

bool STC_FindOutcomeCandidateForCheck(STC_Config &cfg,
                                      STC_RuntimeState &state,
                                      STC_TimeSnapshot &snap,
                                      const int check_index,
                                      STC_SMTCandidateAudit &out_candidate,
                                      string &status_text,
                                      string &rule_note)
{
   STC_ResetSMTCandidateAudit(out_candidate);
   status_text = "not_started";
   rule_note = "";

   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);
   int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);

   if(!check_audit.start_inside_active_m || !check_audit.detection_allowed_for_signal)
   {
      status_text = "check_not_detection_or_entry_eligible_no_outcome";
      rule_note = check_audit.skip_reason;
      return false;
   }
   if(!check_audit.pair_data_complete)
   {
      status_text = "check_pair_data_incomplete_no_outcome";
      rule_note = check_audit.skip_reason;
      return false;
   }
   if(legal_refs <= 0)
   {
      status_text = "no_legal_previous_W_reference_no_outcome";
      rule_note = "W1 has no signal and no W is compared with itself";
      return false;
   }

   int high_count = 0;
   int low_count = 0;
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
            if(c.trade_symbol == cfg.symbol1) STC_ConsiderBestCandidate(c, has_sell_s1, best_sell_s1);
            else STC_ConsiderBestCandidate(c, has_sell_s2, best_sell_s2);
         }
      }
      if(raw.low_exactly_one_hunted)
      {
         low_count++;
         STC_SMTCandidateAudit c;
         if(STC_BuildCandidateFromRaw(cfg, snap, check_audit, raw, STC_SIDE_LOW, c))
         {
            if(c.trade_symbol == cfg.symbol1) STC_ConsiderBestCandidate(c, has_buy_s1, best_buy_s1);
            else STC_ConsiderBestCandidate(c, has_buy_s2, best_buy_s2);
         }
      }
   }

   if(high_count > 0 && low_count > 0)
   {
      status_text = "forgotten_simultaneous_buy_and_sell_no_outcome";
      rule_note = "Locked owner rule: if buy and sell appear in the same check candle, forget the whole check candle";
      return false;
   }
   if(high_count <= 0 && low_count <= 0)
   {
      status_text = "no_exactly_one_symbol_hunt_no_outcome";
      rule_note = "No valid SMT material at this closed check candle";
      return false;
   }

   // Level 09/10 outcome simulator emits one deterministic candidate per signal check when several same-direction rows exist.
   // Preference order is Symbol1 then Symbol2 after the largest-stop selector has chosen the best reference per symbol.
   if(high_count > 0)
   {
      if(has_sell_s1) { out_candidate = best_sell_s1; return true; }
      if(has_sell_s2) { out_candidate = best_sell_s2; return true; }
   }
   else if(low_count > 0)
   {
      if(has_buy_s1) { out_candidate = best_buy_s1; return true; }
      if(has_buy_s2) { out_candidate = best_buy_s2; return true; }
   }

   status_text = "valid_raw_material_but_no_trade_candidate_after_reference_selection";
   rule_note = "All raw candidates failed positive stop-distance checks";
   return false;
}

void STC_FillOutcomeBaseFromPaper(STC_PaperEntryAudit &paper, STC_PaperOutcomeAudit &outcome)
{
   STC_ResetPaperOutcomeAudit(outcome);
   outcome.stc_day_id = paper.stc_day_id;
   outcome.signal_check_index = paper.check_index;
   outcome.entry_check_index = paper.entry_check_index;
   outcome.check_minutes = paper.check_minutes;
   outcome.signal_check_start_ny = paper.signal_check_start_ny;
   outcome.signal_check_end_ny = paper.signal_check_end_ny;
   outcome.entry_check_start_ny = paper.entry_check_start_ny;
   outcome.entry_check_end_ny = paper.entry_check_end_ny;
   outcome.m_cycle = paper.m_cycle;
   outcome.current_w_cycle = paper.current_w_cycle;
   outcome.paper_status = paper.paper_status;
   outcome.signal_id = paper.signal_id;
   outcome.paper_trade_id = paper.paper_trade_id;
   outcome.is_paper_entry = paper.is_paper_entry;
   outcome.direction = paper.direction;
   outcome.trade_symbol = paper.trade_symbol;
   outcome.hunted_symbol = paper.hunted_symbol;
   outcome.clean_symbol = paper.clean_symbol;
   outcome.entry_price = paper.entry_price;
   outcome.stop_price = paper.stop_price;
   outcome.take_profit_price = paper.take_profit_price;
   outcome.risk_distance_price = paper.risk_distance_price;
   outcome.reward_distance_price = paper.reward_distance_price;
   outcome.final_reward_r = paper.final_reward_r;
   outcome.paper_order_volume = paper.paper_order_volume;
   outcome.split_order_count = paper.split_order_count;
   outcome.risk_money = paper.risk_money;
   outcome.spread_points_for_report = paper.spread_points_for_report;
   outcome.commission_per_lot_for_report = paper.commission_per_lot_for_report;
}

void STC_FinalizeOutcomePnL(STC_Config &cfg, STC_PaperOutcomeAudit &outcome)
{
   double gross_r = 0.0;
   if(outcome.outcome_status == STC_OUTCOME_TP_HIT)
      gross_r = outcome.final_reward_r;
   else if(outcome.outcome_status == STC_OUTCOME_SL_HIT)
      gross_r = -1.0;
   else if(outcome.outcome_status == STC_OUTCOME_AMBIGUOUS_SL_TP_SAME_CHECK)
      gross_r = 0.0;
   else
      gross_r = 0.0;

   outcome.realized_r_gross = gross_r;
   outcome.gross_pnl_money = outcome.risk_money * gross_r;

   double point = SymbolInfoDouble(outcome.trade_symbol, SYMBOL_POINT);
   double tick_size = SymbolInfoDouble(outcome.trade_symbol, SYMBOL_TRADE_TICK_SIZE);
   double tick_value = SymbolInfoDouble(outcome.trade_symbol, SYMBOL_TRADE_TICK_VALUE);
   double money_per_price_unit = 0.0;
   if(tick_size > 0.0 && tick_value > 0.0)
      money_per_price_unit = tick_value / tick_size;
   else
      money_per_price_unit = cfg.contract_size;

   double spread_cost = 0.0;
   if(point > 0.0 && money_per_price_unit > 0.0)
      spread_cost = outcome.spread_points_for_report * point * outcome.paper_order_volume * money_per_price_unit;
   double commission_cost = outcome.commission_per_lot_for_report * outcome.paper_order_volume;
   if(outcome.outcome_resolved)
      outcome.estimated_cost_money = spread_cost + commission_cost;
   else
      outcome.estimated_cost_money = 0.0;

   outcome.net_pnl_money = outcome.gross_pnl_money - outcome.estimated_cost_money;
   if(outcome.risk_money > 0.0)
      outcome.realized_r_net = outcome.net_pnl_money / outcome.risk_money;
}

void STC_SimulateOutcomeFromPaper(STC_Config &cfg,
                                  STC_TimeSnapshot &snap,
                                  STC_PaperEntryAudit &paper,
                                  const int last_closed_index,
                                  STC_PaperOutcomeAudit &outcome)
{
   STC_FillOutcomeBaseFromPaper(paper, outcome);

   if(!paper.is_paper_entry || !(paper.paper_status == STC_PAPER_PLANNED || paper.paper_status == STC_PAPER_PLANNED_SPLIT_REQUIRED))
   {
      outcome.outcome_status = STC_OUTCOME_REJECTED_ENTRY_NOT_PLANNED;
      outcome.status = "paper_entry_not_planned_no_outcome_scan";
      outcome.rule_note = paper.rule_note;
      return;
   }

   int start = paper.entry_check_index;
   int end = last_closed_index;
   if(cfg.max_paper_outcome_forward_checks > 0 && end - start + 1 > cfg.max_paper_outcome_forward_checks)
      end = start + cfg.max_paper_outcome_forward_checks - 1;
   if(end < start)
   {
      outcome.outcome_status = STC_OUTCOME_OPEN_UNRESOLVED;
      outcome.status = "entry_check_not_closed_yet_open_unresolved";
      outcome.rule_note = "Outcome scan waits until closed check candles exist after the paper entry open";
      return;
   }

   for(int idx = start; idx <= end; idx++)
   {
      STC_CheckCandleAudit check;
      STC_BuildCheckCandleAudit(cfg, snap, idx, check);
      outcome.last_checked_index = idx;
      outcome.scanned_checks++;

      if(!check.pair_data_complete)
      {
         outcome.outcome_status = STC_OUTCOME_REJECTED_DATA_INCOMPLETE;
         outcome.status = "outcome_scan_stopped_on_incomplete_pair_data";
         outcome.rule_note = "Locked rule: both symbols must have complete data; paper outcome cannot be trusted past an incomplete check candle";
         return;
      }

      double h = STC_OutcomeSymbolHigh(check, paper.trade_symbol, cfg);
      double l = STC_OutcomeSymbolLow(check, paper.trade_symbol, cfg);
      double c = STC_OutcomeSymbolClose(check, paper.trade_symbol, cfg);
      outcome.last_checked_close = c;

      bool tp = false;
      bool sl = false;
      if(paper.direction == STC_DIR_BUY)
      {
         tp = (h >= paper.take_profit_price);
         sl = (l <= paper.stop_price);
         if(paper.risk_distance_price > 0.0)
            outcome.floating_r_at_last_check = (c - paper.entry_price) / paper.risk_distance_price;
      }
      else if(paper.direction == STC_DIR_SELL)
      {
         tp = (l <= paper.take_profit_price);
         sl = (h >= paper.stop_price);
         if(paper.risk_distance_price > 0.0)
            outcome.floating_r_at_last_check = (paper.entry_price - c) / paper.risk_distance_price;
      }

      if(tp || sl)
      {
         outcome.exit_check_index = idx;
         outcome.exit_check_start_ny = check.check_start_ny;
         outcome.exit_check_end_ny = check.check_end_ny;
         outcome.tp_hit = tp;
         outcome.sl_hit = sl;
         outcome.outcome_resolved = true;

         if(tp && sl)
         {
            outcome.ambiguous = true;
            outcome.outcome_status = STC_OUTCOME_AMBIGUOUS_SL_TP_SAME_CHECK;
            outcome.exit_price = 0.0;
            outcome.status = "ambiguous_sl_and_tp_hit_in_same_check_candle";
            outcome.rule_note = "Owner locked rule: if SL and TP are both touched in the same check candle, report AMBIGUOUS instead of forcing a fake order path";
         }
         else if(tp)
         {
            outcome.outcome_status = STC_OUTCOME_TP_HIT;
            outcome.exit_price = paper.take_profit_price;
            outcome.status = "paper_take_profit_hit";
            outcome.rule_note = "Paper TP hit by check-candle high/low on the traded clean symbol";
         }
         else
         {
            outcome.outcome_status = STC_OUTCOME_SL_HIT;
            outcome.exit_price = paper.stop_price;
            outcome.status = "paper_stop_loss_hit";
            outcome.rule_note = "Paper SL hit by check-candle high/low on the traded clean symbol";
         }
         STC_FinalizeOutcomePnL(cfg, outcome);
         return;
      }
   }

   outcome.outcome_status = STC_OUTCOME_OPEN_UNRESOLVED;
   outcome.status = "paper_trade_still_open_after_available_closed_checks";
   outcome.rule_note = "Level 10 simulates SL/TP before partial; hard-close accounting is deferred";
   STC_FinalizeOutcomePnL(cfg, outcome);
}

void STC_AppendOutcomeSkipRow(STC_Config &cfg,
                              STC_RuntimeState &state,
                              STC_TimeSnapshot &snap,
                              const int check_index,
                              const STC_PaperOutcomeStatus status,
                              const string status_text,
                              const string rule_note)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   STC_PaperOutcomeAudit row;
   STC_ResetPaperOutcomeAudit(row);
   row.stc_day_id = check_audit.stc_day_id;
   row.signal_check_index = check_audit.check_index;
   row.entry_check_index = check_audit.check_index + 1;
   row.check_minutes = check_audit.check_minutes;
   row.signal_check_start_ny = check_audit.check_start_ny;
   row.signal_check_end_ny = check_audit.check_end_ny;
   row.m_cycle = check_audit.m_cycle;
   row.current_w_cycle = check_audit.w_cycle;
   row.outcome_status = status;
   row.signal_id = cfg.strategy_id + "|" + row.stc_day_id + "|CHK" + IntegerToString(row.signal_check_index) + "|OUTCOME_SKIP";
   row.paper_trade_id = row.signal_id;
   row.status = status_text;
   row.rule_note = rule_note;
   STC_AppendPaperOutcomeAuditCsv(cfg, state, row);
   state.paper_outcome_rows_audited++;
}

void STC_ProcessOutcomeCandidate(STC_Config &cfg,
                                 STC_RuntimeState &state,
                                 STC_TimeSnapshot &snap,
                                 STC_SMTCandidateAudit &candidate,
                                 const int last_closed_index)
{
   STC_RuntimeState calc_state = state;
   STC_CopyOutcomeCountersIntoPaperCounters(calc_state);

   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, calc_state, candidate, signal);

   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, calc_state, snap, signal, paper);
   STC_CopyPaperCountersBackToOutcomeCounters(calc_state, state);

   STC_PaperOutcomeAudit outcome;
   STC_SimulateOutcomeFromPaper(cfg, snap, paper, last_closed_index, outcome);
   STC_AppendPaperOutcomeAuditCsv(cfg, state, outcome);
   state.paper_outcome_rows_audited++;
}

void STC_ProcessOnePaperOutcomeCheck(STC_Config &cfg,
                                     STC_RuntimeState &state,
                                     STC_TimeSnapshot &snap,
                                     const int check_index,
                                     const int last_closed_index)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);
   if(!check_audit.start_inside_active_m || !check_audit.detection_allowed_for_signal)
   {
      STC_AppendOutcomeSkipRow(cfg, state, snap, check_index, STC_OUTCOME_NO_PAPER_ENTRY,
                               "check_not_detection_or_entry_eligible_no_outcome", check_audit.skip_reason);
      return;
   }
   if(!check_audit.pair_data_complete)
   {
      STC_AppendOutcomeSkipRow(cfg, state, snap, check_index, STC_OUTCOME_REJECTED_DATA_INCOMPLETE,
                               "check_pair_data_incomplete_no_outcome", check_audit.skip_reason);
      return;
   }
   if(legal_refs <= 0)
   {
      STC_AppendOutcomeSkipRow(cfg, state, snap, check_index, STC_OUTCOME_NO_PAPER_ENTRY,
                               "no_legal_previous_W_reference_no_outcome", "W1 has no signal and no W is compared with itself");
      return;
   }

   int high_count = 0;
   int low_count = 0;
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
            if(c.trade_symbol == cfg.symbol1) STC_ConsiderBestCandidate(c, has_sell_s1, best_sell_s1);
            else STC_ConsiderBestCandidate(c, has_sell_s2, best_sell_s2);
         }
      }
      if(raw.low_exactly_one_hunted)
      {
         low_count++;
         STC_SMTCandidateAudit c;
         if(STC_BuildCandidateFromRaw(cfg, snap, check_audit, raw, STC_SIDE_LOW, c))
         {
            if(c.trade_symbol == cfg.symbol1) STC_ConsiderBestCandidate(c, has_buy_s1, best_buy_s1);
            else STC_ConsiderBestCandidate(c, has_buy_s2, best_buy_s2);
         }
      }
   }

   if(high_count > 0 && low_count > 0)
   {
      STC_AppendOutcomeSkipRow(cfg, state, snap, check_index, STC_OUTCOME_NO_PAPER_ENTRY,
                               "forgotten_simultaneous_buy_and_sell_no_outcome", "Locked owner rule: if buy and sell appear in the same check candle, forget the whole check candle");
      return;
   }
   if(high_count <= 0 && low_count <= 0)
   {
      STC_AppendOutcomeSkipRow(cfg, state, snap, check_index, STC_OUTCOME_NO_PAPER_ENTRY,
                               "no_exactly_one_symbol_hunt_no_outcome", "No valid SMT material at this closed check candle");
      return;
   }

   bool emitted = false;
   if(high_count > 0)
   {
      if(has_sell_s1) { STC_ProcessOutcomeCandidate(cfg, state, snap, best_sell_s1, last_closed_index); emitted = true; }
      if(has_sell_s2) { STC_ProcessOutcomeCandidate(cfg, state, snap, best_sell_s2, last_closed_index); emitted = true; }
   }
   else if(low_count > 0)
   {
      if(has_buy_s1) { STC_ProcessOutcomeCandidate(cfg, state, snap, best_buy_s1, last_closed_index); emitted = true; }
      if(has_buy_s2) { STC_ProcessOutcomeCandidate(cfg, state, snap, best_buy_s2, last_closed_index); emitted = true; }
   }

   if(!emitted)
   {
      STC_AppendOutcomeSkipRow(cfg, state, snap, check_index, STC_OUTCOME_NO_PAPER_ENTRY,
                               "valid_raw_material_but_no_trade_candidate_after_reference_selection", "All raw candidates failed positive stop-distance checks");
   }
}

void STC_ProcessClosedPaperOutcomes(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_paper_outcome_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   int max_signal_index_with_entry_open = closed_index - 1;
   if(max_signal_index_with_entry_open < 0)
      return;

   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 2;
   if(max_signal_index_with_entry_open > max_allowed_index)
      max_signal_index_with_entry_open = max_allowed_index;

   if(state.last_paper_outcome_stc_day_id != snap.stc_day_id)
   {
      state.last_paper_outcome_stc_day_id = snap.stc_day_id;
      state.outcome_trade_count_m1 = 0;
      state.outcome_trade_count_m2 = 0;
      state.outcome_trade_count_m3 = 0;
      state.outcome_direction_lock_m1 = STC_DIR_NONE;
      state.outcome_direction_lock_m2 = STC_DIR_NONE;
      state.outcome_direction_lock_m3 = STC_DIR_NONE;
      int backfill = cfg.max_paper_outcome_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_paper_outcome_check_index = max_signal_index_with_entry_open - backfill;
      if(state.last_paper_outcome_check_index < -1) state.last_paper_outcome_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "PAPER_OUTCOME_DAY_RESET", "stc_day=" + snap.stc_day_id + "; max_signal_index_with_entry_open=" + IntegerToString(max_signal_index_with_entry_open));
   }

   int start_index = state.last_paper_outcome_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > max_signal_index_with_entry_open)
      return;

   int catchup = cfg.max_paper_outcome_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = max_signal_index_with_entry_open;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_ProcessOnePaperOutcomeCheck(cfg, state, snap, idx, closed_index);
      state.last_paper_outcome_check_index = idx;
   }
}

#endif
