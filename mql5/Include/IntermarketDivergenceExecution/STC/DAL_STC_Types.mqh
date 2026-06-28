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
   bool write_hunt_audit;
   int max_hunt_backfill_on_init;
   int max_hunt_catchup_per_pulse;
   bool write_smt_candidate_audit;
   int max_smt_backfill_on_init;
   int max_smt_catchup_per_pulse;
   bool write_signal_registry_audit;
   int max_signal_backfill_on_init;
   int max_signal_catchup_per_pulse;
   bool write_paper_entry_audit;
   int max_paper_entry_backfill_on_init;
   int max_paper_entry_catchup_per_pulse;
   bool write_paper_outcome_audit;
   int max_paper_outcome_backfill_on_init;
   int max_paper_outcome_catchup_per_pulse;
   int max_paper_outcome_forward_checks;
   bool write_partial_audit;
   int max_partial_backfill_on_init;
   int max_partial_catchup_per_pulse;
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
   string hunt_audit_file_common;
   string smt_candidate_audit_file_common;
   string signal_registry_file_common;
   string last_check_audit_stc_day_id;
   int last_check_audit_index;
   long check_candles_audited;
   string last_w_level_audit_stc_day_id;
   int last_w_level_audit_serial;
   long w_levels_audited;
   string last_hunt_audit_stc_day_id;
   int last_hunt_audit_check_index;
   long hunt_rows_audited;
   string last_smt_audit_stc_day_id;
   int last_smt_audit_check_index;
   long smt_candidate_rows_audited;
   string last_signal_audit_stc_day_id;
   int last_signal_audit_check_index;
   long signal_rows_audited;
   string paper_entry_file_common;
   string last_paper_entry_stc_day_id;
   int last_paper_entry_check_index;
   long paper_entry_rows_audited;
   string paper_outcome_file_common;
   string last_paper_outcome_stc_day_id;
   int last_paper_outcome_check_index;
   long paper_outcome_rows_audited;
   string partial_audit_file_common;
   string last_partial_audit_stc_day_id;
   int last_partial_audit_check_index;
   long partial_rows_audited;
   int outcome_trade_count_m1;
   int outcome_trade_count_m2;
   int outcome_trade_count_m3;
   STC_Direction outcome_direction_lock_m1;
   STC_Direction outcome_direction_lock_m2;
   STC_Direction outcome_direction_lock_m3;
   int paper_trade_count_m1;
   int paper_trade_count_m2;
   int paper_trade_count_m3;
   STC_Direction paper_direction_lock_m1;
   STC_Direction paper_direction_lock_m2;
   STC_Direction paper_direction_lock_m3;
   int partial_trade_count_m1;
   int partial_trade_count_m2;
   int partial_trade_count_m3;
   STC_Direction partial_direction_lock_m1;
   STC_Direction partial_direction_lock_m2;
   STC_Direction partial_direction_lock_m3;
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


struct STC_ReferenceHuntAudit
{
   string stc_day_id;
   int check_index;
   int check_minutes;
   datetime check_start_ny;
   datetime check_end_ny;
   datetime check_start_server;
   datetime check_end_server;
   STC_MCycle m_cycle;
   STC_WCycle current_w_cycle;
   STC_WCycle reference_w_cycle;
   int reference_w_serial;
   int reference_rank;
   bool detection_allowed_for_signal;
   bool entry_allowed_at_close;
   bool final_check_of_m;
   bool check_pair_data_complete;
   bool reference_pair_data_complete;
   bool pair_data_complete;
   string status;
   string rule_note;

   double s1_reference_high;
   double s1_reference_low;
   double s1_check_high;
   double s1_check_low;
   bool s1_high_hunt;
   bool s1_low_hunt;

   double s2_reference_high;
   double s2_reference_low;
   double s2_check_high;
   double s2_check_low;
   bool s2_high_hunt;
   bool s2_low_hunt;

   STC_HuntPattern high_hunt_pattern;
   STC_HuntPattern low_hunt_pattern;
   bool high_exactly_one_hunted;
   bool low_exactly_one_hunted;
   string high_hunted_symbol;
   string high_clean_symbol;
   string low_hunted_symbol;
   string low_clean_symbol;
};


struct STC_SMTCandidateAudit
{
   string stc_day_id;
   int check_index;
   int check_minutes;
   datetime check_start_ny;
   datetime check_end_ny;
   datetime check_start_server;
   datetime check_end_server;
   STC_MCycle m_cycle;
   STC_WCycle current_w_cycle;
   bool detection_allowed_for_signal;
   bool entry_allowed_at_close;
   bool final_check_of_m;
   bool check_pair_data_complete;

