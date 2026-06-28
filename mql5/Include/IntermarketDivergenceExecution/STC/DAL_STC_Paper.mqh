#ifndef __DAL_STC_PAPER_MQH__
#define __DAL_STC_PAPER_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Signals.mqh>

int STC_GetPaperMTradeCount(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.paper_trade_count_m1;
   if(m == STC_M2) return state.paper_trade_count_m2;
   if(m == STC_M3) return state.paper_trade_count_m3;
   return 0;
}

STC_Direction STC_GetPaperMDirectionLock(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.paper_direction_lock_m1;
   if(m == STC_M2) return state.paper_direction_lock_m2;
   if(m == STC_M3) return state.paper_direction_lock_m3;
   return STC_DIR_NONE;
}

void STC_SetPaperMTradeCount(STC_RuntimeState &state, const STC_MCycle m, const int value)
{
   if(m == STC_M1) state.paper_trade_count_m1 = value;
   else if(m == STC_M2) state.paper_trade_count_m2 = value;
   else if(m == STC_M3) state.paper_trade_count_m3 = value;
}

void STC_SetPaperMDirectionLock(STC_RuntimeState &state, const STC_MCycle m, const STC_Direction direction)
{
   if(m == STC_M1) state.paper_direction_lock_m1 = direction;
   else if(m == STC_M2) state.paper_direction_lock_m2 = direction;
   else if(m == STC_M3) state.paper_direction_lock_m3 = direction;
}

string STC_PaperTradeId(STC_Config &cfg, STC_SignalAudit &signal)
{
   return cfg.strategy_id + "|" + signal.stc_day_id
      + "|CHK" + IntegerToString(signal.check_index)
      + "|ENTRYCHK" + IntegerToString(signal.check_index + 1)
      + "|" + STC_DirectionText(signal.direction)
      + "|" + signal.trade_symbol
      + "|PAPER";
}

double STC_SymbolOpenForEntry(STC_CheckCandleAudit &entry_check, const string symbol, STC_Config &cfg)
{
   if(symbol == cfg.symbol1) return entry_check.symbol1.open;
   if(symbol == cfg.symbol2) return entry_check.symbol2.open;
   return 0.0;
}

int STC_SymbolSpreadForEntry(STC_CheckCandleAudit &entry_check, const string symbol, STC_Config &cfg)
{
   if(symbol == cfg.symbol1) return entry_check.symbol1.spread_max;
   if(symbol == cfg.symbol2) return entry_check.symbol2.spread_max;
   return 0;
}

void STC_LoadSymbolTradeSpecs(const string symbol,
                              double &tick_size,
                              double &tick_value,
                              double &vol_min,
                              double &vol_max,
                              double &vol_step)
{
   tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   tick_value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);
   vol_min = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   vol_max = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   vol_step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
   if(vol_min <= 0.0) vol_min = 0.01;
   if(vol_max <= 0.0) vol_max = 1000000000.0;
   if(vol_step <= 0.0) vol_step = 0.01;
}

double STC_NormalizeVolumeDown(const double volume, const double step)
{
   if(step <= 0.0) return volume;
   if(volume <= 0.0) return 0.0;
   double units = MathFloor(volume / step);
   return units * step;
}

