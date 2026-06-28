#ifndef __DAL_STC_REALPARTIAL_MQH__
#define __DAL_STC_REALPARTIAL_MQH__
#property strict

#include <Trade/Trade.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_AutoEntry.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_Partial.mqh>

bool STC_RealPartialTransportAllowed(STC_Config &cfg)
{
   if(!cfg.enable_broker_position_manager) return false;
   if(!cfg.enable_real_partial_close) return false;
   if(cfg.real_partial_requires_broker_manager && !cfg.enable_broker_position_manager) return false;
   if(cfg.runtime_mode == STC_MODE_AUTO_TRADE) return true;
   if(cfg.runtime_mode == STC_MODE_PAPER_LIVE && cfg.allow_real_partial_in_paper_live) return true;
   return false;
}

string STC_RealPartialMarkerFolder(STC_Config &cfg, STC_TimeSnapshot &snap)
{
   return STC_JoinPath(cfg.output_root_common, STC_JoinPath("real_partial_markers", STC_SafeId(snap.stc_day_id)));
}

string STC_RealPartialMarkerFile(STC_Config &cfg, STC_TimeSnapshot &snap, const long position_identifier)
{
   string folder = STC_RealPartialMarkerFolder(cfg, snap);
   string name = "partial_done_" + IntegerToString(position_identifier) + ".marker";
   return STC_JoinPath(folder, name);
}

bool STC_RealPartialMarkerExists(STC_Config &cfg, STC_TimeSnapshot &snap, const long position_identifier)
{
   string f = STC_RealPartialMarkerFile(cfg, snap, position_identifier);
   return FileIsExist(f, FILE_COMMON);
}

void STC_WriteRealPartialMarker(STC_Config &cfg, STC_TimeSnapshot &snap, STC_RealPartialAudit &audit)
{
   string folder = STC_RealPartialMarkerFolder(cfg, snap);
   STC_EnsureCommonFolderTree(folder);
   string f = STC_RealPartialMarkerFile(cfg, snap, audit.position_identifier);
   int h = FileOpen(f, FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
      return;
   FileWrite(h,
      "stc_day_id", "server_time", "ny_time", "ticket", "position_identifier", "symbol", "magic", "original_volume", "close_volume", "remaining_volume", "status");
   FileWrite(h,
      audit.stc_day_id, STC_TimeText(audit.server_time), STC_TimeText(audit.ny_time), IntegerToString((long)audit.ticket), IntegerToString(audit.position_identifier), audit.symbol, IntegerToString(audit.magic),
      DoubleToString(audit.original_volume, 8), DoubleToString(audit.close_volume, 8), DoubleToString(audit.remaining_volume_estimate, 8), audit.status);
   FileClose(h);
}

bool STC_AppendRealPartialCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, STC_RealPartialAudit &audit)
{
   if(!cfg.write_real_partial_audit) return true;
   bool exists = FileIsExist(state.real_partial_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.real_partial_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append real partial CSV ", state.real_partial_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "ny_time", "stc_day_id", "runtime_mode", "run_id", "symbol1", "symbol2", "magic_config",
         "ticket", "position_identifier", "symbol", "position_magic", "position_type", "open_time", "open_ny", "open_m_cycle", "open_w_cycle",
         "partial_due", "partial_due_ny", "partial_due_server", "m3_partial_disabled", "already_marked_done", "transport_allowed", "partial_enabled", "hard_close_due",
         "original_volume", "broker_min_volume", "broker_max_volume", "broker_volume_step", "close_volume", "remaining_volume_estimate",
         "action_allowed", "action_attempted", "action_succeeded", "trade_result_retcode", "trade_result_comment", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(audit.server_time), STC_TimeText(audit.ny_time), audit.stc_day_id, STC_RuntimeModeText(cfg.runtime_mode), cfg.run_id, cfg.symbol1, cfg.symbol2, IntegerToString(cfg.magic_number),
      IntegerToString((long)audit.ticket), IntegerToString(audit.position_identifier), audit.symbol, IntegerToString(audit.magic), audit.position_type, STC_TimeText(audit.open_time), STC_TimeText(audit.open_ny), STC_MCycleText(audit.open_m_cycle), STC_WCycleText(audit.open_w_cycle),
      STC_BoolText(audit.partial_due), STC_TimeText(audit.partial_due_ny), STC_TimeText(audit.partial_due_server), STC_BoolText(audit.m3_partial_disabled), STC_BoolText(audit.already_marked_done), STC_BoolText(audit.transport_allowed), STC_BoolText(audit.partial_enabled), STC_BoolText(audit.hard_close_due),
      DoubleToString(audit.original_volume, 8), DoubleToString(audit.broker_min_volume, 8), DoubleToString(audit.broker_max_volume, 8), DoubleToString(audit.broker_volume_step, 8), DoubleToString(audit.close_volume, 8), DoubleToString(audit.remaining_volume_estimate, 8),
      STC_BoolText(audit.action_allowed), STC_BoolText(audit.action_attempted), STC_BoolText(audit.action_succeeded), audit.trade_result_retcode, audit.trade_result_comment, audit.status, audit.rule_note);
   FileClose(h);
   state.real_partial_rows_audited++;
   return true;
}