   STC_CandidateStatus candidate_status;
   string candidate_id;
   bool is_trade_candidate;
   STC_Side smt_side;
   STC_Direction direction;
   string hunted_symbol;
   string clean_symbol;
   string trade_symbol;

   STC_WCycle selected_reference_w_cycle;
   int selected_reference_w_serial;
   int selected_reference_rank;
   double selected_reference_price;
   double trade_symbol_check_close;
   double provisional_stop_distance;

   int legal_reference_count;
   int high_raw_candidate_count;
   int low_raw_candidate_count;
   int same_direction_candidate_count;
   bool simultaneous_buy_sell_forget;
   string status;
   string rule_note;
};


struct STC_SignalAudit
{
   string stc_day_id;
   int check_index;
   int check_minutes;
   datetime check_start_ny;
   datetime check_end_ny;
   datetime check_start_server;
   datetime check_end_server;
   STC_MCycle m_cycle;
   STC_WCycle current_w_cycle;
   bool detection_allowed_for_signal;
   bool entry_allowed_at_close;
   bool final_check_of_m;
   bool check_pair_data_complete;

   STC_SignalStatus signal_status;
   string signal_id;
   string source_candidate_id;
   bool is_confirmed_signal;
   bool signal_consumed;
   bool entry_stc_enabled_at_confirmation;
   bool entry_missed_or_late;
   bool order_attempted;
   bool trade_counter_incremented;

   STC_Side smt_side;
   STC_Direction direction;
   string hunted_symbol;
   string clean_symbol;
   string trade_symbol;

   STC_WCycle selected_reference_w_cycle;
   int selected_reference_w_serial;
   int selected_reference_rank;
   double selected_reference_price;
   double trade_symbol_check_close;
   double provisional_stop_distance;

   int legal_reference_count;
   int high_raw_candidate_count;
   int low_raw_candidate_count;
   int selected_same_direction_count;
   bool simultaneous_buy_sell_forget;
   string status;
   string rule_note;
};


struct STC_PaperEntryAudit
{
   string stc_day_id;
   int check_index;
   int entry_check_index;
   int check_minutes;
   datetime signal_check_start_ny;
   datetime signal_check_end_ny;
   datetime entry_check_start_ny;
   datetime entry_check_end_ny;
   datetime entry_check_start_server;
   datetime entry_check_end_server;
   STC_MCycle m_cycle;
   STC_WCycle current_w_cycle;
   STC_PaperEntryStatus paper_status;
   string signal_id;
   string paper_trade_id;
   bool is_paper_entry;
   bool signal_confirmed;
   bool entry_stc_enabled_at_confirmation;
   bool entry_missed_or_late;
   bool entry_check_pair_data_complete;
   bool trade_counter_incremented;
   int m_trade_count_before;
   int m_trade_count_after;
   STC_Direction m_direction_lock_before;
   STC_Direction m_direction_lock_after;
   STC_Direction direction;
   string trade_symbol;
   string hunted_symbol;
   string clean_symbol;
   STC_WCycle selected_reference_w_cycle;
   int selected_reference_w_serial;
   double selected_reference_price;
   double entry_price;
   double stop_price;
   double take_profit_price;
   double risk_distance_price;
   double reward_distance_price;
   double final_reward_r;
   double equity_snapshot;
   double risk_percent;
   double risk_money;
   double tick_size;
   double tick_value;
   double contract_size_used;
   bool used_tick_value;
   double theoretical_volume;
   double broker_min_volume;
   double broker_max_volume;
   double broker_volume_step;
   double paper_order_volume;
   int split_order_count;
   double spread_points_for_report;
   double commission_per_lot_for_report;
   string volume_status;
   string status;
   string rule_note;
};

