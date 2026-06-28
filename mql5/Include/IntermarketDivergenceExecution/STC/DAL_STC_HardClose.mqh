#ifndef __DAL_STC_HARDCLOSE_MQH__
#define __DAL_STC_HARDCLOSE_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Partial.mqh>

int STC_HardCloseCheckIndex(STC_Config &cfg)
{
   if(cfg.check_minutes <= 0) return -1;
   return (STC_DAY_ACTIVE_MINUTES / cfg.check_minutes) - 1;
}

void STC_FillHardCloseBase(STC_Config &cfg,
                           STC_TimeSnapshot &snap,
                           STC_PaperEntryAudit &paper,
                           STC_HardCloseAudit &audit)
{
   STC_ResetHardCloseAudit(audit);
   audit.stc_day_id = paper.stc_day_id;
   audit.signal_check_index = paper.check_index;
   audit.entry_check_index = paper.entry_check_index;
   audit.check_minutes = paper.check_minutes;
   audit.signal_check_start_ny = paper.signal_check_start_ny;
   audit.signal_check_end_ny = paper.signal_check_end_ny;
   audit.entry_check_start_ny = paper.entry_check_start_ny;
   audit.entry_check_end_ny = paper.entry_check_end_ny;
   audit.m_cycle = paper.m_cycle;
   audit.current_w_cycle = paper.current_w_cycle;
   audit.paper_status = paper.paper_status;
   audit.signal_id = paper.signal_id;
   audit.paper_trade_id = paper.paper_trade_id;
   audit.is_paper_entry = paper.is_paper_entry;
   audit.direction = paper.direction;
   audit.trade_symbol = paper.trade_symbol;
   audit.entry_price = paper.entry_price;
   audit.stop_price = paper.stop_price;
   audit.take_profit_price = paper.take_profit_price;
   audit.paper_order_volume = paper.paper_order_volume;
   audit.risk_distance_price = paper.risk_distance_price;
   audit.risk_money = paper.risk_money;

   int hc_idx = STC_HardCloseCheckIndex(cfg);
   audit.hard_close_check_index = hc_idx;
   if(hc_idx >= 0)
   {
      audit.hard_close_ny = (datetime)((long)snap.stc_day_start_ny + STC_DAY_ACTIVE_MINUTES * 60);
      audit.hard_close_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, audit.hard_close_ny);
   }
}

void STC_FinalizeHardClosePnL(STC_Config &cfg, STC_HardCloseAudit &audit)
{
   double r = 0.0;
   if(audit.risk_distance_price > 0.0)
   {
      if(audit.direction == STC_DIR_BUY)
         r = (audit.hard_close_price - audit.entry_price) / audit.risk_distance_price;
      else if(audit.direction == STC_DIR_SELL)
         r = (audit.entry_price - audit.hard_close_price) / audit.risk_distance_price;
   }
   audit.floating_r_at_hard_close = r;
   double ratio = 0.0;
   if(audit.paper_order_volume > 0.0)
      ratio = audit.hard_close_volume / audit.paper_order_volume;
   audit.hard_close_gross_pnl_money = audit.risk_money * r * ratio;

   double point = SymbolInfoDouble(audit.trade_symbol, SYMBOL_POINT);
   double tick_size = SymbolInfoDouble(audit.trade_symbol, SYMBOL_TRADE_TICK_SIZE);
   double tick_value = SymbolInfoDouble(audit.trade_symbol, SYMBOL_TRADE_TICK_VALUE);
   double money_per_price_unit = 0.0;
   if(tick_size > 0.0 && tick_value > 0.0)
      money_per_price_unit = tick_value / tick_size;
   else
      money_per_price_unit = cfg.contract_size;

   double spread_points = (double)SymbolInfoInteger(audit.trade_symbol, SYMBOL_SPREAD);
   double spread_cost = 0.0;
   if(point > 0.0 && money_per_price_unit > 0.0)
      spread_cost = spread_points * point * audit.hard_close_volume * money_per_price_unit;
   double commission_cost = cfg.fallback_commission_per_lot * audit.hard_close_volume;
   audit.hard_close_net_pnl_money = audit.hard_close_gross_pnl_money - spread_cost - commission_cost;
}

