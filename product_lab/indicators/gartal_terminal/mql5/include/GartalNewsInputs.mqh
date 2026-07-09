#ifndef GARTAL_NEWS_INPUTS_MQH
#define GARTAL_NEWS_INPUTS_MQH

input group "01 Data Source / Stage 08"
input string InpForexFactoryUrl              = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"; // FF weekly XML feed used by MT tools
input bool   InpUseSampleData                = true;       // keep true for UI tests; set false for live bridge
input bool   InpUseCache                     = true;
input int    InpRefreshMinutes               = 15;         // avoid over-polling public FF feed
input int    InpSourceFetchMode              = 0;          // 0 Local File Bridge, 1 WebRequest attempt, 2 Auto local->web
input int    InpSourceFormat                 = 0;          // 0 Auto, 1 FF XML, 2 CSV, 3 Website HTML guardrail
input bool   InpAllowIndicatorWebRequest     = false;      // MT5 custom indicators normally return 4014 on WebRequest
input string InpLocalRawFile                 = "GartalTerminal\\ff_calendar_thisweek.xml";
input string InpLocalCacheFile               = "GartalTerminal\\calendar_cache.txt";
input bool   InpSaveRawAfterFetch            = true;
input bool   InpFallbackToSampleOnSourceFail = true;
input bool   InpParserDetectBreakingTitles   = true;
input bool   InpParserIncludeAllDay          = true;
input bool   InpParserLogSkippedRows         = false;
input string InpSourceUserAgent              = "Mozilla/5.0 gartal-terminal/0.8";

input group "02 Time and Broker GMT / Stage 08"
input int    InpBrokerGMTMode                = 0;          // 0 Auto, 1 Manual, 2 Hybrid(auto unless invalid)
input bool   InpAutoDetectBrokerGMT          = true;       // compatibility alias; false forces manual mode
input int    InpBrokerGMTOffsetHours         = 0;          // manual broker GMT hours, e.g. 2 or 3
input int    InpBrokerGMTOffsetMinutes       = 0;          // manual broker GMT minutes, usually 0
input int    InpSourceTimeMode               = 0;          // 0 UTC, 1 Broker time, 2 Manual source GMT
input int    InpSourceGMTOffsetHours         = 0;          // used when SourceTimeMode=2
input int    InpSourceGMTOffsetMinutes       = 0;
input int    InpTimeShiftMinutes             = 0;          // emergency final shift after normalization
input int    InpSampleTimeMode               = 0;          // 0 Broker, 1 Source, 2 UTC
input bool   InpShowTimeDebug                = true;

input group "03 Currency Filter"
input string InpCurrencies                   = "USD,EUR,GBP,JPY,CHF,CAD,AUD,NZD,CNY";
input bool   InpAutoDetectSymbolCurrencies   = true;
input bool   InpShowOnlySymbolCurrencies     = false;
input bool   InpHighlightSymbolCurrencies    = true;

input group "04 Impact Filter"
input bool   InpShowLowImpact                = false;
input bool   InpShowMediumImpact             = true;
input bool   InpShowHighImpact               = true;
input bool   InpShowHoliday                  = false;
input bool   InpShowSpeech                   = true;
input bool   InpShowTentative                = true;
input bool   InpShowBreaking                 = true;

input group "05 Date Range"
input int    InpDaysBack                     = 0;
input int    InpDaysForward                  = 0;
input bool   InpShowPastEvents               = true;

input group "06 Chart Timeline / Stage 04"
input bool   InpShowTimeline                 = true;
input bool   InpShowVerticalLines            = true;
input bool   InpShowEventLabels              = true;
input bool   InpShowBottomTape               = true;
input bool   InpShowDangerZones              = true;
input bool   InpShowTimelineTooltips         = true;
input bool   InpShowReleasedTimelineObjects  = true;
input bool   InpShowTimelineDebug            = true;
input bool   InpTimelineCompactTitles        = true;
input int    InpTimelineMaxEvents            = 24;
input int    InpTimelineLabelRows            = 3;
input int    InpTimelineBottomY              = 22;
input int    InpTimelineProjectionMinutes    = 720;        // future render horizon from broker now
input int    InpPreNewsZoneMinutes           = 15;
input int    InpPostNewsZoneMinutes          = 15;