void STC_ResetPaperEntryAudit(STC_PaperEntryAudit &audit)
{
   audit.stc_day_id = "";
   audit.check_index = -1;
   audit.entry_check_index = -1;
   audit.check_minutes = 0;
   audit.signal_check_start_ny = 0;
   audit.signal_check_end_ny = 0;
   audit.entry_check_start_ny = 0;
   audit.entry_check_end_ny = 0;
   audit.entry_check_start_server = 0;
   audit.entry_check_end_server = 0;
   audit.m_cycle = STC_M_NONE;
   audit.current_w_cycle = STC_W_NONE;
   audit.paper_status = STC_PAPER_NONE;
   audit.signal_id = "";
   audit.paper_trade_id = "";
   audit.is_paper_entry = false;
   audit.signal_confirmed = false;
   audit.entry_stc_enabled_at_confirmation = false;
   audit.entry_missed_or_late = false;
   audit.entry_check_pair_data_complete = false;
   audit.trade_counter_incremented = false;
   audit.m_trade_count_before = 0;
   audit.m_trade_count_after = 0;
   audit.m_direction_lock_before = STC_DIR_NONE;
   audit.m_direction_lock_after = STC_DIR_NONE;
   audit.direction = STC_DIR_NONE;
   audit.trade_symbol = "";
   audit.hunted_symbol = "";
   audit.clean_symbol = "";
   audit.selected_reference_w_cycle = STC_W_NONE;
   audit.selected_reference_w_serial = -1;
   audit.selected_reference_price = 0.0;
   audit.entry_price = 0.0;
   audit.stop_price = 0.0;
   audit.take_profit_price = 0.0;
   audit.risk_distance_price = 0.0;
   audit.reward_distance_price = 0.0;
   audit.final_reward_r = 0.0;
   audit.equity_snapshot = 0.0;
   audit.risk_percent = 0.0;
   audit.risk_money = 0.0;
   audit.tick_size = 0.0;
   audit.tick_value = 0.0;
   audit.contract_size_used = 0.0;
   audit.used_tick_value = false;
   audit.theoretical_volume = 0.0;
   audit.broker_min_volume = 0.0;
   audit.broker_max_volume = 0.0;
   audit.broker_volume_step = 0.0;
   audit.paper_order_volume = 0.0;
   audit.split_order_count = 0;
   audit.spread_points_for_report = 0.0;
   audit.commission_per_lot_for_report = 0.0;
   audit.volume_status = "not_built";
   audit.status = "not_built";
   audit.rule_note = "";
}

struct STC_PaperOutcomeAudit
{
   string stc_day_id;
   int signal_check_index;
   int entry_check_index;
   int exit_check_index;
   int last_checked_index;
   int check_minutes;
   datetime signal_check_start_ny;
   datetime signal_check_end_ny;
   datetime entry_check_start_ny;
   datetime entry_check_end_ny;
   datetime exit_check_start_ny;
   datetime exit_check_end_ny;
   STC_MCycle m_cycle;
   STC_WCycle current_w_cycle;
   STC_PaperOutcomeStatus outcome_status;
   STC_PaperEntryStatus paper_status;
   string signal_id;
   string paper_trade_id;
   bool is_paper_entry;
   bool outcome_resolved;
   bool tp_hit;
   bool sl_hit;
   bool ambiguous;
   STC_Direction direction;
   string trade_symbol;
   string hunted_symbol;
   string clean_symbol;
   double entry_price;
   double stop_price;
   double take_profit_price;
   double exit_price;
   double last_checked_close;
   double risk_distance_price;
   double reward_distance_price;
   double final_reward_r;
   double paper_order_volume;
   int split_order_count;
   double risk_money;
   double gross_pnl_money;
   double estimated_cost_money;
   double net_pnl_money;
   double realized_r_gross;
   double realized_r_net;
   double floating_r_at_last_check;
   double spread_points_for_report;
   double commission_per_lot_for_report;
   int scanned_checks;
   string status;
   string rule_note;
};

void STC_ResetPaperOutcomeAudit(STC_PaperOutcomeAudit &audit)
{
   audit.stc_day_id = "";
   audit.signal_check_index = -1;
   audit.entry_check_index = -1;
   audit.exit_check_index = -1;
   audit.last_checked_index = -1;
   audit.check_minutes = 0;
   audit.signal_check_start_ny = 0;
   audit.signal_check_end_ny = 0;
   audit.entry_check_start_ny = 0;
   audit.entry_check_end_ny = 0;
   audit.exit_check_start_ny = 0;
   audit.exit_check_end_ny = 0;
   audit.m_cycle = STC_M_NONE;
   audit.current_w_cycle = STC_W_NONE;
   audit.outcome_status = STC_OUTCOME_NONE;
   audit.paper_status = STC_PAPER_NONE;
   audit.signal_id = "";
   audit.paper_trade_id = "";
   audit.is_paper_entry = false;
   audit.outcome_resolved = false;
   audit.tp_hit = false;
   audit.sl_hit = false;
   audit.ambiguous = false;
   audit.direction = STC_DIR_NONE;
   audit.trade_symbol = "";
   audit.hunted_symbol = "";
   audit.clean_symbol = "";
   audit.entry_price = 0.0;
   audit.stop_price = 0.0;
   audit.take_profit_price = 0.0;
   audit.exit_price = 0.0;
   audit.last_checked_close = 0.0;
   audit.risk_distance_price = 0.0;
   audit.reward_distance_price = 0.0;
   audit.final_reward_r = 0.0;
   audit.paper_order_volume = 0.0;
   audit.split_order_count = 0;
   audit.risk_money = 0.0;
   audit.gross_pnl_money = 0.0;
   audit.estimated_cost_money = 0.0;
   audit.net_pnl_money = 0.0;
   audit.realized_r_gross = 0.0;
   audit.realized_r_net = 0.0;
   audit.floating_r_at_last_check = 0.0;
   audit.spread_points_for_report = 0.0;
   audit.commission_per_lot_for_report = 0.0;
   audit.scanned_checks = 0;
   audit.status = "not_built";
   audit.rule_note = "";
}


