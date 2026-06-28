#ifndef __DAL_STC_REAL_HARD_CLOSE_MQH__
#define __DAL_STC_REAL_HARD_CLOSE_MQH__
#property strict

#include <Trade/Trade.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_RealPartial.mqh>

bool STC_RealHardCloseFinalizerTransportAllowed(STC_Config &cfg)
{
   if(!cfg.enable_real_hard_close_finalizer) return false;
   if(cfg.real_hard_close_finalizer_requires_broker_manager && !cfg.enable_broker_position_manager) return false;
   if(cfg.runtime_mode == STC_MODE_AUTO_TRADE) return true;
   if(cfg.runtime_mode == STC_MODE_PAPER_LIVE && cfg.allow_real_hard_close_finalizer_in_paper_live) return true;
   return false;
}

string STC_RealHardCloseAttemptFolder(STC_Config &cfg, STC_TimeSnapshot &snap)
{
   return STC_JoinPath(cfg.output_root_common, STC_JoinPath("real_hard_close_attempts", STC_SafeId(snap.stc_day_id)));
}

string STC_RealHardCloseAttemptFile(STC_Config &cfg, STC_TimeSnapshot &snap, const long position_identifier)
{
   return STC_JoinPath(STC_RealHardCloseAttemptFolder(cfg, snap), "attempts_" + IntegerToString(position_identifier) + ".marker");
}

int STC_ReadRealHardCloseAttemptCount(STC_Config &cfg, STC_TimeSnapshot &snap, const long position_identifier)
{
   string file = STC_RealHardCloseAttemptFile(cfg, snap, position_identifier);
   if(!FileIsExist(file, FILE_COMMON)) return 0;
   int h = FileOpen(file, FILE_READ | FILE_TXT | FILE_COMMON | FILE_ANSI);
   if(h == INVALID_HANDLE) return 0;
   string line = "";
   if(!FileIsEnding(h)) line = FileReadString(h);
   FileClose(h);
   return (int)StringToInteger(line);
}

bool STC_WriteRealHardCloseAttemptCount(STC_Config &cfg, STC_TimeSnapshot &snap, const long position_identifier, const int count)
{
   STC_EnsureCommonFolderTree(STC_RealHardCloseAttemptFolder(cfg, snap));
   string file = STC_RealHardCloseAttemptFile(cfg, snap, position_identifier);
   int h = FileOpen(file, FILE_WRITE | FILE_TXT | FILE_COMMON | FILE_ANSI);
   if(h == INVALID_HANDLE) return false;
   FileWriteString(h, IntegerToString(count));
   FileClose(h);
   return true;
}

bool STC_AppendRealHardCloseFinalizerCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, STC_RealHardCloseFinalizerAudit &audit)
{
   if(!cfg.write_real_hard_close_finalizer_audit) return true;
   bool exists = FileIsExist(state.real_hard_close_finalizer_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.real_hard_close_finalizer_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append real hard close finalizer CSV ", state.real_hard_close_finalizer_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "ny_time", "stc_day_id", "runtime_mode", "run_id", "symbol1", "symbol2", "magic_config",
         "ticket", "position_identifier", "symbol", "position_magic", "position_type", "open_time", "open_ny", "volume", "price_open", "price_current", "sl", "tp", "floating_profit",
         "symbol_is_pair_member", "magic_matches", "managed_by_stc", "hard_close_due", "transport_allowed", "action_allowed", "action_attempted", "action_succeeded",
         "attempt_count_before", "attempt_count_after", "max_attempts", "close_deviation_points", "trade_result_retcode", "trade_result_comment", "position_remaining_after_attempt", "managed_positions_remaining_after_scan", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(audit.server_time), STC_TimeText(audit.ny_time), audit.stc_day_id, STC_RuntimeModeText(cfg.runtime_mode), cfg.run_id, cfg.symbol1, cfg.symbol2, IntegerToString(cfg.magic_number),
      IntegerToString((long)audit.ticket), IntegerToString(audit.position_identifier), audit.symbol, IntegerToString(audit.magic), audit.position_type, STC_TimeText(audit.open_time), STC_TimeText(audit.open_ny), DoubleToString(audit.volume, 8), DoubleToString(audit.price_open, 8), DoubleToString(audit.price_current, 8), DoubleToString(audit.stop_loss, 8), DoubleToString(audit.take_profit, 8), DoubleToString(audit.floating_profit, 2),
      STC_BoolText(audit.symbol_is_pair_member), STC_BoolText(audit.magic_matches), STC_BoolText(audit.managed_by_stc), STC_BoolText(audit.hard_close_due), STC_BoolText(audit.transport_allowed), STC_BoolText(audit.action_allowed), STC_BoolText(audit.action_attempted), STC_BoolText(audit.action_succeeded),
      IntegerToString(audit.attempt_count_before), IntegerToString(audit.attempt_count_after), IntegerToString(audit.max_attempts), IntegerToString(audit.close_deviation_points), audit.trade_result_retcode, audit.trade_result_comment, STC_BoolText(audit.position_remaining_after_attempt), IntegerToString(audit.managed_positions_remaining_after_scan), audit.status, audit.rule_note);
   FileClose(h);
   state.real_hard_close_finalizer_rows_audited++;
   return true;
}

