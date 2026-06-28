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
   FileWrite(h, "hunt_audit_enabled", STC_BoolText(cfg.write_hunt_audit));
   FileWrite(h, "hunt_audit_file_common", state.hunt_audit_file_common);
   FileWrite(h, "max_hunt_backfill_on_init", cfg.max_hunt_backfill_on_init);
   FileWrite(h, "max_hunt_catchup_per_pulse", cfg.max_hunt_catchup_per_pulse);
   FileWrite(h, "smt_candidate_audit_enabled", STC_BoolText(cfg.write_smt_candidate_audit));
   FileWrite(h, "smt_candidate_audit_file_common", state.smt_candidate_audit_file_common);
   FileWrite(h, "max_smt_backfill_on_init", cfg.max_smt_backfill_on_init);
   FileWrite(h, "max_smt_catchup_per_pulse", cfg.max_smt_catchup_per_pulse);
   FileWrite(h, "signal_registry_audit_enabled", STC_BoolText(cfg.write_signal_registry_audit));
   FileWrite(h, "signal_registry_file_common", state.signal_registry_file_common);
   FileWrite(h, "max_signal_backfill_on_init", cfg.max_signal_backfill_on_init);
   FileWrite(h, "max_signal_catchup_per_pulse", cfg.max_signal_catchup_per_pulse);
   FileWrite(h, "paper_entry_audit_enabled", STC_BoolText(cfg.write_paper_entry_audit));
   FileWrite(h, "paper_entry_file_common", state.paper_entry_file_common);
   FileWrite(h, "max_paper_entry_backfill_on_init", cfg.max_paper_entry_backfill_on_init);
   FileWrite(h, "max_paper_entry_catchup_per_pulse", cfg.max_paper_entry_catchup_per_pulse);
   FileWrite(h, "paper_outcome_audit_enabled", STC_BoolText(cfg.write_paper_outcome_audit));
   FileWrite(h, "paper_outcome_file_common", state.paper_outcome_file_common);
   FileWrite(h, "max_paper_outcome_backfill_on_init", cfg.max_paper_outcome_backfill_on_init);
   FileWrite(h, "max_paper_outcome_catchup_per_pulse", cfg.max_paper_outcome_catchup_per_pulse);
   FileWrite(h, "max_paper_outcome_forward_checks", cfg.max_paper_outcome_forward_checks);
   FileWrite(h, "partial_audit_enabled", STC_BoolText(cfg.write_partial_audit));
   FileWrite(h, "partial_audit_file_common", state.partial_audit_file_common);
   FileWrite(h, "max_partial_backfill_on_init", cfg.max_partial_backfill_on_init);
   FileWrite(h, "max_partial_catchup_per_pulse", cfg.max_partial_catchup_per_pulse);
   FileWrite(h, "hard_close_audit_enabled", STC_BoolText(cfg.write_hard_close_audit));
   FileWrite(h, "hard_close_audit_file_common", state.hard_close_audit_file_common);
   FileWrite(h, "max_hard_close_backfill_on_init", cfg.max_hard_close_backfill_on_init);
   FileWrite(h, "max_hard_close_catchup_per_pulse", cfg.max_hard_close_catchup_per_pulse);
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


