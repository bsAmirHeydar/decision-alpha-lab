#ifndef __DAL_STC_AUTOENTRY_MQH__
#define __DAL_STC_AUTOENTRY_MQH__
#property strict

#include <Trade/Trade.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_Broker.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_Paper.mqh>

int STC_GetAutoMTradeCount(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.auto_trade_count_m1;
   if(m == STC_M2) return state.auto_trade_count_m2;
   if(m == STC_M3) return state.auto_trade_count_m3;
   return 0;
}

STC_Direction STC_GetAutoMDirectionLock(STC_RuntimeState &state, const STC_MCycle m)
{
   if(m == STC_M1) return state.auto_direction_lock_m1;
   if(m == STC_M2) return state.auto_direction_lock_m2;
   if(m == STC_M3) return state.auto_direction_lock_m3;
   return STC_DIR_NONE;
}

void STC_SetAutoMTradeCount(STC_RuntimeState &state, const STC_MCycle m, const int value)
{
   if(m == STC_M1) state.auto_trade_count_m1 = value;
   else if(m == STC_M2) state.auto_trade_count_m2 = value;
   else if(m == STC_M3) state.auto_trade_count_m3 = value;
}

void STC_SetAutoMDirectionLock(STC_RuntimeState &state, const STC_MCycle m, const STC_Direction direction)
{
   if(m == STC_M1) state.auto_direction_lock_m1 = direction;
   else if(m == STC_M2) state.auto_direction_lock_m2 = direction;
   else if(m == STC_M3) state.auto_direction_lock_m3 = direction;
}

bool STC_AutoEntryTransportAllowed(STC_Config &cfg)
{
   if(!cfg.enable_real_auto_entry) return false;
   if(cfg.auto_entry_requires_broker_manager && !cfg.enable_broker_position_manager) return false;
   if(cfg.runtime_mode == STC_MODE_AUTO_TRADE) return true;
   if(cfg.runtime_mode == STC_MODE_PAPER_LIVE && cfg.allow_auto_entry_in_paper_live) return true;
   return false;
}

string STC_AutoEntryOrderComment(STC_Config &cfg, STC_AutoEntryAudit &audit, const int part_index)
{
   string prefix = cfg.auto_entry_order_comment_prefix;
   if(prefix == "") prefix = "DAL_STC_EXEC001";
   string text = prefix + " " + audit.stc_day_id + " C" + IntegerToString(audit.signal_check_index) + " P" + IntegerToString(part_index);
   if(StringLen(text) > 31)
      text = StringSubstr(text, 0, 31);
   return text;
}

bool STC_AppendAutoEntryAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, STC_AutoEntryAudit &audit)
{
   if(!cfg.write_auto_entry_audit) return true;
   bool exists = FileIsExist(state.auto_entry_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.auto_entry_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append auto entry CSV ", state.auto_entry_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "ny_time", "stc_day_id", "runtime_mode", "run_id", "symbol1", "symbol2", "magic",
         "signal_check_index", "entry_check_index", "check_minutes", "signal_check_end_ny", "entry_check_start_ny", "m_cycle", "w_cycle",
         "signal_id", "paper_trade_id", "auto_order_group_id", "direction", "trade_symbol", "hunted_symbol", "clean_symbol",
         "entry_reference_price", "stop_price", "take_profit_price", "risk_distance_price", "risk_money", "theoretical_volume", "requested_total_volume", "sent_total_volume",
         "broker_min_volume", "broker_max_volume", "broker_volume_step", "planned_split_orders", "attempted_orders", "successful_orders",
         "transport_allowed", "grace_window_ok", "auto_entry_enabled", "broker_manager_required_ok", "order_attempted", "any_order_succeeded",
         "last_retcode", "last_trade_comment", "auto_status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(audit.server_time), STC_TimeText(audit.ny_time), audit.stc_day_id, STC_RuntimeModeText(cfg.runtime_mode), cfg.run_id, cfg.symbol1, cfg.symbol2, IntegerToString(cfg.magic_number),
      audit.signal_check_index, audit.entry_check_index, audit.check_minutes, STC_TimeText(audit.signal_check_end_ny), STC_TimeText(audit.entry_check_start_ny), STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle),
      audit.signal_id, audit.paper_trade_id, audit.auto_order_group_id, STC_DirectionText(audit.direction), audit.trade_symbol, audit.hunted_symbol, audit.clean_symbol,
      DoubleToString(audit.entry_reference_price, 8), DoubleToString(audit.stop_price, 8), DoubleToString(audit.take_profit_price, 8), DoubleToString(audit.risk_distance_price, 8), DoubleToString(audit.risk_money, 2), DoubleToString(audit.theoretical_volume, 8), DoubleToString(audit.requested_total_volume, 8), DoubleToString(audit.sent_total_volume, 8),
      DoubleToString(audit.broker_min_volume, 8), DoubleToString(audit.broker_max_volume, 8), DoubleToString(audit.broker_volume_step, 8), audit.planned_split_orders, audit.attempted_orders, audit.successful_orders,
      STC_BoolText(audit.transport_allowed), STC_BoolText(audit.grace_window_ok), STC_BoolText(audit.auto_entry_enabled), STC_BoolText(audit.broker_manager_required_ok), STC_BoolText(audit.order_attempted), STC_BoolText(audit.any_order_succeeded),
      audit.last_retcode, audit.last_trade_comment, audit.auto_status, audit.rule_note);
   FileClose(h);
   state.auto_entry_rows_audited++;
   return true;
}

