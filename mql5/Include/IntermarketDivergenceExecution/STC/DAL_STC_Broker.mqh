#ifndef __DAL_STC_BROKER_MQH__
#define __DAL_STC_BROKER_MQH__
#property strict

#include <Trade/Trade.mqh>
#include <IntermarketDivergenceExecution/STC/DAL_STC_Alerts.mqh>

string STC_BrokerPositionTypeText(const long position_type)
{
   if(position_type == POSITION_TYPE_BUY) return "BUY";
   if(position_type == POSITION_TYPE_SELL) return "SELL";
   return "UNKNOWN";
}

bool STC_IsPairSymbol(STC_Config &cfg, const string symbol)
{
   return (symbol == cfg.symbol1 || symbol == cfg.symbol2);
}

bool STC_IsManagedMagic(STC_Config &cfg, const long magic)
{
   return (magic == cfg.magic_number);
}

bool STC_IsManagedBrokerPosition(STC_Config &cfg, const string symbol, const long magic)
{
   return STC_IsPairSymbol(cfg, symbol) && STC_IsManagedMagic(cfg, magic);
}

bool STC_AppendBrokerPositionCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, STC_BrokerPositionAudit &audit)
{
   if(!cfg.write_broker_position_audit) return true;
   bool exists = FileIsExist(state.broker_position_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.broker_position_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append broker position CSV ", state.broker_position_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "ny_time", "stc_day_id", "runtime_mode", "run_id", "symbol1", "symbol2", "magic_config",
         "ticket", "position_identifier", "symbol", "position_magic", "position_type", "volume", "price_open", "price_current", "stop_loss", "take_profit", "profit", "swap", "commission", "open_time", "update_time",
         "symbol_is_pair_member", "magic_matches", "managed_by_stc", "hard_close_due", "scan_status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(audit.server_time), STC_TimeText(audit.ny_time), audit.stc_day_id, STC_RuntimeModeText(cfg.runtime_mode), cfg.run_id, cfg.symbol1, cfg.symbol2, IntegerToString(cfg.magic_number),
      IntegerToString((long)audit.ticket), IntegerToString(audit.position_identifier), audit.symbol, IntegerToString(audit.magic), audit.position_type, DoubleToString(audit.volume, 8), DoubleToString(audit.price_open, 8), DoubleToString(audit.price_current, 8), DoubleToString(audit.stop_loss, 8), DoubleToString(audit.take_profit, 8), DoubleToString(audit.profit, 2), DoubleToString(audit.swap, 2), DoubleToString(audit.commission, 2), STC_TimeText(audit.open_time), STC_TimeText(audit.update_time),
      STC_BoolText(audit.symbol_is_pair_member), STC_BoolText(audit.magic_matches), STC_BoolText(audit.managed_by_stc), STC_BoolText(audit.hard_close_due), audit.scan_status, audit.rule_note);
   FileClose(h);
   state.broker_position_rows_audited++;
   return true;
}

bool STC_AppendBrokerActionCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, STC_BrokerActionAudit &audit)
{
   bool exists = FileIsExist(state.broker_action_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.broker_action_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append broker action CSV ", state.broker_action_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "ny_time", "stc_day_id", "runtime_mode", "run_id", "symbol1", "symbol2", "magic_config",
         "action_type", "ticket", "symbol", "position_magic", "position_type", "volume", "action_allowed", "action_attempted", "action_succeeded", "trade_result_retcode", "trade_result_comment", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(audit.server_time), STC_TimeText(audit.ny_time), audit.stc_day_id, STC_RuntimeModeText(cfg.runtime_mode), cfg.run_id, cfg.symbol1, cfg.symbol2, IntegerToString(cfg.magic_number),
      audit.action_type, IntegerToString((long)audit.ticket), audit.symbol, IntegerToString(audit.magic), audit.position_type, DoubleToString(audit.volume, 8), STC_BoolText(audit.action_allowed), STC_BoolText(audit.action_attempted), STC_BoolText(audit.action_succeeded), audit.trade_result_retcode, audit.trade_result_comment, audit.status, audit.rule_note);
   FileClose(h);
   state.broker_action_rows_audited++;
   return true;
}