bool STC_AppendReferenceHuntAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_ReferenceHuntAudit &audit)
{
   bool exists = FileIsExist(state.hunt_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.hunt_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append reference hunt audit CSV ", state.hunt_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "check_index", "check_minutes", "check_start_ny", "check_end_ny", "check_start_server", "check_end_server",
         "m_cycle", "current_w", "reference_w", "reference_w_serial", "reference_rank",
         "detection_allowed_for_signal", "entry_allowed_at_close", "final_check_of_m", "check_pair_data_complete", "reference_pair_data_complete", "pair_data_complete", "status", "rule_note",
         "s1_reference_high", "s1_reference_low", "s1_check_high", "s1_check_low", "s1_high_hunt", "s1_low_hunt",
         "s2_reference_high", "s2_reference_low", "s2_check_high", "s2_check_low", "s2_high_hunt", "s2_low_hunt",
         "high_hunt_pattern", "low_hunt_pattern", "high_exactly_one_hunted", "low_exactly_one_hunted", "high_hunted_symbol", "high_clean_symbol", "low_hunted_symbol", "low_clean_symbol");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.check_index, audit.check_minutes, STC_TimeText(audit.check_start_ny), STC_TimeText(audit.check_end_ny), STC_TimeText(audit.check_start_server), STC_TimeText(audit.check_end_server),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_WCycleText(audit.reference_w_cycle), audit.reference_w_serial, audit.reference_rank,
      STC_BoolText(audit.detection_allowed_for_signal), STC_BoolText(audit.entry_allowed_at_close), STC_BoolText(audit.final_check_of_m), STC_BoolText(audit.check_pair_data_complete), STC_BoolText(audit.reference_pair_data_complete), STC_BoolText(audit.pair_data_complete), audit.status, audit.rule_note,
      DoubleToString(audit.s1_reference_high, 8), DoubleToString(audit.s1_reference_low, 8), DoubleToString(audit.s1_check_high, 8), DoubleToString(audit.s1_check_low, 8), STC_BoolText(audit.s1_high_hunt), STC_BoolText(audit.s1_low_hunt),
      DoubleToString(audit.s2_reference_high, 8), DoubleToString(audit.s2_reference_low, 8), DoubleToString(audit.s2_check_high, 8), DoubleToString(audit.s2_check_low, 8), STC_BoolText(audit.s2_high_hunt), STC_BoolText(audit.s2_low_hunt),
      STC_HuntPatternText(audit.high_hunt_pattern), STC_HuntPatternText(audit.low_hunt_pattern), STC_BoolText(audit.high_exactly_one_hunted), STC_BoolText(audit.low_exactly_one_hunted), audit.high_hunted_symbol, audit.high_clean_symbol, audit.low_hunted_symbol, audit.low_clean_symbol);
   FileClose(h);
   return true;
}

bool STC_AppendSMTCandidateAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_SMTCandidateAudit &audit)
{
   bool exists = FileIsExist(state.smt_candidate_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.smt_candidate_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append SMT candidate audit CSV ", state.smt_candidate_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "check_index", "check_minutes", "check_start_ny", "check_end_ny", "check_start_server", "check_end_server",
         "m_cycle", "current_w", "detection_allowed_for_signal", "entry_allowed_at_close", "final_check_of_m", "check_pair_data_complete",
         "candidate_status", "candidate_id", "is_trade_candidate", "smt_side", "direction", "hunted_symbol", "clean_symbol", "trade_symbol",
         "selected_reference_w", "selected_reference_w_serial", "selected_reference_rank", "selected_reference_price", "trade_symbol_check_close", "provisional_stop_distance",
         "legal_reference_count", "high_raw_candidate_count", "low_raw_candidate_count", "same_direction_candidate_count", "simultaneous_buy_sell_forget", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.check_index, audit.check_minutes, STC_TimeText(audit.check_start_ny), STC_TimeText(audit.check_end_ny), STC_TimeText(audit.check_start_server), STC_TimeText(audit.check_end_server),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_BoolText(audit.detection_allowed_for_signal), STC_BoolText(audit.entry_allowed_at_close), STC_BoolText(audit.final_check_of_m), STC_BoolText(audit.check_pair_data_complete),
      STC_CandidateStatusText(audit.candidate_status), audit.candidate_id, STC_BoolText(audit.is_trade_candidate), STC_SideText(audit.smt_side), STC_DirectionText(audit.direction), audit.hunted_symbol, audit.clean_symbol, audit.trade_symbol,
      STC_WCycleText(audit.selected_reference_w_cycle), audit.selected_reference_w_serial, audit.selected_reference_rank, DoubleToString(audit.selected_reference_price, 8), DoubleToString(audit.trade_symbol_check_close, 8), DoubleToString(audit.provisional_stop_distance, 8),
      audit.legal_reference_count, audit.high_raw_candidate_count, audit.low_raw_candidate_count, audit.same_direction_candidate_count, STC_BoolText(audit.simultaneous_buy_sell_forget), audit.status, audit.rule_note);
   FileClose(h);
   return true;
}

