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
   long pulse_count;
   string output_root_common;
   string sanity_file_common;
   string runtime_events_file_common;
   string lock_name;
};

void STC_ResetConfig(STC_Config &cfg)
{
   cfg.strategy_id = "EXEC001_STC_SMT_Cycles";
   cfg.run_id = "EXEC001_STC_LEVEL01";
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
   state.pulse_count = 0;
   state.output_root_common = "";
   state.sanity_file_common = "";
   state.runtime_events_file_common = "";
   state.lock_name = "";
}

struct STC_BuildSanity
{
   string strategy_id;
   string module_level;
   string build_version;
   string build_scope;
   string locked_contract;
};

void STC_ResetBuildSanity(STC_BuildSanity &sanity)
{
   sanity.strategy_id = "EXEC001_STC_SMT_Cycles";
   sanity.module_level = "LEVEL_01_SKELETON";
   sanity.build_version = "1.00";
   sanity.build_scope = "inputs, validation, folders, journal, timer, instance lock, no-trade engine";
   sanity.locked_contract = "No SMT detection, no W construction, no signals, no orders in level 01";
}

#endif