void STC_BuildRealHardCloseFinalizerAuditFromSelected(STC_Config &cfg, STC_TimeSnapshot &snap, STC_RealHardCloseFinalizerAudit &audit)
{
   STC_ResetRealHardCloseFinalizerAudit(audit);
   audit.stc_day_id = snap.stc_day_id;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   audit.position_identifier = PositionGetInteger(POSITION_IDENTIFIER);
   audit.symbol = PositionGetString(POSITION_SYMBOL);
   audit.magic = PositionGetInteger(POSITION_MAGIC);
   audit.position_type = STC_BrokerPositionTypeText(PositionGetInteger(POSITION_TYPE));
   audit.open_time = (datetime)PositionGetInteger(POSITION_TIME);
   audit.volume = PositionGetDouble(POSITION_VOLUME);
   audit.price_open = PositionGetDouble(POSITION_PRICE_OPEN);
   audit.price_current = PositionGetDouble(POSITION_PRICE_CURRENT);
   audit.stop_loss = PositionGetDouble(POSITION_SL);
   audit.take_profit = PositionGetDouble(POSITION_TP);
   audit.floating_profit = PositionGetDouble(POSITION_PROFIT);
   audit.symbol_is_pair_member = STC_IsPairSymbol(cfg, audit.symbol);
   audit.magic_matches = STC_IsManagedMagic(cfg, audit.magic);
   audit.managed_by_stc = STC_IsManagedBrokerPosition(cfg, audit.symbol, audit.magic);
   audit.hard_close_due = snap.hard_close_due;
   audit.transport_allowed = STC_RealHardCloseFinalizerTransportAllowed(cfg);
   audit.max_attempts = cfg.real_hard_close_finalizer_max_attempts_per_position;
   audit.close_deviation_points = cfg.real_hard_close_finalizer_deviation_points;
   audit.attempt_count_before = STC_ReadRealHardCloseAttemptCount(cfg, snap, audit.position_identifier);
   audit.attempt_count_after = audit.attempt_count_before;
   STC_TimeSnapshot open_snap;
   STC_ResetTimeSnapshot(open_snap);
   STC_BuildTimeSnapshot(cfg, audit.open_time, open_snap);
   audit.open_ny = open_snap.ny_time;
   audit.status = "BUILT";
   audit.rule_note = "Level18 finalizer audits and closes only remaining Symbol1/Symbol2 positions with matching STC magic number after 15:30 New York.";
}

void STC_WriteNoRealHardClosePositionRow(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const string status, const string note, const int managed_remaining)
{
   STC_RealHardCloseFinalizerAudit audit;
   STC_ResetRealHardCloseFinalizerAudit(audit);
   audit.stc_day_id = snap.stc_day_id;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.hard_close_due = snap.hard_close_due;
   audit.transport_allowed = STC_RealHardCloseFinalizerTransportAllowed(cfg);
   audit.managed_positions_remaining_after_scan = managed_remaining;
   audit.status = status;
   audit.rule_note = note;
   STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
}