void STC_FillPaperFromSignal(STC_Config &cfg,
                             STC_RuntimeState &state,
                             STC_TimeSnapshot &snap,
                             STC_SignalAudit &signal,
                             STC_PaperEntryAudit &paper)
{
   STC_ResetPaperEntryAudit(paper);
   paper.stc_day_id = signal.stc_day_id;
   paper.check_index = signal.check_index;
   paper.entry_check_index = signal.check_index + 1;
   paper.check_minutes = signal.check_minutes;
   paper.signal_check_start_ny = signal.check_start_ny;
   paper.signal_check_end_ny = signal.check_end_ny;
   paper.m_cycle = signal.m_cycle;
   paper.current_w_cycle = signal.current_w_cycle;
   paper.signal_id = signal.signal_id;
   paper.paper_trade_id = STC_PaperTradeId(cfg, signal);
   paper.signal_confirmed = signal.is_confirmed_signal;
   paper.entry_stc_enabled_at_confirmation = signal.entry_stc_enabled_at_confirmation;
   paper.entry_missed_or_late = signal.entry_missed_or_late;
   paper.direction = signal.direction;
   paper.trade_symbol = signal.trade_symbol;
   paper.hunted_symbol = signal.hunted_symbol;
   paper.clean_symbol = signal.clean_symbol;
   paper.selected_reference_w_cycle = signal.selected_reference_w_cycle;
   paper.selected_reference_w_serial = signal.selected_reference_w_serial;
   paper.selected_reference_price = signal.selected_reference_price;
   paper.final_reward_r = cfg.final_reward_r;
   paper.equity_snapshot = AccountInfoDouble(ACCOUNT_EQUITY);
   paper.risk_percent = cfg.risk_percent;
   paper.risk_money = paper.equity_snapshot * cfg.risk_percent / 100.0;
   paper.contract_size_used = cfg.contract_size;
   paper.m_trade_count_before = STC_GetPaperMTradeCount(state, signal.m_cycle);
   paper.m_trade_count_after = paper.m_trade_count_before;
   paper.m_direction_lock_before = STC_GetPaperMDirectionLock(state, signal.m_cycle);
   paper.m_direction_lock_after = paper.m_direction_lock_before;
   paper.status = "initialized_from_signal";

   if(!signal.is_confirmed_signal)
   {
      paper.paper_status = STC_PAPER_REJECTED_SIGNAL_NOT_CONFIRMED;
      paper.status = "signal_not_confirmed_no_paper_entry";
      paper.rule_note = "Level 08 only plans paper entries from confirmed consumed signals";
      return;
   }
   if(!signal.entry_stc_enabled_at_confirmation)
   {
      paper.paper_status = STC_PAPER_REJECTED_ENTRY_OFF;
      paper.status = "entry_stc_off_audit_only_no_paper_entry";
      paper.rule_note = "Locked owner rule: Entry STC OFF never creates delayed entry";
      return;
   }
   if(signal.entry_missed_or_late)
   {
      paper.paper_status = STC_PAPER_REJECTED_MISSED_OR_LATE;
      paper.status = "entry_moment_missed_no_late_paper_entry";
      paper.rule_note = "Locked owner rule: if the EA was offline at the exact entry moment, no later entry is allowed";
      return;
   }
   if(paper.m_trade_count_before >= 3)
   {
      paper.paper_status = STC_PAPER_REJECTED_MAX_TRADES_PER_M;
      paper.status = "max_three_trades_per_M_reached_no_paper_entry";
      paper.rule_note = "Locked owner rule: each M allows at most three trades across both symbols";
      return;
   }
   if(!cfg.hedging_enabled && paper.m_direction_lock_before != STC_DIR_NONE && paper.m_direction_lock_before != signal.direction)
   {
      paper.paper_status = STC_PAPER_REJECTED_DIRECTION_LOCK;
      paper.status = "hedging_off_direction_lock_rejected_no_paper_entry";
      paper.rule_note = "Hedging OFF locks direction only within the current M; opposite M signals are rejected";
      return;
   }

   STC_CheckCandleAudit entry_check;
   bool built = STC_BuildCheckCandleAudit(cfg, snap, paper.entry_check_index, entry_check);
   paper.entry_check_start_ny = entry_check.check_start_ny;
   paper.entry_check_end_ny = entry_check.check_end_ny;
   paper.entry_check_start_server = entry_check.check_start_server;
   paper.entry_check_end_server = entry_check.check_end_server;
   paper.entry_check_pair_data_complete = entry_check.pair_data_complete;
   if(!built)
   {
      paper.paper_status = STC_PAPER_REJECTED_NEXT_CHECK_UNAVAILABLE;
      paper.status = "next_check_candle_unavailable_no_paper_entry";
      paper.rule_note = "Paper entry uses the open of the next check candle; that check was not buildable";
      return;
   }
   if(!entry_check.pair_data_complete)
   {
      paper.paper_status = STC_PAPER_REJECTED_NEXT_CHECK_INCOMPLETE;
      paper.status = "next_check_pair_data_incomplete_no_paper_entry";
      paper.rule_note = "Both symbols must have complete data at the paper entry check";
      return;
   }

   paper.entry_price = STC_SymbolOpenForEntry(entry_check, signal.trade_symbol, cfg);
   paper.stop_price = signal.selected_reference_price;
   if(signal.direction == STC_DIR_BUY)
      paper.risk_distance_price = paper.entry_price - paper.stop_price;
   else if(signal.direction == STC_DIR_SELL)
      paper.risk_distance_price = paper.stop_price - paper.entry_price;

   if(paper.entry_price <= 0.0 || paper.stop_price <= 0.0 || paper.risk_distance_price <= 0.0)
   {
      paper.paper_status = STC_PAPER_REJECTED_INVALID_RISK_DISTANCE;
      paper.status = "invalid_entry_or_stop_distance_no_paper_entry";
      paper.rule_note = "The selected reference must remain on the protective side of the next-check open";
      return;
   }

   paper.reward_distance_price = paper.risk_distance_price * cfg.final_reward_r;
   if(signal.direction == STC_DIR_BUY)
      paper.take_profit_price = paper.entry_price + paper.reward_distance_price;
   else if(signal.direction == STC_DIR_SELL)
      paper.take_profit_price = paper.entry_price - paper.reward_distance_price;

   STC_LoadSymbolTradeSpecs(signal.trade_symbol, paper.tick_size, paper.tick_value, paper.broker_min_volume, paper.broker_max_volume, paper.broker_volume_step);
   double money_per_price_unit = 0.0;
   if(paper.tick_size > 0.0 && paper.tick_value > 0.0)
   {
      money_per_price_unit = paper.tick_value / paper.tick_size;
      paper.used_tick_value = true;
   }
   else
   {
      money_per_price_unit = cfg.contract_size;
      paper.used_tick_value = false;
   }

   if(money_per_price_unit <= 0.0)
   {
      paper.paper_status = STC_PAPER_REJECTED_INVALID_RISK_DISTANCE;
      paper.status = "invalid_money_per_price_unit_no_paper_entry";
      paper.rule_note = "Neither broker tick value nor Contract Size produced a valid sizing denominator";
      return;
   }

   paper.theoretical_volume = paper.risk_money / (paper.risk_distance_price * money_per_price_unit);
   paper.paper_order_volume = STC_NormalizeVolumeDown(paper.theoretical_volume, paper.broker_volume_step);
   paper.split_order_count = 1;
   paper.volume_status = "within_broker_limits";

   if(paper.paper_order_volume < paper.broker_min_volume)
   {
      paper.paper_status = STC_PAPER_REJECTED_BROKER_MIN_VOLUME;
      paper.status = "theoretical_volume_below_broker_min_no_paper_entry";
      paper.rule_note = "Level 08 will not round up to broker minimum because that may exceed the requested risk";
      return;
   }

   if(paper.theoretical_volume > paper.broker_max_volume && paper.broker_max_volume > 0.0)
   {
      paper.paper_status = STC_PAPER_PLANNED_SPLIT_REQUIRED;
      paper.split_order_count = (int)MathCeil(paper.theoretical_volume / paper.broker_max_volume);
      paper.paper_order_volume = paper.broker_max_volume;
      paper.volume_status = "theoretical_volume_above_broker_max_split_required";
      paper.rule_note = "Locked owner rule: no internal volume cap; broker max is respected by split-order planning in later auto-trade levels";
   }
   else
   {
      paper.paper_status = STC_PAPER_PLANNED;
      paper.rule_note = "Level 08 no-order paper entry plan created; outcome, partial, hard close, drawing, and real orders are deferred";
   }

   long broker_spread = SymbolInfoInteger(signal.trade_symbol, SYMBOL_SPREAD);
   int data_spread = STC_SymbolSpreadForEntry(entry_check, signal.trade_symbol, cfg);
   if(cfg.use_broker_costs_for_reporting && data_spread > 0)
      paper.spread_points_for_report = (double)data_spread;
   else if(cfg.use_broker_costs_for_reporting && broker_spread > 0)
      paper.spread_points_for_report = (double)broker_spread;
   else
      paper.spread_points_for_report = cfg.fallback_spread_points;
   paper.commission_per_lot_for_report = cfg.fallback_commission_per_lot;

   paper.is_paper_entry = true;
   paper.trade_counter_incremented = true;
   paper.m_trade_count_after = paper.m_trade_count_before + 1;
   paper.m_direction_lock_after = paper.m_direction_lock_before;
   if(!cfg.hedging_enabled && paper.m_direction_lock_after == STC_DIR_NONE)
      paper.m_direction_lock_after = signal.direction;
   STC_SetPaperMTradeCount(state, signal.m_cycle, paper.m_trade_count_after);
   STC_SetPaperMDirectionLock(state, signal.m_cycle, paper.m_direction_lock_after);
   paper.status = "paper_entry_planned_no_order";
}

