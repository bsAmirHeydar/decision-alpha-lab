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
   FileWrite(h, "time_audit_enabled", STC_BoolText(cfg.write_time_audit));
   FileWrite(h, "time_audit_seconds", cfg.time_audit_seconds);
   FileWrite(h, "hard_close_retry_seconds", cfg.hard_close_retry_seconds);
   FileWrite(h, "use_broker_costs_for_reporting", STC_BoolText(cfg.use_broker_costs_for_reporting));
   FileWrite(h, "fallback_spread_points", DoubleToString(cfg.fallback_spread_points, 6));
   FileWrite(h, "fallback_commission_per_lot", DoubleToString(cfg.fallback_commission_per_lot, 6));
   FileWrite(h, "time_audit_file_common", state.time_audit_file_common);
   FileWrite(h, "check_candle_audit_enabled", STC_BoolText(cfg.write_check_candle_audit));
   FileWrite(h, "check_candle_audit_file_common", state.check_candle_audit_file_common);
   FileWrite(h, "max_check_backfill_on_init", cfg.max_check_backfill_on_init);
   FileWrite(h, "max_check_catchup_per_pulse", cfg.max_check_catchup_per_pulse);
   FileWrite(h, "w_level_audit_enabled", STC_BoolText(cfg.write_w_level_audit));
   FileWrite(h, "w_level_audit_file_common", state.w_level_audit_file_common);
   FileWrite(h, "max_w_level_backfill_on_init", cfg.max_w_level_backfill_on_init);
   FileWrite(h, "max_w_level_catchup_per_pulse", cfg.max_w_level_catchup_per_pulse);
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

bool STC_AppendTimeAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_TimeSnapshot &snap)
{
   bool exists = FileIsExist(state.time_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.time_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append time audit CSV ", state.time_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_time", "utc_time", "ny_time", "ny_dst", "broker_utc_offset_seconds", "ny_utc_offset_seconds",
         "stc_day_id", "stc_day_start_ny", "stc_day_end_ny", "elapsed_minutes_from_2000",
         "phase", "phase_reason", "inside_stc_day", "detection_allowed", "entry_allowed_now", "hard_close_due",
         "m_cycle", "w_cycle", "m_start_ny", "m_end_ny", "w_start_ny", "w_end_ny",
         "check_minutes", "check_index", "check_start_ny", "check_end_ny", "check_start_elapsed", "check_end_elapsed",
         "check_inside_active_m", "check_close_inside_m", "final_check_of_m", "check_entry_allowed_at_close");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(snap.server_time),
      STC_TimeText(snap.utc_time),
      STC_TimeText(snap.ny_time),
      STC_BoolText(snap.ny_dst),
      snap.broker_utc_offset_seconds,
      snap.ny_utc_offset_seconds,
      snap.stc_day_id,
      STC_TimeText(snap.stc_day_start_ny),
      STC_TimeText(snap.stc_day_end_ny),
      snap.elapsed_minutes_from_2000,
      STC_TimePhaseText(snap.phase),
      snap.phase_reason,
      STC_BoolText(snap.inside_stc_day),
      STC_BoolText(snap.detection_allowed),
      STC_BoolText(snap.entry_allowed_now),
      STC_BoolText(snap.hard_close_due),
      STC_MCycleText(snap.m_cycle),
      STC_WCycleText(snap.w_cycle),
      STC_TimeText(snap.m_start_ny),
      STC_TimeText(snap.m_end_ny),
      STC_TimeText(snap.w_start_ny),
      STC_TimeText(snap.w_end_ny),
      snap.check_minutes,
      snap.check_index,
      STC_TimeText(snap.check_start_ny),
      STC_TimeText(snap.check_end_ny),
      snap.check_start_elapsed_minutes,
      snap.check_end_elapsed_minutes,
      STC_BoolText(snap.check_inside_active_m),
      STC_BoolText(snap.check_close_inside_m),
      STC_BoolText(snap.final_check_of_m),
      STC_BoolText(snap.check_entry_allowed_at_close));
   FileClose(h);
   return true;
}