void STC_AttemptRealHardCloseFinalizerForSelected(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   STC_RealHardCloseFinalizerAudit audit;
   STC_BuildRealHardCloseFinalizerAuditFromSelected(cfg, snap, audit);

   if(!audit.managed_by_stc)
   {
      audit.status = "SKIPPED_NOT_MANAGED_MAGIC_POSITION";
      audit.rule_note = "Foreign/manual positions are never closed by the STC real hard close finalizer.";
      STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.hard_close_due)
   {
      audit.status = "NOT_DUE_YET";
      audit.rule_note = "Real hard close finalizer is only active after 15:30 New York.";
      STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.transport_allowed)
   {
      audit.status = "BLOCKED_TRANSPORT_DISABLED";
      audit.rule_note = "Real hard close finalizer requires explicit enable input and AUTO_TRADE mode unless Paper Live override is enabled.";
      STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
      return;
   }
   if(audit.attempt_count_before >= audit.max_attempts)
   {
      audit.status = "BLOCKED_MAX_ATTEMPTS_REACHED";
      audit.rule_note = "Per-position hard close finalizer attempt cap reached. Manual review required.";
      STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
      return;
   }

   audit.action_allowed = true;
   audit.action_attempted = true;
   audit.attempt_count_after = audit.attempt_count_before + 1;
   STC_WriteRealHardCloseAttemptCount(cfg, snap, audit.position_identifier, audit.attempt_count_after);

   CTrade trade;
   trade.SetExpertMagicNumber(cfg.magic_number);
   trade.SetDeviationInPoints(cfg.real_hard_close_finalizer_deviation_points);
   ResetLastError();
   bool ok = trade.PositionClose(audit.ticket, cfg.real_hard_close_finalizer_deviation_points);
   audit.action_succeeded = ok;
   audit.trade_result_retcode = (int)trade.ResultRetcode();
   audit.trade_result_comment = trade.ResultComment();

   bool still_open = false;
   if(PositionSelectByTicket(audit.ticket))
   {
      string sym = PositionGetString(POSITION_SYMBOL);
      long mg = PositionGetInteger(POSITION_MAGIC);
      still_open = STC_IsManagedBrokerPosition(cfg, sym, mg);
   }
   audit.position_remaining_after_attempt = still_open;
   if(ok && !still_open)
   {
      audit.status = "REAL_HARD_CLOSE_CONFIRMED_CLOSED";
      audit.rule_note = "Magic-only hard close finalizer sent a close request and the position no longer exists after the attempt.";
   }
   else if(ok && still_open)
   {
      audit.status = "REAL_HARD_CLOSE_SENT_BUT_POSITION_STILL_OPEN";
      audit.rule_note = "Close request was accepted by trade API but the position is still visible; finalizer will retry on the next due scan.";
   }
   else
   {
      audit.status = "REAL_HARD_CLOSE_FAILED";
      audit.rule_note = "Close request failed; finalizer will retry until the attempt cap. err=" + IntegerToString(GetLastError());
   }
   STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
}