void STC_RegisterPaperFromCandidate(STC_Config &cfg,
                                    STC_RuntimeState &state,
                                    STC_TimeSnapshot &snap,
                                    STC_SMTCandidateAudit &candidate)
{
   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, state, candidate, signal);

   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, state, snap, signal, paper);
   STC_AppendPaperEntryAuditCsv(cfg, state, paper);
   state.paper_entry_rows_audited++;
}

void STC_AppendPaperSkipRow(STC_Config &cfg,
                            STC_RuntimeState &state,
                            STC_TimeSnapshot &snap,
                            const int check_index,
                            const STC_PaperEntryStatus paper_status,
                            const string status_text,
                            const string rule_note)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   STC_PaperEntryAudit row;
   STC_ResetPaperEntryAudit(row);
   row.stc_day_id = check_audit.stc_day_id;
   row.check_index = check_audit.check_index;
   row.entry_check_index = check_audit.check_index + 1;
   row.check_minutes = check_audit.check_minutes;
   row.signal_check_start_ny = check_audit.check_start_ny;
   row.signal_check_end_ny = check_audit.check_end_ny;
   row.m_cycle = check_audit.m_cycle;
   row.current_w_cycle = check_audit.w_cycle;
   row.paper_status = paper_status;
   row.signal_id = cfg.strategy_id + "|" + row.stc_day_id + "|CHK" + IntegerToString(row.check_index) + "|PAPER_SKIP";
   row.paper_trade_id = row.signal_id;
   row.m_trade_count_before = STC_GetPaperMTradeCount(state, row.m_cycle);
   row.m_trade_count_after = row.m_trade_count_before;
   row.m_direction_lock_before = STC_GetPaperMDirectionLock(state, row.m_cycle);
   row.m_direction_lock_after = row.m_direction_lock_before;
   row.status = status_text;
   row.rule_note = rule_note;
   STC_AppendPaperEntryAuditCsv(cfg, state, row);
   state.paper_entry_rows_audited++;
}

