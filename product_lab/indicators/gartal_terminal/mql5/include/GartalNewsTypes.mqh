#ifndef GARTAL_NEWS_TYPES_MQH
#define GARTAL_NEWS_TYPES_MQH

#define GT_MAX_EVENTS 256
#define GT_IMPACT_LOW 1
#define GT_IMPACT_MEDIUM 2
#define GT_IMPACT_HIGH 3
#define GT_IMPACT_HOLIDAY 4

struct GT_NewsEvent
{
   string   id;
   datetime time_utc;
   datetime time_broker;
   string   currency;
   int      impact;
   string   title;
   string   actual;
   string   forecast;
   string   previous;
   bool     is_tentative;
   bool     is_speech;
   bool     is_holiday;
   bool     is_breaking;
   bool     is_relevant;
   bool     is_released;
   string   source;
   string   raw_hash;
};

struct GT_NewsStore
{
   GT_NewsEvent events[GT_MAX_EVENTS];
   int          count;
   bool         source_ok;
   datetime     last_refresh;
   string       source_status;
};

struct GT_Config
{
   string object_prefix;
   string currencies_csv;
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

   bool   show_dashboard;
   bool   show_timeline;
   bool   show_vertical_lines;
   bool   clean_objects_on_deinit;

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

   int    days_back;
   int    days_forward;
   int    refresh_seconds;
   bool   use_cache;
   bool   use_sample_data;
   string source_url;
};

struct GT_FilterState
{
   string currencies_csv;
   bool show_low;
   bool show_medium;
   bool show_high;
   bool show_holiday;
   bool show_speech;
   bool show_breaking;
   bool only_symbol;
   bool alerts_enabled;
};

struct GT_AlertState
{
   string sent_keys[1024];
   int    sent_count;
};

#endif