void STC_FillAutoFromPaperPlan(STC_Config &cfg,
                               STC_RuntimeState &state,
                               STC_TimeSnapshot &snap,
                               STC_PaperEntryAudit &paper,
                               STC_AutoEntryAudit &audit)
{
   STC_ResetAutoEntryAudit(audit);
   audit.stc_day_id = paper.stc_day_id;
   audit.signal_check_index = paper.check_index;
   audit.entry_check_index = paper.entry_check_index;
   audit.check_minutes = paper.check_minutes;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.signal_check_end_ny = paper.signal_check_end_ny;
   audit.entry_check_start_ny = paper.entry_check_start_ny;
   audit.m_cycle = paper.m_cycle;
   audit.current_w_cycle = paper.current_w_cycle;
   audit.signal_id = paper.signal_id;
   audit.paper_trade_id = paper.paper_trade_id;
   audit.auto_order_group_id = cfg.strategy_id + "|" + audit.stc_day_id + "|CHK" + IntegerToString(audit.signal_check_index) + "|" + paper.trade_symbol + "|AUTO";
   audit.direction = paper.direction;
   audit.trade_symbol = paper.trade_symbol;
   audit.hunted_symbol = paper.hunted_symbol;
   audit.clean_symbol = paper.clean_symbol;
   audit.entry_reference_price = paper.entry_price;
   audit.stop_price = paper.stop_price;
   audit.take_profit_price = paper.take_profit_price;
   audit.risk_distance_price = paper.risk_distance_price;
   audit.risk_money = paper.risk_money;
   audit.theoretical_volume = paper.theoretical_volume;
   audit.requested_total_volume = STC_NormalizeVolumeDown(paper.theoretical_volume, paper.broker_volume_step);
   audit.broker_min_volume = paper.broker_min_volume;
   audit.broker_max_volume = paper.broker_max_volume;
   audit.broker_volume_step = paper.broker_volume_step;
   audit.planned_split_orders = paper.split_order_count;
   audit.transport_allowed = STC_AutoEntryTransportAllowed(cfg);
   audit.auto_entry_enabled = cfg.enable_real_auto_entry;
   audit.broker_manager_required_ok = (!cfg.auto_entry_requires_broker_manager || cfg.enable_broker_position_manager);
   audit.grace_window_ok = false;
   audit.auto_status = "BUILT_FROM_PAPER_PLAN";
   audit.rule_note = "Level16 real auto-entry router mirrors Level08 paper geometry and only sends orders when all safety gates pass.";

   if(paper.entry_check_start_server > 0)
   {
      int elapsed = (int)((long)TimeCurrent() - (long)paper.entry_check_start_server);
      audit.grace_window_ok = (elapsed >= 0 && elapsed <= cfg.auto_entry_grace_seconds);
   }
}

