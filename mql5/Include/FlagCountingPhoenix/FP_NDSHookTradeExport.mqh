#ifndef __FP_NDS_HOOK_TRADE_EXPORT_MQH__
#define __FP_NDS_HOOK_TRADE_EXPORT_MQH__
#property strict

#include "FP_NDSHookTradeRules.mqh"

string FP_NDSHookTradeCsvSafe(string value)
{
   StringReplace(value, "\"", "\"\"");
   return "\"" + value + "\"";
}

string FP_NDSHookTradeCsvHeader()
{
   return "generated_at,version,schema_version,symbol,period,attempted,ok,action,status,reason,managed_pending,managed_positions,foreign_symbol_positions,order_ticket,position_ticket,close_ticket,setup_sequence_id,setup_family,setup_direction,setup_entry,setup_death,setup_stop,setup_volume,setup_used,setup_key,exit_found,exit_event_id,exit_sequence_id,exit_f1_start,exit_f2_start,exit_f3_terminal,exit_f3_price,state_key";
}

string FP_NDSHookTradeCsvRow(const FP_NDSHookTradeReport &r)
{
   string s = FP_NDSHookTradeCsvSafe(TimeToString(r.generated_at, TIME_DATE|TIME_SECONDS));
   s += "," + FP_NDSHookTradeCsvSafe(r.version);
   s += "," + FP_NDSHookTradeCsvSafe(r.schema_version);
   s += "," + FP_NDSHookTradeCsvSafe(r.symbol);
   s += "," + FP_NDSHookTradeCsvSafe(EnumToString(r.period));
   s += "," + FP_NDSHookTradeBool(r.attempted);
   s += "," + FP_NDSHookTradeBool(r.ok);
   s += "," + FP_NDSHookTradeCsvSafe(r.action_label);
   s += "," + FP_NDSHookTradeCsvSafe(r.status);
   s += "," + FP_NDSHookTradeCsvSafe(r.reason);
   s += "," + IntegerToString(r.managed_pending_count);
   s += "," + IntegerToString(r.managed_position_count);
   s += "," + IntegerToString(r.foreign_symbol_position_count);
   s += "," + IntegerToString((long)r.order_ticket);
   s += "," + IntegerToString((long)r.position_ticket);
   s += "," + IntegerToString((long)r.close_ticket);
   s += "," + IntegerToString(r.setup.sequence_id);
   s += "," + FP_NDSHookTradeCsvSafe(r.setup.family);
   s += "," + FP_NDSHookTradeCsvSafe(r.setup.direction_label);
   s += "," + DoubleToString(r.setup.entry_price, _Digits);
   s += "," + DoubleToString(r.setup.death_price, _Digits);
   s += "," + DoubleToString(r.setup.stop_price, _Digits);
   s += "," + DoubleToString(r.setup.volume, 8);
   s += "," + FP_NDSHookTradeBool(r.setup.already_used);
   s += "," + FP_NDSHookTradeCsvSafe(r.setup.setup_key);
   s += "," + FP_NDSHookTradeBool(r.exit_signal.found);
   s += "," + IntegerToString(r.exit_signal.event_id);
   s += "," + IntegerToString(r.exit_signal.sequence_id);
   s += "," + FP_NDSHookTradeCsvSafe(r.exit_signal.f1_start_time > 0 ? TimeToString(r.exit_signal.f1_start_time, TIME_DATE|TIME_SECONDS) : "");
   s += "," + FP_NDSHookTradeCsvSafe(r.exit_signal.f2_start_time > 0 ? TimeToString(r.exit_signal.f2_start_time, TIME_DATE|TIME_SECONDS) : "");
   s += "," + FP_NDSHookTradeCsvSafe(r.exit_signal.f3_terminal_time > 0 ? TimeToString(r.exit_signal.f3_terminal_time, TIME_DATE|TIME_SECONDS) : "");
   s += "," + DoubleToString(r.exit_signal.f3_terminal_price, _Digits);
   s += "," + FP_NDSHookTradeCsvSafe(r.state_key);
   return s;
}

bool FP_NDSHookTradeExportReport(const FP_NDSHookTradeConfig &cfg,
                                 const FP_NDSHookTradeReport &report)
{
   if(!cfg.export_csv)
      return true;

   string path = cfg.folder + "/nds_hook_limit_f123_trade_ledger.csv";
   int handle = FileOpen(path, FILE_READ|FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(handle == INVALID_HANDLE)
      return false;

   if(FileSize(handle) <= 0)
      FileWriteString(handle, FP_NDSHookTradeCsvHeader() + "\r\n");
   FileSeek(handle, 0, SEEK_END);
   FileWriteString(handle, FP_NDSHookTradeCsvRow(report) + "\r\n");
   FileFlush(handle);
   FileClose(handle);
   return true;
}

#endif // __FP_NDS_HOOK_TRADE_EXPORT_MQH__
