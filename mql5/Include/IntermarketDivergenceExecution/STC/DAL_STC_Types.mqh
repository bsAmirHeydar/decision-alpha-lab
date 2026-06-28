#ifndef __DAL_STC_TYPES_MQH__
#define __DAL_STC_TYPES_MQH__
#property strict

#include <IntermarketDivergenceExecution/STC/DAL_STC_Enums.mqh>

struct STC_Config
{
   string strategy_id;
   string run_id;
   STC_RuntimeMode runtime_mode;
   string symbol1;
   string symbol2;
   bool entry_stc_enabled;
   bool partial_enabled;
   bool hedging_enabled;
   double final_reward_r;
   double risk_percent;
   STC_CandleCheckTf check_tf;
   int check_minutes;
   double contract_size;
   double broker_utc_offset_hours;
   int timer_seconds;
   long magic_number;
   string output_root_common;
   bool use_instance_lock;
   int instance_lock_stale_seconds;
   bool strict_symbol_validation;
   bool enable_drawing;
   bool write_heartbeat;
   int heartbeat_seconds;
   int hard_close_retry_seconds;
   bool use_broker_costs_for_reporting;
   double fallback_spread_points;
   double fallback_commission_per_lot;
   bool write_time_audit;
   int time_audit_seconds;
};

struct STC_RuntimeState
{
   bool configured;
   bool initialized;
   bool lock_acquired;
   STC_InitStatus init_status;
   string init_error;
   string init_warning;
   datetime started_server_time;
   datetime last_pulse_server_time;
   datetime last_heartbeat_server_time;
   datetime last_time_audit_server_time;
   long pulse_count;
   string output_root_common;
   string sanity_file_common;
   string runtime_events_file_common;
   string time_audit_file_common;
   string lock_name;
};

struct STC_BuildSanity
{
   string strategy_id;
   string module_level;
   string build_version;
   string build_scope;
   string locked_contract;
};

struct STC_TimeSnapshot
{
   datetime server_time;
   datetime utc_time;
   datetime ny_time;
   datetime stc_day_start_ny;
   datetime stc_day_end_ny;
   int broker_utc_offset_seconds;
   int ny_utc_offset_seconds;
   bool ny_dst;

   int ny_year;
   int ny_month;
   int ny_day;
   int ny_hour;
   int ny_minute;
   int ny_second;

   string stc_day_id;
   int elapsed_minutes_from_2000;
   int elapsed_seconds_from_2000;
   bool inside_stc_day;
   bool detection_allowed;
   bool entry_allowed_now;
   bool hard_close_due;
   STC_TimePhase phase;
   string phase_reason;

   STC_MCycle m_cycle;
   STC_WCycle w_cycle;
   int m_start_elapsed_minutes;
   int m_end_elapsed_minutes;
   int w_start_elapsed_minutes;
   int w_end_elapsed_minutes;
   datetime m_start_ny;
   datetime m_end_ny;
   datetime w_start_ny;
   datetime w_end_ny;

   int check_minutes;
   int check_index;
   int check_start_elapsed_minutes;
   int check_end_elapsed_minutes;
   datetime check_start_ny;
   datetime check_end_ny;
   bool check_inside_active_m;
   bool check_close_inside_m;
   bool final_check_of_m;
   bool check_entry_allowed_at_close;
};