void STC_ApplyAutoCounterAfterSuccess(STC_Config &cfg, STC_RuntimeState &state, STC_AutoEntryAudit &audit)
{
   int count = STC_GetAutoMTradeCount(state, audit.m_cycle);
   STC_SetAutoMTradeCount(state, audit.m_cycle, count + 1);
   if(!cfg.hedging_enabled && STC_GetAutoMDirectionLock(state, audit.m_cycle) == STC_DIR_NONE)
      STC_SetAutoMDirectionLock(state, audit.m_cycle, audit.direction);
}

bool STC_SendAutoMarketChunk(STC_Config &cfg, STC_AutoEntryAudit &audit, const double volume, const int part_index)
{
   if(volume <= 0.0) return false;
   CTrade trade;
   trade.SetExpertMagicNumber(cfg.magic_number);
   trade.SetDeviationInPoints(cfg.auto_entry_deviation_points);
   string comment = STC_AutoEntryOrderComment(cfg, audit, part_index);
   ResetLastError();
   bool ok = false;
   if(audit.direction == STC_DIR_BUY)
      ok = trade.Buy(volume, audit.trade_symbol, 0.0, audit.stop_price, audit.take_profit_price, comment);
   else if(audit.direction == STC_DIR_SELL)
      ok = trade.Sell(volume, audit.trade_symbol, 0.0, audit.stop_price, audit.take_profit_price, comment);
   audit.last_retcode = (int)trade.ResultRetcode();
   audit.last_trade_comment = trade.ResultComment();
   if(!ok && audit.last_trade_comment == "") audit.last_trade_comment = "send_failed_err_" + IntegerToString(GetLastError());
   return ok;
}

