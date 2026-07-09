#ifndef GARTAL_NEWS_TYPES_MQH
#define GARTAL_NEWS_TYPES_MQH

#define GT_MAX_EVENTS          512
#define GT_MAX_ALERT_KEYS      2048
#define GT_MIN_TIMER_SECONDS   10
#define GT_MAX_TIMER_SECONDS   3600

#define GT_SECONDS_PER_MINUTE  60
#define GT_SECONDS_PER_HOUR    3600
#define GT_SECONDS_PER_DAY     86400

#define GT_IMPACT_NONE         0
#define GT_IMPACT_LOW          1
#define GT_IMPACT_MEDIUM       2
#define GT_IMPACT_HIGH         3
#define GT_IMPACT_HOLIDAY      4

#define GT_DATA_MODE_SAMPLE    0
#define GT_DATA_MODE_DIRECT    1
#define GT_DATA_MODE_CACHE     2

#define GT_EVENT_UPCOMING      0
#define GT_EVENT_ACTIVE        1
#define GT_EVENT_RELEASED      2
#define GT_EVENT_EXPIRED       3

#define GT_EVENT_KIND_ECONOMIC 0
#define GT_EVENT_KIND_SPEECH   1
#define GT_EVENT_KIND_HOLIDAY  2
#define GT_EVENT_KIND_BREAKING 3
#define GT_EVENT_KIND_OTHER    4

#define GT_LOG_INFO            0
#define GT_LOG_WARNING         1
#define GT_LOG_ERROR           2

#define GT_BROKER_GMT_AUTO     0
#define GT_BROKER_GMT_MANUAL   1
#define GT_BROKER_GMT_HYBRID   2

#define GT_SOURCE_TIME_UTC     0
#define GT_SOURCE_TIME_BROKER  1
#define GT_SOURCE_TIME_MANUAL  2

#define GT_SAMPLE_TIME_BROKER  0
#define GT_SAMPLE_TIME_SOURCE  1
#define GT_SAMPLE_TIME_UTC     2

#define GT_STATUS_ACTIVE_WINDOW_SECONDS 900
#define GT_STATUS_EXPIRE_SECONDS        3600

#define GT_TIMELINE_MAX_RENDER_EVENTS     64
#define GT_TIMELINE_MIN_DANGER_MINUTES     0
#define GT_TIMELINE_MAX_DANGER_MINUTES   180

#define GT_DASHBOARD_MODE_COMPACT          0
#define GT_DASHBOARD_MODE_STANDARD         1
#define GT_DASHBOARD_MODE_PRO              2
#define GT_DASHBOARD_MAX_ROWS             20
#define GT_DASHBOARD_MIN_WIDTH           420
#define GT_DASHBOARD_MAX_WIDTH          1200

struct GT_NewsEvent
{
   string   id;
   int      sequence;

   datetime time_source;
   datetime time_utc;
   datetime time_broker;
   datetime day_start_broker;

   int      minute_of_day;
   int      day_offset;
   int      sort_rank;
   int      impact_rank;
   int      kind;

   string   currency;
   int      impact;
   string   title;
   string   normalized_title;
   string   actual;
   string   forecast;
   string   previous;

   bool     is_tentative;
   bool     is_speech;
   bool     is_holiday;
   bool     is_breaking;
   bool     is_relevant;
   bool     is_released;
   bool     is_today;
   bool     in_date_window;

   int      status;
   string   source;
   string   raw_hash;
   string   notes;
};

struct GT_NewsStore
{
   GT_NewsEvent events[GT_MAX_EVENTS];
   int          count;

   bool         source_ok;
   datetime     last_refresh;
   string       source_status;
   string       sample_profile;

   datetime     window_from_broker;
   datetime     window_to_broker;
   datetime     today_start_broker;

   int          high_count;
   int          medium_count;
   int          low_count;
   int          holiday_count;
   int          speech_count;
   int          breaking_count;
   int          released_count;
   int          upcoming_count;
   int          active_count;
   int          expired_count;
   int          relevant_count;
   int          visible_count;

   int          next_event_index;
   int          next_high_index;
   string       checksum;
};

struct GT_Config
{
   string object_prefix;
   string source_url;
   string currencies_csv;

   int    data_mode;
   bool   use_cache;
   bool   use_sample_data;
   int    refresh_seconds;

   bool   auto_detect_symbol_currencies;
   bool   show_only_symbol_currencies;
   bool   highlight_symbol_currencies;

   bool   show_low;
   bool   show_medium;
   bool   show_high;
   bool   show_holiday;
   bool   show_speech;
   bool   show_tentative;
   bool   show_breaking;

