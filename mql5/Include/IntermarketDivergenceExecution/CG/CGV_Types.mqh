#ifndef __CGV_TYPES_MQH__
#define __CGV_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>

#define CGV_OBJECT_PREFIX "EXP0017_P06_"
#define CGV_LEDGER_COLUMN_COUNT 38

enum ECGVAnchorSymbolMode
{
   CGV_ANCHOR_SYMBOL_HUNTER = 0,
   CGV_ANCHOR_SYMBOL_CLEAN  = 1,
   CGV_ANCHOR_SYMBOL_CHART  = 2,
   CGV_ANCHOR_SYMBOL_A      = 3,
   CGV_ANCHOR_SYMBOL_B      = 4
};

enum ECGVAnchorTimeMode
{
   CGV_ANCHOR_TIME_REFERENCE_CYCLE_START   = 0,
   CGV_ANCHOR_TIME_REFERENCE_CYCLE_MIDDLE  = 1,
   CGV_ANCHOR_TIME_REFERENCE_CYCLE_END     = 2,
   CGV_ANCHOR_TIME_EXACT_REFERENCE_EXTREME = 3,
   CGV_ANCHOR_TIME_CURRENT_CYCLE_START     = 4,
   CGV_ANCHOR_TIME_CURRENT_CYCLE_END       = 5,
   CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME   = 6,
   CGV_ANCHOR_TIME_CONFIRMATION_CLOSE      = 7
};

enum ECGVAnchorPriceMode
{
   CGV_ANCHOR_PRICE_HUNTER_REFERENCE       = 0,
   CGV_ANCHOR_PRICE_HUNTER_CURRENT_EXTREME = 1,
   CGV_ANCHOR_PRICE_CLEAN_REFERENCE        = 2,
   CGV_ANCHOR_PRICE_CLEAN_CURRENT_EXTREME  = 3,
   CGV_ANCHOR_PRICE_CLEAN_STOP_REFERENCE   = 4
};

enum ECGVVisualLineStyle
{
   CGV_VISUAL_STYLE_SOLID      = 0,
   CGV_VISUAL_STYLE_DASH       = 1,
   CGV_VISUAL_STYLE_DOT        = 2,
   CGV_VISUAL_STYLE_DASHDOT    = 3,
   CGV_VISUAL_STYLE_DASHDOTDOT = 4
};

enum ECGVVisualMode
{
   CGV_VISUAL_MODE_MINIMAL_LINES_ONLY = 0,
   CGV_VISUAL_MODE_LINES_AND_MARKERS  = 1,
   CGV_VISUAL_MODE_STRUCTURAL_LINES   = 2,
   CGV_VISUAL_MODE_FULL_AUDIT         = 3
};

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

   bool   enable_historical_visual_backfill;
   int    historical_backfill_lookback_trading_days;
   int    historical_backfill_max_closed_candles;
   bool   historical_backfill_write_ledger;
   bool   historical_backfill_print_summary;
   bool   keep_first_visual_for_same_signal_id;

   bool   enable_drawing;
   ECGVVisualMode visual_mode;
   bool   suppress_all_text_objects;
   bool   delete_text_objects_when_suppressed;
   bool   force_all_visual_objects_on;
   bool   clear_objects_on_init;
   bool   clear_objects_on_deinit;
   bool   draw_only_when_chart_is_hunter_symbol;
   bool   draw_on_both_input_symbol_charts;
   bool   open_missing_input_symbol_charts;
   ENUM_TIMEFRAMES visual_chart_timeframe;
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

   bool   draw_divergence_origin_destination_line;
   ECGVAnchorSymbolMode divergence_origin_symbol_mode;
   ECGVAnchorTimeMode   divergence_origin_time_mode;
   ECGVAnchorPriceMode  divergence_origin_price_mode;
   ECGVAnchorSymbolMode divergence_destination_symbol_mode;
   ECGVAnchorTimeMode   divergence_destination_time_mode;
   ECGVAnchorPriceMode  divergence_destination_price_mode;
   ECGVVisualLineStyle  divergence_line_style;
   int    divergence_line_width;
   bool   draw_origin_marker;
   bool   draw_destination_marker;
   int    origin_marker_arrow_code;
   int    destination_marker_arrow_code;
   int    origin_marker_width;
   int    destination_marker_width;
   bool   draw_origin_vertical;
   bool   draw_destination_vertical;
   bool   draw_hunter_reference_guide;
   bool   draw_clean_reference_guide;
   bool   draw_clean_stop_reference_guide;
   bool   draw_hunter_current_extreme_guide;
   bool   draw_clean_comparison_line;
   bool   draw_clean_comparison_only_when_chart_is_clean_symbol;
   ECGVVisualLineStyle  guide_line_style;
   int    guide_line_width;
   int    label_font_size;
   double label_offset_points;
   color  origin_marker_color;
   color  destination_marker_color;
   color  guide_color;
   color  clean_comparison_color;

   int    max_historical_visual_draws;

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