void STC_BuildRealPartialAuditFromSelected(STC_Config &cfg, STC_TimeSnapshot &snap, STC_RealPartialAudit &audit)
{
   STC_ResetRealPartialAudit(audit);
   audit.stc_day_id = snap.stc_day_id;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   audit.position_identifier = PositionGetInteger(POSITION_IDENTIFIER);
   audit.symbol = PositionGetString(POSITION_SYMBOL);
   audit.magic = PositionGetInteger(POSITION_MAGIC);
   audit.position_type = STC_BrokerPositionTypeText(PositionGetInteger(POSITION_TYPE));
   audit.original_volume = PositionGetDouble(POSITION_VOLUME);
   audit.open_time = (datetime)PositionGetInteger(POSITION_TIME);
   audit.partial_enabled = cfg.partial_enabled;
   audit.hard_close_due = snap.hard_close_due;
   audit.transport_allowed = STC_RealPartialTransportAllowed(cfg);
   audit.broker_min_volume = SymbolInfoDouble(audit.symbol, SYMBOL_VOLUME_MIN);
   audit.broker_max_volume = SymbolInfoDouble(audit.symbol, SYMBOL_VOLUME_MAX);
   audit.broker_volume_step = SymbolInfoDouble(audit.symbol, SYMBOL_VOLUME_STEP);
   if(audit.broker_volume_step <= 0.0) audit.broker_volume_step = 0.01;

   STC_TimeSnapshot open_snap;
   STC_ResetTimeSnapshot(open_snap);
   STC_BuildTimeSnapshot(cfg, audit.open_time, open_snap);
   audit.open_ny = open_snap.ny_time;
   audit.open_m_cycle = open_snap.m_cycle;
   audit.open_w_cycle = open_snap.w_cycle;

   int due_elapsed = STC_MEndElapsedForPartial(audit.open_m_cycle);
   if(due_elapsed >= 0)
   {
      audit.partial_due_ny = (datetime)((long)snap.stc_day_start_ny + due_elapsed * 60);
      audit.partial_due_server = STC_NewYorkToServerUsingSnapshot(cfg, snap, audit.partial_due_ny);
   }
   audit.partial_due = (audit.partial_due_ny > 0 && snap.ny_time >= audit.partial_due_ny);
   audit.m3_partial_disabled = (audit.open_m_cycle == STC_M3);
   audit.already_marked_done = STC_RealPartialMarkerExists(cfg, snap, audit.position_identifier);
   audit.status = "BUILT";
   audit.rule_note = "Level17 evaluates real partial close only for current STC-day Symbol1/Symbol2 positions with matching magic number.";
}

