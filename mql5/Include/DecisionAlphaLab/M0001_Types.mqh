//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Types                                 |
//+------------------------------------------------------------------+

#define DAL_NODE_LOW   1
#define DAL_NODE_HIGH -1

struct DAL_Node
{
   int      id;
   int      index;
   int      active_from;
   datetime time;
   int      type;
   double   price;
};

struct DAL_Event
{
   int      node_id;
   int      node_index;
   int      node_type;
   double   node_price;
   int      revisit_id;

   int      entry_index;
   int      exit_index;
   datetime entry_time;
   datetime exit_time;

   int      event_length;
   double   territory_lower;
   double   territory_upper;
   double   expansion_extreme;

   double   mean_inside;
   double   mean_before;
   double   median_inside;
   double   median_before;
   double   rtv;

   bool     hunted;
   int      hunt_index;
   datetime hunt_time;
   double   hunt_price;

   bool     is_open;
};

struct DAL_Config
{
   int      L;
   double   zone_ratio;
   int      exit_gap;
   bool     consume_on_touch;
   int      max_before_logs;
};


#define DAL_PRESET_CUSTOM              0
#define DAL_PRESET_STRUCTURAL          1
#define DAL_PRESET_TERRITORY           2
#define DAL_PRESET_ENTRY_EXIT          3
#define DAL_PRESET_BASELINE_INSIDE     4
#define DAL_PRESET_RTV_FORMULA         5
#define DAL_PRESET_HUNT                6
#define DAL_PRESET_LIVE_OPEN           7
#define DAL_PRESET_CANDLE_CLASS        8
#define DAL_PRESET_STATE_MACHINE       9
#define DAL_PRESET_EVENT_INSPECTOR    10
#define DAL_PRESET_OVERVIEW           11
#define DAL_PRESET_FULL_LAB           12

#define DAL_FOCUS_NONE                 0
#define DAL_FOCUS_SELECTED             1
#define DAL_FOCUS_LATEST_CLOSED        2
#define DAL_FOCUS_LATEST_OPEN          3
#define DAL_FOCUS_LATEST_HUNTED        4
#define DAL_FOCUS_STRONGEST_RTV        5

struct DAL_DrawOptions
{
   int      view_preset;
   int      focus_mode;
   int      selected_node_id;
   int      selected_revisit_id;

   bool     only_selected_event;
   bool     only_open_events;
   bool     only_closed_events;
   bool     only_hunted_events;
   bool     only_strong_rtv;
   double   min_rtv;
   double   max_rtv;
   double   strong_rtv_threshold;

   bool     show_nodes;
   bool     show_node_labels;
   bool     show_node_price_line;
   bool     show_active_from_line;
   bool     show_confirmation_window;

   bool     show_expansion_extreme;
   bool     show_expansion_distance;
   bool     show_territory_bounds;
   bool     show_territory_fill;
   bool     show_zone_ratio_label;

   bool     show_event_window;
   bool     show_entry_marker;
   bool     show_exit_marker;
   bool     show_outside_counter;

   bool     show_before_candles;
   bool     show_inside_candles;
   bool     show_outside_active_candles;
   bool     show_sample_legend;

   bool     show_rtv_label;
   bool     show_formula_panel;
   bool     show_mean_inside;
   bool     show_mean_before;
   bool     show_medians;
   bool     show_counts;

   bool     show_hunt_marker;
   bool     show_hunt_label;

   bool     show_open_event;
   bool     show_live_rtv;
   bool     show_live_counts;

   bool     show_candle_table;
   bool     show_logmove_values;
   bool     show_classification_flags;
   int      max_candles_in_panel;

   bool     show_state_timeline;
   bool     show_state_labels;
   bool     show_transition_markers;
   bool     show_current_state;

   bool     show_inspector_card;
   bool     show_inspector_table;
   bool     auto_focus_chart;

   bool     show_summary_panel;
   bool     render_light_mode;
   int      max_nodes_to_draw;
   int      max_events_to_draw;
   int      max_labels_to_draw;
};