void STC_ProcessOnePaperEntryCheck(STC_Config &cfg,
                                   STC_RuntimeState &state,
                                   STC_TimeSnapshot &snap,
                                   const int check_index)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);
   if(!check_audit.start_inside_active_m || !check_audit.detection_allowed_for_signal)
   {
      STC_AppendPaperSkipRow(cfg, state, snap, check_index, STC_PAPER_REJECTED_SIGNAL_NOT_CONFIRMED,
                             "check_not_detection_or_entry_eligible_no_paper_signal", check_audit.skip_reason);
      return;
   }
   if(!check_audit.pair_data_complete)
   {
      STC_AppendPaperSkipRow(cfg, state, snap, check_index, STC_PAPER_REJECTED_NEXT_CHECK_INCOMPLETE,
                             "check_pair_data_incomplete_no_paper_signal", check_audit.skip_reason);
      return;
   }
   if(legal_refs <= 0)
   {
      STC_AppendPaperSkipRow(cfg, state, snap, check_index, STC_PAPER_REJECTED_SIGNAL_NOT_CONFIRMED,
                             "no_legal_previous_W_reference_no_paper_signal", "W1 has no signal and no W is compared with itself");
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
      STC_AppendPaperSkipRow(cfg, state, snap, check_index, STC_PAPER_REJECTED_SIGNAL_NOT_CONFIRMED,
                             "forgotten_simultaneous_buy_and_sell_no_paper_entry", "Locked owner rule: if buy and sell appear in the same check candle, forget the whole check candle");
      return;
   }
   if(high_count <= 0 && low_count <= 0)
   {
      STC_AppendPaperSkipRow(cfg, state, snap, check_index, STC_PAPER_REJECTED_SIGNAL_NOT_CONFIRMED,
                             "no_exactly_one_symbol_hunt_no_paper_entry", "No valid SMT material at this closed check candle");
      return;
   }

   if(high_count > 0)
   {
      if(has_sell_s1) STC_RegisterPaperFromCandidate(cfg, state, snap, best_sell_s1);
      if(has_sell_s2) STC_RegisterPaperFromCandidate(cfg, state, snap, best_sell_s2);
   }
   else if(low_count > 0)
   {
      if(has_buy_s1) STC_RegisterPaperFromCandidate(cfg, state, snap, best_buy_s1);
      if(has_buy_s2) STC_RegisterPaperFromCandidate(cfg, state, snap, best_buy_s2);
   }
}

