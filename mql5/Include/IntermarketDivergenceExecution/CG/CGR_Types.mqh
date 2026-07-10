#ifndef __CGR_TYPES_MQH__
#define __CGR_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGT_Types.mqh>

#define CGR_PRICE_DIGITS 5

struct SCGRReferenceConfig
{
   string symbol_a;
   string symbol_b;
   int    broker_utc_offset_hours;
   int    max_groups_shown;
   int    max_references_per_group_shown;
   bool   require_m1_history;
   bool   show_only_groups_with_ready_references;
};

struct SCGRSymbolReference
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

struct SCGRReferencePair
{
   string   group_name;
   int      group_minutes;
   int      reference_cycle_index;
   int      reference_cycle_number;
   int      start_minute;
   int      end_minute_exclusive;
   datetime cycle_start_ny;
   datetime cycle_end_ny;
   datetime cycle_start_broker;
   datetime cycle_end_broker;
   bool     complete_cycle;
   bool     ready;
   SCGRSymbolReference symbol_a;
   SCGRSymbolReference symbol_b;
};

struct SCGRGroupReferenceState
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
   bool     has_any_reference;
   bool     has_ready_reference;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
};

#endif
