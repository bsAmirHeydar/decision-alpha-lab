#ifndef __CGT_TYPES_MQH__
#define __CGT_TYPES_MQH__

#define CGT_GROUP_COUNT 21
#define CGT_TRADING_DAY_MINUTES 1380
#define CGT_TRADING_DAY_START_HOUR_NY 18
#define CGT_TRADING_DAY_END_HOUR_NY 17

enum ECGTGroupId
{
   CGT_CG3M = 0,
   CGT_CG5M = 1,
   CGT_CG9M = 2,
   CGT_CG10M = 3,
   CGT_CG15M = 4,
   CGT_CG18M = 5,
   CGT_CG20M = 6,
   CGT_CG24M = 7,
   CGT_CG30M = 8,
   CGT_CG40M = 9,
   CGT_CG45M = 10,
   CGT_CG60M = 11,
   CGT_CG72M = 12,
   CGT_CG90M = 13,
   CGT_CG120M = 14,
   CGT_CG150M = 15,
   CGT_CG180M = 16,
   CGT_CG240M = 17,
   CGT_CG300M = 18,
   CGT_CG360M = 19,
   CGT_CG720M = 20
};

struct SCGTGroupDef
{
   ECGTGroupId id;
   string      name;
   int         minutes;
   bool        enabled;
};

struct SCGTTimeConfig
{
   int  broker_utc_offset_hours;
   bool use_auto_new_york_dst;
   int  manual_new_york_utc_offset_hours;
   int  max_previous_cycles_shown;
};

struct SCGTTimeSnapshot
{
   datetime broker_now;
   datetime utc_now;
   datetime new_york_now;
   datetime trading_day_start_ny;
   datetime trading_day_end_ny;
   bool     inside_trading_day;
   int      elapsed_minutes_from_day_start;
   int      remaining_minutes_to_day_end;
   int      new_york_utc_offset_hours;
   string   trading_day_label;
};

struct SCGTCycleSnapshot
{
   string   group_name;
   int      group_minutes;
   bool     enabled;
   bool     inside_trading_day;
   int      current_cycle_index;
   int      current_cycle_number;
   int      total_cycle_count;
   int      previous_cycle_count;
   int      cycle_start_minute;
   int      cycle_end_minute;
   datetime cycle_start_ny;
   datetime cycle_end_ny;
   int      minutes_elapsed_in_cycle;
   int      minutes_remaining_in_cycle;
   bool     is_last_cycle_of_day;
   bool     is_partial_last_cycle;
};

#endif