void STC_EvaluateHardCloseFromPaper(STC_Config &cfg,
                                    STC_TimeSnapshot &snap,
                                    STC_PaperEntryAudit &paper,
                                    const int last_closed_index,
                                    STC_HardCloseAudit &audit)
{
   STC_FillHardCloseBase(cfg, snap, paper, audit);

   if(!paper.is_paper_entry || !(paper.paper_status == STC_PAPER_PLANNED || paper.paper_status == STC_PAPER_PLANNED_SPLIT_REQUIRED))
   {
      audit.hard_close_status = STC_HARDCLOSE_NO_PAPER_ENTRY;
      audit.status = "paper_entry_not_planned_no_hard_close";
      audit.rule_note = paper.rule_note;
      return;
   }

   int hard_idx = audit.hard_close_check_index;
   if(hard_idx < 0 || last_closed_index < hard_idx)
   {
      audit.hard_close_status = STC_HARDCLOSE_NOT_DUE_YET;
      audit.status = "hard_close_check_not_closed_yet";
      audit.rule_note = "Paper hard-close accounting waits for the 15:30 New York check candle to close; delayed hard close is recovered later";
      return;
   }
   audit.hard_close_due = true;
   audit.hard_close_recovered_late = (last_closed_index > hard_idx);

   STC_PaperOutcomeAudit pre;
   STC_SimulateOutcomeFromPaper(cfg, snap, paper, hard_idx, pre);
   audit.pre_hard_outcome_status = pre.outcome_status;
   audit.last_checked_index = pre.last_checked_index;

   if(pre.outcome_status == STC_OUTCOME_REJECTED_DATA_INCOMPLETE)
   {
      audit.hard_close_status = STC_HARDCLOSE_REJECTED_DATA_INCOMPLETE;
      audit.status = "pre_hard_close_outcome_data_incomplete_no_forced_close";
      audit.rule_note = pre.rule_note;
      return;
   }

   if(pre.outcome_status != STC_OUTCOME_OPEN_UNRESOLVED)
   {
      audit.hard_close_status = STC_HARDCLOSE_NOT_OPEN_AT_1530;
      audit.status = "trade_not_open_at_1530_no_hard_close_action";
      audit.rule_note = "TP, SL, ambiguity, rejection, or another terminal state occurred before the 15:30 hard-close checkpoint";
      return;
   }

   STC_CheckCandleAudit hard_check;
   STC_BuildCheckCandleAudit(cfg, snap, hard_idx, hard_check);
   if(!hard_check.pair_data_complete)
   {
      audit.hard_close_status = STC_HARDCLOSE_REJECTED_DATA_INCOMPLETE;
      audit.status = "hard_close_check_pair_data_incomplete";
      audit.rule_note = "Hard close accounting requires complete pair data at the 15:30 check candle";
      return;
   }

   audit.open_at_hard_close = true;
   audit.hard_close_price = STC_OutcomeSymbolClose(hard_check, paper.trade_symbol, cfg);

   double close_volume = paper.paper_order_volume;
   STC_PartialAudit partial;
   STC_EvaluatePartialFromPaper(cfg, snap, paper, hard_idx, partial);
   audit.partial_status = partial.partial_status;
   audit.partial_close_volume = partial.close_volume;
   audit.remaining_after_partial_volume = paper.paper_order_volume;

   if(partial.partial_status == STC_PARTIAL_FULL_CLOSE_BY_SMALL_VOLUME)
   {
      audit.partial_applied_before_hard_close = true;
      audit.partial_full_close_before_hard_close = true;
      audit.hard_close_status = STC_HARDCLOSE_SKIPPED_ALREADY_FULLY_CLOSED_BY_PARTIAL;
      audit.status = "already_fully_closed_by_w4_partial_no_hard_close_remainder";
      audit.rule_note = "The W4 partial consumed the whole small-volume paper trade before 15:30";
      return;
   }
   if(partial.partial_status == STC_PARTIAL_PARTIAL_CLOSE)
   {
      audit.partial_applied_before_hard_close = true;
      audit.remaining_after_partial_volume = partial.remaining_volume;
      close_volume = partial.remaining_volume;
      audit.hard_close_status = STC_HARDCLOSE_REMAINING_AFTER_PARTIAL;
      audit.status = "hard_close_remaining_volume_after_w4_partial";
      audit.rule_note = "Locked owner rule: any paper volume still open at 15:30 New York is force-closed; partial remainder is closed here";
   }
   else
   {
      audit.hard_close_status = STC_HARDCLOSE_FULL_VOLUME;
      audit.status = "hard_close_full_paper_volume_at_1530";
      audit.rule_note = "Locked owner rule: no paper position remains open after 15:30 New York; M3 partial is disabled and other unpartialed trades close in full";
   }

   audit.hard_close_volume = close_volume;
   audit.hard_close_action_taken = (audit.hard_close_volume > 0.0);
   STC_FinalizeHardClosePnL(cfg, audit);
}