void STC_ProcessClosedPaperEntries(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_paper_entry_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   // A paper entry for signal check N uses the open of check N+1, so N+1 must already be available/closed or current.
   int max_signal_index_with_entry_open = closed_index - 1;
   if(max_signal_index_with_entry_open < 0)
      return;

   int max_allowed_index = (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 2;
   if(max_signal_index_with_entry_open > max_allowed_index)
      max_signal_index_with_entry_open = max_allowed_index;

   if(state.last_paper_entry_stc_day_id != snap.stc_day_id)
   {
      state.last_paper_entry_stc_day_id = snap.stc_day_id;
      state.paper_trade_count_m1 = 0;
      state.paper_trade_count_m2 = 0;
      state.paper_trade_count_m3 = 0;
      state.paper_direction_lock_m1 = STC_DIR_NONE;
      state.paper_direction_lock_m2 = STC_DIR_NONE;
      state.paper_direction_lock_m3 = STC_DIR_NONE;
      int backfill = cfg.max_paper_entry_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_paper_entry_check_index = max_signal_index_with_entry_open - backfill;
      if(state.last_paper_entry_check_index < -1) state.last_paper_entry_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "PAPER_ENTRY_DAY_RESET", "stc_day=" + snap.stc_day_id + "; max_signal_index_with_entry_open=" + IntegerToString(max_signal_index_with_entry_open));
   }

   int start_index = state.last_paper_entry_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > max_signal_index_with_entry_open)
      return;

   int catchup = cfg.max_paper_entry_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = max_signal_index_with_entry_open;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_ProcessOnePaperEntryCheck(cfg, state, snap, idx);
      state.last_paper_entry_check_index = idx;
   }
}

#endif