struct STC_PartialAudit
{
   string stc_day_id;
   int signal_check_index;
   int entry_check_index;
   int partial_due_check_index;
   int last_checked_index;
   int check_minutes;
   datetime signal_check_start_ny;
   datetime signal_check_end_ny;
   datetime entry_check_start_ny;
   datetime entry_check_end_ny;
   datetime partial_due_ny;
   datetime partial_due_server;
   STC_MCycle m_cycle;
   STC_WCycle current_w_cycle;
   STC_PartialStatus partial_status;
   STC_PaperEntryStatus paper_status;
   STC_PaperOutcomeStatus pre_partial_outcome_status;
   string signal_id;
   string paper_trade_id;
   bool is_paper_entry;
   bool partial_enabled;
   bool partial_due;
   bool partial_action_taken;
   bool full_close_by_small_volume;
   bool open_at_w4_end;
   STC_Direction direction;
   string trade_symbol;
   double entry_price;
   double stop_price;
   double take_profit_price;
   double paper_order_volume;
   double broker_volume_step;
   double close_volume;
   double remaining_volume;
   double close_volume_ratio;
   double last_checked_close;
   double floating_r_at_partial;
   string status;
   string rule_note;
};

void STC_ResetPartialAudit(STC_PartialAudit &audit)
{
   audit.stc_day_id = "";
   audit.signal_check_index = -1;
   audit.entry_check_index = -1;
   audit.partial_due_check_index = -1;
   audit.last_checked_index = -1;
   audit.check_minutes = 0;
   audit.signal_check_start_ny = 0;
   audit.signal_check_end_ny = 0;
   audit.entry_check_start_ny = 0;
   audit.entry_check_end_ny = 0;
   audit.partial_due_ny = 0;
   audit.partial_due_server = 0;
   audit.m_cycle = STC_M_NONE;
   audit.current_w_cycle = STC_W_NONE;
   audit.partial_status = STC_PARTIAL_NONE;
   audit.paper_status = STC_PAPER_NONE;
   audit.pre_partial_outcome_status = STC_OUTCOME_NONE;
   audit.signal_id = "";
   audit.paper_trade_id = "";
   audit.is_paper_entry = false;
   audit.partial_enabled = false;
   audit.partial_due = false;
   audit.partial_action_taken = false;
   audit.full_close_by_small_volume = false;
   audit.open_at_w4_end = false;
   audit.direction = STC_DIR_NONE;
   audit.trade_symbol = "";
   audit.entry_price = 0.0;
   audit.stop_price = 0.0;
   audit.take_profit_price = 0.0;
   audit.paper_order_volume = 0.0;
   audit.broker_volume_step = 0.0;
   audit.close_volume = 0.0;
   audit.remaining_volume = 0.0;
   audit.close_volume_ratio = 0.0;
   audit.last_checked_close = 0.0;
   audit.floating_r_at_partial = 0.0;
   audit.status = "not_built";
   audit.rule_note = "";
}

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
   cfg.run_id = "EXEC001_STC_LEVEL10";
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
   cfg.write_hunt_audit = true;
   cfg.max_hunt_backfill_on_init = 24;
   cfg.max_hunt_catchup_per_pulse = 48;
   cfg.write_smt_candidate_audit = true;
   cfg.max_smt_backfill_on_init = 24;
   cfg.max_smt_catchup_per_pulse = 48;
   cfg.write_signal_registry_audit = true;
   cfg.max_signal_backfill_on_init = 24;
   cfg.max_signal_catchup_per_pulse = 48;
   cfg.write_paper_entry_audit = true;
   cfg.max_paper_entry_backfill_on_init = 24;
   cfg.max_paper_entry_catchup_per_pulse = 48;
   cfg.write_paper_outcome_audit = true;
   cfg.max_paper_outcome_backfill_on_init = 24;
   cfg.max_paper_outcome_catchup_per_pulse = 24;
   cfg.max_paper_outcome_forward_checks = 288;
   cfg.write_partial_audit = true;
   cfg.max_partial_backfill_on_init = 24;
   cfg.max_partial_catchup_per_pulse = 24;
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
   state.hunt_audit_file_common = "";
   state.smt_candidate_audit_file_common = "";
   state.signal_registry_file_common = "";
   state.paper_entry_file_common = "";
   state.paper_outcome_file_common = "";
   state.partial_audit_file_common = "";
   state.last_check_audit_stc_day_id = "";
   state.last_check_audit_index = -1;
   state.check_candles_audited = 0;
   state.last_w_level_audit_stc_day_id = "";
   state.last_w_level_audit_serial = -1;
   state.w_levels_audited = 0;
   state.last_hunt_audit_stc_day_id = "";
   state.last_hunt_audit_check_index = -1;
   state.hunt_rows_audited = 0;
   state.last_smt_audit_stc_day_id = "";
   state.last_smt_audit_check_index = -1;
   state.smt_candidate_rows_audited = 0;
   state.last_signal_audit_stc_day_id = "";
   state.last_signal_audit_check_index = -1;
   state.signal_rows_audited = 0;
   state.last_paper_entry_stc_day_id = "";
   state.last_paper_entry_check_index = -1;
   state.paper_entry_rows_audited = 0;
   state.last_paper_outcome_stc_day_id = "";
   state.last_paper_outcome_check_index = -1;
   state.paper_outcome_rows_audited = 0;
   state.last_partial_audit_stc_day_id = "";
   state.last_partial_audit_check_index = -1;
   state.partial_rows_audited = 0;
   state.outcome_trade_count_m1 = 0;
   state.outcome_trade_count_m2 = 0;
   state.outcome_trade_count_m3 = 0;
   state.outcome_direction_lock_m1 = STC_DIR_NONE;
   state.outcome_direction_lock_m2 = STC_DIR_NONE;
   state.outcome_direction_lock_m3 = STC_DIR_NONE;
   state.paper_trade_count_m1 = 0;
   state.paper_trade_count_m2 = 0;
   state.paper_trade_count_m3 = 0;
   state.paper_direction_lock_m1 = STC_DIR_NONE;
   state.paper_direction_lock_m2 = STC_DIR_NONE;
   state.paper_direction_lock_m3 = STC_DIR_NONE;
   state.partial_trade_count_m1 = 0;
   state.partial_trade_count_m2 = 0;
   state.partial_trade_count_m3 = 0;
   state.partial_direction_lock_m1 = STC_DIR_NONE;
   state.partial_direction_lock_m2 = STC_DIR_NONE;
   state.partial_direction_lock_m3 = STC_DIR_NONE;
   state.lock_name = "";
}