input group "07 Luxury Dashboard / Stage 08"
input bool   InpShowDashboard                = true;
input bool   InpCleanObjectsOnDeinit         = true;
input string InpObjectPrefix                 = "GT_";
input int    InpDashboardCorner              = 1;          // 0 LU, 1 RU, 2 LL, 3 RL
input int    InpDashboardX                   = 20;
input int    InpDashboardY                   = 28;
input int    InpDashboardRows                = 8;
input int    InpDashboardMode                = 2;          // 0 Compact, 1 Standard, 2 Pro
input int    InpDashboardWidth               = 720;
input int    InpDashboardRowHeight           = 18;
input bool   InpDashboardShowHeader          = true;
input bool   InpDashboardShowNextCard        = true;
input bool   InpDashboardShowHighCard        = true;
input bool   InpDashboardShowMetrics         = true;
input bool   InpDashboardShowFilterBar       = true;
input bool   InpDashboardShowHealthBar       = true;
input bool   InpDashboardShowEventTable      = true;
input bool   InpDashboardShowMiniTape        = true;
input bool   InpDashboardLuxuryTheme         = true;
input color  InpDashboardBgColor             = clrBlack;
input color  InpDashboardPanelColor          = clrMidnightBlue;
input color  InpDashboardBorderColor         = clrDarkSlateGray;
input color  InpDashboardTextColor           = clrWhite;
input color  InpDashboardMutedColor          = clrSilver;
input color  InpDashboardAccentColor         = clrDeepSkyBlue;

input group "08 Runtime Dashboard Filters / Stage 06"
input bool   InpDashboardEnableClickFilters  = true;
input bool   InpDashboardCurrencyToggles     = true;
input bool   InpDashboardShowCurrencyButtons = true;
input bool   InpDashboardShowFilterUtilities = true;
input bool   InpDashboardClickRepaintsTimeline = true;


input group "10 Cache / Resilience / Stage 09"
input bool   InpCacheWriteMetadata           = true;
input bool   InpCacheAllowStale              = true;
input bool   InpCacheAllowExpired            = false;
input bool   InpCacheAcceptUnknownAge        = true;
input string InpCacheMetadataFile            = "GartalTerminal\calendar_cache.meta";
input int    InpCacheFreshMinutes            = 60;
input int    InpCacheStaleAfterMinutes       = 180;
input int    InpCacheMaxAgeHours             = 36;
input int    InpSourceMinRawBytes            = 250;
input int    InpSourceMaxRawBytes            = 2000000;
input int    InpSourceMinEventBlocks         = 3;
input bool   InpSourceRequireEventBlocks     = true;
input int    InpSourceMinRefreshSeconds      = 60;
input bool   InpShowResilienceDebug          = true;

input group "09 Alerts / Stage 07"
input bool   InpEnableAlerts                 = true;
input bool   InpAlertPopup                   = true;
input bool   InpAlertSound                   = true;
input bool   InpAlertPush                    = false;
input bool   InpAlertEmail                   = false;
input bool   InpAlertBefore60                = false;
input bool   InpAlertBefore30                = true;
input bool   InpAlertBefore15                = true;
input bool   InpAlertBefore5                 = true;
input bool   InpAlertBefore1                 = false;
input bool   InpAlertAtRelease               = true;
input bool   InpAlertAfterActual             = false;
input bool   InpAlertRespectRuntimeFilters   = true;
input bool   InpAlertHighImpactOnly          = false;
input bool   InpAlertIncludeMedium           = true;
input bool   InpAlertIncludeLow              = false;
input bool   InpAlertIncludeHoliday          = false;
input bool   InpAlertSpeech                  = true;
input bool   InpAlertBreaking                = true;
input bool   InpAlertTentative               = true;
input bool   InpAlertPastEvents              = false;
input bool   InpAlertIncludeActualRow        = true;
input bool   InpAlertIncludeForecastPrevious = true;
input bool   InpAlertLogOnly                 = false;
input int    InpAlertReleaseWindowSeconds    = 90;
input int    InpAlertCooldownSeconds         = 10;
input string InpAlertSoundFile               = "alert.wav";

