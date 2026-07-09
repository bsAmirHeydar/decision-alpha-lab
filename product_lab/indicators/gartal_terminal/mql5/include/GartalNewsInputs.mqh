#ifndef GARTAL_NEWS_INPUTS_MQH
#define GARTAL_NEWS_INPUTS_MQH

input group "01 Data Source / Stage 01"
input string InpForexFactoryUrl              = "https://www.forexfactory.com/calendar";
input bool   InpUseSampleData                = true;       // Stage 01 default: true. Direct source begins in Stage 08.
input bool   InpUseCache                     = true;
input int    InpRefreshMinutes               = 5;

input group "02 Time and Broker GMT"
input bool   InpAutoDetectBrokerGMT          = true;
input int    InpBrokerGMTOffsetHours         = 0;
input int    InpSourceGMTOffsetHours         = 0;

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

input group "06 Dashboard / Objects"
input bool   InpShowDashboard                = true;
input bool   InpShowTimeline                 = true;
input bool   InpShowVerticalLines            = true;
input bool   InpCleanObjectsOnDeinit         = true;
input string InpObjectPrefix                 = "GT_";
input int    InpDashboardCorner              = 1;          // 0 LU, 1 RU, 2 LL, 3 RL
input int    InpDashboardX                   = 20;
input int    InpDashboardY                   = 28;
input int    InpDashboardRows                = 8;

input group "07 Alerts"
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
   config.broker_gmt_offset_hours = GT_ClampInt(InpBrokerGMTOffsetHours, -12, 14);
   config.source_gmt_offset_hours = GT_ClampInt(InpSourceGMTOffsetHours, -12, 14);

   config.days_back = GT_ClampInt(InpDaysBack, 0, 14);
   config.days_forward = GT_ClampInt(InpDaysForward, 0, 14);
   config.show_past_events = InpShowPastEvents;

   config.show_dashboard = InpShowDashboard;
   config.show_timeline = InpShowTimeline;
   config.show_vertical_lines = InpShowVerticalLines;
   config.clean_objects_on_deinit = InpCleanObjectsOnDeinit;
   config.dashboard_corner = GT_ClampInt(InpDashboardCorner, 0, 3);
   config.dashboard_x = GT_ClampInt(InpDashboardX, 0, 3000);
   config.dashboard_y = GT_ClampInt(InpDashboardY, 0, 3000);
   config.dashboard_rows = GT_ClampInt(InpDashboardRows, 1, 20);

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

   if(!config.show_low && !config.show_medium && !config.show_high && !config.show_holiday)
   {
      runtime.last_warning = "All impact filters are disabled. Dashboard can appear empty.";
   }

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
   filters.only_symbol = config.show_only_symbol_currencies;
   filters.alerts_enabled = config.enable_alerts;
}

#endif