bool STC_AppendSignalRegistryCsv(STC_Config &cfg, STC_RuntimeState &state, STC_SignalAudit &audit)
{
   bool exists = FileIsExist(state.signal_registry_file_common, FILE_COMMON);
   int h = FileOpen(state.signal_registry_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append signal registry CSV ", state.signal_registry_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "check_index", "check_minutes", "check_start_ny", "check_end_ny", "check_start_server", "check_end_server",
         "m_cycle", "current_w", "detection_allowed_for_signal", "entry_allowed_at_close", "final_check_of_m", "check_pair_data_complete",
         "signal_status", "signal_id", "source_candidate_id", "is_confirmed_signal", "signal_consumed", "entry_stc_enabled_at_confirmation", "entry_missed_or_late", "order_attempted", "trade_counter_incremented",
         "smt_side", "direction", "hunted_symbol", "clean_symbol", "trade_symbol",
         "selected_reference_w", "selected_reference_w_serial", "selected_reference_rank", "selected_reference_price", "trade_symbol_check_close", "provisional_stop_distance",
         "legal_reference_count", "high_raw_candidate_count", "low_raw_candidate_count", "selected_same_direction_count", "simultaneous_buy_sell_forget", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.check_index, audit.check_minutes, STC_TimeText(audit.check_start_ny), STC_TimeText(audit.check_end_ny), STC_TimeText(audit.check_start_server), STC_TimeText(audit.check_end_server),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_BoolText(audit.detection_allowed_for_signal), STC_BoolText(audit.entry_allowed_at_close), STC_BoolText(audit.final_check_of_m), STC_BoolText(audit.check_pair_data_complete),
      STC_SignalStatusText(audit.signal_status), audit.signal_id, audit.source_candidate_id, STC_BoolText(audit.is_confirmed_signal), STC_BoolText(audit.signal_consumed), STC_BoolText(audit.entry_stc_enabled_at_confirmation), STC_BoolText(audit.entry_missed_or_late), STC_BoolText(audit.order_attempted), STC_BoolText(audit.trade_counter_incremented),
      STC_SideText(audit.smt_side), STC_DirectionText(audit.direction), audit.hunted_symbol, audit.clean_symbol, audit.trade_symbol,
      STC_WCycleText(audit.selected_reference_w_cycle), audit.selected_reference_w_serial, audit.selected_reference_rank, DoubleToString(audit.selected_reference_price, 8), DoubleToString(audit.trade_symbol_check_close, 8), DoubleToString(audit.provisional_stop_distance, 8),
      audit.legal_reference_count, audit.high_raw_candidate_count, audit.low_raw_candidate_count, audit.selected_same_direction_count, STC_BoolText(audit.simultaneous_buy_sell_forget), audit.status, audit.rule_note);
   FileClose(h);
   return true;
}