void STC_BuildBrokerPositionAuditFromSelected(STC_Config &cfg, STC_TimeSnapshot &snap, STC_BrokerPositionAudit &audit)
{
   STC_ResetBrokerPositionAudit(audit);
   audit.stc_day_id = snap.stc_day_id;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   audit.position_identifier = PositionGetInteger(POSITION_IDENTIFIER);
   audit.symbol = PositionGetString(POSITION_SYMBOL);
   audit.magic = PositionGetInteger(POSITION_MAGIC);
   audit.position_type = STC_BrokerPositionTypeText(PositionGetInteger(POSITION_TYPE));
   audit.volume = PositionGetDouble(POSITION_VOLUME);
   audit.price_open = PositionGetDouble(POSITION_PRICE_OPEN);
   audit.price_current = PositionGetDouble(POSITION_PRICE_CURRENT);
   audit.stop_loss = PositionGetDouble(POSITION_SL);
   audit.take_profit = PositionGetDouble(POSITION_TP);
   audit.profit = PositionGetDouble(POSITION_PROFIT);
   audit.swap = PositionGetDouble(POSITION_SWAP);
   audit.commission = 0.0;
   audit.open_time = (datetime)PositionGetInteger(POSITION_TIME);
   audit.update_time = (datetime)PositionGetInteger(POSITION_TIME_UPDATE);
   audit.symbol_is_pair_member = STC_IsPairSymbol(cfg, audit.symbol);
   audit.magic_matches = STC_IsManagedMagic(cfg, audit.magic);
   audit.managed_by_stc = STC_IsManagedBrokerPosition(cfg, audit.symbol, audit.magic);
   audit.hard_close_due = snap.hard_close_due;
   audit.scan_status = audit.managed_by_stc ? "MANAGED_MAGIC_POSITION" : (audit.symbol_is_pair_member ? "PAIR_SYMBOL_FOREIGN_MAGIC" : "IGNORED_NOT_PAIR_SYMBOL");
   audit.rule_note = "Level15 scans broker positions but manages only Symbol1/Symbol2 positions with matching magic number.";
}

bool STC_RealHardCloseTransportAllowed(STC_Config &cfg)
{
   if(!cfg.enable_broker_position_manager) return false;
   if(!cfg.enable_real_hard_close) return false;
   if(cfg.runtime_mode == STC_MODE_AUTO_TRADE) return true;
   if(cfg.runtime_mode == STC_MODE_PAPER_LIVE && cfg.allow_real_close_in_paper_live) return true;
   return false;
}

void STC_WriteNoPositionBrokerAction(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const string status, const string note)
{
   STC_BrokerActionAudit audit;
   STC_ResetBrokerActionAudit(audit);
   audit.stc_day_id = snap.stc_day_id;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.action_type = "NO_POSITION_ACTION";
   audit.action_allowed = false;
   audit.action_attempted = false;
   audit.action_succeeded = false;
   audit.status = status;
   audit.rule_note = note;
   STC_AppendBrokerActionCsv(cfg, state, snap, audit);
}

void STC_AttemptHardCloseSelectedPosition(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   STC_BrokerActionAudit audit;
   STC_ResetBrokerActionAudit(audit);
   audit.stc_day_id = snap.stc_day_id;
   audit.server_time = TimeCurrent();
   audit.ny_time = snap.ny_time;
   audit.action_type = "REAL_HARD_CLOSE_MAGIC_POSITION";
   audit.ticket = (ulong)PositionGetInteger(POSITION_TICKET);
   audit.symbol = PositionGetString(POSITION_SYMBOL);
   audit.magic = PositionGetInteger(POSITION_MAGIC);
   audit.position_type = STC_BrokerPositionTypeText(PositionGetInteger(POSITION_TYPE));
   audit.volume = PositionGetDouble(POSITION_VOLUME);
   audit.action_allowed = STC_RealHardCloseTransportAllowed(cfg) && snap.hard_close_due && STC_IsManagedBrokerPosition(cfg, audit.symbol, audit.magic);
   audit.action_attempted = false;
   audit.action_succeeded = false;
   audit.status = "NOT_ATTEMPTED";
   audit.rule_note = "Only matching magic positions on Symbol1/Symbol2 are eligible for real hard close.";

   if(!audit.action_allowed)
   {
      audit.status = "BLOCKED_BY_SAFETY";
      if(!snap.hard_close_due) audit.rule_note = "Hard close is not due yet.";
      else if(!STC_RealHardCloseTransportAllowed(cfg)) audit.rule_note = "Real hard close transport is disabled by inputs or runtime mode.";
      else audit.rule_note = "Position is not managed by this STC strategy instance.";
      STC_AppendBrokerActionCsv(cfg, state, snap, audit);
      return;
   }

   CTrade trade;
   trade.SetExpertMagicNumber(cfg.magic_number);
   trade.SetDeviationInPoints(cfg.broker_close_deviation_points);
   ResetLastError();
   audit.action_attempted = true;
   bool ok = trade.PositionClose(audit.ticket, cfg.broker_close_deviation_points);
   audit.action_succeeded = ok;
   audit.trade_result_retcode = (int)trade.ResultRetcode();
   audit.trade_result_comment = trade.ResultComment();
   audit.status = ok ? "CLOSE_SENT_OK" : "CLOSE_FAILED";
   audit.rule_note = ok ? "Magic-only hard close order sent." : ("Magic-only hard close failed; err=" + IntegerToString(GetLastError()));
   STC_AppendBrokerActionCsv(cfg, state, snap, audit);
}

