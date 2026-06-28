#ifndef __DAL_STC_JOURNAL_MQH__
#define __DAL_STC_JOURNAL_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Config.mqh>

bool STC_WriteBuildSanityCsv(STC_Config &cfg, STC_RuntimeState &state, STC_BuildSanity &sanity)
{
   int h = FileOpen(state.sanity_file_common, FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to write build sanity CSV ", state.sanity_file_common, " err=", GetLastError());
      return false;
   }

   FileWrite(h, "field", "value");
   FileWrite(h, "strategy_id", sanity.strategy_id);
   FileWrite(h, "module_level", sanity.module_level);
   FileWrite(h, "build_version", sanity.build_version);
   FileWrite(h, "build_scope", sanity.build_scope);
   FileWrite(h, "locked_contract", sanity.locked_contract);
   FileWrite(h, "created_server_time", STC_TimeText(TimeCurrent()));
   FileWrite(h, "terminal_common_data_path", TerminalInfoString(TERMINAL_COMMONDATA_PATH));
   FileWrite(h, "account_login", IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)));
   FileWrite(h, "terminal_build", IntegerToString(TerminalInfoInteger(TERMINAL_BUILD)));
   FileWrite(h, "runtime_mode", STC_RuntimeModeText(cfg.runtime_mode));
   FileWrite(h, "run_id", cfg.run_id);
   FileWrite(h, "symbol1", cfg.symbol1);
   FileWrite(h, "symbol2", cfg.symbol2);
   FileWrite(h, "entry_stc_enabled", STC_BoolText(cfg.entry_stc_enabled));
   FileWrite(h, "partial_enabled", STC_BoolText(cfg.partial_enabled));
   FileWrite(h, "hedging_enabled", STC_BoolText(cfg.hedging_enabled));
   FileWrite(h, "final_reward_r", DoubleToString(cfg.final_reward_r, 6));
   FileWrite(h, "risk_percent", DoubleToString(cfg.risk_percent, 6));
   FileWrite(h, "check_tf", STC_CheckTfText(cfg.check_tf));
   FileWrite(h, "check_minutes", cfg.check_minutes);
   FileWrite(h, "contract_size", DoubleToString(cfg.contract_size, 6));
   FileWrite(h, "broker_utc_offset_hours", DoubleToString(cfg.broker_utc_offset_hours, 6));
   FileWrite(h, "timer_seconds", cfg.timer_seconds);
   FileWrite(h, "magic_number", IntegerToString(cfg.magic_number));
   FileWrite(h, "output_root_common", cfg.output_root_common);
   FileWrite(h, "instance_lock_enabled", STC_BoolText(cfg.use_instance_lock));
   FileWrite(h, "instance_lock_name", state.lock_name);
   FileWrite(h, "strict_symbol_validation", STC_BoolText(cfg.strict_symbol_validation));
   FileWrite(h, "drawing_enabled", STC_BoolText(cfg.enable_drawing));
   FileWrite(h, "heartbeat_enabled", STC_BoolText(cfg.write_heartbeat));
   FileWrite(h, "heartbeat_seconds", cfg.heartbeat_seconds);
   FileWrite(h, "hard_close_retry_seconds", cfg.hard_close_retry_seconds);
   FileWrite(h, "use_broker_costs_for_reporting", STC_BoolText(cfg.use_broker_costs_for_reporting));
   FileWrite(h, "fallback_spread_points", DoubleToString(cfg.fallback_spread_points, 6));
   FileWrite(h, "fallback_commission_per_lot", DoubleToString(cfg.fallback_commission_per_lot, 6));
   FileWrite(h, "locked_rules", STC_LockedRulesOneLine());
   FileWrite(h, "validation_warning", state.init_warning);
   FileClose(h);
   return true;
}

bool STC_AppendRuntimeEventCsv(STC_Config &cfg, STC_RuntimeState &state, const string event_type, const string details)
{
   bool exists = FileIsExist(state.runtime_events_file_common, FILE_COMMON);
   int h = FileOpen(state.runtime_events_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append runtime event CSV ", state.runtime_events_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h, "server_time", "strategy_id", "run_id", "runtime_mode", "symbol1", "symbol2", "magic", "pulse_count", "event_type", "details");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
             STC_TimeText(TimeCurrent()),
             cfg.strategy_id,
             cfg.run_id,
             STC_RuntimeModeText(cfg.runtime_mode),
             cfg.symbol1,
             cfg.symbol2,
             IntegerToString(cfg.magic_number),
             state.pulse_count,
             event_type,
             details);
   FileClose(h);
   return true;
}

#endif