bool STC_AppendPaperEntryAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_PaperEntryAudit &audit)
{
   bool exists = FileIsExist(state.paper_entry_file_common, FILE_COMMON);
   int h = FileOpen(state.paper_entry_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append paper entry CSV ", state.paper_entry_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "signal_check_index", "entry_check_index", "check_minutes", "signal_check_start_ny", "signal_check_end_ny", "entry_check_start_ny", "entry_check_end_ny", "entry_check_start_server", "entry_check_end_server",
         "m_cycle", "current_w", "paper_status", "signal_id", "paper_trade_id", "is_paper_entry", "signal_confirmed", "entry_stc_enabled_at_confirmation", "entry_missed_or_late", "entry_check_pair_data_complete",
         "trade_counter_incremented", "m_trade_count_before", "m_trade_count_after", "m_direction_lock_before", "m_direction_lock_after",
         "direction", "trade_symbol", "hunted_symbol", "clean_symbol", "selected_reference_w", "selected_reference_w_serial", "selected_reference_price",
         "entry_price", "stop_price", "take_profit_price", "risk_distance_price", "reward_distance_price", "final_reward_r",
         "equity_snapshot", "risk_percent", "risk_money", "tick_size", "tick_value", "contract_size_used", "used_tick_value",
         "theoretical_volume", "broker_min_volume", "broker_max_volume", "broker_volume_step", "paper_order_volume", "split_order_count",
         "spread_points_for_report", "commission_per_lot_for_report", "volume_status", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.check_index, audit.entry_check_index, audit.check_minutes, STC_TimeText(audit.signal_check_start_ny), STC_TimeText(audit.signal_check_end_ny), STC_TimeText(audit.entry_check_start_ny), STC_TimeText(audit.entry_check_end_ny), STC_TimeText(audit.entry_check_start_server), STC_TimeText(audit.entry_check_end_server),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_PaperEntryStatusText(audit.paper_status), audit.signal_id, audit.paper_trade_id, STC_BoolText(audit.is_paper_entry), STC_BoolText(audit.signal_confirmed), STC_BoolText(audit.entry_stc_enabled_at_confirmation), STC_BoolText(audit.entry_missed_or_late), STC_BoolText(audit.entry_check_pair_data_complete),
      STC_BoolText(audit.trade_counter_incremented), audit.m_trade_count_before, audit.m_trade_count_after, STC_DirectionText(audit.m_direction_lock_before), STC_DirectionText(audit.m_direction_lock_after),
      STC_DirectionText(audit.direction), audit.trade_symbol, audit.hunted_symbol, audit.clean_symbol, STC_WCycleText(audit.selected_reference_w_cycle), audit.selected_reference_w_serial, DoubleToString(audit.selected_reference_price, 8),
      DoubleToString(audit.entry_price, 8), DoubleToString(audit.stop_price, 8), DoubleToString(audit.take_profit_price, 8), DoubleToString(audit.risk_distance_price, 8), DoubleToString(audit.reward_distance_price, 8), DoubleToString(audit.final_reward_r, 2),
      DoubleToString(audit.equity_snapshot, 2), DoubleToString(audit.risk_percent, 4), DoubleToString(audit.risk_money, 2), DoubleToString(audit.tick_size, 8), DoubleToString(audit.tick_value, 8), DoubleToString(audit.contract_size_used, 8), STC_BoolText(audit.used_tick_value),
      DoubleToString(audit.theoretical_volume, 8), DoubleToString(audit.broker_min_volume, 8), DoubleToString(audit.broker_max_volume, 8), DoubleToString(audit.broker_volume_step, 8), DoubleToString(audit.paper_order_volume, 8), audit.split_order_count,
      DoubleToString(audit.spread_points_for_report, 2), DoubleToString(audit.commission_per_lot_for_report, 2), audit.volume_status, audit.status, audit.rule_note);
   FileClose(h);
   return true;
}


