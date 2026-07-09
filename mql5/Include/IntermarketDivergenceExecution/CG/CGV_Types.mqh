#ifndef __CGV_TYPES_MQH__
#define __CGV_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>

#define CGV_OBJECT_PREFIX "EXP0017_P06_"
#define CGV_LEDGER_COLUMN_COUNT 38

struct SCGVVisualLedgerConfig
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

   bool   enable_drawing;
   bool   clear_objects_on_init;
   bool   clear_objects_on_deinit;
   bool   draw_only_when_chart_is_hunter_symbol;
   bool   draw_confirmed_tradeable;
   bool   draw_invalidated_double_hunts;
   bool   draw_reference_cycle_anchor;
   bool   draw_confirmation_marker;
   bool   draw_text_label;
   int    line_width;
   color  buy_color;
   color  sell_color;
   color  invalidated_color;
   color  text_color;

   bool   enable_ledger;
   bool   ledger_use_common_files;
   string ledger_file_name;
   bool   write_confirmed_to_ledger;
   bool   write_invalidated_to_ledger;
   bool   use_file_duplicate_guard;
};

struct SCGVGroupVisualLedgerState
{
   string group_name;
   int    group_minutes;
   bool   enabled;
   bool   inside_trading_day;
   int    current_cycle_number;
   int    previous_cycle_count;
   int    final_state_count;
   int    confirmed_count;
   int    invalidated_count;
   int    drawn_count;
   int    skipped_draw_count;
   int    ledger_written_count;
   int    ledger_duplicate_count;
   int    buy_count;
   int    sell_count;
   datetime current_cycle_start_ny;
   datetime current_cycle_end_ny;
};

struct SCGVLedgerWriteResult
{
   bool attempted;
   bool written;
   bool duplicate;
   bool error;
   string message;
};

#endif
