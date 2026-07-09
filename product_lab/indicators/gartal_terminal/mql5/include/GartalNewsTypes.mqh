#ifndef GARTAL_NEWS_TYPES_MQH
#define GARTAL_NEWS_TYPES_MQH

#define GT_MAX_EVENTS          512
#define GT_MAX_ALERT_KEYS      2048
#define GT_MIN_TIMER_SECONDS   10
#define GT_MAX_TIMER_SECONDS   3600

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

#define GT_STATUS_ACTIVE_WINDOW_SECONDS 900
#define GT_STATUS_EXPIRE_SECONDS        3600

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

   bool   auto_detect_broker_gmt;
   int    broker_gmt_offset_hours;
   int    source_gmt_offset_hours;

   int    days_back;
   int    days_forward;
   bool   show_past_events;

   bool   show_dashboard;
   bool   show_timeline;
   bool   show_vertical_lines;
   bool   clean_objects_on_deinit;

   int    dashboard_corner;
   int    dashboard_x;
   int    dashboard_y;
   int    dashboard_rows;

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
   int      broker_gmt_detected_hours;
   string   last_error;
   string   last_warning;
   string   last_info;
};

#endif