void GT_LoadConfig(GT_Config &config)
{
   config.object_prefix = GT_Trim(InpObjectPrefix);
   if(GT_IsEmpty(config.object_prefix))
      config.object_prefix = "GT_";

   config.source_url = GT_Trim(InpForexFactoryUrl);
   config.use_sample_data = InpUseSampleData;
   config.use_cache = InpUseCache;
   config.data_mode = config.use_sample_data ? GT_DATA_MODE_SAMPLE : GT_DATA_MODE_DIRECT;
   config.refresh_seconds = GT_ClampInt(InpRefreshMinutes * 60, GT_MIN_TIMER_SECONDS, GT_MAX_TIMER_SECONDS);
   config.source_fetch_mode = GT_ClampInt(InpSourceFetchMode, GT_FETCH_LOCAL_FILE, GT_FETCH_AUTO);
   config.source_format = GT_ClampInt(InpSourceFormat, GT_SOURCE_FORMAT_AUTO, GT_SOURCE_FORMAT_HTML);
   config.allow_indicator_webrequest = InpAllowIndicatorWebRequest;
   config.local_raw_file = GT_Trim(InpLocalRawFile);
   if(GT_IsEmpty(config.local_raw_file))
      config.local_raw_file = "GartalTerminal\\ff_calendar_thisweek.xml";
   config.local_cache_file = GT_Trim(InpLocalCacheFile);
   if(GT_IsEmpty(config.local_cache_file))
      config.local_cache_file = "GartalTerminal\\calendar_cache.txt";
   config.save_raw_after_fetch = InpSaveRawAfterFetch;
   config.fallback_to_sample_on_source_fail = InpFallbackToSampleOnSourceFail;
   config.parser_detect_breaking_titles = InpParserDetectBreakingTitles;
   config.parser_include_all_day = InpParserIncludeAllDay;
   config.parser_log_skipped_rows = InpParserLogSkippedRows;
   config.source_user_agent = GT_Trim(InpSourceUserAgent);
   if(GT_IsEmpty(config.source_user_agent))
      config.source_user_agent = "Mozilla/5.0 gartal-terminal/0.8";

   config.cache_write_metadata = InpCacheWriteMetadata;
   config.cache_allow_stale = InpCacheAllowStale;
   config.cache_allow_expired = InpCacheAllowExpired;
   config.cache_accept_unknown_age = InpCacheAcceptUnknownAge;
   config.cache_metadata_file = GT_Trim(InpCacheMetadataFile);
   if(GT_IsEmpty(config.cache_metadata_file))
      config.cache_metadata_file = "GartalTerminal\\calendar_cache.meta";
   config.cache_fresh_minutes = GT_ClampInt(InpCacheFreshMinutes, 1, 1440);
   config.cache_stale_after_minutes = GT_ClampInt(InpCacheStaleAfterMinutes, config.cache_fresh_minutes, 10080);
   config.cache_max_age_hours = GT_ClampInt(InpCacheMaxAgeHours, 1, 168);
   config.cache_fresh_seconds = config.cache_fresh_minutes * GT_SECONDS_PER_MINUTE;
   config.cache_stale_after_seconds = config.cache_stale_after_minutes * GT_SECONDS_PER_MINUTE;
   config.cache_max_age_seconds = config.cache_max_age_hours * GT_SECONDS_PER_HOUR;
   config.source_min_raw_bytes = GT_ClampInt(InpSourceMinRawBytes, 0, 5000000);
   config.source_max_raw_bytes = GT_ClampInt(InpSourceMaxRawBytes, 0, 10000000);
   config.source_min_event_blocks = GT_ClampInt(InpSourceMinEventBlocks, 0, 500);
   config.source_require_event_blocks = InpSourceRequireEventBlocks;
   config.source_min_refresh_seconds = GT_ClampInt(InpSourceMinRefreshSeconds, 0, 3600);
   config.show_resilience_debug = InpShowResilienceDebug;


   config.currencies_csv = GT_ToUpper(GT_Trim(InpCurrencies));
   config.auto_detect_symbol_currencies = InpAutoDetectSymbolCurrencies;
   config.show_only_symbol_currencies = InpShowOnlySymbolCurrencies;
   config.highlight_symbol_currencies = InpHighlightSymbolCurrencies;

   config.show_low = InpShowLowImpact;
   config.show_medium = InpShowMediumImpact;
   config.show_high = InpShowHighImpact;
   config.show_holiday = InpShowHoliday;
   config.show_speech = InpShowSpeech;
   config.show_tentative = InpShowTentative;
   config.show_breaking = InpShowBreaking;

   config.auto_detect_broker_gmt = InpAutoDetectBrokerGMT;
   config.broker_gmt_mode = GT_ClampInt(InpBrokerGMTMode, GT_BROKER_GMT_AUTO, GT_BROKER_GMT_HYBRID);
   if(!config.auto_detect_broker_gmt)
      config.broker_gmt_mode = GT_BROKER_GMT_MANUAL;

   config.broker_gmt_offset_hours = GT_ClampInt(InpBrokerGMTOffsetHours, -12, 14);
   config.broker_gmt_offset_minutes = GT_ClampInt(InpBrokerGMTOffsetMinutes, -59, 59);
   config.broker_gmt_offset_seconds = GT_OffsetPartsToSeconds(config.broker_gmt_offset_hours, config.broker_gmt_offset_minutes);

   config.source_time_mode = GT_ClampInt(InpSourceTimeMode, GT_SOURCE_TIME_UTC, GT_SOURCE_TIME_MANUAL);
   config.source_gmt_offset_hours = GT_ClampInt(InpSourceGMTOffsetHours, -12, 14);
   config.source_gmt_offset_minutes = GT_ClampInt(InpSourceGMTOffsetMinutes, -59, 59);
   config.source_gmt_offset_seconds = GT_OffsetPartsToSeconds(config.source_gmt_offset_hours, config.source_gmt_offset_minutes);

   config.time_shift_minutes = GT_ClampInt(InpTimeShiftMinutes, -720, 720);
   config.time_shift_seconds = config.time_shift_minutes * GT_SECONDS_PER_MINUTE;
   config.sample_time_mode = GT_ClampInt(InpSampleTimeMode, GT_SAMPLE_TIME_BROKER, GT_SAMPLE_TIME_UTC);
   config.show_time_debug = InpShowTimeDebug;

   config.days_back = GT_ClampInt(InpDaysBack, 0, 14);
   config.days_forward = GT_ClampInt(InpDaysForward, 0, 14);
   config.show_past_events = InpShowPastEvents;

   config.show_dashboard = InpShowDashboard;
   config.show_timeline = InpShowTimeline;
   config.show_vertical_lines = InpShowVerticalLines;
   config.show_event_labels = InpShowEventLabels;
   config.show_bottom_tape = InpShowBottomTape;
   config.show_danger_zones = InpShowDangerZones;
   config.show_timeline_tooltips = InpShowTimelineTooltips;
   config.show_released_timeline_objects = InpShowReleasedTimelineObjects;
   config.show_timeline_debug = InpShowTimelineDebug;
   config.timeline_compact_titles = InpTimelineCompactTitles;
   config.timeline_max_events = GT_ClampInt(InpTimelineMaxEvents, 1, GT_TIMELINE_MAX_RENDER_EVENTS);
   config.timeline_label_rows = GT_ClampInt(InpTimelineLabelRows, 1, 6);
   config.timeline_bottom_y = GT_ClampInt(InpTimelineBottomY, 0, 600);
   config.timeline_projection_minutes = GT_ClampInt(InpTimelineProjectionMinutes, 30, 10080);
   config.pre_news_zone_minutes = GT_ClampInt(InpPreNewsZoneMinutes, GT_TIMELINE_MIN_DANGER_MINUTES, GT_TIMELINE_MAX_DANGER_MINUTES);
   config.post_news_zone_minutes = GT_ClampInt(InpPostNewsZoneMinutes, GT_TIMELINE_MIN_DANGER_MINUTES, GT_TIMELINE_MAX_DANGER_MINUTES);
   config.clean_objects_on_deinit = InpCleanObjectsOnDeinit;
   config.dashboard_corner = GT_ClampInt(InpDashboardCorner, 0, 3);
   config.dashboard_x = GT_ClampInt(InpDashboardX, 0, 3000);
   config.dashboard_y = GT_ClampInt(InpDashboardY, 0, 3000);
   config.dashboard_rows = GT_ClampInt(InpDashboardRows, 1, GT_DASHBOARD_MAX_ROWS);
   config.dashboard_mode = GT_ClampInt(InpDashboardMode, GT_DASHBOARD_MODE_COMPACT, GT_DASHBOARD_MODE_PRO);
   config.dashboard_width = GT_ClampInt(InpDashboardWidth, GT_DASHBOARD_MIN_WIDTH, GT_DASHBOARD_MAX_WIDTH);
   config.dashboard_row_height = GT_ClampInt(InpDashboardRowHeight, 14, 28);
   config.dashboard_show_header = InpDashboardShowHeader;
   config.dashboard_show_next_card = InpDashboardShowNextCard;
   config.dashboard_show_high_card = InpDashboardShowHighCard;
   config.dashboard_show_metrics = InpDashboardShowMetrics;
   config.dashboard_show_filter_bar = InpDashboardShowFilterBar;
   config.dashboard_show_health_bar = InpDashboardShowHealthBar;
   config.dashboard_show_event_table = InpDashboardShowEventTable;
   config.dashboard_show_mini_tape = InpDashboardShowMiniTape;
   config.dashboard_use_luxury_theme = InpDashboardLuxuryTheme;
   config.dashboard_enable_click_filters = InpDashboardEnableClickFilters;
   config.dashboard_enable_currency_toggles = InpDashboardCurrencyToggles;
   config.dashboard_show_currency_buttons = InpDashboardShowCurrencyButtons;
   config.dashboard_show_filter_utilities = InpDashboardShowFilterUtilities;
   config.dashboard_click_repaints_timeline = InpDashboardClickRepaintsTimeline;
   config.dashboard_bg_color = InpDashboardBgColor;
   config.dashboard_panel_color = InpDashboardPanelColor;
   config.dashboard_border_color = InpDashboardBorderColor;
   config.dashboard_text_color = InpDashboardTextColor;
   config.dashboard_muted_color = InpDashboardMutedColor;
   config.dashboard_accent_color = InpDashboardAccentColor;

   config.enable_alerts = InpEnableAlerts;
   config.alert_popup = InpAlertPopup;
   config.alert_sound = InpAlertSound;
   config.alert_push = InpAlertPush;
   config.alert_email = InpAlertEmail;
   config.alert_before_60 = InpAlertBefore60;
   config.alert_before_30 = InpAlertBefore30;
   config.alert_before_15 = InpAlertBefore15;
   config.alert_before_5 = InpAlertBefore5;
   config.alert_before_1 = InpAlertBefore1;
   config.alert_at_release = InpAlertAtRelease;
   config.alert_after_actual = InpAlertAfterActual;
   config.alert_respect_runtime_filters = InpAlertRespectRuntimeFilters;
   config.alert_high_impact_only = InpAlertHighImpactOnly;
   config.alert_include_medium = InpAlertIncludeMedium;
   config.alert_include_low = InpAlertIncludeLow;
   config.alert_include_holiday = InpAlertIncludeHoliday;
   config.alert_speech = InpAlertSpeech;
   config.alert_breaking = InpAlertBreaking;
   config.alert_tentative = InpAlertTentative;
   config.alert_past_events = InpAlertPastEvents;
   config.alert_include_actual_row = InpAlertIncludeActualRow;
   config.alert_include_forecast_previous = InpAlertIncludeForecastPrevious;
   config.alert_log_only = InpAlertLogOnly;
   config.alert_release_window_seconds = GT_ClampInt(InpAlertReleaseWindowSeconds, 5, 900);
   config.alert_cooldown_seconds = GT_ClampInt(InpAlertCooldownSeconds, GT_ALERT_MIN_COOLDOWN_SECONDS, GT_ALERT_MAX_COOLDOWN_SECONDS);
   config.alert_sound_file = InpAlertSoundFile;
}