bool STC_AppendPaperOutcomeAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_PaperOutcomeAudit &audit)
{
   bool exists = FileIsExist(state.paper_outcome_file_common, FILE_COMMON);
   int h = FileOpen(state.paper_outcome_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append paper outcome CSV ", state.paper_outcome_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "signal_check_index", "entry_check_index", "exit_check_index", "last_checked_index", "check_minutes",
         "signal_check_start_ny", "signal_check_end_ny", "entry_check_start_ny", "entry_check_end_ny", "exit_check_start_ny", "exit_check_end_ny",
         "m_cycle", "current_w", "outcome_status", "paper_status", "signal_id", "paper_trade_id", "is_paper_entry", "outcome_resolved", "tp_hit", "sl_hit", "ambiguous",
         "direction", "trade_symbol", "hunted_symbol", "clean_symbol",
         "entry_price", "stop_price", "take_profit_price", "exit_price", "last_checked_close", "risk_distance_price", "reward_distance_price", "final_reward_r",
         "paper_order_volume", "split_order_count", "risk_money", "gross_pnl_money", "estimated_cost_money", "net_pnl_money", "realized_r_gross", "realized_r_net", "floating_r_at_last_check",
         "spread_points_for_report", "commission_per_lot_for_report", "scanned_checks", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.signal_check_index, audit.entry_check_index, audit.exit_check_index, audit.last_checked_index, audit.check_minutes,
      STC_TimeText(audit.signal_check_start_ny), STC_TimeText(audit.signal_check_end_ny), STC_TimeText(audit.entry_check_start_ny), STC_TimeText(audit.entry_check_end_ny), STC_TimeText(audit.exit_check_start_ny), STC_TimeText(audit.exit_check_end_ny),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_PaperOutcomeStatusText(audit.outcome_status), STC_PaperEntryStatusText(audit.paper_status), audit.signal_id, audit.paper_trade_id, STC_BoolText(audit.is_paper_entry), STC_BoolText(audit.outcome_resolved), STC_BoolText(audit.tp_hit), STC_BoolText(audit.sl_hit), STC_BoolText(audit.ambiguous),
      STC_DirectionText(audit.direction), audit.trade_symbol, audit.hunted_symbol, audit.clean_symbol,
      DoubleToString(audit.entry_price, 8), DoubleToString(audit.stop_price, 8), DoubleToString(audit.take_profit_price, 8), DoubleToString(audit.exit_price, 8), DoubleToString(audit.last_checked_close, 8), DoubleToString(audit.risk_distance_price, 8), DoubleToString(audit.reward_distance_price, 8), DoubleToString(audit.final_reward_r, 2),
      DoubleToString(audit.paper_order_volume, 8), audit.split_order_count, DoubleToString(audit.risk_money, 2), DoubleToString(audit.gross_pnl_money, 2), DoubleToString(audit.estimated_cost_money, 2), DoubleToString(audit.net_pnl_money, 2), DoubleToString(audit.realized_r_gross, 4), DoubleToString(audit.realized_r_net, 4), DoubleToString(audit.floating_r_at_last_check, 4),
      DoubleToString(audit.spread_points_for_report, 2), DoubleToString(audit.commission_per_lot_for_report, 2), audit.scanned_checks, audit.status, audit.rule_note);
   FileClose(h);
   return true;
}


bool STC_AppendPartialAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_PartialAudit &audit)
{
   bool exists = FileIsExist(state.partial_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.partial_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append partial audit CSV ", state.partial_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "signal_check_index", "entry_check_index", "partial_due_check_index", "last_checked_index", "check_minutes",
         "signal_check_start_ny", "signal_check_end_ny", "entry_check_start_ny", "entry_check_end_ny", "partial_due_ny", "partial_due_server",
         "m_cycle", "current_w", "partial_status", "paper_status", "pre_partial_outcome_status",
         "signal_id", "paper_trade_id", "is_paper_entry", "partial_enabled", "partial_due", "partial_action_taken", "full_close_by_small_volume", "open_at_w4_end",
         "direction", "trade_symbol", "entry_price", "stop_price", "take_profit_price", "paper_order_volume", "broker_volume_step", "close_volume", "remaining_volume", "close_volume_ratio",
         "last_checked_close", "floating_r_at_partial", "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.signal_check_index, audit.entry_check_index, audit.partial_due_check_index, audit.last_checked_index, audit.check_minutes,
      STC_TimeText(audit.signal_check_start_ny), STC_TimeText(audit.signal_check_end_ny), STC_TimeText(audit.entry_check_start_ny), STC_TimeText(audit.entry_check_end_ny), STC_TimeText(audit.partial_due_ny), STC_TimeText(audit.partial_due_server),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_PartialStatusText(audit.partial_status), STC_PaperEntryStatusText(audit.paper_status), STC_PaperOutcomeStatusText(audit.pre_partial_outcome_status),
      audit.signal_id, audit.paper_trade_id, STC_BoolText(audit.is_paper_entry), STC_BoolText(audit.partial_enabled), STC_BoolText(audit.partial_due), STC_BoolText(audit.partial_action_taken), STC_BoolText(audit.full_close_by_small_volume), STC_BoolText(audit.open_at_w4_end),
      STC_DirectionText(audit.direction), audit.trade_symbol, DoubleToString(audit.entry_price, 8), DoubleToString(audit.stop_price, 8), DoubleToString(audit.take_profit_price, 8), DoubleToString(audit.paper_order_volume, 8), DoubleToString(audit.broker_volume_step, 8), DoubleToString(audit.close_volume, 8), DoubleToString(audit.remaining_volume, 8), DoubleToString(audit.close_volume_ratio, 4),
      DoubleToString(audit.last_checked_close, 8), DoubleToString(audit.floating_r_at_partial, 4), audit.status, audit.rule_note);
   FileClose(h);
   return true;
}