void STC_ResetConfig(STC_Config &cfg)
{
   cfg.strategy_id = "EXEC001_STC_SMT_Cycles";
   cfg.run_id = "EXEC001_STC_LEVEL02";
   cfg.runtime_mode = STC_MODE_RESEARCH_BACKTEST;
   cfg.symbol1 = "SPXUSD";
   cfg.symbol2 = "NDXUSD";
   cfg.entry_stc_enabled = true;
   cfg.partial_enabled = true;
   cfg.hedging_enabled = false;
   cfg.final_reward_r = 10.0;
   cfg.risk_percent = 0.50;
   cfg.check_tf = STC_CHECK_M5;
   cfg.check_minutes = 5;
   cfg.contract_size = 10.0;
   cfg.broker_utc_offset_hours = 0.0;
   cfg.timer_seconds = 10;
   cfg.magic_number = 16001001;
   cfg.output_root_common = "dal/stc/EXEC001_STC_SMT_Cycles";
   cfg.use_instance_lock = true;
   cfg.instance_lock_stale_seconds = 120;
   cfg.strict_symbol_validation = false;
   cfg.enable_drawing = true;
   cfg.write_heartbeat = true;
   cfg.heartbeat_seconds = 60;
   cfg.hard_close_retry_seconds = 5;
   cfg.use_broker_costs_for_reporting = true;
   cfg.fallback_spread_points = 0.0;
   cfg.fallback_commission_per_lot = 0.0;
   cfg.write_time_audit = true;
   cfg.time_audit_seconds = 60;
}

void STC_ResetRuntimeState(STC_RuntimeState &state)
{
   state.configured = false;
   state.initialized = false;
   state.lock_acquired = false;
   state.init_status = STC_INIT_OK;
   state.init_error = "";
   state.init_warning = "";
   state.started_server_time = 0;
   state.last_pulse_server_time = 0;
   state.last_heartbeat_server_time = 0;
   state.last_time_audit_server_time = 0;
   state.pulse_count = 0;
   state.output_root_common = "";
   state.sanity_file_common = "";
   state.runtime_events_file_common = "";
   state.time_audit_file_common = "";
   state.lock_name = "";
}

void STC_ResetBuildSanity(STC_BuildSanity &sanity)
{
   sanity.strategy_id = "EXEC001_STC_SMT_Cycles";
   sanity.module_level = "LEVEL_02_TIME_ENGINE";
   sanity.build_version = "1.10";
   sanity.build_scope = "level01 skeleton plus broker-UTC-NewYork conversion, DST, STC day, M/W cycles, gaps, check-candle anchoring, final-check flags, time audit";
   sanity.locked_contract = "No SMT detection, no W construction, no signals, no paper trades, no orders in level 02";
}

void STC_ResetTimeSnapshot(STC_TimeSnapshot &snap)
{
   snap.server_time = 0;
   snap.utc_time = 0;
   snap.ny_time = 0;
   snap.stc_day_start_ny = 0;
   snap.stc_day_end_ny = 0;
   snap.broker_utc_offset_seconds = 0;
   snap.ny_utc_offset_seconds = 0;
   snap.ny_dst = false;
   snap.ny_year = 0;
   snap.ny_month = 0;
   snap.ny_day = 0;
   snap.ny_hour = 0;
   snap.ny_minute = 0;
   snap.ny_second = 0;
   snap.stc_day_id = "";
   snap.elapsed_minutes_from_2000 = -1;
   snap.elapsed_seconds_from_2000 = -1;
   snap.inside_stc_day = false;
   snap.detection_allowed = false;
   snap.entry_allowed_now = false;
   snap.hard_close_due = false;
   snap.phase = STC_PHASE_PRE_DAY_OR_POST_CLOSE;
   snap.phase_reason = "not_initialized";
   snap.m_cycle = STC_M_NONE;
   snap.w_cycle = STC_W_NONE;
   snap.m_start_elapsed_minutes = -1;
   snap.m_end_elapsed_minutes = -1;
   snap.w_start_elapsed_minutes = -1;
   snap.w_end_elapsed_minutes = -1;
   snap.m_start_ny = 0;
   snap.m_end_ny = 0;
   snap.w_start_ny = 0;
   snap.w_end_ny = 0;
   snap.check_minutes = 0;
   snap.check_index = -1;
   snap.check_start_elapsed_minutes = -1;
   snap.check_end_elapsed_minutes = -1;
   snap.check_start_ny = 0;
   snap.check_end_ny = 0;
   snap.check_inside_active_m = false;
   snap.check_close_inside_m = false;
   snap.final_check_of_m = false;
   snap.check_entry_allowed_at_close = false;
}

#endif