void STC_ResetBuildSanity(STC_BuildSanity &sanity)
{
   sanity.strategy_id = "EXEC001_STC_SMT_Cycles";
   sanity.module_level = "LEVEL_10_PARTIAL_CLOSE_SIMULATOR";
   sanity.build_version = "1.90";
   sanity.build_scope = "level01 skeleton through level10 partial close simulator and W4 management";
   sanity.locked_contract = "Simulate W4 partial-close decisions for open paper trades in M1/M2; M3 partial is disabled by hard close; no real orders yet";
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


void STC_ResetReferenceHuntAudit(STC_ReferenceHuntAudit &audit)
{
   audit.stc_day_id = "";
   audit.check_index = -1;
   audit.check_minutes = 0;
   audit.check_start_ny = 0;
   audit.check_end_ny = 0;
   audit.check_start_server = 0;
   audit.check_end_server = 0;
   audit.m_cycle = STC_M_NONE;
   audit.current_w_cycle = STC_W_NONE;
   audit.reference_w_cycle = STC_W_NONE;
   audit.reference_w_serial = -1;
   audit.reference_rank = -1;
   audit.detection_allowed_for_signal = false;
   audit.entry_allowed_at_close = false;
   audit.final_check_of_m = false;
   audit.check_pair_data_complete = false;
   audit.reference_pair_data_complete = false;
   audit.pair_data_complete = false;
   audit.status = "not_built";
   audit.rule_note = "";
   audit.s1_reference_high = 0.0;
   audit.s1_reference_low = 0.0;
   audit.s1_check_high = 0.0;
   audit.s1_check_low = 0.0;
   audit.s1_high_hunt = false;
   audit.s1_low_hunt = false;
   audit.s2_reference_high = 0.0;
   audit.s2_reference_low = 0.0;
   audit.s2_check_high = 0.0;
   audit.s2_check_low = 0.0;
   audit.s2_high_hunt = false;
   audit.s2_low_hunt = false;
   audit.high_hunt_pattern = STC_HUNT_NONE;
   audit.low_hunt_pattern = STC_HUNT_NONE;
   audit.high_exactly_one_hunted = false;
   audit.low_exactly_one_hunted = false;
   audit.high_hunted_symbol = "";
   audit.high_clean_symbol = "";
   audit.low_hunted_symbol = "";
   audit.low_clean_symbol = "";
}


void STC_ResetSMTCandidateAudit(STC_SMTCandidateAudit &audit)
{
   audit.stc_day_id = "";
   audit.check_index = -1;
   audit.check_minutes = 0;
   audit.check_start_ny = 0;
   audit.check_end_ny = 0;
   audit.check_start_server = 0;
   audit.check_end_server = 0;
   audit.m_cycle = STC_M_NONE;
   audit.current_w_cycle = STC_W_NONE;
   audit.detection_allowed_for_signal = false;
   audit.entry_allowed_at_close = false;
   audit.final_check_of_m = false;
   audit.check_pair_data_complete = false;
   audit.candidate_status = STC_CANDIDATE_NONE;
   audit.candidate_id = "";
   audit.is_trade_candidate = false;
   audit.smt_side = STC_SIDE_NONE;
   audit.direction = STC_DIR_NONE;
   audit.hunted_symbol = "";
   audit.clean_symbol = "";
   audit.trade_symbol = "";
   audit.selected_reference_w_cycle = STC_W_NONE;
   audit.selected_reference_w_serial = -1;
   audit.selected_reference_rank = -1;
   audit.selected_reference_price = 0.0;
   audit.trade_symbol_check_close = 0.0;
   audit.provisional_stop_distance = 0.0;
   audit.legal_reference_count = 0;
   audit.high_raw_candidate_count = 0;
   audit.low_raw_candidate_count = 0;
   audit.same_direction_candidate_count = 0;
   audit.simultaneous_buy_sell_forget = false;
   audit.status = "not_built";
   audit.rule_note = "";
}


void STC_ResetSignalAudit(STC_SignalAudit &audit)
{
   audit.stc_day_id = "";
   audit.check_index = -1;
   audit.check_minutes = 0;
   audit.check_start_ny = 0;
   audit.check_end_ny = 0;
   audit.check_start_server = 0;
   audit.check_end_server = 0;
   audit.m_cycle = STC_M_NONE;
   audit.current_w_cycle = STC_W_NONE;
   audit.detection_allowed_for_signal = false;
   audit.entry_allowed_at_close = false;
   audit.final_check_of_m = false;
   audit.check_pair_data_complete = false;
   audit.signal_status = STC_SIGNAL_NONE;
   audit.signal_id = "";
   audit.source_candidate_id = "";
   audit.is_confirmed_signal = false;
   audit.signal_consumed = false;
   audit.entry_stc_enabled_at_confirmation = false;
   audit.entry_missed_or_late = false;
   audit.order_attempted = false;
   audit.trade_counter_incremented = false;
   audit.smt_side = STC_SIDE_NONE;
   audit.direction = STC_DIR_NONE;
   audit.hunted_symbol = "";
   audit.clean_symbol = "";
   audit.trade_symbol = "";
   audit.selected_reference_w_cycle = STC_W_NONE;
   audit.selected_reference_w_serial = -1;
   audit.selected_reference_rank = -1;
   audit.selected_reference_price = 0.0;
   audit.trade_symbol_check_close = 0.0;
   audit.provisional_stop_distance = 0.0;
   audit.legal_reference_count = 0;
   audit.high_raw_candidate_count = 0;
   audit.low_raw_candidate_count = 0;
   audit.selected_same_direction_count = 0;
   audit.simultaneous_buy_sell_forget = false;
   audit.status = "not_built";
   audit.rule_note = "";
}

#endif
