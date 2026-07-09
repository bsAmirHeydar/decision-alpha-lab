#ifndef __CGD_TYPES_MQH__
#define __CGD_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGH_Types.mqh>

#define CGD_PRICE_DIGITS 5

enum ECGDDivergenceDirection
{
   CGD_DIRECTION_NONE = 0,
   CGD_DIRECTION_BUY  = 1,
   CGD_DIRECTION_SELL = 2
};

enum ECGDDivergenceSide
{
   CGD_SIDE_NONE = 0,
   CGD_SIDE_LOW  = 1,
   CGD_SIDE_HIGH = 2
};

enum ECGDDivergenceStatus
{
   CGD_STATUS_NONE = 0,
   CGD_STATUS_CANDIDATE = 1,
   CGD_STATUS_SYMMETRIC_HUNT_NO_DIVERGENCE = 2,
   CGD_STATUS_MISSING_DATA = 3
};

struct SCGDDivergenceConfig
{
   string symbol_a;
   string symbol_b;
   int    broker_utc_offset_hours;
   int    max_groups_shown;
   int    max_candidates_per_group_shown;
   bool   require_m1_history;
   bool   show_only_groups_with_divergence;
   bool   show_prices;
   bool   show_symmetric_no_divergence_counts;
};

struct SCGDDivergenceCandidate
{
   string   divergence_id;
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
   ECGDDivergenceDirection direction;
   ECGDDivergenceSide side;
   ECGDDivergenceStatus status;
   string hunter_symbol;
   string clean_symbol;
   string non_hunter_symbol;
   bool   symbol_a_is_hunter;
   bool   symbol_b_is_hunter;
   bool   one_sided_hunt;
   bool   both_symbols_hunted_same_side;
   bool   data_ready;
   double hunter_reference_price;
   double clean_reference_price;
   double hunter_current_extreme;
   double clean_current_extreme;
   double clean_stop_reference_price;
   string note;
};

struct SCGDGroupDivergenceState
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
   int      candidate_count;
   int      buy_candidate_count;
   int      sell_candidate_count;
   int      symbol_a_hunter_count;
   int      symbol_b_hunter_count;
   int      symbol_a_clean_count;
   int      symbol_b_clean_count;
   int      symmetric_high_no_divergence_count;
   int      symmetric_low_no_divergence_count;
   int      missing_data_count;
   bool     has_any_candidate;
   datetime trading_day_start_ny;
   datetime trading_day_end_ny;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
};

#endif
