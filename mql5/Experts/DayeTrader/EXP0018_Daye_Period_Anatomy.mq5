
#property strict
#property version   "2.00"
#property description "EXP0018 P03 period aggregation and completeness. No hunt, signal, drawing, risk, or trading authority."

#include <DayeTrader/EXP0018/DAYE_PeriodEngine.mqh>

input group "EXP0018 P03 — Symbols"
input string InpSymbolA = "SPXUSD";
input string InpSymbolB = "NDXUSD";
input string InpCanonicalSymbolA = "SPX";
input string InpCanonicalSymbolB = "NDX";

input group "EXP0018 P03 — Source Bars"
input ENUM_TIMEFRAMES InpBaseTimeframe = PERIOD_M1;
input int InpRequestedBarsPerSymbol = 10000;
input int InpMinimumCommonBars = 500;
input int InpMaximumPairsToPublish = 10000;
input bool InpUseClosedBarsOnly = true;
input bool InpRequireSeriesSynchronized = true;
input bool InpFailOnAnyInvalidBar = true;
input bool InpRequireCompleteSourceAlignment = false;

input group "EXP0018 P03 — Period Families"
input bool InpIncludeDailyPeriods = true;
input bool InpIncludeSessionPeriods = true;
input bool InpIncludeSubcyclePeriods = true;
input bool InpIncludeWeeklyPeriods = false;

input group "EXP0018 P03 — Completeness"
input bool InpIncludeOpenPeriods = true;
input bool InpPublishPartialPeriods = true;
input bool InpRequireBothSymbolsComplete = false;
input double InpMinimumPublishableCoveragePercent = 0.0;
input int InpMinimumCompletePairedPeriods = 10;
input int InpMaximumPeriodsToPublish = 2000;

input group "EXP0018 P03 — Refresh"
input bool InpEnforceSourceFreshness = false;
input int InpMaximumLatestBarAgeSeconds = 300;
input int InpForceFullRefreshSeconds = 60;
input int InpTimerSeconds = 2;

input group "EXP0018 P03 — Time Adapter"
input DAYE_BrokerOffsetMode InpBrokerOffsetMode = DAYE_BROKER_OFFSET_MANUAL_FIXED;
input double InpBrokerUtcOffsetHours = 3.0;
input DAYE_NyOffsetMode InpNewYorkOffsetMode = DAYE_NY_AUTO_US_DST;
input double InpManualNewYorkUtcOffsetHours = -5.0;
input DAYE_LocalResolutionPolicy InpAmbiguousStartPolicy = DAYE_LOCAL_EARLIEST;
input DAYE_LocalResolutionPolicy InpAmbiguousEndPolicy = DAYE_LOCAL_LATEST;

input group "EXP0018 P03 — Runtime Diagnostics"
input bool InpRunEmbeddedSelfTestsOnInit = true;
input bool InpPrintSummaryOnRefresh = true;
input bool InpPrintLatestPeriodOnRefresh = true;
input bool InpPrintTransitionEvents = true;
input bool InpShowChartComment = false;

input group "EXP0018 P03 — Optional Audit Ledger"
input bool InpWriteAuditCsv = false;
input bool InpWriteSummaryRows = true;
input int InpAuditLatestPeriodCount = 10;
input string InpAuditCsvFilename = "EXP0018_Phase03_Period_Audit_v2.csv";

CDayePeriodAggregationEngine g_daye_period_engine;

void DAYE_BuildP03TimeConfig(DAYE_TimeConfig &config)
{
   config.schema_version = DAYE_TIME_SCHEMA_VERSION;
   config.broker_offset_mode = InpBrokerOffsetMode;
   config.broker_utc_offset_minutes = (int)MathRound(InpBrokerUtcOffsetHours * 60.0);
   config.ny_offset_mode = InpNewYorkOffsetMode;
   config.manual_new_york_utc_offset_minutes = (int)MathRound(InpManualNewYorkUtcOffsetHours * 60.0);
   config.ambiguous_start_policy = InpAmbiguousStartPolicy;
   config.ambiguous_end_policy = InpAmbiguousEndPolicy;
}

