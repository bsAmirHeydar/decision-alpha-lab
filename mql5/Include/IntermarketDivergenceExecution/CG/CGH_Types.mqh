#ifndef __CGH_TYPES_MQH__
#define __CGH_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGR_Types.mqh>

#define CGH_PRICE_DIGITS 5

enum ECGHHuntRelation
{
   CGH_HUNT_NONE = 0,
   CGH_HUNT_HIGH = 1,
   CGH_HUNT_LOW = 2,
   CGH_HUNT_BOTH_SIDES = 3
};

struct SCGHHuntConfig
{
   string symbol_a;
   string symbol_b;
   int    broker_utc_offset_hours;
   int    max_groups_shown;
   int    max_hunts_per_group_shown;
   bool   require_m1_history;
   bool   show_only_groups_with_hunts;
   bool   show_reference_prices;
   bool   show_current_cycle_ranges;
};

struct SCGHCurrentSymbolRange
{
   string   symbol;
   bool     selected;
   bool     data_ok;
   int      copied_bars;
   double   high;
   double   low;
   datetime high_time_broker;
   datetime low_time_broker;
   datetime first_bar_broker;
   datetime last_bar_broker;
   string   error_text;
};

struct SCGHSymbolHuntState
{
   string symbol;
   bool   reference_ready;
   bool   current_range_ready;
   double reference_high;
   double reference_low;
   datetime reference_high_time_broker;
   datetime reference_low_time_broker;
   double current_high;
   double current_low;
   datetime current_high_time_broker;
   datetime current_low_time_broker;
   bool   high_hunted;
   bool   low_hunted;
   bool   any_hunt;
   string status_text;
};

struct SCGHReferenceHuntState
{
   string   group_name;
   int      group_minutes;
   int      reference_cycle_index;
   int      reference_cycle_number;
   datetime reference_cycle_start_ny;
   datetime reference_cycle_end_ny;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
   bool     reference_ready;
   bool     current_range_ready;
   bool     any_hunt;
   bool     high_hunted_by_both_symbols;
   bool     low_hunted_by_both_symbols;
   bool     high_hunted_by_one_symbol_only;
   bool     low_hunted_by_one_symbol_only;
   SCGHSymbolHuntState symbol_a;
   SCGHSymbolHuntState symbol_b;
};

struct SCGHGroupHuntState
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
   int      ready_current_range_count;
   int      hunt_state_count;
   int      any_hunt_count;
   int      high_hunt_count;
   int      low_hunt_count;
   int      symbol_a_hunt_count;
   int      symbol_b_hunt_count;
   int      one_symbol_high_hunt_count;
   int      one_symbol_low_hunt_count;
   int      both_symbol_high_hunt_count;
   int      both_symbol_low_hunt_count;
   bool     has_any_hunt;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
   SCGHCurrentSymbolRange current_a;
   SCGHCurrentSymbolRange current_b;
};

#endif
