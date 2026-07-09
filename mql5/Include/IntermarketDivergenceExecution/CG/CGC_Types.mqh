#ifndef __CGC_TYPES_MQH__
#define __CGC_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGH_Types.mqh>

#define CGC_PRICE_DIGITS 5

enum ECGCSignalDirection
{
   CGC_DIRECTION_NONE = 0,
   CGC_DIRECTION_BUY  = 1,
   CGC_DIRECTION_SELL = 2
};

enum ECGCSignalSide
{
   CGC_SIDE_NONE = 0,
   CGC_SIDE_LOW  = 1,
   CGC_SIDE_HIGH = 2
};

enum ECGCFinalStatus
{
   CGC_STATUS_NONE = 0,
   CGC_STATUS_CONFIRMED_TRADEABLE = 1,
   CGC_STATUS_INVALIDATED_DOUBLE_HUNT = 2,
   CGC_STATUS_MISSING_DATA = 3
};

struct SCGCConfirmationConfig
{
   string symbol_a;
   string symbol_b;
   int    broker_utc_offset_hours;
   ENUM_TIMEFRAMES confirmation_timeframe;
   bool   use_last_closed_candle_boundary;
   int    max_groups_shown;
   int    max_signals_per_group_shown;
   bool   require_m1_history;
   bool   show_only_groups_with_final_states;
   bool   show_invalidated_double_hunts;
   bool   show_prices;
   bool   show_stop_reference_preview;

   // Hotfix007: protected-reference lifecycle.
   // A reference side remains eligible for repeated divergence only while the clean/protected symbol
   // has not hunted its own reference. Once the protected side is breached, the reference side is retired.
   bool   enable_protected_reference_retirement;
   bool   retire_reference_when_protected_hunts;
   bool   allow_repeated_divergence_while_protected_survives;
   bool   suppress_retired_reference_signals;
   bool   reset_lifecycle_at_new_trading_day;
   int    max_protected_reference_records;
};

struct SCGCProtectedReferenceLifecycleRecord
{
   string   key;
   string   group_name;
   ECGCSignalSide side;
   bool     active;
   bool     retired;
   string   protected_symbol;
   string   first_hunter_symbol;
   datetime trading_day_start_ny;
   datetime reference_cycle_start_ny;
   datetime reference_cycle_end_ny;
   datetime first_confirmation_time_ny;
   datetime last_allowed_confirmation_time_ny;
   datetime retirement_time_ny;
   string   retirement_reason;
};

struct SCGCFinalSignal
{
   string   signal_id;
   string   group_name;
   int      group_minutes;
   int      current_cycle_index;
   int      current_cycle_number;
   int      reference_cycle_index;
   int      reference_cycle_number;
   datetime trading_day_start_ny;
   datetime trading_day_end_ny;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
   datetime reference_cycle_start_ny;
   datetime reference_cycle_end_ny;
   datetime confirmation_time_broker;
   datetime confirmation_time_utc;
   datetime confirmation_time_ny;
   ENUM_TIMEFRAMES confirmation_timeframe;
   int      confirmation_timeframe_seconds;
   ECGCSignalDirection direction;
   ECGCSignalSide side;
   ECGCFinalStatus status;
   string hunter_symbol;
   string clean_symbol;
   bool   symbol_a_is_hunter;
   bool   symbol_b_is_hunter;
   bool   one_sided_hunt;
   bool   double_hunt_invalidated;
   bool   trade_permission_preview;
   bool   data_ready;
   double hunter_reference_price;
   double clean_reference_price;
   double hunter_current_extreme;
   double clean_current_extreme;
   double clean_stop_reference_price;

   // Hotfix003: symbol-local visual fields for dual-chart drawing.
   // These allow Phase 06 to draw the SPXUSD leg on the SPXUSD chart and
   // the NDXUSD leg on the NDXUSD chart, including invalidated double-hunt states.
   double symbol_a_reference_price;
   double symbol_b_reference_price;
   double symbol_a_current_extreme;
   double symbol_b_current_extreme;

   string note;
};

struct SCGCGroupConfirmationState
{
   string   group_name;
   int      group_minutes;
   bool     enabled;
   bool     inside_trading_day;
   int      current_cycle_index;
   int      current_cycle_number;
   int      previous_cycle_count;
   int      ready_reference_count;
   int      missing_reference_count;
   int      raw_hunt_count;
   int      final_state_count;
   int      confirmed_tradeable_count;
   int      invalidated_double_hunt_count;
   int      missing_data_count;
   int      buy_confirmed_count;
   int      sell_confirmed_count;
   int      symbol_a_clean_count;
   int      symbol_b_clean_count;
   int      high_side_final_count;
   int      low_side_final_count;
   bool     has_any_final_state;
   bool     has_confirmed_tradeable_signal;
   datetime trading_day_start_ny;
   datetime trading_day_end_ny;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
   datetime confirmation_time_broker;
   datetime confirmation_time_ny;
};

#endif