void DAYE_BuildP03Config(DAYE_PeriodAggregationConfig &config)
{
   ZeroMemory(config);
   config.schema_version = DAYE_PERIOD_AGG_SCHEMA_VERSION;
   config.data_config.schema_version = DAYE_DATA_SCHEMA_VERSION;
   config.data_config.broker_symbol_a = InpSymbolA;
   config.data_config.broker_symbol_b = InpSymbolB;
   config.data_config.canonical_symbol_a = InpCanonicalSymbolA;
   config.data_config.canonical_symbol_b = InpCanonicalSymbolB;
   config.data_config.base_timeframe = InpBaseTimeframe;
   config.data_config.requested_bars_per_symbol = InpRequestedBarsPerSymbol;
   config.data_config.minimum_common_bars = InpMinimumCommonBars;
   config.data_config.maximum_pairs_to_publish = InpMaximumPairsToPublish;
   config.data_config.use_closed_bars_only = InpUseClosedBarsOnly;
   config.data_config.require_series_synchronized = InpRequireSeriesSynchronized;
   config.data_config.fail_on_any_invalid_bar = InpFailOnAnyInvalidBar;
   config.data_config.require_complete_alignment = InpRequireCompleteSourceAlignment;
   config.data_config.enforce_freshness = InpEnforceSourceFreshness;
   config.data_config.maximum_latest_bar_age_seconds = InpMaximumLatestBarAgeSeconds;
   config.data_config.force_full_refresh_seconds = InpForceFullRefreshSeconds;

   config.include_daily_periods = InpIncludeDailyPeriods;
   config.include_session_periods = InpIncludeSessionPeriods;
   config.include_subcycle_periods = InpIncludeSubcyclePeriods;
   config.include_weekly_periods = InpIncludeWeeklyPeriods;
   config.include_open_periods = InpIncludeOpenPeriods;
   config.publish_partial_periods = InpPublishPartialPeriods;
   config.require_both_symbols_complete = InpRequireBothSymbolsComplete;
   config.minimum_publishable_coverage_percent = InpMinimumPublishableCoveragePercent;
   config.minimum_complete_paired_periods = InpMinimumCompletePairedPeriods;
   config.maximum_periods_to_publish = InpMaximumPeriodsToPublish;
   config.force_full_refresh_seconds = InpForceFullRefreshSeconds;
}

datetime DAYE_P03CurrentBrokerTime(void)
{
   datetime value = TimeTradeServer();
   if(value <= 0) value = TimeCurrent();
   return value;
}

int OnInit()
{
   DAYE_TimeConfig time_config;
   DAYE_PeriodAggregationConfig config;
   DAYE_BuildP03TimeConfig(time_config);
   DAYE_BuildP03Config(config);

   if(!g_daye_period_engine.Initialize(config,time_config,InpRunEmbeddedSelfTestsOnInit,InpWriteAuditCsv,InpAuditCsvFilename))
      return INIT_FAILED;

   int timer_seconds = InpTimerSeconds;
   if(timer_seconds < 1) timer_seconds = 1;
   if(!EventSetTimer(timer_seconds))
   {
      Print("EXP0018 P03 EventSetTimer failed error=",GetLastError());
      g_daye_period_engine.Shutdown();
      return INIT_FAILED;
   }

   datetime now = DAYE_P03CurrentBrokerTime();
   if(now > 0)
      g_daye_period_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestPeriodOnRefresh,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestPeriodCount);
   return INIT_SUCCEEDED;
}

void OnTimer()
{
   datetime now = DAYE_P03CurrentBrokerTime();
   if(now > 0)
      g_daye_period_engine.Process(now,InpPrintSummaryOnRefresh,InpPrintLatestPeriodOnRefresh,InpPrintTransitionEvents,InpShowChartComment,InpWriteSummaryRows,InpAuditLatestPeriodCount);
}

void OnTick()
{
   // P03 is timer-driven. It intentionally performs no hunt, divergence, drawing, or trading work.
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   g_daye_period_engine.Shutdown();
}