void STC_AttemptAutoOrdersFromPaper(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, STC_PaperEntryAudit &paper)
{
   STC_AutoEntryAudit audit;
   STC_FillAutoFromPaperPlan(cfg, state, snap, paper, audit);

   if(!paper.is_paper_entry || !(paper.paper_status == STC_PAPER_PLANNED || paper.paper_status == STC_PAPER_PLANNED_SPLIT_REQUIRED))
   {
      audit.auto_status = "REJECTED_NO_VALID_PAPER_PLAN";
      audit.rule_note = "Real auto-entry only mirrors valid Level08 paper entry plans.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.transport_allowed)
   {
      audit.auto_status = "BLOCKED_TRANSPORT_DISABLED";
      audit.rule_note = "Real auto-entry requires InpEnableRealAutoEntry=true and AUTO_TRADE mode unless explicit paper-live override is enabled.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.grace_window_ok)
   {
      audit.auto_status = "REJECTED_ENTRY_GRACE_EXPIRED";
      audit.rule_note = "Locked owner rule: no late entry after the exact entry moment; grace window elapsed.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }
   if(STC_GetAutoMTradeCount(state, audit.m_cycle) >= 3)
   {
      audit.auto_status = "REJECTED_MAX_THREE_REAL_TRADES_PER_M";
      audit.rule_note = "Real auto-entry obeys the same max three trades per M rule.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }
   if(!cfg.hedging_enabled && STC_GetAutoMDirectionLock(state, audit.m_cycle) != STC_DIR_NONE && STC_GetAutoMDirectionLock(state, audit.m_cycle) != audit.direction)
   {
      audit.auto_status = "REJECTED_REAL_DIRECTION_LOCK";
      audit.rule_note = "Hedging OFF locks real auto-entry direction inside the current M only.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }
   if(audit.requested_total_volume < audit.broker_min_volume)
   {
      audit.auto_status = "REJECTED_BELOW_BROKER_MIN_VOLUME";
      audit.rule_note = "Do not round up to broker minimum because that may exceed requested risk.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }

   double remaining = audit.requested_total_volume;
   int split_limit = cfg.max_auto_split_orders;
   if(split_limit < 1) split_limit = 1;
   int safety_orders_needed = 1;
   if(audit.broker_max_volume > 0.0 && remaining > audit.broker_max_volume)
      safety_orders_needed = (int)MathCeil(remaining / audit.broker_max_volume);
   if(safety_orders_needed > split_limit)
   {
      audit.auto_status = "REJECTED_SPLIT_ORDER_LIMIT";
      audit.rule_note = "The calculated volume requires more split orders than InpMaxAutoSplitOrders allows.";
      STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
      return;
   }

   audit.order_attempted = true;
   int part = 0;
   while(remaining >= audit.broker_min_volume && part < split_limit)
   {
      double chunk = remaining;
      if(audit.broker_max_volume > 0.0 && chunk > audit.broker_max_volume)
         chunk = audit.broker_max_volume;
      chunk = STC_NormalizeVolumeDown(chunk, audit.broker_volume_step);
      if(chunk < audit.broker_min_volume || chunk <= 0.0)
         break;
      part++;
      audit.attempted_orders++;
      bool ok = STC_SendAutoMarketChunk(cfg, audit, chunk, part);
      if(ok)
      {
         audit.successful_orders++;
         audit.sent_total_volume += chunk;
         remaining -= chunk;
      }
      else
      {
         // Stop immediately on first failed chunk. This avoids partial over-retry loops.
         break;
      }
   }

   audit.any_order_succeeded = (audit.successful_orders > 0);
   if(audit.any_order_succeeded)
   {
      STC_ApplyAutoCounterAfterSuccess(cfg, state, audit);
      audit.auto_status = (audit.sent_total_volume + audit.broker_volume_step >= audit.requested_total_volume) ? "REAL_ENTRY_SENT_OK" : "REAL_ENTRY_PARTIAL_SPLIT_SENT";
      audit.rule_note = "One or more magic-number real entry orders were sent with STC SL/TP. Remaining unsent volume, if any, is recorded in this audit row.";
   }
   else
   {
      audit.auto_status = "REAL_ENTRY_SEND_FAILED";
      audit.rule_note = "No real entry order succeeded; signal is consumed and will not be retried on later check candles.";
   }
   STC_AppendAutoEntryAuditCsv(cfg, state, snap, audit);
}

void STC_RegisterAutoFromCandidate(STC_Config &cfg,
                                   STC_RuntimeState &state,
                                   STC_TimeSnapshot &snap,
                                   STC_SMTCandidateAudit &candidate)
{
   STC_SignalAudit signal;
   STC_FinalizeSignalFromCandidate(cfg, state, candidate, signal);

   STC_RuntimeState scratch = state;
   scratch.paper_trade_count_m1 = state.auto_trade_count_m1;
   scratch.paper_trade_count_m2 = state.auto_trade_count_m2;
   scratch.paper_trade_count_m3 = state.auto_trade_count_m3;
   scratch.paper_direction_lock_m1 = state.auto_direction_lock_m1;
   scratch.paper_direction_lock_m2 = state.auto_direction_lock_m2;
   scratch.paper_direction_lock_m3 = state.auto_direction_lock_m3;

   STC_PaperEntryAudit paper;
   STC_FillPaperFromSignal(cfg, scratch, snap, signal, paper);
   STC_AttemptAutoOrdersFromPaper(cfg, state, snap, paper);
}

void STC_AppendAutoSkipRow(STC_Config &cfg,
                           STC_RuntimeState &state,
                           STC_TimeSnapshot &snap,
                           const int check_index,
                           const string status_text,
                           const string rule_note)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);
   STC_AutoEntryAudit row;
   STC_ResetAutoEntryAudit(row);
   row.stc_day_id = check_audit.stc_day_id;
   row.signal_check_index = check_audit.check_index;
   row.entry_check_index = check_audit.check_index + 1;
   row.check_minutes = check_audit.check_minutes;
   row.server_time = TimeCurrent();
   row.ny_time = snap.ny_time;
   row.signal_check_end_ny = check_audit.check_end_ny;
   row.m_cycle = check_audit.m_cycle;
   row.current_w_cycle = check_audit.w_cycle;
   row.auto_status = status_text;
   row.rule_note = rule_note;
   row.transport_allowed = STC_AutoEntryTransportAllowed(cfg);
   row.auto_entry_enabled = cfg.enable_real_auto_entry;
   row.broker_manager_required_ok = (!cfg.auto_entry_requires_broker_manager || cfg.enable_broker_position_manager);
   STC_AppendAutoEntryAuditCsv(cfg, state, snap, row);
}

void STC_ProcessOneAutoEntryCheck(STC_Config &cfg,
                                  STC_RuntimeState &state,
                                  STC_TimeSnapshot &snap,
                                  const int check_index)
{
   STC_CheckCandleAudit check_audit;
   STC_BuildCheckCandleAudit(cfg, snap, check_index, check_audit);

   int legal_refs = STC_HuntReferenceCount(check_audit.w_cycle);
   if(!check_audit.start_inside_active_m || !check_audit.detection_allowed_for_signal)
   {
      STC_AppendAutoSkipRow(cfg, state, snap, check_index, "SKIPPED_NOT_DETECTION_ELIGIBLE", check_audit.skip_reason);
      return;
   }
   if(!check_audit.pair_data_complete)
   {
      STC_AppendAutoSkipRow(cfg, state, snap, check_index, "SKIPPED_PAIR_DATA_INCOMPLETE", check_audit.skip_reason);
      return;
   }
   if(legal_refs <= 0)
   {
      STC_AppendAutoSkipRow(cfg, state, snap, check_index, "SKIPPED_NO_LEGAL_REFERENCE", "W1 has no signal and no W is compared with itself");
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
      STC_AppendAutoSkipRow(cfg, state, snap, check_index, "FORGOTTEN_SIMULTANEOUS_BUY_SELL", "Locked owner rule: if buy and sell appear in the same check candle, forget the whole check candle");
      return;
   }
   if(high_count <= 0 && low_count <= 0)
   {
      STC_AppendAutoSkipRow(cfg, state, snap, check_index, "SKIPPED_NO_EXACTLY_ONE_HUNT", "No valid SMT material at this closed check candle");
      return;
   }

   if(high_count > 0)
   {
      if(has_sell_s1) STC_RegisterAutoFromCandidate(cfg, state, snap, best_sell_s1);
      if(has_sell_s2) STC_RegisterAutoFromCandidate(cfg, state, snap, best_sell_s2);
   }
   else if(low_count > 0)
   {
      if(has_buy_s1) STC_RegisterAutoFromCandidate(cfg, state, snap, best_buy_s1);
      if(has_buy_s2) STC_RegisterAutoFromCandidate(cfg, state, snap, best_buy_s2);
   }
}

void STC_ProcessAutoEntryRouter(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const bool force_baseline)
{
   if(!cfg.write_auto_entry_audit && !cfg.enable_real_auto_entry)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   int closed_index = STC_LastClosedCheckIndex(snap);
   if(closed_index < 0)
      return;

   if(state.last_auto_entry_stc_day_id != snap.stc_day_id)
   {
      state.last_auto_entry_stc_day_id = snap.stc_day_id;
      state.auto_trade_count_m1 = 0;
      state.auto_trade_count_m2 = 0;
      state.auto_trade_count_m3 = 0;
      state.auto_direction_lock_m1 = STC_DIR_NONE;
      state.auto_direction_lock_m2 = STC_DIR_NONE;
      state.auto_direction_lock_m3 = STC_DIR_NONE;
      state.last_auto_entry_check_index = closed_index;
      state.auto_entry_status = "BASELINED_CURRENT_DAY_NO_BACKFILL";
      STC_AppendRuntimeEventCsv(cfg, state, "AUTO_ENTRY_DAY_BASELINE", "stc_day=" + snap.stc_day_id + "; closed_index=" + IntegerToString(closed_index) + "; no historical real entries will be sent");
      if(force_baseline)
         return;
   }

   if(force_baseline)
      return;

   int next_index = state.last_auto_entry_check_index + 1;
   if(next_index < 0) next_index = 0;
   if(next_index > closed_index)
      return;

   // Process only newly closed check candles. Missed historical checks will be marked late by the grace gate.
   for(int idx = next_index; idx <= closed_index; idx++)
   {
      STC_ProcessOneAutoEntryCheck(cfg, state, snap, idx);
      state.last_auto_entry_check_index = idx;
   }
   state.auto_entry_status = STC_AutoEntryTransportAllowed(cfg) ? "AUTO_ENTRY_TRANSPORT_ARMED" : "AUTO_ENTRY_TRANSPORT_DISABLED";
}

#endif