   // Stage 03 time normalization contract.
   bool   auto_detect_broker_gmt;        // compatibility alias for legacy toggles
   int    broker_gmt_mode;               // 0 auto, 1 manual, 2 hybrid
   int    broker_gmt_offset_hours;       // human input/display component
   int    broker_gmt_offset_minutes;     // human input/display component
   int    broker_gmt_offset_seconds;     // canonical offset used by conversion
   int    source_time_mode;              // 0 UTC, 1 broker, 2 manual source GMT
   int    source_gmt_offset_hours;
   int    source_gmt_offset_minutes;
   int    source_gmt_offset_seconds;
   int    time_shift_minutes;            // emergency correction after all normalization
   int    time_shift_seconds;
   int    sample_time_mode;              // broker/source/UTC anchor for deterministic tests
   bool   show_time_debug;

   int    days_back;
   int    days_forward;
   bool   show_past_events;

   bool   show_dashboard;
   bool   show_timeline;
   bool   show_vertical_lines;

   // Stage 04 chart timeline renderer contract.
   bool   show_event_labels;
   bool   show_bottom_tape;
   bool   show_danger_zones;
   bool   show_timeline_tooltips;
   bool   show_released_timeline_objects;
   bool   show_timeline_debug;
   bool   timeline_compact_titles;
   int    timeline_max_events;
   int    timeline_label_rows;
   int    timeline_bottom_y;
   int    timeline_projection_minutes;
   int    pre_news_zone_minutes;
   int    post_news_zone_minutes;

   bool   clean_objects_on_deinit;

   int    dashboard_corner;
   int    dashboard_x;
   int    dashboard_y;
   int    dashboard_rows;

   // Stage 05 luxury dashboard contract.
   int    dashboard_mode;                 // 0 compact, 1 standard, 2 pro
   int    dashboard_width;
   int    dashboard_row_height;
   bool   dashboard_show_header;
   bool   dashboard_show_next_card;
   bool   dashboard_show_high_card;
   bool   dashboard_show_metrics;
   bool   dashboard_show_filter_bar;
   bool   dashboard_show_health_bar;
   bool   dashboard_show_event_table;
   bool   dashboard_show_mini_tape;
   bool   dashboard_use_luxury_theme;
   color  dashboard_bg_color;
   color  dashboard_panel_color;
   color  dashboard_border_color;
   color  dashboard_text_color;
   color  dashboard_muted_color;
   color  dashboard_accent_color;

   bool   enable_alerts;
   bool   alert_popup;
   bool   alert_sound;
   bool   alert_push;
   bool   alert_email;
   bool   alert_before_60;
   bool   alert_before_30;
   bool   alert_before_15;
   bool   alert_before_5;
   bool   alert_before_1;
   bool   alert_at_release;
   bool   alert_after_actual;
   string alert_sound_file;
};

struct GT_FilterState
{
   string currencies_csv;
   bool show_low;
   bool show_medium;
   bool show_high;
   bool show_holiday;
   bool show_speech;
   bool show_tentative;
   bool show_breaking;
   bool show_past_events;
   bool only_symbol;
   bool alerts_enabled;
};

struct GT_AlertState
{
   string sent_keys[GT_MAX_ALERT_KEYS];
   int    sent_count;
};

struct GT_RuntimeState
{
   datetime boot_at;
   datetime last_timer_at;
   datetime last_calculate_at;
   datetime last_refresh_started_at;
   datetime last_refresh_finished_at;
   datetime last_refresh_at;

   bool     last_refresh_ok;
   int      refresh_attempts;

   // Stage 04 renderer diagnostics.
   int      timeline_last_visible_rendered;
   int      timeline_last_vertical_lines;
   int      timeline_last_labels;
   int      timeline_last_zones;
   datetime timeline_last_render_at;
   string   timeline_last_render_summary;

   // Stage 05 dashboard diagnostics.
   int      dashboard_last_objects;
   int      dashboard_last_rows;
   int      dashboard_last_cards;
   datetime dashboard_last_render_at;
   string   dashboard_last_render_summary;

   // Stage 03 diagnostic snapshot.
   bool     time_normalization_ok;
   datetime time_snapshot_server;
   datetime time_snapshot_gmt;
   datetime time_snapshot_local;
   int      broker_gmt_detected_hours;   // compatibility summary
   int      broker_gmt_detected_seconds;
   int      broker_gmt_effective_seconds;
   int      source_gmt_effective_seconds;
   int      time_shift_effective_seconds;
   int      server_gmt_raw_delta_seconds;
   int      broker_gmt_confidence;
   string   time_summary;

   string   last_error;
   string   last_warning;
   string   last_info;
};

#endif
