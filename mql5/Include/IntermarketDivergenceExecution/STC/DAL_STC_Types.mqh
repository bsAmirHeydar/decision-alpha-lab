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
   bool write_check_candle_audit;
   int max_check_backfill_on_init;
   int max_check_catchup_per_pulse;
   bool write_w_level_audit;
   int max_w_level_backfill_on_init;
   int max_w_level_catchup_per_pulse;
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
   string check_candle_audit_file_common;
   string w_level_audit_file_common;
   string last_check_audit_stc_day_id;
   int last_check_audit_index;
   long check_candles_audited;
   string last_w_level_audit_stc_day_id;
   int last_w_level_audit_serial;
   long w_levels_audited;
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

struct STC_SymbolCheckAggregate
{
   string symbol;
   bool selected;
   bool complete;
   int expected_m1_bars;
   int actual_m1_bars;
   datetime first_m1_server_time;
   datetime last_m1_server_time;
   double open;
   double high;
   double low;
   double close;
   long tick_volume;
   long real_volume;
   int spread_max;
   string status;
};

struct STC_CheckCandleAudit
{
   string stc_day_id;
   int check_index;
   int check_minutes;
   datetime check_start_ny;
   datetime check_end_ny;
   datetime check_start_server;
   datetime check_end_server;
   int check_start_elapsed_minutes;
   int check_end_elapsed_minutes;
   STC_MCycle m_cycle;
   STC_WCycle w_cycle;
   bool start_inside_active_m;
   bool close_inside_m;
   bool final_check_of_m;
   bool entry_allowed_at_close;
   bool detection_allowed_for_signal;
   string skip_reason;
   STC_SymbolCheckAggregate symbol1;
   STC_SymbolCheckAggregate symbol2;
   bool pair_data_complete;
};

struct STC_WLevelAudit
{
   string stc_day_id;
   int w_serial;
   STC_MCycle m_cycle;
   STC_WCycle w_cycle;
   int w_start_elapsed_minutes;
   int w_end_elapsed_minutes;
   datetime w_start_ny;
   datetime w_end_ny;
   datetime w_start_server;
   datetime w_end_server;
   bool w_closed;
   bool w1_no_signal;
   bool future_reference_candidate;
   bool pair_data_complete;
   string signal_reference_set_for_this_w;
   string future_reference_role;
   string status;
   STC_SymbolCheckAggregate symbol1;
   STC_SymbolCheckAggregate symbol2;
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
   cfg.run_id = "EXEC001_STC_LEVEL04";
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
   cfg.write_check_candle_audit = true;
   cfg.max_check_backfill_on_init = 12;
   cfg.max_check_catchup_per_pulse = 32;
   cfg.write_w_level_audit = true;
   cfg.max_w_level_backfill_on_init = 12;
   cfg.max_w_level_catchup_per_pulse = 12;
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
   state.check_candle_audit_file_common = "";
   state.w_level_audit_file_common = "";
   state.last_check_audit_stc_day_id = "";
   state.last_check_audit_index = -1;
   state.check_candles_audited = 0;
   state.last_w_level_audit_stc_day_id = "";
   state.last_w_level_audit_serial = -1;
   state.w_levels_audited = 0;
   state.lock_name = "";
}

void STC_ResetBuildSanity(STC_BuildSanity &sanity)
{
   sanity.strategy_id = "EXEC001_STC_SMT_Cycles";
   sanity.module_level = "LEVEL_04_W_LEVEL_BUILDER";
   sanity.build_version = "1.30";
   sanity.build_scope = "level01 skeleton plus level02 time engine plus level03 check-candle aggregation plus M1-based W high/low construction and W level audit CSV";
   sanity.locked_contract = "Build closed 90-minute W levels for each symbol independently; no SMT detection, no confirmation, no signals, no paper trades, no orders in level 04";
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

void STC_ResetSymbolCheckAggregate(STC_SymbolCheckAggregate &agg)
{
   agg.symbol = "";
   agg.selected = false;
   agg.complete = false;
   agg.expected_m1_bars = 0;
   agg.actual_m1_bars = 0;
   agg.first_m1_server_time = 0;
   agg.last_m1_server_time = 0;
   agg.open = 0.0;
   agg.high = 0.0;
   agg.low = 0.0;
   agg.close = 0.0;
   agg.tick_volume = 0;
   agg.real_volume = 0;
   agg.spread_max = 0;
   agg.status = "not_built";
}

void STC_ResetCheckCandleAudit(STC_CheckCandleAudit &audit)
{
   audit.stc_day_id = "";
   audit.check_index = -1;
   audit.check_minutes = 0;
   audit.check_start_ny = 0;
   audit.check_end_ny = 0;
   audit.check_start_server = 0;
   audit.check_end_server = 0;
   audit.check_start_elapsed_minutes = -1;
   audit.check_end_elapsed_minutes = -1;
   audit.m_cycle = STC_M_NONE;
   audit.w_cycle = STC_W_NONE;
   audit.start_inside_active_m = false;
   audit.close_inside_m = false;
   audit.final_check_of_m = false;
   audit.entry_allowed_at_close = false;
   audit.detection_allowed_for_signal = false;
   audit.skip_reason = "not_built";
   STC_ResetSymbolCheckAggregate(audit.symbol1);
   STC_ResetSymbolCheckAggregate(audit.symbol2);
   audit.pair_data_complete = false;
}


void STC_ResetWLevelAudit(STC_WLevelAudit &audit)
{
   audit.stc_day_id = "";
   audit.w_serial = -1;
   audit.m_cycle = STC_M_NONE;
   audit.w_cycle = STC_W_NONE;
   audit.w_start_elapsed_minutes = -1;
   audit.w_end_elapsed_minutes = -1;
   audit.w_start_ny = 0;
   audit.w_end_ny = 0;
   audit.w_start_server = 0;
   audit.w_end_server = 0;
   audit.w_closed = false;
   audit.w1_no_signal = false;
   audit.future_reference_candidate = false;
   audit.pair_data_complete = false;
   audit.signal_reference_set_for_this_w = "NONE";
   audit.future_reference_role = "not_built";
   audit.status = "not_built";
   STC_ResetSymbolCheckAggregate(audit.symbol1);
   STC_ResetSymbolCheckAggregate(audit.symbol2);
}

#endif