bool STC_AppendHardCloseAuditCsv(STC_Config &cfg, STC_RuntimeState &state, STC_HardCloseAudit &audit)
{
   bool exists = FileIsExist(state.hard_close_audit_file_common, FILE_COMMON);
   int h = FileOpen(state.hard_close_audit_file_common, FILE_READ | FILE_WRITE | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(h == INVALID_HANDLE)
   {
      Print("STC: failed to append hard close audit CSV ", state.hard_close_audit_file_common, " err=", GetLastError());
      return false;
   }
   if(!exists || FileSize(h) == 0)
   {
      FileWrite(h,
         "server_write_time", "strategy_id", "run_id", "symbol1", "symbol2", "stc_day_id",
         "signal_check_index", "entry_check_index", "hard_close_check_index", "last_checked_index", "check_minutes",
         "signal_check_start_ny", "signal_check_end_ny", "entry_check_start_ny", "entry_check_end_ny", "hard_close_ny", "hard_close_server",
         "m_cycle", "current_w", "hard_close_status", "paper_status", "pre_hard_outcome_status", "partial_status",
         "signal_id", "paper_trade_id", "is_paper_entry", "hard_close_due", "hard_close_action_taken", "hard_close_recovered_late", "open_at_hard_close",
         "partial_applied_before_hard_close", "partial_full_close_before_hard_close",
         "direction", "trade_symbol", "entry_price", "stop_price", "take_profit_price", "paper_order_volume", "partial_close_volume", "remaining_after_partial_volume",
         "hard_close_volume", "hard_close_price", "risk_distance_price", "risk_money", "floating_r_at_hard_close", "hard_close_gross_pnl_money", "hard_close_net_pnl_money",
         "status", "rule_note");
   }
   FileSeek(h, 0, SEEK_END);
   FileWrite(h,
      STC_TimeText(TimeCurrent()), cfg.strategy_id, cfg.run_id, cfg.symbol1, cfg.symbol2, audit.stc_day_id,
      audit.signal_check_index, audit.entry_check_index, audit.hard_close_check_index, audit.last_checked_index, audit.check_minutes,
      STC_TimeText(audit.signal_check_start_ny), STC_TimeText(audit.signal_check_end_ny), STC_TimeText(audit.entry_check_start_ny), STC_TimeText(audit.entry_check_end_ny), STC_TimeText(audit.hard_close_ny), STC_TimeText(audit.hard_close_server),
      STC_MCycleText(audit.m_cycle), STC_WCycleText(audit.current_w_cycle), STC_HardCloseStatusText(audit.hard_close_status), STC_PaperEntryStatusText(audit.paper_status), STC_PaperOutcomeStatusText(audit.pre_hard_outcome_status), STC_PartialStatusText(audit.partial_status),
      audit.signal_id, audit.paper_trade_id, STC_BoolText(audit.is_paper_entry), STC_BoolText(audit.hard_close_due), STC_BoolText(audit.hard_close_action_taken), STC_BoolText(audit.hard_close_recovered_late), STC_BoolText(audit.open_at_hard_close),
      STC_BoolText(audit.partial_applied_before_hard_close), STC_BoolText(audit.partial_full_close_before_hard_close),
      STC_DirectionText(audit.direction), audit.trade_symbol, DoubleToString(audit.entry_price, 8), DoubleToString(audit.stop_price, 8), DoubleToString(audit.take_profit_price, 8), DoubleToString(audit.paper_order_volume, 8), DoubleToString(audit.partial_close_volume, 8), DoubleToString(audit.remaining_after_partial_volume, 8),
      DoubleToString(audit.hard_close_volume, 8), DoubleToString(audit.hard_close_price, 8), DoubleToString(audit.risk_distance_price, 8), DoubleToString(audit.risk_money, 2), DoubleToString(audit.floating_r_at_hard_close, 4), DoubleToString(audit.hard_close_gross_pnl_money, 2), DoubleToString(audit.hard_close_net_pnl_money, 2),
      audit.status, audit.rule_note);
   FileClose(h);
   return true;
}

#endif