void STC_ProcessRealHardCloseFinalizer(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const bool force_scan)
{
   if(!cfg.enable_broker_position_manager)
   {
      state.real_hard_close_finalizer_status = "BROKER_MANAGER_DISABLED";
      return;
   }
   if(!cfg.write_real_hard_close_finalizer_audit && !cfg.enable_real_hard_close_finalizer)
      return;
   if(snap.stc_day_id == "") return;

   datetime now = TimeCurrent();
   bool due_scan = force_scan || state.last_real_hard_close_finalizer_scan_server_time <= 0 || now - state.last_real_hard_close_finalizer_scan_server_time >= cfg.real_hard_close_finalizer_scan_seconds;
   bool due_retry = snap.hard_close_due && (force_scan || state.last_real_hard_close_finalizer_attempt_server_time <= 0 || now - state.last_real_hard_close_finalizer_attempt_server_time >= cfg.real_hard_close_finalizer_retry_seconds);
   if(!due_scan && !due_retry) return;

   state.last_real_hard_close_finalizer_scan_server_time = now;
   if(due_retry) state.last_real_hard_close_finalizer_attempt_server_time = now;

   int managed_remaining = 0;
   int audited_positions = 0;
   int total = PositionsTotal();
   for(int i = total - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(!PositionSelectByTicket(ticket)) continue;
      string symbol = PositionGetString(POSITION_SYMBOL);
      long magic = PositionGetInteger(POSITION_MAGIC);
      bool managed = STC_IsManagedBrokerPosition(cfg, symbol, magic);
      bool foreign_pair = STC_IsPairSymbol(cfg, symbol) && !managed;
      if(managed) managed_remaining++;
      if(!managed && !(cfg.audit_foreign_pair_positions && foreign_pair)) continue;

      STC_RealHardCloseFinalizerAudit audit;
      STC_BuildRealHardCloseFinalizerAuditFromSelected(cfg, snap, audit);
      if(!managed)
      {
         audit.status = "AUDIT_FOREIGN_PAIR_POSITION_NOT_MANAGED";
         audit.rule_note = "Pair-symbol position with nonmatching magic number is audited but never closed.";
         STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
         audited_positions++;
         continue;
      }

      if(snap.hard_close_due && due_retry)
      {
         STC_AttemptRealHardCloseFinalizerForSelected(cfg, state, snap);
      }
      else
      {
         audit.status = snap.hard_close_due ? "HARD_CLOSE_DUE_WAITING_FOR_RETRY_INTERVAL" : "PRE_1530_MANAGED_POSITION_AUDIT";
         audit.rule_note = snap.hard_close_due ? "Hard close is due, but retry interval has not elapsed." : "Managed position is visible before hard close; no finalizer action yet.";
         STC_AppendRealHardCloseFinalizerCsv(cfg, state, snap, audit);
      }
      audited_positions++;
   }

   // Re-count after attempts so the status reflects the terminal-visible final state.
   int remaining_after = 0;
   int total_after = PositionsTotal();
   for(int j = total_after - 1; j >= 0; j--)
   {
      ulong t = PositionGetTicket(j);
      if(t == 0) continue;
      if(!PositionSelectByTicket(t)) continue;
      if(STC_IsManagedBrokerPosition(cfg, PositionGetString(POSITION_SYMBOL), PositionGetInteger(POSITION_MAGIC)))
         remaining_after++;
   }
   state.real_hard_close_finalizer_positions_remaining_last_scan = remaining_after;
   if(!snap.hard_close_due)
      state.real_hard_close_finalizer_status = "NOT_DUE";
   else if(remaining_after <= 0)
      state.real_hard_close_finalizer_status = "ALL_MANAGED_POSITIONS_CLOSED";
   else if(STC_RealHardCloseFinalizerTransportAllowed(cfg))
      state.real_hard_close_finalizer_status = "RETRYING_REMAINING_MANAGED_POSITIONS";
   else
      state.real_hard_close_finalizer_status = "DUE_BUT_TRANSPORT_DISABLED";

   if(audited_positions == 0 || (snap.hard_close_due && remaining_after <= 0))
   {
      string st = snap.hard_close_due ? "NO_REMAINING_MANAGED_POSITIONS" : "NO_AUDITABLE_POSITIONS";
      string note = snap.hard_close_due ? "Hard close due and no Symbol1/Symbol2 magic-number positions remain." : "No managed magic positions and no auditable foreign pair positions were found.";
      STC_WriteNoRealHardClosePositionRow(cfg, state, snap, st, note, remaining_after);
   }

   if(snap.hard_close_due && remaining_after > 0 && cfg.real_hard_close_alert_unclosed_positions)
      Print("STC LEVEL18 WARNING: ", remaining_after, " managed magic position(s) still remain after hard-close scan; status=", state.real_hard_close_finalizer_status);
}

#endif