bool GT_ValidateConfig(GT_Config &config, GT_RuntimeState &runtime)
{
   bool ok = true;

   if(GT_IsEmpty(config.currencies_csv))
   {
      runtime.last_error = "Currency filter cannot be empty.";
      ok = false;
   }

   if(!config.use_sample_data && GT_IsEmpty(config.source_url))
   {
      runtime.last_error = "Source URL cannot be empty when sample data is disabled.";
      ok = false;
   }

   if(!config.use_sample_data && config.source_fetch_mode != GT_FETCH_LOCAL_FILE && !config.allow_indicator_webrequest)
      runtime.last_warning = "Live source is enabled, but indicator WebRequest is disabled. Use the downloader EA bridge or enable the unsafe WebRequest attempt for diagnostics.";

   if(!config.use_sample_data && config.source_fetch_mode == GT_FETCH_LOCAL_FILE && GT_IsEmpty(config.local_raw_file))
   {
      runtime.last_error = "Local raw file cannot be empty in Local File Bridge mode.";
      ok = false;
   }



   if(config.use_cache && GT_IsEmpty(config.local_cache_file))
   {
      runtime.last_error = "Local cache file cannot be empty when cache is enabled.";
      ok = false;
   }

   if(config.cache_stale_after_seconds < config.cache_fresh_seconds)
      runtime.last_warning = "Cache stale threshold is below fresh threshold; values were clamped.";

   if(config.cache_max_age_seconds < config.cache_stale_after_seconds)
      runtime.last_warning = "Cache max age is below stale threshold; expired cache may appear earlier than expected.";

   if(config.source_max_raw_bytes > 0 && config.source_min_raw_bytes > config.source_max_raw_bytes)
   {
      runtime.last_error = "Source raw byte limits are invalid.";
      ok = false;
   }

   if(!config.show_low && !config.show_medium && !config.show_high && !config.show_holiday)
   {
      runtime.last_warning = "All impact filters are disabled. Dashboard can appear empty.";
   }

   if(MathAbs(config.broker_gmt_offset_seconds) > 14 * GT_SECONDS_PER_HOUR)
   {
      runtime.last_error = "Broker GMT offset is outside the supported range.";
      ok = false;
   }

   if(MathAbs(config.source_gmt_offset_seconds) > 14 * GT_SECONDS_PER_HOUR)
   {
      runtime.last_error = "Source GMT offset is outside the supported range.";
      ok = false;
   }

   if(config.timeline_projection_minutes < 30)
   {
      runtime.last_error = "Timeline projection must be at least 30 minutes.";
      ok = false;
   }

   if(config.pre_news_zone_minutes == 0 && config.post_news_zone_minutes == 0 && config.show_danger_zones)
      runtime.last_warning = "Danger zones are enabled but both pre/post news zone windows are zero.";

   if(config.dashboard_show_event_table && config.dashboard_rows < 1)
   {
      runtime.last_error = "Dashboard table is enabled but row count is invalid.";
      ok = false;
   }

   if(config.dashboard_width < GT_DASHBOARD_MIN_WIDTH)
   {
      runtime.last_error = "Dashboard width is below the supported minimum.";
      ok = false;
   }

   if(config.enable_alerts && !config.alert_popup && !config.alert_sound && !config.alert_push && !config.alert_email && !config.alert_log_only)
      runtime.last_warning = "Alerts are enabled but no delivery channel is active.";

   if(config.alert_high_impact_only && (config.alert_include_medium || config.alert_include_low || config.alert_include_holiday))
      runtime.last_warning = "AlertHighImpactOnly overrides medium/low/holiday alert inclusion flags.";

   return ok;
}

void GT_InitFilterState(GT_FilterState &filters, GT_Config &config)
{
   filters.currencies_csv = config.currencies_csv;
   filters.show_low = config.show_low;
   filters.show_medium = config.show_medium;
   filters.show_high = config.show_high;
   filters.show_holiday = config.show_holiday;
   filters.show_speech = config.show_speech;
   filters.show_tentative = config.show_tentative;
   filters.show_breaking = config.show_breaking;
   filters.show_past_events = config.show_past_events;
   filters.only_symbol = config.show_only_symbol_currencies;
   filters.alerts_enabled = config.enable_alerts;
}

#endif
