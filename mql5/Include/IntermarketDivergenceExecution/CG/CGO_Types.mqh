#ifndef __CGO_TYPES_MQH__
#define __CGO_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>

enum ECGOEntryPriceMode
{
   CGO_ENTRY_CONFIRMATION_CLOSE = 0,
   CGO_ENTRY_NEXT_M1_OPEN = 1
};

enum ECGOOutcomeAvailability
{
   CGO_OUTCOME_UNAVAILABLE = 0,
   CGO_OUTCOME_COMPLETE = 1,
   CGO_OUTCOME_PENDING_FUTURE = 2,
   CGO_OUTCOME_MISSING_DATA = 3,
   CGO_OUTCOME_ZERO_RISK = 4
};

struct SCGOOutcomeConfig
{
   string symbol_a;
   string symbol_b;
   ECGOEntryPriceMode entry_price_mode;
   ENUM_TIMEFRAMES execution_timeframe;
   bool require_complete_future_window;
   bool skip_zero_risk;
   double minimum_risk_points;
   int forward_cycles;
   bool study_cycle_end;
   bool study_forward_cycles;
   bool study_day_end;
   bool study_intraday_extremes;
   bool detect_stop_before_window_close;
   bool use_clean_symbol_daily_range_for_normalization;
   bool enable_ledger;
   bool ledger_use_common_files;
   string ledger_file_name;
   bool clear_ledger_on_init;
   bool use_in_memory_duplicate_guard;
   int max_rows_to_write;
   bool show_chart_panel;
   bool print_summary;
};

struct SCGOOutcomeRow
{
   string signal_id;
   string outcome_id;
   string group_name;
   int group_minutes;
   int current_cycle_number;
   int reference_cycle_number;
   datetime trading_day_start_ny;
   datetime trading_day_end_ny;
   datetime confirmation_time_broker;
   datetime confirmation_time_ny;
   datetime entry_time_broker;
   datetime entry_time_ny;
   string clean_symbol;
   string hunter_symbol;
   ECGCSignalDirection direction;
   ECGCSignalSide side;
   double entry_price;
   double stop_price;
   double stop_distance_price;
   double stop_distance_points;
   double point_size;
   double tick_value;
   double tick_size;
   bool data_ready;
   ECGOOutcomeAvailability availability;
   string availability_note;
   datetime cycle_end_time_broker;
   double cycle_end_price;
   double cycle_end_points;
   double cycle_end_r;
   bool cycle_end_stop_hit;
   datetime plus1_time_broker;
   double plus1_price;
   double plus1_points;
   double plus1_r;
   datetime plus2_time_broker;
   double plus2_price;
   double plus2_points;
   double plus2_r;
   datetime plus3_time_broker;
   double plus3_price;
   double plus3_points;
   double plus3_r;
   datetime day_end_time_broker;
   double day_end_price;
   double day_end_points;
   double day_end_r;
   double mfe_price;
   double mfe_points;
   double mfe_r;
   double mae_price;
   double mae_points;
   double mae_r;
   bool stop_hit_intraday;
   datetime stop_hit_time_broker;
   double daily_range_points;
   double day_end_normalized_by_daily_range;
   double mfe_normalized_by_daily_range;
   string note;
};

struct SCGOStudySummary
{
   int observations;
   int confirmed_signals_seen;
   int rows_ready;
   int rows_written;
   int rows_duplicate;
   int rows_missing_data;
   int rows_pending_future;
   int rows_zero_risk;
   int buy_rows;
   int sell_rows;
   int stop_hit_rows;
   double average_cycle_end_r;
   double average_day_end_r;
   double average_mfe_r;
};

#endif
