#ifndef __CGV_TYPES_MQH__
#define __CGV_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>

#define CGV_OBJECT_PREFIX "EXP0017_P06_"
#define CGV_LEDGER_COLUMN_COUNT 38

// Visual-language anchor symbol selection.
enum ECGVAnchorSymbolMode
{
   CGV_ANCHOR_SYMBOL_HUNTER = 0,
   CGV_ANCHOR_SYMBOL_CLEAN  = 1,
   CGV_ANCHOR_SYMBOL_CHART  = 2,
   CGV_ANCHOR_SYMBOL_A      = 3,
   CGV_ANCHOR_SYMBOL_B      = 4
};

// Visual-language anchor time selection.
enum ECGVAnchorTimeMode
{
   CGV_ANCHOR_TIME_REFERENCE_CYCLE_START  = 0,
   CGV_ANCHOR_TIME_REFERENCE_CYCLE_MIDDLE = 1,
   CGV_ANCHOR_TIME_REFERENCE_CYCLE_END    = 2,
   CGV_ANCHOR_TIME_EXACT_REFERENCE_EXTREME= 3,
   CGV_ANCHOR_TIME_CURRENT_CYCLE_START    = 4,
   CGV_ANCHOR_TIME_CURRENT_CYCLE_END      = 5,
   CGV_ANCHOR_TIME_EXACT_CURRENT_EXTREME  = 6,
   CGV_ANCHOR_TIME_CONFIRMATION_CLOSE     = 7
};

// Visual-language anchor price selection.
enum ECGVAnchorPriceMode
{
   CGV_ANCHOR_PRICE_HUNTER_REFERENCE       = 0,
   CGV_ANCHOR_PRICE_HUNTER_CURRENT_EXTREME = 1,
   CGV_ANCHOR_PRICE_CLEAN_REFERENCE        = 2,
   CGV_ANCHOR_PRICE_CLEAN_CURRENT_EXTREME  = 3,
   CGV_ANCHOR_PRICE_CLEAN_STOP_REFERENCE   = 4
};

// MQL line-style input wrapper. Converted to OBJPROP_STYLE in drawing code.
enum ECGVVisualLineStyle
{
   CGV_VISUAL_STYLE_SOLID      = 0,
   CGV_VISUAL_STYLE_DASH       = 1,
   CGV_VISUAL_STYLE_DOT        = 2,
   CGV_VISUAL_STYLE_DASHDOT    = 3,
   CGV_VISUAL_STYLE_DASHDOTDOT = 4
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

   // Hotfix 002: full visual language and origin-to-destination divergence drawing.
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