bool STC_AppendCheckCandleAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_CheckCandleAudit &audit)
{
   bool exists = FileIsExist(state.check_candle_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.check_candle_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append check candle audit CSV ", state.check_candle_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "check_index", "check_minutes", "check_start_ny", "check_end_ny", "check_start_server", "check_end_server",
         "check_start_elapsed", "check_end_elapsed", "m_cycle", "w_cycle",
         "start_inside_active_m", "close_inside_m", "final_check_of_m", "entry_allowed_at_close", "detection_allowed_for_signal", "pair_data_complete", "skip_reason",
         "s1_symbol", "s1_selected", "s1_complete", "s1_expected_m1", "s1_actual_m1", "s1_first_m1_server", "s1_last_m1_server", "s1_open", "s1_high", "s1_low", "s1_close", "s1_tick_volume", "s1_real_volume", "s1_spread_max", "s1_status",
         "s2_symbol", "s2_selected", "s2_complete", "s2_expected_m1", "s2_actual_m1", "s2_first_m1_server", "s2_last_m1_server", "s2_open", "s2_high", "s2_low", "s2_close", "s2_tick_volume", "s2_real_volume", "s2_spread_max", "s2_status");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.check_index, audit.check_minutes, STC_TimeText(audit.check_start_ny), STC_TimeText(audit.check_end_ny), STC_TimeText(audit.check_start_server), STC_TimeText(audit.check_end_server),
      audit.check_start_elapsed_minutes, audit.check_end_elapsed_minutes, STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.w_cycle),
      STC_BoolText(audit.start_inside_active_m), STC_BoolText(audit.close_inside_m), STC_BoolText(audit.final_check_of_m), STC_BoolText(audit.entry_allowed_at_close), STC_BoolText(audit.detection_allowed_for_signal), STC_BoolText(audit.pair_data_complete), audit.skip_reason,
      audit.symbol1.symbol, STC_BoolText(audit.symbol1.selected), STC_BoolText(audit.symbol1.complete), audit.symbol1.expected_m1_bars, audit.symbol1.actual_m1_bars, STC_TimeText(audit.symbol1.first_m1_server_time), STC_TimeText(audit.symbol1.last_m1_server_time),
      DoubleToString(audit.symbol1.open, 8), DoubleToString(audit.symbol1.high, 8), DoubleToString(audit.symbol1.low, 8), DoubleToString(audit.symbol1.close, 8), audit.symbol1.tick_volume, audit.symbol1.real_volume, audit.symbol1.spread_max, audit.symbol1.status,
      audit.symbol2.symbol, STC_BoolText(audit.symbol2.selected), STC_BoolText(audit.symbol2.complete), audit.symbol2.expected_m1_bars, audit.symbol2.actual_m1_bars, STC_TimeText(audit.symbol2.first_m1_server_time), STC_TimeText(audit.symbol2.last_m1_server_time),
      DoubleToString(audit.symbol2.open, 8), DoubleToString(audit.symbol2.high, 8), DoubleToString(audit.symbol2.low, 8), DoubleToString(audit.symbol2.close, 8), audit.symbol2.tick_volume, audit.symbol2.real_volume, audit.symbol2.spread_max, audit.symbol2.status);
   FileClose(h);
   return true;
}


bool STC_AppendWLevelAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_WLevelAudit &audit)
{
   bool exists = FileIsExist(state.w_level_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.w_level_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append W level audit CSV ", state.w_level_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "w_serial", "m_cycle", "w_cycle", "w_start_ny", "w_end_ny", "w_start_server", "w_end_server", "w_start_elapsed", "w_end_elapsed",
         "w_closed", "w1_no_signal", "future_reference_candidate", "pair_data_complete", "signal_reference_set_for_this_w", "future_reference_role", "status",
         "s1_symbol", "s1_selected", "s1_complete", "s1_expected_m1", "s1_actual_m1", "s1_first_m1_server", "s1_last_m1_server", "s1_open", "s1_high", "s1_low", "s1_close", "s1_tick_volume", "s1_real_volume", "s1_spread_max", "s1_status",
         "s2_symbol", "s2_selected", "s2_complete", "s2_expected_m1", "s2_actual_m1", "s2_first_m1_server", "s2_last_m1_server", "s2_open", "s2_high", "s2_low", "s2_close", "s2_tick_volume", "s2_real_volume", "s2_spread_max", "s2_status");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.w_serial, STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.w_cycle), STC_TimeText(audit.w_start_ny), STC_TimeText(audit.w_end_ny), STC_TimeText(audit.w_start_server), STC_TimeText(audit.w_end_server), audit.w_start_elapsed_minutes, audit.w_end_elapsed_minutes,
      STC_BoolText(audit.w_closed), STC_BoolText(audit.w1_no_signal), STC_BoolText(audit.future_reference_candidate), STC_BoolText(audit.pair_data_complete), audit.signal_reference_set_for_this_w, audit.future_reference_role, audit.status,
      audit.symbol1.symbol, STC_BoolText(audit.symbol1.selected), STC_BoolText(audit.symbol1.complete), audit.symbol1.expected_m1_bars, audit.symbol1.actual_m1_bars, STC_TimeText(audit.symbol1.first_m1_server_time), STC_TimeText(audit.symbol1.last_m1_server_time),
      DoubleToString(audit.symbol1.open, 8), DoubleToString(audit.symbol1.high, 8), DoubleToString(audit.symbol1.low, 8), DoubleToString(audit.symbol1.close, 8), audit.symbol1.tick_volume, audit.symbol1.real_volume, audit.symbol1.spread_max, audit.symbol1.status,
      audit.symbol2.symbol, STC_BoolText(audit.symbol2.selected), STC_BoolText(audit.symbol2.complete), audit.symbol2.expected_m1_bars, audit.symbol2.actual_m1_bars, STC_TimeText(audit.symbol2.first_m1_server_time), STC_TimeText(audit.symbol2.last_m1_server_time),
      DoubleToString(audit.symbol2.open, 8), DoubleToString(audit.symbol2.high, 8), DoubleToString(audit.symbol2.low, 8), DoubleToString(audit.symbol2.close, 8), audit.symbol2.tick_volume, audit.symbol2.real_volume, audit.symbol2.spread_max, audit.symbol2.status);
   FileClose(h);
   return true;
}

#endif