void STC_AttemptRealPartialForSelectedPosition(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   STC_RealPartialAudit audit;
   STC_BuildRealPartialAuditFromSelected(cfg, snap, audit);

   if(!STC_IsManagedBrokerPosition(cfg, audit.symbol, audit.magic))
   {
      audit.status = "SKIPPED_NOT_MANAGED_MAGIC_POSITION";
      audit.rule_note = "Foreign/manual positions are never partial-closed by STC.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.partial_enabled)
   {
      audit.status = "SKIPPED_PARTIAL_SWITCH_OFF";
      audit.rule_note = "InpPartial=false disables real partial close but does not disable hard close.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(audit.hard_close_due)
   {
      audit.status = "SKIPPED_HARD_CLOSE_HAS_PRIORITY";
      audit.rule_note = "After 15:30 New York, real hard close owns the remaining position; partial is not attempted.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(audit.open_m_cycle == STC_M_NONE || audit.open_w_cycle == STC_W_NONE || audit.open_ny < snap.stc_day_start_ny || audit.open_ny >= snap.stc_day_end_ny)
   {
      audit.status = "SKIPPED_POSITION_NOT_FROM_CURRENT_STC_ACTIVE_M";
      audit.rule_note = "Real partial only applies to positions opened inside the current STC trading day active M cycles.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(audit.m3_partial_disabled)
   {
      audit.status = "SKIPPED_M3_PARTIAL_DISABLED";
      audit.rule_note = "Locked owner rule: M3 partial is meaningless because 15:30 hard close has priority.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.partial_due)
   {
      audit.status = "NOT_DUE_YET";
      audit.rule_note = "Real partial is due exactly at W4/M end and can be recovered later before hard close.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(audit.already_marked_done)
   {
      audit.status = "SKIPPED_ALREADY_PARTIALED";
      audit.rule_note = "A current-day real partial marker already exists for this position identifier; no duplicate partial is attempted.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(!audit.transport_allowed)
   {
      audit.status = "BLOCKED_TRANSPORT_DISABLED";
      audit.rule_note = "Real partial requires InpEnableRealPartialClose=true and AUTO_TRADE mode unless explicit Paper Live override is enabled.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }

   double step = audit.broker_volume_step;
   if(step <= 0.0) step = 0.01;
   double half = audit.original_volume * 0.5;
   double close_volume = STC_CeilVolumeToStep(half, step);
   if(close_volume > audit.original_volume) close_volume = audit.original_volume;
   close_volume = STC_NormalizeVolumeDown(close_volume, step);
   if(close_volume <= 0.0)
   {
      audit.status = "REJECTED_ZERO_CLOSE_VOLUME";
      audit.rule_note = "Calculated partial volume normalized to zero.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(close_volume < audit.broker_min_volume && close_volume < audit.original_volume)
   {
      audit.status = "REJECTED_BELOW_BROKER_MIN_VOLUME";
      audit.rule_note = "Partial volume would be below broker minimum and cannot safely be rounded upward beyond the locked risk geometry.";
      STC_AppendRealPartialCsv(cfg, state, snap, audit);
      return;
   }
   if(close_volume >= audit.original_volume || audit.original_volume <= step)
   {
      close_volume = audit.original_volume;
      audit.remaining_volume_estimate = 0.0;
   }
   else
   {
      audit.remaining_volume_estimate = audit.original_volume - close_volume;
   }
   audit.close_volume = close_volume;
   audit.action_allowed = true;
   audit.action_attempted = true;

   CTrade trade;
   trade.SetExpertMagicNumber(cfg.magic_number);
   trade.SetDeviationInPoints(cfg.real_partial_deviation_points);
   ResetLastError();
   bool ok = false;
   if(close_volume >= audit.original_volume)
      ok = trade.PositionClose(audit.ticket, cfg.real_partial_deviation_points);
   else
      ok = trade.PositionClosePartial(audit.ticket, close_volume, cfg.real_partial_deviation_points);

   audit.action_succeeded = ok;
   audit.trade_result_retcode = (int)trade.ResultRetcode();
   audit.trade_result_comment = trade.ResultComment();
   if(ok)
   {
      audit.status = (close_volume >= audit.original_volume) ? "REAL_PARTIAL_FULL_CLOSE_SMALL_VOLUME_SENT_OK" : "REAL_PARTIAL_CLOSE_SENT_OK";
      audit.rule_note = "Magic-only real partial close was sent. A marker was written to prevent duplicate partial after restart.";
      STC_WriteRealPartialMarker(cfg, snap, audit);
   }
   else
   {
      audit.status = "REAL_PARTIAL_CLOSE_FAILED";
      audit.rule_note = "Real partial close failed; no marker was written, so the next due scan may retry. err=" + IntegerToString(GetLastError());
   }
   STC_AppendRealPartialCsv(cfg, state, snap, audit);
}

void STC_ProcessRealPartialManager(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const bool force_scan)
{
   if(!cfg.enable_broker_position_manager)
   {
      state.real_partial_status = "BROKER_MANAGER_DISABLED";
      return;
   }
   if(!cfg.write_real_partial_audit && !cfg.enable_real_partial_close)
      return;
   if(snap.stc_day_id == "" || snap.elapsed_seconds_from_2000 <= 0)
      return;

   datetime now = TimeCurrent();
   bool due_scan = force_scan || state.last_real_partial_scan_server_time <= 0 || now - state.last_real_partial_scan_server_time >= cfg.real_partial_scan_seconds;
   if(!due_scan)
      return;
   state.last_real_partial_scan_server_time = now;

   int total_positions = PositionsTotal();
   int eligible_seen = 0;
   for(int i = total_positions - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(!PositionSelectByTicket(ticket)) continue;
      string symbol = PositionGetString(POSITION_SYMBOL);
      long magic = PositionGetInteger(POSITION_MAGIC);
      if(!STC_IsManagedBrokerPosition(cfg, symbol, magic))
         continue;
      eligible_seen++;
      STC_AttemptRealPartialForSelectedPosition(cfg, state, snap);
   }

   if(eligible_seen <= 0 && cfg.write_real_partial_audit)
   {
      STC_RealPartialAudit empty;
      STC_ResetRealPartialAudit(empty);
      empty.stc_day_id = snap.stc_day_id;
      empty.server_time = now;
      empty.ny_time = snap.ny_time;
      empty.transport_allowed = STC_RealPartialTransportAllowed(cfg);
      empty.partial_enabled = cfg.partial_enabled;
      empty.hard_close_due = snap.hard_close_due;
      empty.status = "NO_MANAGED_MAGIC_POSITIONS";
      empty.rule_note = "No Symbol1/Symbol2 positions with this magic number were available for real partial scan.";
      STC_AppendRealPartialCsv(cfg, state, snap, empty);
   }

   state.real_partial_status = STC_RealPartialTransportAllowed(cfg) ? "REAL_PARTIAL_TRANSPORT_ARMED" : "REAL_PARTIAL_TRANSPORT_DISABLED";
}

#endif