void STC_AppendHardCloseSkipRow(STC_Config &cfg,
                                STC_RuntimeState &state,
                                STC_TimeSnapshot &snap,
                                const int check_index,
                                const STC_HardCloseStatus status,
                                const string status_text,
                                const string rule_note)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   STC_HardCloseAudit row;
   STC_ResetHardCloseAudit(row);
   row.stc_day_id = check_audit.stc_day_id;
   row.signal_check_index = check_audit.check_index;
   row.entry_check_index = check_audit.check_index + 1;
   row.hard_close_check_index = STC_HardCloseCheckIndex(cfg);
   row.check_minutes = check_audit.check_minutes;
   row.signal_check_start_ny = check_audit.check_start_ny;
   row.signal_check_end_ny = check_audit.check_end_ny;
   row.m_cycle = check_audit.m_cycle;
   row.current_w_cycle = check_audit.w_cycle;
   row.hard_close_status = status;
   row.hard_close_ny = snap.stc_day_end_ny;
   row.hard_close_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, row.hard_close_ny);
   row.signal_id = cfg.strategy_id + "|" + row.stc_day_id + "|CHK" + IntegerToString(row.signal_check_index) + "|HARDCLOSE_SKIP";
   row.paper_trade_id = row.signal_id;
   row.status = status_text;
   row.rule_note = rule_note;
   STC_AppendHardCloseAuditCsv(cfg, state, row);
   state.hard_close_rows_audited++;
}

void STC_ProcessHardCloseCandidate(STC_Config &cfg,
                                   STC_RuntimeState &state,
                                   STC_TimeSnapshot &snap,
                                   STC_SMTCandidateAudit &candidate,
                                   const int last_closed_index)
{
   STC_RuntimeState calc_state = state;
   STC_CopyPartialCountersIntoPaperCounters(calc_state);

   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, calc_state, candidate, signal);

   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, calc_state, snap, signal, paper);
   STC_CopyPaperCountersBackToPartialCounters(calc_state, state);

   STC_HardCloseAudit hard;
   STC_EvaluateHardCloseFromPaper(cfg, snap, paper, last_closed_index, hard);
   STC_AppendHardCloseAuditCsv(cfg, state, hard);
   state.hard_close_rows_audited++;
}

void STC_ProcessOneHardCloseCheck(STC_Config &cfg,
                                  STC_RuntimeState &state,
                                  STC_TimeSnapshot &snap,
                                  const int check_index,
                                  const int last_closed_index)
{
   STC_SMTCandidateAudit candidate;
   string status_text = "";
   string rule_note = "";
   if(!STC_FindOutcomeCandidateForCheck(cfg, state, snap, check_index, candidate, status_text, rule_note))
   {
      STC_AppendHardCloseSkipRow(cfg, state, snap, check_index, STC_HARDCLOSE_NO_PAPER_ENTRY, status_text, rule_note);
      return;
   }
   STC_ProcessHardCloseCandidate(cfg, state, snap, candidate, last_closed_index);
}

void STC_ProcessClosedHardCloses(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   if(!cfg.write_hard_close_audit)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   int hard_idx = STC_HardCloseCheckIndex(cfg);
   if(closed_index < hard_idx || hard_idx < 0)
      return;

   int max_signal_index_with_entry_before_hard_close = hard_idx - 1;
   if(max_signal_index_with_entry_before_hard_close < 0)
      return;

   if(state.last_hard_close_audit_stc_day_id != snap.stc_day_id)
   {
      state.last_hard_close_audit_stc_day_id = snap.stc_day_id;
      int backfill = cfg.max_hard_close_backfill_on_init;
      if(backfill < 0) backfill = 0;
      state.last_hard_close_audit_check_index = max_signal_index_with_entry_before_hard_close - backfill;
      if(state.last_hard_close_audit_check_index < -1) state.last_hard_close_audit_check_index = -1;
      STC_AppendRuntimeEventCsv(cfg, state, "HARD_CLOSE_DAY_RESET", "stc_day=" + snap.stc_day_id + "; hard_close_check_index=" + IntegerToString(hard_idx));
   }

   int start_index = state.last_hard_close_audit_check_index + 1;
   if(start_index < 0) start_index = 0;
   if(start_index > max_signal_index_with_entry_before_hard_close)
      return;

   int catchup = cfg.max_hard_close_catchup_per_pulse;
   if(catchup < 1) catchup = 1;
   int end_index = max_signal_index_with_entry_before_hard_close;
   if(end_index - start_index + 1 > catchup)
      end_index = start_index + catchup - 1;

   for(int idx = start_index; idx <= end_index; idx++)
   {
      STC_ProcessOneHardCloseCheck(cfg, state, snap, idx, closed_index);
      state.last_hard_close_audit_check_index = idx;
   }
}

#endif