void STC_ProcessBrokerPositionManager(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap, const bool force_scan)
{
   if(!cfg.enable_broker_position_manager)
   {
      state.broker_position_scan_status = "DISABLED";
      return;
   }

   datetime now = TimeCurrent();
   bool due_scan = force_scan || state.last_broker_position_scan_server_time <= 0 || now - state.last_broker_position_scan_server_time >= cfg.broker_position_scan_seconds;
   bool due_hard_close_retry = snap.hard_close_due && (state.last_real_hard_close_attempt_server_time <= 0 || now - state.last_real_hard_close_attempt_server_time >= cfg.hard_close_retry_seconds);
   if(!due_scan && !due_hard_close_retry)
      return;

   state.last_broker_position_scan_server_time = now;
   state.broker_managed_positions_last_scan = 0;
   state.broker_foreign_pair_positions_last_scan = 0;
   int total_positions = PositionsTotal();
   int audited = 0;

   for(int i = total_positions - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0) continue;
      if(!PositionSelectByTicket(ticket)) continue;

      string symbol = PositionGetString(POSITION_SYMBOL);
      long magic = PositionGetInteger(POSITION_MAGIC);
      bool pair_symbol = STC_IsPairSymbol(cfg, symbol);
      bool managed = STC_IsManagedBrokerPosition(cfg, symbol, magic);
      if(managed) state.broker_managed_positions_last_scan++;
      if(pair_symbol && !managed) state.broker_foreign_pair_positions_last_scan++;
      if(!managed && !(cfg.audit_foreign_pair_positions && pair_symbol))
         continue;

      STC_BrokerPositionAudit position_audit;
      STC_BuildBrokerPositionAuditFromSelected(cfg, snap, position_audit);
      STC_AppendBrokerPositionCsv(cfg, state, snap, position_audit);
      audited++;

      if(managed && snap.hard_close_due && due_hard_close_retry)
         STC_AttemptHardCloseSelectedPosition(cfg, state, snap);
   }

   if(snap.hard_close_due && due_hard_close_retry)
   {
      state.last_real_hard_close_attempt_server_time = now;
      if(state.broker_managed_positions_last_scan <= 0)
         STC_WriteNoPositionBrokerAction(cfg, state, snap, "NO_MANAGED_POSITIONS", "Hard close due but no Symbol1/Symbol2 position with this magic number exists.");
   }

   state.broker_position_scan_status = "SCANNED";
   state.broker_hard_close_status = snap.hard_close_due ? (STC_RealHardCloseTransportAllowed(cfg) ? "REAL_HARD_CLOSE_ARMED" : "REAL_HARD_CLOSE_TRANSPORT_DISABLED") : "NOT_DUE";

   if(audited == 0 && cfg.write_broker_position_audit)
   {
      STC_BrokerPositionAudit empty_audit;
      STC_ResetBrokerPositionAudit(empty_audit);
      empty_audit.stc_day_id = snap.stc_day_id;
      empty_audit.server_time = now;
      empty_audit.ny_time = snap.ny_time;
      empty_audit.hard_close_due = snap.hard_close_due;
      empty_audit.scan_status = "NO_AUDITABLE_POSITIONS";
      empty_audit.rule_note = "No managed magic positions and no auditable foreign pair positions were found.";
      STC_AppendBrokerPositionCsv(cfg, state, snap, empty_audit);
   }
}

#endif
