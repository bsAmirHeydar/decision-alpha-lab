#ifndef GARTAL_NEWS_INPUTS_MQH
#define GARTAL_NEWS_INPUTS_MQH

input group "01 Data Source"
input string InpForexFactoryUrl       = "https://www.forexfactory.com/calendar";
input bool   InpUseCache              = true;
input int    InpRefreshMinutes        = 5;
input bool   InpUseSampleData         = true; // dev default; set false for production adapter

input group "02 Time and Broker GMT"
input bool   InpAutoDetectBrokerGMT   = true;
input int    InpBrokerGMTOffsetHours  = 0;
input int    InpSourceGMTOffsetHours  = 0;

input group "03 Currency Filter"
input string InpCurrencies            = "USD,EUR,GBP,JPY,CHF,CAD,AUD,NZD,CNY";
input bool   InpAutoDetectSymbolCurrencies = true;
input bool   InpShowOnlySymbolCurrencies   = false;
input bool   InpHighlightSymbolCurrencies  = true;

input group "04 Impact Filter"
input bool   InpShowLowImpact         = false;
input bool   InpShowMediumImpact      = true;
input bool   InpShowHighImpact        = true;
input bool   InpShowHoliday           = false;
input bool   InpShowSpeech            = true;
input bool   InpShowTentative         = true;
input bool   InpShowBreaking          = true;

input group "05 Date Range"
input int    InpDaysBack              = 0;
input int    InpDaysForward           = 0;
input bool   InpShowPastEvents        = true;

input group "06 Dashboard"
input bool   InpShowDashboard         = true;
input bool   InpShowTimeline          = true;
input bool   InpShowVerticalLines     = true;
input bool   InpCleanObjectsOnDeinit  = true;
input string InpObjectPrefix          = "GT_";

input group "07 Alerts"
input bool   InpEnableAlerts          = true;
input bool   InpAlertPopup            = true;
input bool   InpAlertSound            = true;
input bool   InpAlertPush             = false;
input bool   InpAlertEmail            = false;
input bool   InpAlertBefore60         = false;
input bool   InpAlertBefore30         = true;
input bool   InpAlertBefore15         = true;
input bool   InpAlertBefore5          = true;
input bool   InpAlertBefore1          = false;
input bool   InpAlertAtRelease        = true;
input bool   InpAlertAfterActual      = false;
input string InpAlertSoundFile        = "alert.wav";

void GT_LoadConfig(GT_Config &config)
{
   config.object_prefix = InpObjectPrefix;
   config.currencies_csv = InpCurrencies;
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
   config.broker_gmt_offset_hours = InpBrokerGMTOffsetHours;
   config.source_gmt_offset_hours = InpSourceGMTOffsetHours;

   if(config.auto_detect_broker_gmt)
   {
      int detected = (int)MathRound((double)(TimeCurrent() - TimeGMT()) / 3600.0);
      if(detected >= -12 && detected <= 14)
         config.broker_gmt_offset_hours = detected;
   }

   config.show_dashboard = InpShowDashboard;
   config.show_timeline = InpShowTimeline;
   config.show_vertical_lines = InpShowVerticalLines;
   config.clean_objects_on_deinit = InpCleanObjectsOnDeinit;

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

   config.days_back = InpDaysBack;
   config.days_forward = InpDaysForward;
   config.refresh_seconds = MathMax(30, InpRefreshMinutes * 60);
   config.use_cache = InpUseCache;
   config.use_sample_data = InpUseSampleData;
   config.source_url = InpForexFactoryUrl;
}

void GT_InitFilterState(GT_FilterState &filters, GT_Config &config)
{
   filters.currencies_csv = config.currencies_csv;
   filters.show_low = config.show_low;
   filters.show_medium = config.show_medium;
   filters.show_high = config.show_high;
   filters.show_holiday = config.show_holiday;
   filters.show_speech = config.show_speech;
   filters.show_breaking = config.show_breaking;
   filters.only_symbol = config.show_only_symbol_currencies;
   filters.alerts_enabled = config.enable_alerts;
}

#endif
